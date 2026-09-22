def edit(path, pairs):
    s = open(path, encoding="utf-8", newline="").read()
    nl = "\r\n" if "\r\n" in s else "\n"
    for old, new in pairs:
        old = old.replace("\n", nl)
        new = new.replace("\n", nl)
        assert s.count(old) == 1, (path, old)
        s = s.replace(old, new)
    open(path, "w", encoding="utf-8", newline="").write(s)

# P2D/Window.h
edit("include/P2D/Window.h", [
    ("\tvoid setTexture(Texture* tex)\n"
     "\t{\n"
     "\t\tmTLCornerTexture->setTexture(tex);\n"
     "\t\tmTRCornerTexture->setTexture(tex);\n"
     "\t\tmBLCornerTexture->setTexture(tex);\n"
     "\t\tmBRCornerTexture->setTexture(tex);\n"
     "\t}\n"
     "\n"
     "\tP2DWindow(P2DPane*, RandomAccessStream*, u16);\n",

     "\tvoid setTexture(Texture* tex)\n"
     "\t{\n"
     "\t\tmTLCornerTexture->setTexture(tex);\n"
     "\t\tmTRCornerTexture->setTexture(tex);\n"
     "\t\tmBLCornerTexture->setTexture(tex);\n"
     "\t\tmBRCornerTexture->setTexture(tex);\n"
     "\t}\n"
     "\n"
     "\t// PC/Android: flat multiply-tint for all four corners (recolour mod).\n"
     "\tvoid setFlatColour(Colour c)\n"
     "\t{\n"
     "\t\tmTLCornerColour = mTRCornerColour = mBLCornerColour = mBRCornerColour = c;\n"
     "\t}\n"
     "\n"
     "\tP2DWindow(P2DPane*, RandomAccessStream*, u16);\n"),
])

# goalItem.cpp
edit("src/plugPikiKando/goalItem.cpp", [
    ('#include "Piki.h"\n',
     '#include "Piki.h"\n#if defined(PIKI_PC_PORT)\n#include "mods/pc_recolor.h"\n#endif\n'),

    ("\t\tif (!mSpotEfx) {\n"
     "\t\t\tmSpotEfx = effectMgr->create(efxIDs[mOnionColour], mSRT.t, nullptr, nullptr);\n"
     "\t\t\tif (mSpotEfx) {\n"
     "\t\t\t\tmSpotEfx->setEmitPosPtr(&mSRT.t);\n"
     "\t\t\t}\n"
     "\t\t\tSeSystem::playSysSe(SYSSE_CONTAINER_OK);\n"
     "\t\t}\n",

     "\t\tif (!mSpotEfx) {\n"
     "\t\t\tmSpotEfx = effectMgr->create(efxIDs[mOnionColour], mSRT.t, nullptr, nullptr);\n"
     "\t\t\tif (mSpotEfx) {\n"
     "\t\t\t\tmSpotEfx->setEmitPosPtr(&mSRT.t);\n"
     "#if defined(PIKI_PC_PORT)\n"
     "\t\t\t\tpc_recolor::tintEffect(mSpotEfx, mOnionColour);\n"
     "#endif\n"
     "\t\t\t}\n"
     "\t\t\tSeSystem::playSysSe(SYSSE_CONTAINER_OK);\n"
     "\t\t}\n"),

    ("\t\tif (!mHaloEfx) {\n"
     "\t\t\tmHaloEfx = effectMgr->create(efxIDs[mOnionColour], mSRT.t, nullptr, nullptr);\n"
     "\t\t\tif (mHaloEfx) {\n"
     "\t\t\t\tmHaloEfx->setEmitPosPtr(&mSRT.t);\n"
     "\t\t\t}\n"
     "\t\t}\n",

     "\t\tif (!mHaloEfx) {\n"
     "\t\t\tmHaloEfx = effectMgr->create(efxIDs[mOnionColour], mSRT.t, nullptr, nullptr);\n"
     "\t\t\tif (mHaloEfx) {\n"
     "\t\t\t\tmHaloEfx->setEmitPosPtr(&mSRT.t);\n"
     "#if defined(PIKI_PC_PORT)\n"
     "\t\t\t\tpc_recolor::tintEffect(mHaloEfx, mOnionColour);\n"
     "#endif\n"
     "\t\t\t}\n"
     "\t\t}\n"),
])

