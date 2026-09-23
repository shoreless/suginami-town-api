# suginami-town-api

Open data about the neighborhoods of Suginami, Tokyo, served as static JSON. It is maintained as a
volunteer project and is the data behind the すぎなみ好き (Suginami Suki) stamp-book app.

There is no server: every endpoint is a file, served by GitHub Pages, so it is free to use and has
no rate limits or keys.

## Endpoints

Base URL: `https://shoreless.github.io/suginami-town-api/`

| Path | What it holds |
| --- | --- |
| `v0/content.json` | The 23 neighborhood areas: names in English and Japanese, the official towns (丁目) each covers, a short introduction, places worth visiting, and dated happenings |
| `v0/towns.geojson` | All 139 towns (丁目) of Suginami as polygons, each tagged with its area and official census code |

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

Neighborhood descriptions, places and happenings are written for this project from facts gathered
locally. They are not copied from their sources.

The licence for this project's own content has not yet been chosen.
