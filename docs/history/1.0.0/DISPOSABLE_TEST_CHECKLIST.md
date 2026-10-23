# Disposable-world acceptance checklist — not yet run

Only perform these steps after authorizing installation and game/server operation. Use a fresh disposable world and only Ewing's Clothes first. Do not use a valuable save as the test target.

- [ ] Confirm game reports 42.21 and package hash matches the provided sidecar.
- [ ] Install/enable only `EwingsClothes`; confirm mod name/version and no loading/XML/translation/texture warnings.
- [ ] Search `EwingsClothes.OneJobTShirt` in debug item browser; add multiple copies. Confirm name, original purple/yellow icon and fixed color across instances.
- [ ] Wear via normal inventory action. Confirm T-shirt slot, pullover action and successful unequip/re-equip.
- [ ] Test male and female bodies: front reads exact **One Job** left-to-right at chest; back stays plain. Inspect neckline, shoulder, sleeve and waist seams at all rotations.
- [ ] Check idle, walking, running, crouching, aiming, combat and seated poses for seam gaps/stretching. Text should stay within the front panel.
- [ ] Wear/remove shirts and jackets over it; verify native layering and reappearance of the design.
- [ ] Test blood, dirt, holes, repair patches, washing and wet/dry behavior. Damage may obscure the print; washing should not recolor the baked design.
- [ ] Check cotton ripping and inherited statistics, 0.3 weight, 0.2 insulation and 0.05 wind resistance.
- [ ] Drop, rotate and pick up the shirt. Confirm native ground mesh loads and its texture is acceptable.
- [ ] Save/reload and restart the disposable world. Verify worn, inventory, container and dropped items retain the full ID and visual.
- [ ] Confirm no added recipes or natural loot distribution; debug spawning is the intended availability in 1.0.0.
- [ ] Repeat with intended other mods only after isolated checks pass.
- [ ] Dedicated/local MP disposable world: identical package on server and two clients; both genders observed by another client; equip/transfer/drop, rejoin, server restart and persistence.
- [ ] Review logs from these tests without uploading private saves or unrelated logs.

Record the exact build, package SHA, pass/fail and any screenshots separately. Offline previews and checks do not mark these boxes passed.
