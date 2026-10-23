require "Items/ProceduralDistributions"

-- Additive relative weights, not percentages. Existing tables are never replaced.
local pools = {
    ClothingStoresShirts = 0.2,
    ClothingStorageAllShirts = 0.1,
    WardrobeGeneric = 0.05,
}
local shirts = {
    "EwingsClothes.OneJobTShirt",
    "EwingsClothes.DogTShirt",
    "EwingsClothes.CatTShirt",
}

for name, weight in pairs(pools) do
    local pool = ProceduralDistributions.list[name]
    if pool and type(pool.items) == "table" then
        for _, item in ipairs(shirts) do
            local found = false
            for i = 1, #pool.items, 2 do
                if pool.items[i] == item then found = true; break end
            end
            if not found then
                table.insert(pool.items, item)
                table.insert(pool.items, weight)
            end
        end
    else
        print("[EwingsClothes] Missing native clothing loot pool: " .. name)
    end
end
