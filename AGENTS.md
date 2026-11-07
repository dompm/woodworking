# Collection guidance

Discuss meaningful design and fabrication tradeoffs before changing approach.
Keep agent guidance focused on transferable intent and non-obvious constraints.
Use examples sparingly; extract the general rule instead of turning a particular
project's solution into policy. Implementation details belong in shared code.

## Visual identity

Quiet studio product photography, restrained technical drawings, and warm
editorial guides should read as one collection across project pages and guides.
Use plain, descriptive copy. State what a project is and what is known about it;
omit slogans, marketing claims and self-conscious language about making things.

- **Renders:** use [lib/render_style.py](lib/render_style.py) for the grey studio,
  soft lighting and color management. Compose for each object's proportions;
  comparable variants should retain the same angle, crop and scale. Keep
  headings, dimensions and website chrome outside the reusable image.
- **Materials:** preserve species and grain direction. Plywood layers belong
  on cut edges, not broad faces. Materials and cameras remain project-specific;
  sharing a studio does not mean imposing one material or camera on every object.
- **Drawings:** use [lib/render_drawing.py](lib/render_drawing.py) and
  [lib/drawing_theme.json](lib/drawing_theme.json) for OpenSCAD publication views.
  Use neutral stock, muted teal highlights, thin lines and external labels.
  Show reference edges and motion where an assembly or operation depends on them.
- **Guides:** use [lib/guide_style.css](lib/guide_style.css) for palette,
  typography and spacing. Lead with the object and purpose, then pair process
  illustrations with concise step instructions. Preserve full-resolution
  masters separately from website-sized derivatives.

## Sources and constraints

Rendered assemblies and cut lists derive from CAD exports. A presentation pass
preserves dimensions, build sequence and project-specific caveats. Label
simplified tools and omitted setup components in process illustrations.
Use [TOOLS.md](TOOLS.md) when choosing fabrication methods.

Generated guide pages are outputs of their editable sources. Existing casework
uses [lib/guide.py](lib/guide.py); Markdown guides share
[lib/guide_pages.py](lib/guide_pages.py). Local guide pages are the publication
source rather than account-gated artifact links. Keep necessary rationale near
its model or generator and remove obsolete guidance.
