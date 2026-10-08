---
name: icon-generation
description: Create or edit one or more raster icons as a visually coherent set, including collections split into groups with shared or group-specific visual systems. Use when icons need generated artwork, reference matching, consistent style across assets, or icon-set continuity. For existing repo-native SVG, CSS, canvas, or design-system icons, edit the native source directly instead.
metadata:
  short-description: Create coherent single icons and icon sets
---

# Icon Generation

Create icons as usable assets, not as a presentation sheet. Support one standalone icon, a coordinated set, or several groups whose icons share a visual language within each group. Preserve the user's descriptions and references, and make the requested degree of consistency explicit before generating.

## Workflow

1. **Choose the right medium.** Use the project's existing SVG, CSS, canvas, or icon library when the request is to extend that system. For newly generated raster artwork, use the built-in `$imagegen` path and follow `${CODEX_HOME:-$HOME/.codex}/skills/.system/imagegen/SKILL.md`. Do not switch to an image API or CLI unless the user explicitly requests or confirms that fallback.
2. **Turn the request into an icon brief.** Identify intended use and display size, output format/background, overall collection description, icon inventory, and any group boundaries. Preserve explicit choices. Infer only missing production details that can be decided safely, and state important assumptions briefly.
3. **Build a compact visual system.** Define the reusable style anchors before generation: silhouette language, geometry, stroke or edge treatment, palette, perspective, lighting, material/texture, detail density, canvas, safe margins, and background. Specify which are global and which may vary by group or icon. Capture each icon's unique subject and distinguishing feature separately.
4. **Assign references clear roles.** Mark each input as an identity/content reference, style reference, palette reference, composition reference, or edit target. Keep user-provided defining features intact. Use the strongest approved icon as the canonical style reference for sibling icons; do not rely on a prose description alone when the reference can be attached.
5. **Generate one deliverable icon per call.** Generate the first representative icon for a group, inspect it, and use it as a visual anchor for the remaining icons in that group. Generate distinct subjects with distinct prompts; do not ask for multiple unrelated icons in one image, use a grid as the deliverable, or treat `n` variants as a substitute for individual icon briefs. Variants of one icon are appropriate only when requested or useful for choosing a direction.
6. **Inspect and repair.** Review each output by itself and alongside its group at intended display size. Repair only the icon or property that failed, carrying forward the approved anchor and every property that already passed. Recheck the repaired icon in the collection.
7. **Save and report.** Keep final icons as separate, clearly named files. If intended for a project, copy the selected outputs into the workspace and any requested destination; do not leave project-referenced assets only in the default generated-images folder. A contact sheet may be provided as a preview in addition to the individual files, never instead of them.

For multi-group continuity, read [references/visual-continuity.md](references/visual-continuity.md) before generation.

## Prompt and output rules

- Keep each prompt focused on one icon. Include its ID or filename, subject, purpose, unique cue, shared visual anchors, framing, background/alpha needs, and the most important avoidances.
- Be specific without inventing content. If the user supplies a detailed description, normalize it into a clear visual spec rather than adding motifs, objects, text, brand cues, or narrative.
- Prefer a bold, simple silhouette, centered subject, consistent optical scale, and sufficient padding. Keep fine detail large enough to survive the smallest intended size; simplify rather than shrink details into noise.
- Do not add labels, letters, numbers, watermarks, UI, borders, decorative scenery, or unrelated props unless requested. Exact required text must be quoted in the prompt and inspected character by character.
- Use a transparent background when the user requests it or the asset's use calls for it. Preserve and inspect the generated alpha; otherwise use the background specified by the user or intended UI context. Do not simulate transparency with a checkerboard.
- Keep canvas dimensions, crop, subject scale, baseline, visual center, padding, edge treatment, and rendering quality consistent across siblings. Allow optical adjustment when mathematical alignment would make one icon appear heavier or smaller.
- Match palette, contrast, edge softness, stroke weight, lighting direction, shadow treatment, material response, perspective, and detail density across icons in a group. Do not accidentally mix flat/vector, outlined, painted, pixel, and 3D rendering treatments.
- Never imply that generated outputs are vectors. If editable vector output is required, use the established native/vector workflow or ask for the requested vector source format.

## Completion criteria

A set is ready when each requested icon exists separately, reads clearly at its intended size, matches its own description, and preserves the group's approved visual anchors. Review identity drift, inconsistent framing or optical scale, palette and lighting drift, inconsistent edges or materials, accidental background pixels or halos, clipped silhouettes, weak contrast, stray objects, and unintended text. A single icon still needs a legible silhouette and clean export; set continuity is not a reason to add unnecessary decoration.

If a generated icon fails, identify the visible mismatch and make one targeted correction. Keep all successful properties fixed, reuse the canonical reference, and compare before and after at the same scale. Do not regenerate the entire collection for one local defect.