# uteffect.cpp
edit("src/plugPikiKando/uteffect.cpp", [
    ('#include "Matrix3f.h"\n#include "zen/Math.h"\n',
     '#include "Matrix3f.h"\n#include "zen/Math.h"\n#if defined(PIKI_PC_PORT)\n#include "mods/pc_recolor.h"\n#endif\n'),

    ("void FreeLightEffect::emit(immut EffectParm& parm)\n"
     "{\n"
     "\tif (!mEfx) {\n"
     "\t\tmEfx = effectMgr->create((EffectMgr::effTypeTable)(EffectMgr::EFF_Piki_IdleBlue - mColor), *parm.mPositionRef, nullptr, nullptr);\n"
     "\t\tif (mEfx) {\n"
     "\t\t\tmScale = mEfx->getScaleSize();\n"
     "\t\t\tmEfx->setEmitPosPtr(parm.mPositionRef);\n"
     "\t\t}\n"
     "\t}\n",

     "void FreeLightEffect::emit(immut EffectParm& parm)\n"
     "{\n"
     "\tif (!mEfx) {\n"
     "\t\tmEfx = effectMgr->create((EffectMgr::effTypeTable)(EffectMgr::EFF_Piki_IdleBlue - mColor), *parm.mPositionRef, nullptr, nullptr);\n"
     "\t\tif (mEfx) {\n"
     "\t\t\tmScale = mEfx->getScaleSize();\n"
     "\t\t\tmEfx->setEmitPosPtr(parm.mPositionRef);\n"
     "#if defined(PIKI_PC_PORT)\n"
     "\t\t\tpc_recolor::tintEffect(mEfx, mColor);\n"
     "#endif\n"
     "\t\t}\n"
     "\t}\n"),
])

# pelletMgr.cpp
edit("src/plugPikiKando/pelletMgr.cpp", [
    ('#include "MapMgr.h"\n#include "Pellet.h"\n',
     '#include "MapMgr.h"\n#include "Pellet.h"\n#if defined(PIKI_PC_PORT)\n#include "mods/pc_recolor.h"\n#endif\n'),

    ("\tif (mConfig->mPelletColor() != PELCOLOR_NULL) {\n"
     "\t\tf32 val = mConfig->mPelletColor();\n"
     "\t\tmAnimatedMaterials.animate(&val);\n"
     "\t} else if (isUfoParts()) {\n"
     "\t\tmAnimatedMaterials.animate(nullptr);\n"
     "\t}\n",

     "\tif (mConfig->mPelletColor() != PELCOLOR_NULL) {\n"
     "\t\tf32 val = mConfig->mPelletColor();\n"
     "\t\tmAnimatedMaterials.animate(&val);\n"
     "#if defined(PIKI_PC_PORT)\n"
     "\t\tpc_recolor::applyMaterial(mAnimatedMaterials, mConfig->mPelletColor());\n"
     "#endif\n"
     "\t} else if (isUfoParts()) {\n"
     "\t\tmAnimatedMaterials.animate(nullptr);\n"
     "\t}\n"),
])

# piki.cpp
edit("src/plugPikiKando/piki.cpp", [
    ('#include "Piki.h"\n',
     '#include "Piki.h"\n#if defined(PIKI_PC_PORT)\n#include "mods/pc_recolor.h"\n#endif\n'),

    ("void Piki::initColor(int color)\n"
     "{\n"
     "\tmColor = color;\n",

     "void Piki::initColor(int color)\n"
     "{\n"
     "\tmColor = color;\n"
     "#if defined(PIKI_PC_PORT)\n"
     "\t{\n"
     "\t\tstatic const Colour kOriginalPikiColours[3] = {\n"
     "\t\t\tColour(0, 50, 255, 255),\n"
     "\t\t\tColour(255, 30, 0, 255),\n"
     "\t\t\tColour(255, 210, 0, 255),\n"
     "\t\t};\n"
     "\t\tpc_recolor::refreshTable(pikiColors, kOriginalPikiColours);\n"
     "\t}\n"
     "#endif\n"),
])

