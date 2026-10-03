# Native FreeCAD Automation

Use this guide for FreeCAD Python modeling, geometric verification, and manufacturing exports. General process, encoding, transport, and Git rules remain in [transport.md](./transport.md) and [commit.md](./commit.md).

## Runtime and source preservation

- Read the project's declared toolchain and use the installed FreeCAD bundled Python for scripts with ordinary command-line arguments. Import `FreeCAD` before `Part` so native paths are initialized. Keep source loading and mutation behind a guarded entry point.
- For focused work, load a hash-bound saved document and copy its shapes. Build in a new document and fresh contained staging directory. Preserve the authoritative document and old release files until the complete replacement has passed its gates.
- Keep exact producer/source hashes, parameters, native-tool version, and output hashes. Recheck inputs before publishing. A successful save or native process exit is not geometric verification.

## Boolean and local-clearance operations

- A whole-solid offset on a complex Boolean result can fail with a closed-boundary error even when the input BRep is valid. Treat that as a deterministic geometry failure; do not retry the unchanged operation or return the input shape as a successful result.
- For a local interface relief, prefer an explicit bounded cutter or a native feature whose extent and clearance can be verified directly. Measure resulting validity, solid count, intersections, receiver material and wall/fillet geometry. Do not substitute the intended clearance value for measuring the actual result.
- Avoid zero-thickness and exactly tangent intersections. For example, a circular clearance hole tangent to a relieved roof can produce a non-manifold triangle edge while the native solid still reports valid and closed. Introduce deliberate finite clearance or an intentionally open groove, without creating an unprintably thin roof. Verify feature and wall dimensions against the actual process.

## Native and exchange-file verification

- Check both the native BRep and the serialized STL topology. Count boundary and non-manifold edges when a mesh fails. Do not assume finer tessellation can repair a geometric knife edge, or use a mesh splitter that silently fills holes as evidence of original closure.
- Native bounding boxes can include untrimmed supporting-surface extrema. Use trimmed-face intersections, exact sections, or bounded tessellation to establish physical extents; report any difference rather than silently relaxing a size limit.
- Reopen STEP and saved native files independently. Check valid closed solids, symmetric-difference volume, units and dimensions. Load STL through an independent reader without automatic hole repair; verify closure, winding, envelope and volume error.
- Hardware envelope proxies must be labeled as proxies. A smooth nominal screw or insert is not a manufacturer thread/knurl model or a qualified tolerance stack.

## Assembly and service evidence

- Model the actual installation and removal sequence, not only final poses. Include the complete key/driver body, socket engagement, approach, withdrawal, turning/reindexing space and relevant neighboring parts.
- Discrete collision-free samples establish only the sampled poses. For a continuous motion claim, use a conservative swept envelope, an analytic separation bound, or an equivalent coverage argument; retain the scope and assumptions with the result.
- Check the purchased board or module envelope as well as its printed cassette. A narrower printed carrier does not bound the wider board it contains.
- For through-hole assemblies, include the untrimmed contact tails, solder/pigtail process allowance, underside insulation and fastener/support stack, not only the flat PCB box. Distinguish board-top, board-underside, component seating-flange and table/floor datums. Read the actual dimensioned manufacturer drawing and tolerance notes before deriving heights. A retained contact-compression value couples PCB height, free-tip height, mating plane and the supported assembly pose; do not move one independently or assume tail trimming is an approved fix.
- Keep digital joint candidates separate from whole-assembly approval. Retain physical coupon, torque, tolerance, load, drop, service-cycle and safety gates. Explicitly state required power isolation, empty assembly state, and whether service requires lifting the unit off its supporting surface.
