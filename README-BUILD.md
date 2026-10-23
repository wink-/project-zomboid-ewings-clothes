# Development and release checks

Runtime players need only the install ZIP; Python and Blender are development tools.

## Validate and package

Use Python 3.12 or a compatible Python 3 with the standard library. Supply your own installed game directory:

```text
python tools/validate_and_package.py --game "<ProjectZomboid game directory>"
```

The validator targets game 42.21 and Steam build 25485521. It reads selected installed files without changing them. It checks native item/XML/model/texture references, GUID/item identity, PNG dimensions/alpha, front-chest UV samples/orientation, original art identity, portable layout and ZIP member bytes. It writes `dist/` ZIPs and SHA-256 sidecars. It does not install, launch the game/server or access saves.

Packaging does not require regenerating art or previews. The release contains the original ready-to-load PNGs and existing preview.

## Optional art and preview regeneration

Art regeneration requires Pillow and a legally available bold font. The original build used Arial Bold; a different font can change the lettering and requires review.

```text
python tools/build_art.py --font "<bold font file>"
blender --background --factory-startup --python tools/render_preview.py -- --game "<ProjectZomboid game directory>"
python tools/compose_preview.py --bold-font "<bold font file>" --regular-font "<regular font file>"
```

Use an already installed Blender; the checked preview used Blender 5.2.3 LTS. Native body coordinates are read in memory only. Do not export or commit game meshes, textures, scenes or source.

## Publication verification

The 29 offline checks are documented in `docs/VALIDATION.json`; runtime testing remains pending. `docs/PUBLICATION_VALIDATION.json` records original hashes and exact runtime/art preservation after sanitization. Verify downloaded ZIP checksums against the release sidecars, CRC/member layout and downloaded members against the tagged `EwingsClothes/` folder.

Do not publish local paths, credentials, game assets, logs or saves. `dist/` and caches are ignored. Read `NOTICE.md` for license/provenance; no new repository-wide license is assumed.
