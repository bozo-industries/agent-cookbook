# KiCad Python Automation Reliability

Use these rules when automating KiCad boards with `pcbnew`:

1. In KiCad 10, call `PCB_VIA.GetWidth(via.TopLayer())` (or another explicit applicable copper layer) when recording a via diameter. Although the generated Python help also advertises a zero-argument overload, `PCB_VIA.GetWidth()` can trigger a native assertion and hidden modal warning under a headless worker.
2. Run mutation and diagnostic workers with an exact process-tree deadline and captured stdout/stderr. A native KiCad assertion can leave Python responsive but blocked on an invisible dialog, so low CPU or `Responding=True` is not completion evidence.
3. Distinguish vias from ordinary tracks before using shared `PCB_TRACK` accessors because `PCB_VIA` inherits from `PCB_TRACK` in the bindings. Prefer exact-type checks for segments and the via-specific API for vias.
