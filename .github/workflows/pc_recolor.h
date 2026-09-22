// pc_recolor.h -- Recolour mod (Onions, Pellets, Piki, lights, container UI)
//
// Everything the game colours by PikiColor slot (0 Blue, 1 Red, 2 Yellow) goes
// through this one file. Two things are chosen from the F1 / Mods menu:
// whether the mod is on at all ("Recolour Mod"), and which palette to use
// ("Recolour Palette", cycled with Left/Right). Nothing here touches a
// texture or particle asset on disc:
//
//   1) Onions & Pellets: no colour of their own in the code -- both drive a
//      colour animation whose result we hue-shift after
//      `mAnimatedMaterials.animate()` runs.
//   2) Onion beacon/halo lights and the idle Piki/sprout glow: pre-baked
//      particle effects picked by colour index. Recoloured with the port's
//      own `particleGenerator::setTint()`.
//   3) Piki bodies, seeds/sprouts and cutscene Piki: flat single-colour
//      models, so these get a full colour swap rather than a hue-shift.
//   4) The container transfer screen ("Take N Pikmin out?"): uses real
//      per-colour textures, so instead of touching those files we
//      multiply-tint the panes that display them (P2DPicture::setWhite,
//      P2DWindow::setFlatColour).
//
// EDIT kPalettes BELOW to add/change palettes. R, G, B from 0 to 255.
// IMPORTANT: pc_settings.cpp keeps its own copy of the palette NAMES
// (kRecolorPaletteNames), for display, decoupled from this header. If you
// add or remove a palette here, update that list too, in the same order.
#pragma once

#include "Colour.h"
#include "GlobalGameOptions.h"
#include "Material.h"
#include "P2D/Picture.h"
#include "P2D/Window.h"
#include "Shape.h"
#include "zen/particle.h"

#include <math.h>

// Wired to the F1 / Mods menu; see pc_settings.h / pc_settings.cpp.
extern "C" int pc_settings_get_recolor_mod(void);
extern "C" int pc_settings_get_recolor_palette(void);

