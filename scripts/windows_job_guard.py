"""Run up to two Windows workloads with per-child-tree limits and system reserve checks.

No third-party packages. Logs contain memory counters/process basenames, never argv,
environment, screenshots, dumps, or process memory. No unrelated process is terminated.
"""
import argparse
import ctypes as C
from ctypes import wintypes as W
import json
import os
from pathlib import Path
import subprocess
import sys
import time

GIB = 1024**3
SIZE = C.c_size_t
U64 = C.c_ulonglong


class Performance(C.Structure):
    _fields_ = [('cb', W.DWORD)] + [(name, SIZE) for name in (
        'CommitTotal', 'CommitLimit', 'CommitPeak', 'PhysicalTotal', 'PhysicalAvailable',
        'SystemCache', 'KernelTotal', 'KernelPaged', 'KernelNonpaged', 'PageSize')] + [
        ('HandleCount', W.DWORD), ('ProcessCount', W.DWORD), ('ThreadCount', W.DWORD)]


class BasicLimit(C.Structure):
    _fields_ = [('PerProcessUserTimeLimit', U64), ('PerJobUserTimeLimit', U64),
        ('LimitFlags', W.DWORD), ('MinimumWorkingSetSize', SIZE), ('MaximumWorkingSetSize', SIZE),
        ('ActiveProcessLimit', W.DWORD), ('Affinity', SIZE), ('PriorityClass', W.DWORD),
        ('SchedulingClass', W.DWORD)]


class IoCounters(C.Structure):
    _fields_ = [(name, U64) for name in ('ReadOperationCount', 'WriteOperationCount',
        'OtherOperationCount', 'ReadTransferCount', 'WriteTransferCount', 'OtherTransferCount')]


class ExtendedLimit(C.Structure):
    _fields_ = [('BasicLimitInformation', BasicLimit), ('IoInfo', IoCounters)] + [
        (name, SIZE) for name in ('ProcessMemoryLimit', 'JobMemoryLimit',
                                'PeakProcessMemoryUsed', 'PeakJobMemoryUsed')]


class StartupInfo(C.Structure):
    _fields_ = [('cb', W.DWORD), ('lpReserved', W.LPWSTR), ('lpDesktop', W.LPWSTR),
        ('lpTitle', W.LPWSTR)] + [(name, W.DWORD) for name in (
        'dwX', 'dwY', 'dwXSize', 'dwYSize', 'dwXCountChars', 'dwYCountChars',
        'dwFillAttribute', 'dwFlags')] + [('wShowWindow', W.WORD), ('cbReserved2', W.WORD),
        ('lpReserved2', C.POINTER(C.c_byte)), ('hStdInput', W.HANDLE),
        ('hStdOutput', W.HANDLE), ('hStdError', W.HANDLE)]


class ProcessInfo(C.Structure):
    _fields_ = [('hProcess', W.HANDLE), ('hThread', W.HANDLE),
                ('dwProcessId', W.DWORD), ('dwThreadId', W.DWORD)]


class ProcessEntry(C.Structure):
    _fields_ = [('dwSize', W.DWORD), ('cntUsage', W.DWORD), ('th32ProcessID', W.DWORD),
        ('th32DefaultHeapID', SIZE), ('th32ModuleID', W.DWORD), ('cntThreads', W.DWORD),
        ('th32ParentProcessID', W.DWORD), ('pcPriClassBase', W.LONG),
        ('dwFlags', W.DWORD), ('szExeFile', W.WCHAR*260)]


class ProcessMemory(C.Structure):
    _fields_ = [('cb', W.DWORD), ('PageFaultCount', W.DWORD)] + [(name, SIZE) for name in (
        'PeakWorkingSetSize', 'WorkingSetSize', 'QuotaPeakPagedPoolUsage', 'QuotaPagedPoolUsage',
        'QuotaPeakNonPagedPoolUsage', 'QuotaNonPagedPoolUsage', 'PagefileUsage',
        'PeakPagefileUsage', 'PrivateUsage')]


def check(ok):
    if not ok: raise C.WinError(C.get_last_error())
    return ok


