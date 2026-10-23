-- Native ProceduralDistributions has already been loaded by the Kahlua runner.
local checks = 0
local function check(v, message) assert(v, message); checks = checks + 1 end
local pools = {ClothingStoresShirts=0.2, ClothingStorageAllShirts=0.1, WardrobeGeneric=0.05}
local ids = {"EwingsClothes.OneJobTShirt", "EwingsClothes.DogTShirt", "EwingsClothes.CatTShirt"}
for name, weight in pairs(pools) do
    local before = EwingsClothesTestBefore[name]
    local current = ProceduralDistributions.list[name]
    check(current == before.identity, "pool object replaced")
    check(current.rolls == before.rolls, "roll count changed")
    check(#current.items == #before.items + 6, "wrong additive entry count")
    for i, value in ipairs(before.items) do check(current.items[i] == value, "native entry changed") end
    for _, id in ipairs(ids) do
        local found = 0
        for i=1,#current.items,2 do
            if current.items[i] == id then found=found+1;check(current.items[i+1] == weight, "wrong relative weight") end
        end
        check(found == 1, "missing or duplicate new item")
    end
end
for name, pool in pairs(ProceduralDistributions.list) do
    local before = EwingsClothesTestUnrelated[name]
    if before then
        check(pool == before.identity, "unrelated pool replaced")
        if before.items then
            check(#pool.items == #before.items, "unrelated pool length changed")
            for i,value in ipairs(before.items) do check(pool.items[i] == value, "unrelated pool entry changed") end
        end
    end
end
return "distribution assertions passed after repeated loads", checks