namespace pc_recolor {

static const int kPaletteCount = 4;

// Target tint for each slot, per palette. Keep names in pc_settings.cpp in
// the same order as this array.
static const float kPalettes[kPaletteCount][3][3] = {
	// 0: Roxo / Rosa / Branco
	{
	    { 255.0f, 255.0f, 255.0f }, // Blue slot   -> White
	    { 150.0f, 40.0f, 220.0f },  // Red slot    -> Purple
	    { 255.0f, 100.0f, 180.0f }, // Yellow slot -> Pink
	},
	// 1: Verde / Ciano / Laranja
	{
	    { 0.0f, 220.0f, 255.0f }, // Blue slot   -> Cyan
	    { 255.0f, 140.0f, 0.0f }, // Red slot    -> Orange
	    { 40.0f, 220.0f, 80.0f }, // Yellow slot -> Green
	},
	// 2: Preto e Branco
	{
	    { 235.0f, 235.0f, 235.0f }, // Blue slot   -> Light grey
	    { 20.0f, 20.0f, 20.0f },    // Red slot    -> Near black
	    { 140.0f, 140.0f, 140.0f }, // Yellow slot -> Mid grey
	},
	// 3: Pastel
	{
	    { 190.0f, 230.0f, 255.0f }, // Blue slot   -> Pastel blue
	    { 255.0f, 190.0f, 205.0f }, // Red slot    -> Pastel pink
	    { 255.0f, 245.0f, 180.0f }, // Yellow slot -> Pastel yellow
	},
};

// Hue (degrees, 0-360) of the ORIGINAL colour of each slot, and how far from
// it a colour may be and still get recoloured. Used only by the hue-shift
// path (Onions, Pellets), not by the flat-swap path (Piki, UI panes).
static const float kSrcHue[3]    = { 220.0f, 0.0f, 55.0f };
static const float kHueTolerance = 60.0f;

inline bool enabled()
{
	return pc_settings_get_recolor_mod() != 0;
}

inline int paletteIndex()
{
	int idx = pc_settings_get_recolor_palette();
	if (idx < 0 || idx >= kPaletteCount) {
		return 0;
	}
	return idx;
}

inline u8 toU8(float v)
{
	return (u8)(v < 0.0f ? 0.0f : (v > 255.0f ? 255.0f : v + 0.5f));
}

inline s16 toS16(float v)
{
	return (s16)(v < 0.0f ? 0.0f : (v > 255.0f ? 255.0f : v + 0.5f));
}

inline Colour tintColour(int slot, u8 alpha = 255)
{
	const float(*p)[3] = kPalettes[paletteIndex()];
	return Colour(toU8(p[slot][0]), toU8(p[slot][1]), toU8(p[slot][2]), alpha);
}

// r, g, b in 0..255 (in/out). Returns without touching them if the colour is
// grey or its hue is not the one expected for this slot.
static inline void recolour(int slot, float& r, float& g, float& b)
{
	float mx = r > g ? (r > b ? r : b) : (g > b ? g : b);
	float mn = r < g ? (r < b ? r : b) : (g < b ? g : b);
	float d  = mx - mn;
	if (mx <= 0.0f || d < 0.001f) {
		return;
	}

	float s = d / mx;
	float h;
	if (mx == r) {
		h = 60.0f * fmodf((g - b) / d, 6.0f);
	} else if (mx == g) {
		h = 60.0f * ((b - r) / d + 2.0f);
	} else {
		h = 60.0f * ((r - g) / d + 4.0f);
	}
	if (h < 0.0f) {
		h += 360.0f;
	}

	float diff = fabsf(h - kSrcHue[slot]);
	if (diff > 180.0f) {
		diff = 360.0f - diff;
	}
	if (diff > kHueTolerance) {
		return;
	}

	const float(*p)[3] = kPalettes[paletteIndex()];
	r = mx * (1.0f - s * (1.0f - p[slot][0] / 255.0f));
	g = mx * (1.0f - s * (1.0f - p[slot][1] / 255.0f));
	b = mx * (1.0f - s * (1.0f - p[slot][2] / 255.0f));
}

// --- 1) Onions & Pellets: colour-animation materials -----------------------
// Call right after `mAnimatedMaterials.animate(&rate)`, before drawing.
static inline void applyMaterial(ShapeDynMaterials& dyn, int slot)
{
	if (!enabled() || slot < 0 || slot > 2) {
		return;
	}

	for (int i = 0; i < dyn.mMatCount; i++) {
		Material& mat = dyn.mMaterials[i];
		if (!(mat.mFlags & MATFLAG_PVW)) {
			continue;
		}

		if (mat.mColourInfo.mTotalFrameCount != 0) {
			Colour& c = mat.colour();
			float r = c.r, g = c.g, b = c.b;
			recolour(slot, r, g, b);
			c.r = toU8(r);
			c.g = toU8(g);
			c.b = toU8(b);
		}

		for (int t = 0; t < 3; t++) {
			PVWTevColReg& reg = mat.mTevInfo->mTevColRegs[t];
			if (reg.mAnimFrameCount) {
				ShortColour& c = reg.mAnimatedColor;
				float r = c.r, g = c.g, b = c.b;
				recolour(slot, r, g, b);
				c.r = toS16(r);
				c.g = toS16(g);
				c.b = toS16(b);
			}
		}
	}
}

// --- 2) Onion beacon/halo + idle Piki/sprout glow: particle tint -----------
// Call right after `effectMgr->create(...)` returns the generator.
static inline void tintEffect(zen::particleGenerator* efx, int slot)
{
	if (!efx) {
		return;
	}
	if (!enabled() || slot < 0 || slot > 2) {
		efx->clearTint();
		return;
	}
	efx->setTint(tintColour(slot));
}

// --- 3) Piki bodies / seeds / cutscene Piki: flat colour swap ---------------
static inline Colour pikiColour(int slot, const Colour& original)
{
	if (!enabled() || slot < 0 || slot > 2) {
		return original;
	}
	return tintColour(slot, original.a);
}

template <typename ColourTableT>
static inline void refreshTable(ColourTableT& table, const Colour original[3])
{
	for (int slot = 0; slot < 3; slot++) {
		table[slot] = pikiColour(slot, original[slot]);
	}
}

// --- 4) Container transfer screen: tint the panes, not the textures --------
static inline void tintPane(P2DPicture* pic, int slot)
{
	if (!pic) {
		return;
	}
	if (!enabled() || slot < 0 || slot > 2) {
		pic->setWhite(Colour(255, 255, 255, 255));
		return;
	}
	pic->setWhite(tintColour(slot));
}

static inline void tintWindow(P2DWindow* win, int slot)
{
	if (!win) {
		return;
	}
	if (!enabled() || slot < 0 || slot > 2) {
		win->setFlatColour(Colour(255, 255, 255, 255));
		return;
	}
	win->setFlatColour(tintColour(slot));
}

} // namespace pc_recolor