# pikiheadItem.cpp
edit("src/plugPikiKando/pikiheadItem.cpp", [
    ('#include "MapMgr.h"\n#include "NaviMgr.h"\n',
     '#include "MapMgr.h"\n#include "NaviMgr.h"\n#if defined(PIKI_PC_PORT)\n#include "mods/pc_recolor.h"\n#endif\n'),

    ("void PikiHeadItem::startAI(int)\n"
     "{\n"
     "\tstartFix();\n",

     "void PikiHeadItem::startAI(int)\n"
     "{\n"
     "\tstartFix();\n"
     "#if defined(PIKI_PC_PORT)\n"
     "\t{\n"
     "\t\tstatic const Colour kOriginalPikiColours[3] = {\n"
     "\t\t\tColour(0, 50, 255, 255),\n"
     "\t\t\tColour(255, 30, 0, 255),\n"
     "\t\t\tColour(255, 210, 0, 255),\n"
     "\t\t};\n"
     "\t\tpc_recolor::refreshTable(Piki::pikiColors, kOriginalPikiColours);\n"
     "\t}\n"
     "#endif\n"),
])

# cinePlayer.cpp
edit("src/plugPikiColin/cinePlayer.cpp", [
    ('#include "Creature.h"\n#include "DebugLog.h"\n',
     '#include "Creature.h"\n#include "DebugLog.h"\n#if defined(PIKI_PC_PORT)\n#include "mods/pc_recolor.h"\n#endif\n'),

    ('mActiveActor->mModel->mMaterialList[0].setColour(Colour(0, 50, 255, 255));',
     '#if defined(PIKI_PC_PORT)\n\t\tmActiveActor->mModel->mMaterialList[0].setColour(pc_recolor::pikiColour(0, Colour(0, 50, 255, 255)));\n#else\n\t\tmActiveActor->mModel->mMaterialList[0].setColour(Colour(0, 50, 255, 255));\n#endif'),

    ('mActiveActor->mModel->mMaterialList[0].setColour(Colour(255, 30, 0, 255));',
     '#if defined(PIKI_PC_PORT)\n\t\tmActiveActor->mModel->mMaterialList[0].setColour(pc_recolor::pikiColour(1, Colour(255, 30, 0, 255)));\n#else\n\t\tmActiveActor->mModel->mMaterialList[0].setColour(Colour(255, 30, 0, 255));\n#endif'),

    ('mActiveActor->mModel->mMaterialList[0].setColour(Colour(255, 210, 0, 255));',
     '#if defined(PIKI_PC_PORT)\n\t\tmActiveActor->mModel->mMaterialList[0].setColour(pc_recolor::pikiColour(2, Colour(255, 210, 0, 255)));\n#else\n\t\tmActiveActor->mModel->mMaterialList[0].setColour(Colour(255, 210, 0, 255));\n#endif'),
])

# drawContainer.cpp
edit("src/plugPikiYamashita/drawContainer.cpp", [
    ('#if defined(PIKI_PC_PORT)\n#include "pc_gfx.h"\n#endif\n',
     '#if defined(PIKI_PC_PORT)\n#include "pc_gfx.h"\n#include "mods/pc_recolor.h"\n#endif\n'),

    ("\t\tP2DWindow* pane = static_cast<P2DWindow*>(mScreen.search('p264', true));\n"
     "\t\tpane->setTexture(mPikminTextures[mColor]);\n"
     "\t\tP2DPicture* pic = static_cast<P2DPicture*>(mScreen.search('ws8c', true));\n"
     "\t\tpic->setTexture(mWindowTextures[mColor], 0);\n"
     "\t\tpic = static_cast<P2DPicture*>(mScreen.search('p2c4', true));\n"
     "\t\tpic->setTexture(mContainerTextures[mColor], 0);\n"
     "\t\tpic = static_cast<P2DPicture*>(mScreen.search('ws8u', true));\n"
     "\t\tpic->setTexture(mWindowTextures[mColor], 0);\n"
     "\t\tpic = static_cast<P2DPicture*>(mScreen.search('ws8l', true));\n"
     "\t\tpic->setTexture(mWindowTextures[mColor], 0);\n"
     "\t\tSeSystem::playSysSe(SYSSE_CMENU_ON);\n",

     "\t\tP2DWindow* pane = static_cast<P2DWindow*>(mScreen.search('p264', true));\n"
     "\t\tpane->setTexture(mPikminTextures[mColor]);\n"
     "\t\tP2DPicture* pic = static_cast<P2DPicture*>(mScreen.search('ws8c', true));\n"
     "\t\tpic->setTexture(mWindowTextures[mColor], 0);\n"
     "\t\tpic = static_cast<P2DPicture*>(mScreen.search('p2c4', true));\n"
     "\t\tpic->setTexture(mContainerTextures[mColor], 0);\n"
     "\t\tpic = static_cast<P2DPicture*>(mScreen.search('ws8u', true));\n"
     "\t\tpic->setTexture(mWindowTextures[mColor], 0);\n"
     "\t\tpic = static_cast<P2DPicture*>(mScreen.search('ws8l', true));\n"
     "\t\tpic->setTexture(mWindowTextures[mColor], 0);\n"
     "#if defined(PIKI_PC_PORT)\n"
     "\t\tpc_recolor::tintWindow(pane, mColor);\n"
     "\t\tpc_recolor::tintPane(static_cast<P2DPicture*>(mScreen.search('ws8c', true)), mColor);\n"
     "\t\tpc_recolor::tintPane(static_cast<P2DPicture*>(mScreen.search('p2c4', true)), mColor);\n"
     "\t\tpc_recolor::tintPane(static_cast<P2DPicture*>(mScreen.search('ws8u', true)), mColor);\n"
     "\t\tpc_recolor::tintPane(static_cast<P2DPicture*>(mScreen.search('ws8l', true)), mColor);\n"
     "#endif\n"
     "\t\tSeSystem::playSysSe(SYSSE_CMENU_ON);\n"),
])

