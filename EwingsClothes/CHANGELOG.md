# Changelog

## 1.1.0 — staged animal shirt update

- Added fixed original Dog and Cat shirts, matching photo-reference recipes, and original SVG/PNG/icon sources.
- Kept One Job item/XML/texture/icon, original art and earlier previews byte-for-byte; retained `EwingsClothes` mod ID.
- Photos (`Base.Photo` with matching native collectible keys) and native brushes are retained. Four verified native paint types cost one use each; a consumed unworn plain shirt supplies preserved garment state through `CopyClothing`.
- Added all three shirts at low relative weights to three standard clothing pools; guarded repeated loads, no overwrites or forced respawn.
- Added native parser/Kahlua and offline asset/preservation checks and inspected CPU UV preview pixels. Actual gameplay/render/crafting UI/MP tests remain not run.
- Developed only in a separate 1.1.0 staging tree; not installed, enabled, pushed or published.

## 1.0.0 — 2026-10-22

- Initial independent `EwingsClothes` mod for inspected game 42.21, Steam build 25485521.
- Added `EwingsClothes.OneJobTShirt`: fixed purple cotton shirt, yellow **One Job** on front, plain back.
- Original 1024px body-atlas texture, 128px inventory icon and editable art sources.
- Native T-shirt clothing slot, vanilla ground-model reference, unique GUID mapping and English item name.
- No crafting, loot distribution, overrides or custom executable runtime code.
- Offline validation and local male/female front/back preview; actual game and MP validation pending.
