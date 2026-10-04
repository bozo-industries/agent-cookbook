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