# pc_settings.h
edit("pc_port/settings/pc_settings.h", [
    ("/// Minutes of play per in-game day. 10 is the original.\n"
     "int pc_settings_get_day_minutes(void);\n",

     "/// Minutes of play per in-game day. 10 is the original.\n"
     "int pc_settings_get_day_minutes(void);\n"
     "\n"
     "/// Recolour mod: Onions, Pellets, Piki, lights and the container UI\n"
     "/// retinted from mods/pc_recolor.h's palette. Off leaves everything\n"
     "/// exactly as the retail game looks.\n"
     "int pc_settings_get_recolor_mod(void);\n"
     "\n"
     "/// Which palette the recolour mod uses. Index into pc_recolor.h's\n"
     "/// kPalettes / pc_settings.cpp's kRecolorPaletteNames.\n"
     "int pc_settings_get_recolor_palette(void);\n"),
])

# pc_settings.cpp: palette-name table (kept local to this file, decoupled from pc_recolor.h)
edit("pc_port/settings/pc_settings.cpp", [
    ("// The debug row is the last one, so leaving it off simply shortens the list.\n"
     "constexpr int kModsRowCount = 6;\n"
     "#endif\n"
     "\n"
     "// Field-limit stops. 100 is what the original game uses.\n",

     "// The debug row is the last one, so leaving it off simply shortens the list.\n"
     "constexpr int kModsRowCount = 6;\n"
     "#endif\n"
     "\n"
     "// Recolour mod palette names. Keep this in sync with pc_recolor.h's\n"
     "// kPalettes array (same order, same count) -- this file does not include\n"
     "// pc_recolor.h, to keep the settings menu decoupled from game headers.\n"
     "constexpr const char* kRecolorPaletteNames[] = {\n"
     "    \"Roxo / Rosa / Branco\",\n"
     "    \"Verde / Ciano / Laranja\",\n"
     "    \"Preto e Branco\",\n"
     "    \"Pastel\",\n"
     "    \"Custom\",\n"
     "};\n"
     "constexpr int kRecolorPaletteCount = int(sizeof(kRecolorPaletteNames) / sizeof(kRecolorPaletteNames[0]));\n"
     "\n"
     "// Field-limit stops. 100 is what the original game uses.\n"),
])

