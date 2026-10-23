# Offline development — 1.1.0

Runtime players need only the install ZIP. Existing Python/Pillow/NumPy and the installed game's existing JRE are development tools; no dependencies were downloaded for this update.

```text
python tools/build_animal_art.py
python tools/pixel_preview.py --game "<ProjectZomboid directory>" --font "<local bold font>"
python tools/native_checks.py --game "<ProjectZomboid directory>"
python tools/run_behavior_checks.py --game "<ProjectZomboid directory>"
python tools/validate_and_package.py --game "<ProjectZomboid directory>"
```

The art builder only generates new Dog/Cat assets. It uses the alpha silhouette of the original mod-owned One Job texture, not extracted game pixels. Do not regenerate or overwrite the protected originals. Historical tools in `tools/legacy/` describe the earlier project layout and are not the current build entry points.

Native checks generate tiny original JVM runners and invoke the installed crafting parser/Kahlua VM, never the game entry point. Temporary classes, a private copy of the installed VM standard library, isolated user.home, and test logs stay under `.validation/` and are excluded from every package. No native source/binary or compiled harness is distributed. `run_behavior_checks.py` reads installed vanilla Lua locally to test additive pools and the actual clothing-copy routine with isolated tables.

CPU previews read native mesh coordinates/UVs in memory and write PNGs only. No GUI, screen/mouse/keyboard, game/server or external service is used. Tests do not install/enable the mod or inspect saves. Actual game/MP behavior remains untested.
