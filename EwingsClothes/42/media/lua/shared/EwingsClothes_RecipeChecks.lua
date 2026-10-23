-- Fixed illustrations use a reusable native photo as a reference, never its pixels.
EwingsClothesRecipeChecks = EwingsClothesRecipeChecks or {}

local dogKeys = {
    IGUI_Photo_aDog = true,
    IGUI_Photo_aSleepingDog = true,
    IGUI_Photo_DogsPlaying = true,
    IGUI_Photo_aChildPlayingWithaDog = true,
    IGUI_Photo_aDogandaCat = true,
}
local catKeys = {
    IGUI_Photo_aCat = true,
    IGUI_Photo_aSleepingCat = true,
    IGUI_Photo_aChildPlayingWithaCat = true,
    IGUI_Photo_aDogandaCat = true,
}

local function matchingPhoto(item, keys)
    if not item then return false end
    -- Native OnTest is called for every input candidate, including paint/tools.
    if item:getFullType() ~= "Base.Photo" then return true end
    local data = item:getModData()
    return data ~= nil and keys[data.collectibleKey] == true
end

function EwingsClothesRecipeChecks.dogPhoto(item, character)
    return matchingPhoto(item, dogKeys)
end

function EwingsClothesRecipeChecks.catPhoto(item, character)
    return matchingPhoto(item, catKeys)
end