# pc_settings.cpp: struct field, defaults, save, load
edit("pc_port/settings/pc_settings.cpp", [
    ("    // Debug shortcuts (F5/F6). A menu option rather than an environment\n"
     "    // variable: the launcher starts the game as a child process, so an\n"
     "    // exported variable does not reliably reach it.\n"
     "    int debugKeys = 0;\n",

     "    // Debug shortcuts (F5/F6). A menu option rather than an environment\n"
     "    // variable: the launcher starts the game as a child process, so an\n"
     "    // exported variable does not reliably reach it.\n"
     "    int debugKeys = 0;\n"
     "    // Recolour mod (Onions, Pellets, Piki, lights, container UI). On by\n"
     "    // default since it is the whole point of this fork.\n"
     "    int recolorMod = 1;\n"
     "    // Which palette the recolour mod uses. Index into kRecolorPaletteNames.\n"
     "    int recolorPalette = 0;\n"
     "    // \"Custom\" palette (last entry in kRecolorPaletteNames): R/G/B per slot,\n"
     "    // edited live in the F1 / Mods menu. Defaults match the game's original\n"
     "    // Piki colours, so Custom starts out identical to the unmodified game.\n"
     "    int recolorCustomBlueR = 0;\n"
     "    int recolorCustomBlueG = 50;\n"
     "    int recolorCustomBlueB = 255;\n"
     "    int recolorCustomRedR = 255;\n"
     "    int recolorCustomRedG = 30;\n"
     "    int recolorCustomRedB = 0;\n"
     "    int recolorCustomYellowR = 255;\n"
     "    int recolorCustomYellowG = 210;\n"
     "    int recolorCustomYellowB = 0;\n"),

    ("        saturation    = 1.0f;\n"
     "        debugKeys = 0;\n",

     "        saturation    = 1.0f;\n"
     "        debugKeys = 0;\n"
     "        recolorMod = 1;\n"
     "        recolorPalette = 0;\n"
     "        recolorCustomBlueR = 0;\n"
     "        recolorCustomBlueG = 50;\n"
     "        recolorCustomBlueB = 255;\n"
     "        recolorCustomRedR = 255;\n"
     "        recolorCustomRedG = 30;\n"
     "        recolorCustomRedB = 0;\n"
     "        recolorCustomYellowR = 255;\n"
     "        recolorCustomYellowG = 210;\n"
     "        recolorCustomYellowB = 0;\n"),

    ('    out << "brightness = " << sConfig.brightness << "\\n";\n'
     '    out << "saturation = " << sConfig.saturation << "\\n";\n'
     '    out << "debugKeys = " << sConfig.debugKeys << "\\n";\n',

     '    out << "brightness = " << sConfig.brightness << "\\n";\n'
     '    out << "saturation = " << sConfig.saturation << "\\n";\n'
     '    out << "debugKeys = " << sConfig.debugKeys << "\\n";\n'
     '    out << "recolorMod = " << sConfig.recolorMod << "\\n";\n'
     '    out << "recolorPalette = " << sConfig.recolorPalette << "\\n";\n'
     '    out << "recolorCustomBlueR = " << sConfig.recolorCustomBlueR << "\\n";\n'
     '    out << "recolorCustomBlueG = " << sConfig.recolorCustomBlueG << "\\n";\n'
     '    out << "recolorCustomBlueB = " << sConfig.recolorCustomBlueB << "\\n";\n'
     '    out << "recolorCustomRedR = " << sConfig.recolorCustomRedR << "\\n";\n'
     '    out << "recolorCustomRedG = " << sConfig.recolorCustomRedG << "\\n";\n'
     '    out << "recolorCustomRedB = " << sConfig.recolorCustomRedB << "\\n";\n'
     '    out << "recolorCustomYellowR = " << sConfig.recolorCustomYellowR << "\\n";\n'
     '    out << "recolorCustomYellowG = " << sConfig.recolorCustomYellowG << "\\n";\n'
     '    out << "recolorCustomYellowB = " << sConfig.recolorCustomYellowB << "\\n";\n'),

    ('        else if (key == "debugKeys") {\n'
     '            sConfig.debugKeys = atoi(val.c_str()) ? 1 : 0;\n'
     '        }\n',

     '        else if (key == "debugKeys") {\n'
     '            sConfig.debugKeys = atoi(val.c_str()) ? 1 : 0;\n'
     '        }\n'
     '        else if (key == "recolorMod") {\n'
     '            sConfig.recolorMod = atoi(val.c_str()) ? 1 : 0;\n'
     '        }\n'
     '        else if (key == "recolorPalette") {\n'
     '            sConfig.recolorPalette = atoi(val.c_str());\n'
     '            if (sConfig.recolorPalette < 0 || sConfig.recolorPalette >= kRecolorPaletteCount) sConfig.recolorPalette = 0;\n'
     '        }\n'
     '        else if (key == "recolorCustomBlueR") { sConfig.recolorCustomBlueR = atoi(val.c_str()); }\n'
     '        else if (key == "recolorCustomBlueG") { sConfig.recolorCustomBlueG = atoi(val.c_str()); }\n'
     '        else if (key == "recolorCustomBlueB") { sConfig.recolorCustomBlueB = atoi(val.c_str()); }\n'
     '        else if (key == "recolorCustomRedR") { sConfig.recolorCustomRedR = atoi(val.c_str()); }\n'
     '        else if (key == "recolorCustomRedG") { sConfig.recolorCustomRedG = atoi(val.c_str()); }\n'
     '        else if (key == "recolorCustomRedB") { sConfig.recolorCustomRedB = atoi(val.c_str()); }\n'
     '        else if (key == "recolorCustomYellowR") { sConfig.recolorCustomYellowR = atoi(val.c_str()); }\n'
     '        else if (key == "recolorCustomYellowG") { sConfig.recolorCustomYellowG = atoi(val.c_str()); }\n'
     '        else if (key == "recolorCustomYellowB") { sConfig.recolorCustomYellowB = atoi(val.c_str()); }\n'),
])

