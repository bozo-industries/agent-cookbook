# KiCad Python Automation Reliability

Use these rules when automating KiCad boards with `pcbnew`:

1. In KiCad 10, call `PCB_VIA.GetFrontWidth()` when recording an ordinary through-via diameter. Although the generated Python help advertises `GetWidth()` overloads, both the zero-argument call and a Python integer from `via.TopLayer()` can dispatch to an asserting native path and open a hidden modal warning under a headless worker. Verify a different accessor explicitly before using it for blind, buried, or layer-dependent vias.
2. Run mutation and diagnostic workers with an exact process-tree deadline and captured stdout/stderr. A native KiCad assertion can leave Python responsive but blocked on an invisible dialog, so low CPU or `Responding=True` is not completion evidence.
3. Distinguish vias from ordinary tracks before using shared `PCB_TRACK` accessors because `PCB_VIA` inherits from `PCB_TRACK` in the bindings. Prefer exact-type checks for segments and the via-specific API for vias.
4. Before launching a headless Specctra autorouter, create and resolve the parent directory of every requested DSN/SES/log output. Freerouting does not create missing output directories; it may finish a long route successfully and then discard the result when the final SES path has no parent directory.
