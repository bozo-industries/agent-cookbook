# Blender automation

## Render engine identifiers

Do not assume `BLENDER_EEVEE_NEXT` is a valid `bpy` render-engine identifier from
the installed Blender version or its marketing name.  Query
`bpy.types.RenderSettings.bl_rna.properties['engine'].enum_items` when a script
must support an unknown installation.  In Blender 5.2, select Eevee with
`scene.render.engine = "BLENDER_EEVEE"`.

## Background Python failure propagation

Launch validation and rendering scripts with `--python-exit-code 1` before
`--python`. Without that option, Blender can print an uncaught Python exception
and still exit with status zero. Require both a successful native exit and the
expected fresh, source-bound report; neither process completion nor an old
report proves the script passed. When collecting output before filtering it,
capture the exit code immediately and propagate it after the reporting step.

## Sibling Python helpers

Blender's `--python` invocation may not add the script's directory to
`sys.path`. Before importing a sibling helper, explicitly add the verified
`Path(__file__).resolve().parent` directory. Inspect the helper for a guarded
entry point so importing it cannot start a second build or overwrite outputs.
Verify the import in the actual Blender runtime before an expensive render;
do not change the current working directory or install a package to compensate.

## Recovering a graphics-backend render failure

If a graphics backend crashes after saving a view, preserve that image and each
already-saved scene. Verify the failed worker is terminal, then resume from the
specific saved scene with Cycles and `scene.cycles.device = "CPU"` instead of
rebuilding CAD, restarting the driver, or retrying the unchanged graphics backend.
Compare loaded mesh coordinates, topology and poses with the source-bound geometry
before rendering. Write fresh output names and record source-scene/output hashes.
Keep process-tree resource limits, allow measured same-runtime headroom, and require
both native success and a fresh render report. A crash module and diagnostics, not
merely a peak near a memory limit, establish which failure layer is evidenced.

For millimetre-coordinate engineering scenes, make illumination consistent with
the camera and length scale. Area-light attenuation can leave an underside view
unreadably dark. Use an appropriate ambient/directional light or scale-aware area
lighting, then inspect the actual pixels; successful rendering alone is not visual QA.