# pc_settings.cpp: row count (+2: Recolour Mod, Recolour Palette)
edit("pc_port/settings/pc_settings.cpp", [
    ("#if PIKI_DEBUG_KEYS\n"
     "constexpr int kModsRowCount = 7;\n"
     "#else\n"
     "// The debug row is the last one, so leaving it off simply shortens the list.\n"
     "constexpr int kModsRowCount = 6;\n"
     "#endif\n",

     "#if PIKI_DEBUG_KEYS\n"
     "constexpr int kModsRowCount = 18;\n"
     "#else\n"
     "// The debug row is the last one, so leaving it off simply shortens the list.\n"
     "constexpr int kModsRowCount = 17;\n"
     "#endif\n"),
])

# pc_settings.cpp: input handling (6 = mod toggle, 7 = palette cycle, 8 = debug)
edit("pc_port/settings/pc_settings.cpp", [
    ("        // Debug shortcuts.\n"
     "        else if (sModsSelection == 6) {\n"
     "            if (left || right) sPending.debugKeys = sPending.debugKeys ? 0 : 1;\n"
     "        }\n"
     "        return;\n",

     "        // Recolour mod (Onions, Pellets, Piki, lights, container UI).\n"
     "        else if (sModsSelection == 6) {\n"
     "            if (left || right) sPending.recolorMod = sPending.recolorMod ? 0 : 1;\n"
     "        }\n"
     "        // Recolour palette (which colours the mod swaps things to).\n"
     "        else if (sModsSelection == 7) {\n"
     "            if (left) sPending.recolorPalette = (sPending.recolorPalette + kRecolorPaletteCount - 1) % kRecolorPaletteCount;\n"
     "            else if (right) sPending.recolorPalette = (sPending.recolorPalette + 1) % kRecolorPaletteCount;\n"
     "        }\n"
     "        // Custom palette colours (pick \"Custom\" on Recolour Palette to see them).\n"
     "        else if (sModsSelection == 8) {\n"
     "            if (left) sPending.recolorCustomBlueR = (sPending.recolorCustomBlueR - 5 < 0) ? 0 : sPending.recolorCustomBlueR - 5;\n"
     "            else if (right) sPending.recolorCustomBlueR = (sPending.recolorCustomBlueR + 5 > 255) ? 255 : sPending.recolorCustomBlueR + 5;\n"
     "        }\n"
     "        else if (sModsSelection == 9) {\n"
     "            if (left) sPending.recolorCustomBlueG = (sPending.recolorCustomBlueG - 5 < 0) ? 0 : sPending.recolorCustomBlueG - 5;\n"
     "            else if (right) sPending.recolorCustomBlueG = (sPending.recolorCustomBlueG + 5 > 255) ? 255 : sPending.recolorCustomBlueG + 5;\n"
     "        }\n"
     "        else if (sModsSelection == 10) {\n"
     "            if (left) sPending.recolorCustomBlueB = (sPending.recolorCustomBlueB - 5 < 0) ? 0 : sPending.recolorCustomBlueB - 5;\n"
     "            else if (right) sPending.recolorCustomBlueB = (sPending.recolorCustomBlueB + 5 > 255) ? 255 : sPending.recolorCustomBlueB + 5;\n"
     "        }\n"
     "        else if (sModsSelection == 11) {\n"
     "            if (left) sPending.recolorCustomRedR = (sPending.recolorCustomRedR - 5 < 0) ? 0 : sPending.recolorCustomRedR - 5;\n"
     "            else if (right) sPending.recolorCustomRedR = (sPending.recolorCustomRedR + 5 > 255) ? 255 : sPending.recolorCustomRedR + 5;\n"
     "        }\n"
     "        else if (sModsSelection == 12) {\n"
     "            if (left) sPending.recolorCustomRedG = (sPending.recolorCustomRedG - 5 < 0) ? 0 : sPending.recolorCustomRedG - 5;\n"
     "            else if (right) sPending.recolorCustomRedG = (sPending.recolorCustomRedG + 5 > 255) ? 255 : sPending.recolorCustomRedG + 5;\n"
     "        }\n"
     "        else if (sModsSelection == 13) {\n"
     "            if (left) sPending.recolorCustomRedB = (sPending.recolorCustomRedB - 5 < 0) ? 0 : sPending.recolorCustomRedB - 5;\n"
     "            else if (right) sPending.recolorCustomRedB = (sPending.recolorCustomRedB + 5 > 255) ? 255 : sPending.recolorCustomRedB + 5;\n"
     "        }\n"
     "        else if (sModsSelection == 14) {\n"
     "            if (left) sPending.recolorCustomYellowR = (sPending.recolorCustomYellowR - 5 < 0) ? 0 : sPending.recolorCustomYellowR - 5;\n"
     "            else if (right) sPending.recolorCustomYellowR = (sPending.recolorCustomYellowR + 5 > 255) ? 255 : sPending.recolorCustomYellowR + 5;\n"
     "        }\n"
     "        else if (sModsSelection == 15) {\n"
     "            if (left) sPending.recolorCustomYellowG = (sPending.recolorCustomYellowG - 5 < 0) ? 0 : sPending.recolorCustomYellowG - 5;\n"
     "            else if (right) sPending.recolorCustomYellowG = (sPending.recolorCustomYellowG + 5 > 255) ? 255 : sPending.recolorCustomYellowG + 5;\n"
     "        }\n"
     "        else if (sModsSelection == 16) {\n"
     "            if (left) sPending.recolorCustomYellowB = (sPending.recolorCustomYellowB - 5 < 0) ? 0 : sPending.recolorCustomYellowB - 5;\n"
     "            else if (right) sPending.recolorCustomYellowB = (sPending.recolorCustomYellowB + 5 > 255) ? 255 : sPending.recolorCustomYellowB + 5;\n"
     "        }\n"
     "        // Debug shortcuts.\n"
     "        else if (sModsSelection == 17) {\n"
     "            if (left || right) sPending.debugKeys = sPending.debugKeys ? 0 : 1;\n"
     "        }\n"
     "        return;\n"),
])