def reserve_failure(sample, *, starting=False):
    if sample['commitLimitBytes'] <= 0: return 'unavailable commit limit'
    reserve = sample['commitLimitBytes']-sample['committedBytes']
    if sample['committedBytes']/sample['commitLimitBytes'] >= (.65 if starting else .75):
        return 'system commit percentage'
    if reserve < (16 if starting else 12)*GIB: return 'system commit reserve'
    if sample['availableBytes'] < (8 if starting else 4)*GIB: return 'available physical memory'
    return None


class Windows:
    def __init__(self):
        if os.name != 'nt' or C.sizeof(C.c_void_p) != 8:
            raise RuntimeError('64-bit Windows Python is required')
        self.kernel = C.WinDLL('kernel32', use_last_error=True)
        self.psapi = C.WinDLL('psapi', use_last_error=True)
        declarations = {
            'CreateJobObjectW': ([C.c_void_p, W.LPCWSTR], W.HANDLE),
            'SetInformationJobObject': ([W.HANDLE, C.c_int, C.c_void_p, W.DWORD], W.BOOL),
            'QueryInformationJobObject': ([W.HANDLE, C.c_int, C.c_void_p, W.DWORD, C.c_void_p], W.BOOL),
            'AssignProcessToJobObject': ([W.HANDLE, W.HANDLE], W.BOOL),
            'TerminateJobObject': ([W.HANDLE, W.UINT], W.BOOL),
            'CloseHandle': ([W.HANDLE], W.BOOL),
            'CreateMutexW': ([C.c_void_p, W.BOOL, W.LPCWSTR], W.HANDLE),
            'ReleaseMutex': ([W.HANDLE], W.BOOL),
            'WaitForSingleObject': ([W.HANDLE, W.DWORD], W.DWORD),
            'ResumeThread': ([W.HANDLE], W.DWORD),
            'TerminateProcess': ([W.HANDLE, W.UINT], W.BOOL),
            'GetExitCodeProcess': ([W.HANDLE, C.POINTER(W.DWORD)], W.BOOL),
            'CreateProcessW': ([W.LPCWSTR, W.LPWSTR, C.c_void_p, C.c_void_p, W.BOOL,
                               W.DWORD, C.c_void_p, W.LPCWSTR,
                               C.POINTER(StartupInfo), C.POINTER(ProcessInfo)], W.BOOL),
            'CreateToolhelp32Snapshot': ([W.DWORD, W.DWORD], W.HANDLE),
            'Process32FirstW': ([W.HANDLE, C.POINTER(ProcessEntry)], W.BOOL),
            'Process32NextW': ([W.HANDLE, C.POINTER(ProcessEntry)], W.BOOL),
            'OpenProcess': ([W.DWORD, W.BOOL, W.DWORD], W.HANDLE),
        }
        for name, (args, result) in declarations.items():
            fn = getattr(self.kernel, name)
            fn.argtypes, fn.restype = args, result
        self.psapi.GetPerformanceInfo.argtypes = [C.POINTER(Performance), W.DWORD]
        self.psapi.GetPerformanceInfo.restype = W.BOOL
        self.psapi.GetProcessMemoryInfo.argtypes = [W.HANDLE, C.POINTER(ProcessMemory), W.DWORD]
        self.psapi.GetProcessMemoryInfo.restype = W.BOOL

    def memory(self):
        value = Performance()
        value.cb = C.sizeof(value)
        check(self.psapi.GetPerformanceInfo(C.byref(value), value.cb))
        return {'committedBytes':value.CommitTotal*value.PageSize,
                'commitLimitBytes':value.CommitLimit*value.PageSize,
                'availableBytes':value.PhysicalAvailable*value.PageSize,
                'nonpagedPoolBytes':value.KernelNonpaged*value.PageSize,
                'processCount':value.ProcessCount}

    def consumers(self):
        snapshot = self.kernel.CreateToolhelp32Snapshot(2, 0)
        if snapshot == C.c_void_p(-1).value: return []
        rows = []
        try:
            entry = ProcessEntry()
            entry.dwSize = C.sizeof(entry)
            valid = self.kernel.Process32FirstW(snapshot, C.byref(entry))
            while valid:
                process = self.kernel.OpenProcess(0x1000, False, entry.th32ProcessID)
                if process:
                    try:
                        counters = ProcessMemory()
                        counters.cb = C.sizeof(counters)
                        if self.psapi.GetProcessMemoryInfo(process, C.byref(counters), counters.cb):
                            rows.append({'pid':entry.th32ProcessID, 'parentPid':entry.th32ParentProcessID,
                                'name':entry.szExeFile, 'privateBytes':counters.PrivateUsage,
                                'workingSetBytes':counters.WorkingSetSize})
                    finally: self.kernel.CloseHandle(process)
                valid = self.kernel.Process32NextW(snapshot, C.byref(entry))
        finally: self.kernel.CloseHandle(snapshot)
        return sorted(rows, key=lambda row:row['privateBytes'], reverse=True)[:12]


