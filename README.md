# Woodworking

Furniture I'm building, designed before it's cut. Each piece is a parametric
OpenSCAD model, and everything downstream — the shop drawings, the jig models,
the cut lists, the photoreal renders and the illustrated build guides — is
generated from that model, so none of it can drift from the design.

| | | |
|---|---|---|
| **[Document unit](projects/document-unit/)** | 10 cells for letter and A4 laid flat, in pine. 26-1/4 × 9-1/4 × 22. | **building first** · [guide](https://claude.ai/code/artifact/87fcd98c-7703-488a-8ec8-152ccdd2b3c9) |
| **[Wine rack](projects/wine-rack/)** | 12 bottles in walnut, on splayed tapered legs. 10-1/4 × 9 × 39-1/2. | the real one · [guide](https://claude.ai/code/artifact/a3f2afa2-34b5-4bcf-a35a-0f884b502578) |
| **[Coffee table](projects/coffee-table/)** | 48 × 21 × 15 in solid walnut, all joinery hidden. | someday |

![Walnut wine rack](projects/wine-rack/renders/beauty_walnut.png)

The document unit and the wine rack are **the same model** — one parametric
cell-grid case in [`lib/casework.scad`](lib/casework.scad), with the cell
proportions and the legs switched by parameter. That is deliberate: the
document unit is a full rehearsal of the wine rack's joinery at a more
forgiving scale and in cheaper wood, and building it teaches the real piece.

## Layout

```
lib/         shared across every project
projects/    one directory per piece
```

`lib/` is the part that gets reused. The wood shader, the jig models and the
guide generator have nothing to do with any particular piece of furniture.

| | |
|---|---|
| `lib/casework.scad` | the parametric cell-grid case — wine rack *and* document unit |
| `lib/jigs.scad` | the shop jigs, drawn so they can be seen rather than imagined |
| `lib/export_casework.scad` | writes one STL per board, for the renderer |
| `lib/scene.py` | the Cycles scene: procedural wood, studio lights |
| `lib/guide.py` | builds the illustrated shop guides |
| `lib/cameras.sh` | camera helpers — every camera in this repo is written in inches |
| `lib/render_jigs.sh` | renders the jig drawings both guides pull from |

Each project directory holds its own model or preset, its docs, its
`render.sh` / `render_beauty.sh`, and its own `renders/` and `exports/`.
Run the scripts from anywhere; they locate the repo root themselves.

The coffee table keeps its model in its own directory rather than in `lib/`,
because nothing else uses it. `casework.scad` is in `lib/` because two projects
do.

## Requirements

```sh
brew install --cask openscad   # working drawings, meshes, jig drawings
brew install --cask blender    # photoreal renders only (optional)
pip install pillow             # the guide generator inlines its images
```

Nothing else. The wood shader is procedural, so there are no texture files to
download, and every drawing is generated rather than drawn.

## Regenerating everything

```sh
projects/wine-rack/render.sh          # OpenSCAD views + STL/3MF   (seconds)
projects/wine-rack/render_beauty.sh   # per-part STLs + Cycles     (minutes)
lib/render_jigs.sh                    # the shared jig drawings
python3 lib/guide.py                  # -> projects/wine-rack/guide.html
python3 lib/guide.py documents        # -> projects/document-unit/guide.html
```

### Units

The design math is in inches, but every model is scaled by `UNIT = 25.4` on
output, so the scene OpenSCAD draws is in millimetres. This matters: a 40-unit
tall object sits right on OpenSCAD's near clip plane, which is what makes the
view clip when you zoom in and makes the mouse feel hair-trigger. At mm scale
the object is ~1000 units and navigates normally.

Set `UNIT = 1` for exports in inches — the render scripts scale their camera
positions by the same factor, so they follow automatically.

### Beauty renders

The wood is fully procedural — no texture files — so it renders anywhere with
nothing to download. Growth rings are built as concentric cylinders about a
pith axis outside the board, so cathedral figure is *derived* from where the
board sits in the log rather than faked. Each board is imported as its own
object and the shader offsets it by `Object Info > Random`, anisotropically
(metres along the grain, ±15 mm across it) so no two boards match without
moving the pith itself.

Species live in `WOODS` at the top of [`lib/scene.py`](lib/scene.py): a ring
`profile` (`SAW` for softwoods — gradual earlywood, abrupt boundary; `SIN` for
diffuse-porous hardwoods), a colour pair, and a knot density. Add one and it
becomes a `--wood` choice.