# pc_settings.cpp: labels
edit("pc_port/settings/pc_settings.cpp", [
    ("        const char* modsLabels[kModsRowCount] = {\n"
     '            "Control Scheme",\n'
     '            "Chain Pikmin Actions",\n'
     '            "Hold to Pluck",\n'
     '            "Mouse Wheel",\n'
     '            "Pikmin Limit",\n'
     '            "Day Length",\n'
     "#if PIKI_DEBUG_KEYS\n"
     '            "Debug Keys (F5/F6)",\n'
     "#endif\n"
     "        };\n",

     "        const char* modsLabels[kModsRowCount] = {\n"
     '            "Control Scheme",\n'
     '            "Chain Pikmin Actions",\n'
     '            "Hold to Pluck",\n'
     '            "Mouse Wheel",\n'
     '            "Pikmin Limit",\n'
     '            "Day Length",\n'
     '            "Recolour Mod",\n'
     '            "Recolour Palette",\n'
     '            "Custom Blue R",\n'
     '            "Custom Blue G",\n'
     '            "Custom Blue B",\n'
     '            "Custom Red R",\n'
     '            "Custom Red G",\n'
     '            "Custom Red B",\n'
     '            "Custom Yellow R",\n'
     '            "Custom Yellow G",\n'
     '            "Custom Yellow B",\n'
     "#if PIKI_DEBUG_KEYS\n"
     '            "Debug Keys (F5/F6)",\n'
     "#endif\n"
     "        };\n"),
])

