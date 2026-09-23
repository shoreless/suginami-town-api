# First pass · Evening layers

Kugayama and Nishi-Ogikubo, each composed for a round watch, square phone widget and wide phone
widget. This is a visual prototype; it does not update the installed phone/watch apps or the
published `v0` content.

## Review

From the repository root:

```sh
python3 -m http.server 8000
```

Open http://localhost:8000/artwork/review/. The page uses local artwork and browser-rendered time
and date. Switch to the device clock, try Japanese, toggle the character and information, show
layout guides, or change the display scale. Weather is explicitly sample data, not a live feed.

The five image assets are independent: two square backgrounds, two wide backgrounds, and one
transparent awake Namisuke. The wide backgrounds are separately composed views of the same
places, not stretched squares. Each composition places the character independently. A soft
contact shadow and the readability shading are CSS layers, not pixels in the artwork.

[Six-composition preview](review/compositions.png) · [Full review-page capture](review/first-pass.png)

Browser review confirmed all five source assets load, all six compositions render, the layer
toggles work, and the page fits a 390px viewport. English/Japanese dates and sample weather were
reviewed. The character PNG has a genuine alpha channel; source pixels are preserved unchanged.
These checks do not establish native widget/watch performance.

## Asset and prompt map

| Asset | Source | Exact generation prompt |
| --- | --- | --- |
| Kugayama square | [PNG](sources/backgrounds/kugayama/evening/square-v01.png) | [Prompt](prompts/kugayama-evening-square-v01.txt) |
| Kugayama wide | [PNG](sources/backgrounds/kugayama/evening/wide-v01.png) | [Prompt](prompts/kugayama-evening-wide-v01.txt) |
| Nishi-Ogikubo square | [PNG](sources/backgrounds/nishi-ogikubo/evening/square-v01.png) | [Prompt](prompts/nishi-ogikubo-evening-square-v01.txt) |
| Nishi-Ogikubo wide | [PNG](sources/backgrounds/nishi-ogikubo/evening/wide-v01.png) | [Prompt](prompts/nishi-ogikubo-evening-wide-v01.txt) |
| Namisuke, awake/evening | [Transparent PNG](sources/characters/namisuke/awake-evening-v01.png) | [Prompt](prompts/namisuke-awake-evening-v01.txt) |

Generated with the built-in `image_gen` tool. Delivered images are copied unchanged; their original
output names, hashes, dimensions and transparency inspection are recorded in `manifest.json`.
No painted time, date, weather or blank clock boards are part of the new layers.

[Composition values](layouts/first-pass.json) are normalized fractions of the display rectangle.
The `focal_point` field controls background positioning under a cover crop. Character `x` means
horizontal center, `bottom` is inset from the bottom, and `width` is a fraction of display width.
Information `x` and `y` identify its upper-left corner. Typography tokens specify a regular serif, 95% text opacity (a five-percentage-point reduction), and Japanese-first neighborhood labels with smaller English below. The CSS applies those tokens and controls the scrims. The language selector changes dates/weather; neighborhood names retain Japanese-first order.
This descriptor is a design prototype, not a format accepted by the current native clients.

## Provenance

The two evening edit targets are copied unchanged into `references/` from the app repository's
approved original masters. Their original prompts remain in `namisuke-no-toki/prompts/evening/`.
The identity reference is Suginami City's Namisuke image, copied from the existing app reference:
https://www.city.suginami.tokyo.jp/images/10619/nmsk01_logo01.jpg

Namisuke is a third-party character; storing the reference here does not assert a license grant.
The neighborhood paintings are imagined composites. River fireflies represent the early-summer
art direction rather than year-round weather or wildlife information.

## Before native integration

Review the character scale, clock placement, square/wide scene consistency, and contrast at the
smallest intended size. Then derive the other phases from the selected backgrounds, add the
sleepy character, and translate the chosen layouts to native widgets and Watch Face Format.
Phone weather needs a provider; the preview only reserves an optional slot. Watch ambient mode
will use its own minimal mostly-black composition.

The app's existing source masters and the API's current `v0/art/` exports stay intact. This pass
establishes new source artwork in this repository; it does not migrate every legacy asset or
change the current publisher, which still rebuilds `v0/` from the app repository.
