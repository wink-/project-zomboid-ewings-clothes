-- Run in the installed native Kahlua VM with the mod checks already loaded.
local checks = 0
local function check(value, message)
    assert(value, message)
    checks = checks + 1
end
local function item(fullType, key)
    local data = {collectibleKey = key}
    return {
        getFullType = function() return fullType end,
        getModData = function() return data end,
        getDisplayName = function() return "arbitrary translated name" end,
    }
end
local dogKeys = {"IGUI_Photo_aDog", "IGUI_Photo_aSleepingDog", "IGUI_Photo_DogsPlaying", "IGUI_Photo_aChildPlayingWithaDog", "IGUI_Photo_aDogandaCat"}
local catKeys = {"IGUI_Photo_aCat", "IGUI_Photo_aSleepingCat", "IGUI_Photo_aChildPlayingWithaCat", "IGUI_Photo_aDogandaCat"}
for _, key in ipairs(dogKeys) do
    local photo = item("Base.Photo", key)
    check(EwingsClothesRecipeChecks.dogPhoto(photo, nil), "dog variant rejected")
    check(photo:getModData().collectibleKey == key, "reference photo mutated")
end
for _, key in ipairs(catKeys) do
    local photo = item("Base.Photo", key)
    check(EwingsClothesRecipeChecks.catPhoto(photo, nil), "cat variant rejected")
    check(photo:getModData().collectibleKey == key, "reference photo mutated")
end
for _, key in ipairs({"IGUI_Photo_aCat", "IGUI_Photo_aSleepingCat", "IGUI_Photo_aChildPlayingWithaCat"}) do
    check(not EwingsClothesRecipeChecks.dogPhoto(item("Base.Photo", key), nil), "cat accepted for dog")
end
for _, key in ipairs({"IGUI_Photo_aDog", "IGUI_Photo_aSleepingDog", "IGUI_Photo_DogsPlaying", "IGUI_Photo_aChildPlayingWithaDog"}) do
    check(not EwingsClothesRecipeChecks.catPhoto(item("Base.Photo", key), nil), "dog accepted for cat")
end
for _, key in ipairs({"IGUI_Photo_aHouse", "aDog", "IGUI_Photo_adog", "", "Dog T-shirt"}) do
    check(not EwingsClothesRecipeChecks.dogPhoto(item("Base.Photo", key), nil), "unrelated key accepted")
    check(not EwingsClothesRecipeChecks.catPhoto(item("Base.Photo", key), nil), "unrelated key accepted")
end
check(not EwingsClothesRecipeChecks.dogPhoto(item("Base.Photo", nil), nil), "unlabelled photo accepted")
check(not EwingsClothesRecipeChecks.catPhoto(nil, nil), "nil photo accepted")
for _, fullType in ipairs({"Base.PaintBlack", "Base.PaintWhite", "Base.PaintTurquoise", "Base.PaintBrown", "Base.PaintBlue", "Base.PaintOrange", "Base.Paintbrush", "Base.PaintbrushCrafted", "Base.Tshirt_WhiteTINT", "Base.Tshirt_DefaultTEXTURE"}) do
    check(EwingsClothesRecipeChecks.dogPhoto(item(fullType, nil), nil), "nonphoto input rejected by dog predicate")
    check(EwingsClothesRecipeChecks.catPhoto(item(fullType, nil), nil), "nonphoto input rejected by cat predicate")
end
-- Candidate-order assertion: only the qualifying Base.Photo passes the gate.
for _, reversed in ipairs({false, true}) do
    local good = item("Base.Photo", "IGUI_Photo_aDog")
    local bad = item("Base.Photo", "IGUI_Photo_aCat")
    local candidates = reversed and {good, bad} or {bad, good}
    local found = nil
    for _, candidate in ipairs(candidates) do
        if EwingsClothesRecipeChecks.dogPhoto(candidate, nil) then found = candidate; break end
    end
    check(found == good, "candidate order changed photo qualification")
end
return "photo predicate assertions passed", checks
