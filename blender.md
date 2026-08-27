# Blender automation

## Render engine identifiers

Do not assume `BLENDER_EEVEE_NEXT` is a valid `bpy` render-engine identifier from
the installed Blender version or its marketing name.  Query
`bpy.types.RenderSettings.bl_rna.properties['engine'].enum_items` when a script
must support an unknown installation.  In Blender 5.2, select Eevee with
`scene.render.engine = "BLENDER_EEVEE"`.