# Retain the original name as slot 0 so an older active guard still consumes a slot.
WORKLOAD_SLOTS = ('Local\\CodexCookbookBoundedWorkload',
                  'Local\\CodexCookbookBoundedWorkload2')


def acquire_workload_slot(kernel):
    for slot, name in enumerate(WORKLOAD_SLOTS):
        mutex = check(kernel.CreateMutexW(None, False, name))
        result = kernel.WaitForSingleObject(mutex, 0)
        if result in (0, 0x80):
            return mutex, slot
        kernel.CloseHandle(mutex)
        if result != 258:
            raise C.WinError(C.get_last_error())
    raise RuntimeError('Two guarded workloads are already running')


def run(args):
    import msvcrt
    windows = Windows()
    kernel = windows.kernel
    command = args.command[1:] if args.command[:1] == ['--'] else args.command
    if not command or not Path(command[0]).is_absolute() or Path(command[0]).suffix.lower() != '.exe':
        raise ValueError('Supply an absolute executable path after --; invoke .bat with cmd.exe explicitly')
    if not Path(command[0]).is_file(): raise ValueError('Executable is missing')
    if not 64 <= args.memory_mib <= 16384 or not 1 <= args.processes <= 64:
        raise ValueError('Memory limit must be 64..16384 MiB; process limit 1..64')
    if not 1 <= args.timeout <= 7200: raise ValueError('Timeout must be 1..7200 seconds')
    cwd = args.cwd.resolve(strict=True)
    if not cwd.is_dir(): raise ValueError('Working directory must exist')
    if args.log.exists(): raise ValueError('Choose a new telemetry file')
    args.log.parent.mkdir(parents=True, exist_ok=True)
    mutex, workload_slot = acquire_workload_slot(kernel)
    acquired = True
    job = None
    info = ProcessInfo()
    started = time.monotonic()
    try:
        initial = windows.memory()
        reason = reserve_failure(initial, starting=True)
        if reason: raise RuntimeError('Preflight refused: '+reason)
        job = check(kernel.CreateJobObjectW(None, None))
        limits = ExtendedLimit()
        limits.BasicLimitInformation.LimitFlags = 0x2000 | 0x200 | 0x8
        limits.BasicLimitInformation.ActiveProcessLimit = args.processes
        limits.JobMemoryLimit = args.memory_mib*1024*1024
        check(kernel.SetInformationJobObject(job, 9, C.byref(limits), C.sizeof(limits)))
        with args.log.open('x',encoding='utf-8') as log, \
             args.log.with_suffix('.stdout.log').open('xb') as stdout, \
             args.log.with_suffix('.stderr.log').open('xb') as stderr, open(os.devnull,'rb') as stdin:
            startup = StartupInfo()
            startup.cb = C.sizeof(startup)
            startup.dwFlags = 0x100
            handles = [msvcrt.get_osfhandle(value.fileno()) for value in (stdin,stdout,stderr)]
            for handle in handles: os.set_handle_inheritable(handle, True)
            startup.hStdInput, startup.hStdOutput, startup.hStdError = handles
            environment = os.environ.copy()
            for name in ('OMP_NUM_THREADS','MKL_NUM_THREADS','OPENBLAS_NUM_THREADS','NUMEXPR_NUM_THREADS'):
                environment[name] = '2'
            env_block = C.create_unicode_buffer('\0'.join(f'{k}={v}' for k,v in sorted(environment.items()))+'\0\0')
            try:
                check(kernel.CreateProcessW(command[0], C.create_unicode_buffer(subprocess.list2cmdline(command)),
                    None,None,True,0x4 | 0x400 | 0x08000000,env_block,str(cwd),C.byref(startup),C.byref(info)))
            finally:
                for handle in handles: os.set_handle_inheritable(handle, False)
            # The child cannot execute even one instruction outside the memory-limited job.
            if not kernel.AssignProcessToJobObject(job,info.hProcess):
                error=C.get_last_error()
                kernel.TerminateProcess(info.hProcess,125)
                kernel.WaitForSingleObject(info.hProcess,5000)
                raise C.WinError(error)
            if kernel.ResumeThread(info.hThread) == 0xffffffff: raise C.WinError(C.get_last_error())
            last_consumers = -10.0
            reason = None
            while True:
                elapsed = time.monotonic()-started
                sample = windows.memory()
                sample.update(elapsedSeconds=round(elapsed,2),rootPid=info.dwProcessId,
                              jobMemoryLimitBytes=limits.JobMemoryLimit,workloadSlot=workload_slot,workloadCapacity=len(WORKLOAD_SLOTS))
                usage = ExtendedLimit()
                check(kernel.QueryInformationJobObject(job,9,C.byref(usage),C.sizeof(usage),None))
                sample['peakJobMemoryBytes'] = usage.PeakJobMemoryUsed
                if elapsed-last_consumers >= 5:
                    sample['topPrivateMemoryConsumers'] = windows.consumers()
                    last_consumers = elapsed
                log.write(json.dumps(sample)+'\n'); log.flush()
                reason = reserve_failure(sample)
                if not reason and elapsed >= args.timeout: reason='workload timeout'
                if reason:
                    check(kernel.TerminateJobObject(job,125))
                    kernel.WaitForSingleObject(info.hProcess,5000)
                    break
                wait = kernel.WaitForSingleObject(info.hProcess,500)
                if wait == 0: break
                if wait != 258: raise C.WinError(C.get_last_error())
            status = W.DWORD()
            check(kernel.GetExitCodeProcess(info.hProcess,C.byref(status)))
            check(kernel.QueryInformationJobObject(job,9,C.byref(usage),C.sizeof(usage),None))
            summary = {'exitCode':int(status.value), 'guardStop':reason,
                       'workloadSlot':workload_slot, 'workloadCapacity':len(WORKLOAD_SLOTS),
                       'peakJobMemoryBytes':usage.PeakJobMemoryUsed,
                       'elapsedSeconds':round(time.monotonic()-started,2)}
            log.write(json.dumps({'summary':summary})+'\n'); log.flush()
            print(json.dumps(summary),flush=True)
            return 125 if reason else (0 if status.value == 0 else 1)
    finally:
        # KILL_ON_JOB_CLOSE also cleans up detached children; never kill by process name.
        if job: kernel.CloseHandle(job)
        for handle in (info.hThread, info.hProcess):
            if handle: kernel.CloseHandle(handle)
        if acquired: kernel.ReleaseMutex(mutex)
        kernel.CloseHandle(mutex)


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--cwd',type=Path,required=True)
    parser.add_argument('--log',type=Path,required=True)
    parser.add_argument('--memory-mib',type=int,default=8192)
    parser.add_argument('--processes',type=int,default=24)
    parser.add_argument('--timeout',type=int,default=1800)
    parser.add_argument('command',nargs=argparse.REMAINDER)
    try: return run(parser.parse_args())
    except Exception as error:
        # Do not serialize subprocess command lines or environment on failures.
        print(json.dumps({'guardError':type(error).__name__,'detail':str(error)}),file=sys.stderr)
        return 125


if __name__ == '__main__': raise SystemExit(main())
