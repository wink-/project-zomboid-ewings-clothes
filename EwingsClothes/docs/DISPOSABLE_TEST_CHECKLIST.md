# 1.1.0 disposable tests — not run in game

Only perform after authorizing installation/game operation; never use a valuable live save to discover compatibility.

- [ ] Install only this version, confirm modID/version and all three debug item IDs.
- [ ] Check new Dog/Cat front art, plain backs, sleeves/necklines, animations and clothing layers on both sexes. Confirm One Job is unchanged.
- [ ] Gather both plain-shirt variants, native brushes, partially used paint cans and eligible photos. Confirm quantities/retained tools match the recipe document.
- [ ] With only a wrong-animal, scenic, missing-key or unrelated photo, ensure the corresponding recipe cannot craft. Test wrong photo first in inventory plus a matching photo later; the qualifying reference must be selected.
- [ ] Test every listed dog/cat variant and combined dog-and-cat photo. Confirm photo ID/modData/condition and brush persist over repeated crafts.
- [ ] Test unworn versus worn shirts. Damaged, dirty, bloody, patched and wet eligible inputs must preserve state; output must keep the new fixed art instead of random tint/decal.
- [ ] Check one native use per paint, depletion behavior and normal empty-bucket replacement; missing or insufficient paint must prevent crafting. Check no accidental whole-can destruction.
- [ ] Test single crafting, cancellation, changing selected inventory inputs and output naming. No One Job or already-animal shirt is a blank input.
- [ ] Inspect new/generated shirt-store/storage/wardrobe containers under normal loot settings. Existing generated containers must not be forced to respawn/refill. Other loot remains present.
- [ ] Test save/reload, item transfer/drop/pickup, and rollback after removing new item instances.
- [ ] With identical packages on server/two clients, test remote crafting eligibility, retained photos, state transfer, rendering, server loot generation and rejoin/restart persistence.

Record build/hash and outcomes separately. Offline native-parser/VM/mocked checks do not tick these gameplay boxes.
