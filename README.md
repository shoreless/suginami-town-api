# suginami-town-api

Open data about the neighborhoods of Suginami, Tokyo, served as static JSON. It is maintained as a
volunteer project and is the data behind the すぎなみ好き (Suginami Suki) stamp-book app.

This repository is also the home for the new [layered artwork system](artwork/README.md):
neighborhood backgrounds and separate Namisuke artwork, composed by phone widgets and watch
faces beneath live time/date information. The source migration and new renderer are planned;
the current `v0/art/` files remain the compatible flattened images.

[Review the neighborhood collection](artwork/COLLECTION.md): 23 neighborhoods across four times
of day, with separate square/wide backgrounds and transparent Namisuke layers. The browser
study keeps Japanese names first and uses regular serif text at 95% opacity. The
[original two-neighborhood evening study](artwork/FIRST-PASS.md) is retained as the design baseline.

There is no server: every endpoint is a file, served by GitHub Pages, so it is free to use and has
no rate limits or keys.

## Endpoints

Base URL: `https://suginamisuki.com/` (formerly `https://shoreless.github.io/suginami-town-api/`, which redirects)

| Path | What it holds |
| --- | --- |
| `v0/index.json` | The 23 neighborhood areas: names in English and Japanese, how many towns, places and happenings each has, and the path to its own file |
| `v0/areas/{id}.json` | One area in full, e.g. `v0/areas/kugayama.json`: its towns, introduction, places and happenings |
| `v0/spots.json` | Every place worth visiting across Suginami, each tagged with its area |
| `v0/happenings.json` | Every dated happening across Suginami, earliest first, each tagged with its area. Ones that have ended are included; filter by `ends` |
| `v0/trash.json` | Trash and recycling collection days for every block (町丁目) in the ward, by census code, with the New Year break (`break`, month-day). `days` are weekdays; `weeks`, when present, are the weeks of the month (1 = first) |
| `v0/kami.json` | The kami enshrined at Suginami's shrines, each explained once in English and Japanese. Shrines in the files above list theirs by id |
| `v0/content.json` | Everything above in one file, for apps that want a single consistent request |
| `v0/map.en.kml`, `v0/map.ja.kml` | A map to import into a map app: neighborhood outlines, then a layer per kind of place. One file per language, because map apps show one name per pin |
| `v0/spots.geojson` | Every place as GeoJSON points, for developers and GIS tools |
| `v0/towns.geojson` | All 139 towns (丁目) of Suginami as polygons, each tagged with its area and official census code |

All of these are cut from the same build, so they always agree with each other. Every JSON file
carries `version` and `languages`.

## Put it on your own map

Download `map.en.kml` or `map.ja.kml`, then:

- **Google My Maps** (mymaps.google.com): create a map, choose *Import* on a layer, and upload the file. It
  then appears in Google Maps on your phone under *Saved* → *Maps*.
- **Google Earth** (earth.google.com): *Projects* → *New project* → *Import KML file*.
- **Organic Maps, OsmAnd and most offline map apps**: open the file with the app, or import it from its
  bookmarks or tracks screen.

Apple Maps cannot import files.

Towns are identified by their **official census code** (e.g. `13115001001` for 方南一丁目), so this
data can be joined to other datasets. Areas are identified by a short id (e.g. `kugayama`).

Every text field a reader might see is given in both languages as `{"en": "…", "ja": "…"}`.

Places carry a `checked` date: when someone last confirmed they were still there. Happenings carry
`starts` and `ends` dates; a happening is over the day after it ends. Each place and happening
names its `source`.

## Versioning

**`v0` is not yet stable.** Fields may change while the app that uses it settles. When the format is
stable it will be published as `v1`, and from then on a breaking change means a new version path, not
an edit to an existing one.

## Please check the source

This is a convenience, not an authority. Shops close and events move. Where it matters, check the
source each entry names.

## Attribution

The town boundaries and codes are processed from:

> 「令和2年国勢調査町丁・字等別境界データ」（総務省統計局）を加工して作成
> 出典：政府統計の総合窓口(e-Stat) https://www.e-stat.go.jp/

If you republish the town data, keep that credit and say that it has been processed. This dataset
is not published by the Japanese government, and does not represent it.

Trash collection days are converted from Suginami City's published list of collection days by
block (杉並区「ごみ・資源の収集曜日」, https://www.city.suginami.tokyo.jp/documents/12125/garbage.csv).
The city's calendars are the authority; check them if in doubt.

Neighborhood descriptions, places and happenings are written for this project from facts gathered
locally. They are not copied from their sources.

The licence for this project's own content has not yet been chosen.