# pc_settings.cpp: drawn values (6 = mod, 7 = palette name, 8 = debug)
edit("pc_port/settings/pc_settings.cpp", [
    ("            } else if (i == 3) {\n"
     '                snprintf(value, sizeof(value), "%s",\n'
     '                         sPending.mouseWheelAction ? "Camera Zoom" : "Pikmin Colour");\n'
     "            } else if (i == 6) {\n"
     '                snprintf(value, sizeof(value), "%s",\n'
     '                         sPending.debugKeys ? "On" : "Off");\n'
     "            } else if (i == 5) {\n",

     "            } else if (i == 3) {\n"
     '                snprintf(value, sizeof(value), "%s",\n'
     '                         sPending.mouseWheelAction ? "Camera Zoom" : "Pikmin Colour");\n'
     "            } else if (i == 6) {\n"
     '                snprintf(value, sizeof(value), "%s",\n'
     '                         sPending.recolorMod ? "On" : "Off (original)");\n'
     "            } else if (i == 7) {\n"
     '                snprintf(value, sizeof(value), "%s", kRecolorPaletteNames[sPending.recolorPalette]);\n'
     "            } else if (i == 8) {\n"
     '                snprintf(value, sizeof(value), "%d", sPending.recolorCustomBlueR);\n'
     "            } else if (i == 9) {\n"
     '                snprintf(value, sizeof(value), "%d", sPending.recolorCustomBlueG);\n'
     "            } else if (i == 10) {\n"
     '                snprintf(value, sizeof(value), "%d", sPending.recolorCustomBlueB);\n'
     "            } else if (i == 11) {\n"
     '                snprintf(value, sizeof(value), "%d", sPending.recolorCustomRedR);\n'
     "            } else if (i == 12) {\n"
     '                snprintf(value, sizeof(value), "%d", sPending.recolorCustomRedG);\n'
     "            } else if (i == 13) {\n"
     '                snprintf(value, sizeof(value), "%d", sPending.recolorCustomRedB);\n'
     "            } else if (i == 14) {\n"
     '                snprintf(value, sizeof(value), "%d", sPending.recolorCustomYellowR);\n'
     "            } else if (i == 15) {\n"
     '                snprintf(value, sizeof(value), "%d", sPending.recolorCustomYellowG);\n'
     "            } else if (i == 16) {\n"
     '                snprintf(value, sizeof(value), "%d", sPending.recolorCustomYellowB);\n'
     "            } else if (i == 17) {\n"
     '                snprintf(value, sizeof(value), "%s",\n'
     '                         sPending.debugKeys ? "On" : "Off");\n'
     "            } else if (i == 5) {\n"),
])

# pc_settings.cpp: getters
edit("pc_port/settings/pc_settings.cpp", [
    ("int pc_settings_get_debug_keys(void) {\n"
     "    return sConfig.debugKeys;\n"
     "}\n",

     "int pc_settings_get_debug_keys(void) {\n"
     "    return sConfig.debugKeys;\n"
     "}\n"
     "\n"
     "int pc_settings_get_recolor_mod(void) {\n"
     "    return sConfig.recolorMod;\n"
     "}\n"
     "\n"
     "int pc_settings_get_recolor_palette(void) {\n"
     "    return sConfig.recolorPalette;\n"
     "}\n"
     "\n"
     "int pc_settings_get_recolor_custom_blue_r(void) { return sConfig.recolorCustomBlueR; }\n"
     "int pc_settings_get_recolor_custom_blue_g(void) { return sConfig.recolorCustomBlueG; }\n"
     "int pc_settings_get_recolor_custom_blue_b(void) { return sConfig.recolorCustomBlueB; }\n"
     "int pc_settings_get_recolor_custom_red_r(void) { return sConfig.recolorCustomRedR; }\n"
     "int pc_settings_get_recolor_custom_red_g(void) { return sConfig.recolorCustomRedG; }\n"
     "int pc_settings_get_recolor_custom_red_b(void) { return sConfig.recolorCustomRedB; }\n"
     "int pc_settings_get_recolor_custom_yellow_r(void) { return sConfig.recolorCustomYellowR; }\n"
     "int pc_settings_get_recolor_custom_yellow_g(void) { return sConfig.recolorCustomYellowG; }\n"
     "int pc_settings_get_recolor_custom_yellow_b(void) { return sConfig.recolorCustomYellowB; }\n"),
])

# app separado: outro nome de pacote, assim nao mexe no seu Open Nectar atual
edit("android/app/build.gradle", [
    ("applicationId 'org.opennectar'", "applicationId 'org.opennectar.recolor'"),
])
edit("android/app/src/main/res/values/strings.xml", [
    ('<string name="app_name">Open Nectar</string>', '<string name="app_name">Open Nectar Recolor</string>'),
])
print("patch aplicado")
