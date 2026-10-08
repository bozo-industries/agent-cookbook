# Visual Continuity for Icon Collections

Use this reference for a coordinated icon set or for multiple groups. Keep the generation plan short enough to use: record only visual decisions that affect how the icons must match.

## Brief structure

Write a compact brief containing:

- **Collection:** its purpose, audience, and one-sentence set description.
- **Groups:** each group name, relationship to the larger collection, and whether it inherits the global style or has its own style anchors.
- **Icons:** a stable ID or filename, subject, intended meaning/use, distinctive silhouette or feature, and any icon-specific exclusions.
- **Shared anchors:** style, geometry, palette, edge/stroke treatment, perspective, lighting, material, detail density, canvas/crop, safe margins, background, and output requirements.
- **Allowed variation:** the features that may change per icon or group, such as subject, pose, secondary accent color, or one material cue.
- **References:** each image/file and the role it plays; name a canonical approved icon for every group.

A useful icon list can be a small table. Do not force a schema on a simple one-icon request; retain the same thinking without creating paperwork.

## Continuity hierarchy

Treat visual sources in this order unless the user sets another priority:

1. User's explicit instructions and approved brand/design constraints.
2. User-provided identity or content references for the subject's defining features.
3. Approved canonical icon for the same group, for rendering style and collection consistency.
4. Supporting references for palette, material, lighting, or composition.
5. The written brief for details that are absent from the images.

Do not let a style reference replace the requested subject, and do not let one icon's incidental features become collection-wide rules. Never copy a logo or protected mark from a reference unless the user has supplied it and explicitly asked for its use.

Keep identity and rendering separate. For each icon, lock the intended subject, category, key silhouette, signature details, and meaning. For each group, lock rendering choices such as geometry, corners, stroke width, palette, viewing angle, light direction, shadows, material, texture, and density. This makes icons distinct in meaning while still related in appearance.

## Groups and anchors

A collection may have one system across all icons or multiple group systems:

- Record collection-wide invariants first (for example, canvas, padding, edge cleanliness, or a shared brand accent).
- Give each group its own palette, materials, perspective, and canonical style icon when the groups intentionally differ.
- Match icons within a group tightly. Preserve only the declared collection-wide invariants across groups; do not force a shared rendering style when the request calls for distinct groups.
- Generate one representative icon per group first. Inspect and approve its style, then attach it as the group's style reference for the other icons.
- If two groups must blend, identify the bridge features that both share and the details that remain group-specific.

## Generation and repair

For each icon, use a concise prompt built around:

- Stable icon ID and exact subject/meaning.
- Distinctive content and required details.
- Group's approved style anchors and attached canonical reference.
- Composition, viewpoint, scale, and safe margins.
- Background or transparency and intended use.
- A short avoid list for likely errors.

Generate separate icons in separate calls so each has its own subject brief and output. Reuse the group anchor and the same concise style-lock wording for every sibling. Attach identity references when they define subject details; attach style references for matching rendering. For edits, clearly identify which image is the target and which images are references, and list the invariants to preserve.

When an icon needs repair, classify the issue (wrong meaning, identity drift, style drift, crop/scale, contrast/readability, edge/alpha, text, or stray detail). Make one focused change, preserve properties that already pass, and review the result beside its unchanged siblings. Do not regenerate passing icons just to make the process uniform. If the group anchor itself is wrong, approve a replacement anchor and then update only the affected group members that no longer match.

## Review checklist

Review each final image both alone and in its group, at full resolution and at the smallest intended display size:

- Meaning and silhouette are recognizable without relying on a label.
- Defining details match the description and identity references.
- Siblings have compatible canvas, optical scale, center, crop, padding, edge/stroke weight, contrast, palette, perspective, lighting, material, and detail density.
- Group boundaries are clear; only intended traits carry across groups.
- No unintended text, logo, symbol, prop, duplicated object, clipped edge, stray pixel, blur, halo, shadow, or background fragment appears.
- Alpha is truly transparent when requested, with clean edges and no matte fringe; otherwise the background is uniform and intentional.
- The exported dimensions and format meet the destination's requirements.

A contact sheet is a useful comparison aid. Keep it as a review/preview artifact and verify that each source icon remains a separate deliverable.

## Handoff

Save final assets using stable, descriptive names that map to the brief (for example, `navigation-home.png` or `alerts-warning.png`). For multi-group collections, preserve group names in filenames or folders. Report the set description, group organization, final file paths, format and dimensions, any assumptions that materially affected output, and any icon that remains unresolved. Include a preview sheet only when useful or requested.
