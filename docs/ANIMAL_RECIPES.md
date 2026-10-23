# Animal designs and photo recipes — 1.1.0

Two fixed, original illustrations: friendly cream/brown dog on teal, orange tabby cat on navy. No slogans or native photo pixels. Each photo acts as a reusable drawing reference; changing the photo variant never changes the output design.

## Exact recipes

Both one-step recipes are in **Tailoring**, use the native MixingBucket action, take 180 native recipe-time units and allow one craft at a time. Time and ingredient amounts are mod-selected balance choices, not a chemical/fabric-paint simulation. No skill unlock or new dependency is required.

| Input | Dog recipe | Cat recipe | Result |
| --- | --- | --- | --- |
| Plain T-shirt | 1 `Base.Tshirt_DefaultTEXTURE` OR `Base.Tshirt_WhiteTINT` | same | Consumed/replaced; must be unworn |
| Matching photograph | 1 `Base.Photo`, dog key below | 1 `Base.Photo`, cat key below | **Retained**, not consumed |
| Paintbrush | 1 `Base.Paintbrush` OR `Base.PaintbrushCrafted` | same | **Retained** |
| Base-color paint | 1 use `Base.PaintTurquoise` | 1 use `Base.PaintBlue` | One native drainable use consumed |
| Portrait paint | 1 use `Base.PaintBrown` | 1 use `Base.PaintOrange` | One native drainable use consumed |
| Light paint | 1 use `Base.PaintWhite` | same | One native drainable use consumed |
| Outline paint | 1 use `Base.PaintBlack` | same | One native drainable use consumed |
| Output | 1 `EwingsClothes.DogTShirt` | 1 `EwingsClothes.CatTShirt` | Fixed design/color |

The six paint types are actual native drainable items with `UseDelta=0.1`; recipes use native item-use counts, **not fluid liters**, and do not destroy whole paint cans. Native depletion/empty-bucket behavior applies. Using ordinary game paint on clothing is explicitly a gameplay abstraction; no fictitious fabric-paint item is introduced.

## Matching photographs

Dog/cat photographs are subjects of **`Base.Photo`**, not separate dog/cat item IDs. The predicate checks `item:getModData().collectibleKey`, never translated display names. Do not substitute a scenic/racy/secret/very-old photo type.

Dog whitelist:

- `IGUI_Photo_aDog`
- `IGUI_Photo_aSleepingDog`
- `IGUI_Photo_DogsPlaying`
- `IGUI_Photo_aChildPlayingWithaDog`
- `IGUI_Photo_aDogandaCat`

Cat whitelist:

- `IGUI_Photo_aCat`
- `IGUI_Photo_aSleepingCat`
- `IGUI_Photo_aChildPlayingWithaCat`
- `IGUI_Photo_aDogandaCat`

The combined dog-and-cat photo works for either recipe and remains reusable. Empty, missing, unrelated, case-mismatched or wrong-animal keys fail qualification. A debug-created generic `Base.Photo` may randomize to an unrelated subject; owning any photo is not sufficient. Actual crafting UI selection of the qualifying photograph remains an in-game test item.

## Garment state

The consumed shirt has native flags `IsNotWorn;CopyClothing`. The inspected engine resolves CopyClothing through `InventoryItem.copyClothing` to the installed `copyClothingItem` routine. This preserves visual dirt/blood/holes/patches, garment condition, wetness, patches, favorite state and modData. It does not freely repair or wash the shirt. The allowed plain inputs have a single base texture; no `InheritColor` flag is used. New clothing XML disables random hue/tint and has no dye tag, so the output uses the fixed baked design under normal native creation. Other mods/debug recoloring can alter normal behavior.

## Additive natural loot

All three shirts (existing One Job, Dog, Cat) are appended once to these inspected native pools:

| Native pool | Each shirt's relative weight |
| --- | --- |
| `ClothingStoresShirts` | 0.2 |
| `ClothingStorageAllShirts` | 0.1 |
| `WardrobeGeneric` | 0.05 |

These are **relative weights, not spawn percentages**. Native rolls, loot rarity and other mods affect results. Wardrobe aliases that share the generic table inherit its additions. No lists, native entries, roll counts or unrelated pool tables are replaced; repeat loads do not duplicate entries. No zombie outfits or photo distributions are changed. New content appears only when normal loot generation/server respawn rules generate containers; this mod does not force respawns or refill existing containers.
