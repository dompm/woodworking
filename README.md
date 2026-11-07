# Woodworking

Models, drawings and build notes for my woodworking projects.

Browse the [projects and build guides](https://woodworking.dominiquepiche.com/).

| Project | Description | Status | Build notes |
|---|---|---|---|
| [Travel Yahtzee box](https://woodworking.dominiquepiche.com/projects/travel-yahtzee/) | A sliding-lid box for five dice, a mini mechanical pencil and a 4 × 6-inch scorepad. | Design | [Box build guide](https://woodworking.dominiquepiche.com/guides/travel-yahtzee/guide.html) · [Optional router table and finger joints](https://woodworking.dominiquepiche.com/guides/travel-yahtzee/router-table-guide.html) |
| [Document unit](https://woodworking.dominiquepiche.com/projects/document-unit/) | A pine unit with ten compartments for letter and A4 folders. | Built | [Build guide](https://woodworking.dominiquepiche.com/guides/document-unit/guide.html) |
| [Wine rack](https://woodworking.dominiquepiche.com/projects/wine-rack/) | A twelve-bottle rack with housed shelves and splayed legs. | Design | [Build guide](https://woodworking.dominiquepiche.com/guides/wine-rack/guide.html) |
| [Salt boxes](https://woodworking.dominiquepiche.com/projects/salt-boxes/) | Two small hardwood boxes with pivoting lids, sized for MSG and sugar. | Design | [Build notes](https://woodworking.dominiquepiche.com/guides/salt-boxes/guide.html) |
| [Bedside table](https://woodworking.dominiquepiche.com/projects/bedside-table/) | An open birch cubby on tapered steel legs. | Design | [Build guide](https://woodworking.dominiquepiche.com/guides/bedside-table/guide.html) |

## Website

The static website is built from `site/projects.json` and the project files.
The same catalog supplies the project list above. Edit `site/readme.md.in` for
the rest of this README.

```sh
python3 site/build.py
python3 -m http.server 8000 --directory site/dist
```

Open [localhost:8000](http://localhost:8000) to preview it. Upload the contents
of `site/dist/` to a static web host to publish it.

## Files

- `projects/`: models, renders, build notes and generated guides for each project.
- `lib/`: shared models, rendering tools and guide styles.
- [TOOLS.md](TOOLS.md): shop tools and accessories.
- [JIGS.md](JIGS.md): jig designs and setup notes.
- [SHOPPING.md](SHOPPING.md): materials and tools still to buy.

The document unit and wine rack use the same casework model with different
parameters. The other projects have their own models.

## Generating drawings and guides

OpenSCAD generates the working views and meshes. Blender generates the studio
renders. Python and Pillow are used for publication images, guides and the site.

```sh
brew install --cask openscad blender
python3 -m pip install pillow

projects/wine-rack/render.sh
projects/wine-rack/render_beauty.sh
lib/render_jigs.sh
python3 lib/build_guides.py
```

Each project contains its own generation scripts. Design dimensions are in
inches unless noted; the OpenSCAD models export millimetres by default.
Check stock thickness and fit before using a generated cut list.
