# Suginami Suki artwork system

Design direction agreed 23 September 2026. This repository owns new artwork, source files,
generation prompts, composition metadata and published exports. The app repository owns rendering,
live information and collection rules. This brief defines the next asset format; the existing
clients and published `v0/art/` images still use the original flattened illustrations.

## Three layers

| Layer | Contents | Owner |
| --- | --- | --- |
| Neighborhood | Full-bleed background for morning, midday, evening or night; no Namisuke and no blank clock board | Artwork repository |
| Namisuke | Transparent character cutout, with awake and sleepy poses initially; separate soft contact shadow if needed | Artwork repository |
| Information | Live time, date, optional weather, neighborhood label and a contrast scrim | Phone/watch renderer |

Remove the oversized blank signboards by reconstructing the scene behind them. Ordinary shop
signage can remain where it belongs. Never bake clock digits, dates or weather into artwork.
Preserve the recognizable bookshop and river scenes, character anatomy and textured palette.

Separating the character means its placement can adapt without moving the architecture. Use
reviewed lighting variants where required: a sunny character must not look pasted onto a night
scene. Keep any contact shadow independent of the background and position it with the character.

## Composition presets

| Surface | First layout to explore |
| --- | --- |
| Round watch | Time in the upper-middle safe area; small date beneath; Namisuke lower-center; optional compact weather slot |
| Compact square widget | Time and date above a small character; weather omitted when space is tight |
| Wide widget | Time/date on the left, Namisuke on the right, optional weather beneath the date |
| Larger widget | More of the neighborhood visible; time/date and a short weather row kept together |
| Stamp-book image | Background plus character, without live information |

These are composition targets, not fixed launcher grid-cell dimensions. Fit the actual available
size. Supply reviewed square and wide backgrounds, or crop windows that genuinely work; do not
stretch the square watch art to fill a wide widget. Keep faces, landmarks and text clear of round
and rounded-corner clipping. Recompose the artwork when a crop cannot preserve its identity.

Time has the strongest typographic emphasis, date is secondary, weather tertiary. Begin with
warm cream text over a localized dark-teal scrim, or dark teal over a light scrim. Choose contrast
per scene and verify it at rendered size, including long Japanese dates, 12/24-hour clocks and
font scaling. The scrim is a renderer layer, not a new painted signboard.

Layout metadata should describe normalized crop rectangles, landmark/focal points, character
anchor and scale, text-safe rectangles, contrast treatment and supported aspect ratios. Each
asset needs an immutable version, dimensions, hash and provenance. Lock background geometry
across all four phases. Layer separation is an authoring contract: a platform may cache a static
background/character composite while keeping time and other information live.

## Live information

Use the device's time, timezone, locale and clock preference for the displayed clock. A collected
scene still represents the period it was earned in; a night stamp can show the current daytime
clock. Automatic scene cycling is a separate product choice, not part of this asset migration.

Weather is optional. Reserve its space, but do not assume access to another phone app's weather.
A phone implementation needs a chosen data source and freshness/offline behavior; a watch can
use an appropriate complication source. Collapse the slot when unavailable. Ambient watch mode
remains a separate mostly-black, minimal-clock composition, not the illustrated night variant.

Android references: [responsive widget layouts](https://developer.android.com/develop/ui/compose/glance/build-ui),
[RemoteViews and supported views, including TextClock](https://developer.android.com/reference/android/widget/RemoteViews),
and [watch-face complications](https://developer.android.com/training/wearables/wff/complications).
Widget rendering must use the platform's supported clock/update mechanism, not a timer that
rebuilds the illustrated bitmap every minute.

## Ownership and migration

Source locations (the collection backgrounds, characters, prompts and layout values populate these):

```text
artwork/sources/backgrounds/<area>/<phase>/
artwork/sources/characters/namisuke/
artwork/prompts/
artwork/records/                 # per-asset provenance and visual review
artwork/layouts/
artwork/exports/                 # versioned runtime assets and scene descriptors
```

Keep authored files outside `v0/`: the existing app-side publisher deletes and rebuilds that
directory. It currently resolves source art inside the app checkout and renders flattened JPEGs;
the phone's loader also only accepts those JPEG paths. Neither supports the new layers yet.

1. The approved Kugayama and Nishi-Ogikubo evening study establishes the round watch, square
   widget and wide widget presets, using separate backgrounds and transparent Namisuke.
2. The collection extends those presets to all 23 neighborhoods and four phases. Its manifest
   records asset availability; its browser preview is a design study, not a client renderer.
3. Migrate the original masters and provenance here without losing their history/reference links;
   update both build pipelines to read the new source of truth. Existing app-side masters remain
   legacy references until that migration is complete.
4. Add scene descriptors and transparent-layer loading to the clients. Keep existing `art` fields
   and their published URLs working for older clients; publish the layered format additively.
5. Update the publisher before deploying the new sources. Preserve immutable historical exports,
   including artwork for stamps already collected, and publish data/assets as a consistent set.
6. Build widgets and updated watch layouts, then check crops, readability, offline behavior and
   device resource use before shipping the collection to clients.

The initial implementation should deliver time and date; weather is an optional extension.
[The collection review](COLLECTION.md) provides separate artwork and an interactive browser study.
[The first evening pass](FIRST-PASS.md) preserves the original design baseline. Native widget code
and runtime migration remain future work.
