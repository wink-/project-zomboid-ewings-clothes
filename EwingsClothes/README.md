# Ewing's Clothes

An independent Project Zomboid Build 42 clothing mod. Version **1.0.0** adds a solid purple T-shirt with the exact words **One Job** in bold yellow on the front chest. The back is plain purple.

![Offline male/female front and back preview](preview/EwingsClothes-1.0.0-front-back-preview.png)

The image is an offline Blender UV preview, not an in-game screenshot. Game loading, equip/render, animation, save/reload and multiplayer tests have **not** been run.

| Identity | Value |
| --- | --- |
| Mod ID | `EwingsClothes` |
| Item ID | `EwingsClothes.OneJobTShirt` |
| Inventory name | One Job T-shirt |
| Version | 1.0.0 |
| Inspected target | Game 42.21, Steam build 25485521, Windows |
| Bounds | 42.21 only; later builds require reinspection |

## Download and install

Download **EwingsClothes-1.0.0-install.zip** and its `.sha256` sidecar from the [v1.0.0 release](https://github.com/wink-/project-zomboid-ewings-clothes/releases/tag/v1.0.0). GitHub's automatic source archives are development source, not the install ZIP.

1. Close the game/server and back up any world you intend to test.
2. Extract the single `EwingsClothes` folder into the effective Project Zomboid user-data `mods` directory. Normally this is `%UserProfile%\Zomboid\mods` on Windows; custom `-cachedir` changes it.
3. Confirm `mods/EwingsClothes/42/mod.info` with sibling `mods/EwingsClothes/common/`.
4. Enable **Ewing's Clothes** in a disposable test world and complete the [test checklist](docs/DISPOSABLE_TEST_CHECKLIST.md).

Do not overwrite the game installation or another Ewing's mod. No Python, Blender or additional mod dependency is needed to play. There is no Workshop item or Workshop ID.

## Find and spawn the shirt

Search **`EwingsClothes.OneJobTShirt`** in the debug item browser and add it to inventory. A debug Lua console, if available in your setup, can use:

```lua
getPlayer():getInventory():AddItem("EwingsClothes.OneJobTShirt")
```

Debug console availability is not certified. Version 1.0.0 adds no natural loot distribution or crafting recipes. Wear the shirt through the normal clothing action.

## Behavior and balance

Uses the native `base:tshirt` slot, `BloodLocation = Shirt`, cotton fabric and native T-shirt body-layer behavior for male and female characters. Random hue/tint are disabled; there is no dye tag. Blood, dirt, holes, patches or covering garments may obscure the print normally.

Insulation **0.2** and wind resistance **0.05** match vanilla `Tshirt_DefaultTEXTURE`; weight **0.3** is a mod-selected light cotton shirt value. Other protection/durability behavior uses native defaults. Cotton ripping is retained. Native `TShirt_Ground` is referenced without bundling a model; its appearance needs in-game confirmation.

No global overrides, Lua hooks, new equipment slots, executable runtime code or networking system are added. The clothing GUID table has one owned entry and uses the native merge path.

## Validation and limitations

**29 offline checks pass:** references, stable IDs/GUID, fixed-color fields, PNG dimensions/alpha, front-chest UV placement/orientation for both bodies, ZIP integrity and exact member bytes. Preview inspection caught and corrected sleeve coverage and chest placement before the final build. The final preview shows readable front text and plain backs on both bodies.

**Not run:** native game loading, actual debug browser/equip/render, animation/layering, dropped-item rendering, damage/washing, save/reload or multiplayer. Offline checks are not gameplay certification. See [inspection evidence](docs/INSPECTION.md), [validation results](docs/VALIDATION.json) and [publication preservation evidence](docs/PUBLICATION_VALIDATION.json).

The public ZIP has sanitized documentation and a new checksum. Its `42/` and `common/` runtime files, original texture/icon and stable IDs are byte-identical to the originally checked build.

## Multiplayer and rollback

Server and every client need the identical package, with `EwingsClothes` in the server mod list. MP support is an untested expectation; test two clients and persistence in a disposable world first.

For updates, back up the complete mod folder outside active mod directories and replace it as a unit. Before removal, remove all `EwingsClothes.OneJobTShirt` instances from characters, containers and ground, save, then disable/remove only this mod. Missing definitions can make remaining instances disappear or log errors. Restore the matching package and an appropriate backup if needed. Preserve the stable IDs.

## Source and provenance

`EwingsClothes/` is the portable mod. `art/` contains original SVG/PNG sources and color/print specifications; `preview/` contains offline renders; `tools/` contains development utilities. New clothing should receive unique item names, GUIDs, textures and icons while preserving current IDs.

See [README-BUILD.md](README-BUILD.md), [CHANGELOG.md](CHANGELOG.md) and [NOTICE.md](NOTICE.md). No repository-wide open-source license has been selected. No proprietary game textures, models, scripts, binaries, saves or font files are redistributed. This project is independent of The Indie Stone.
