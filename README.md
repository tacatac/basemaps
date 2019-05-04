# Basemaps

Basemaps is used to generate mapfiles for [MapServer](https://mapserver.org) in order to serve and style [OpenStreetMap](https://www.openstreetmap.org) data.

This package uses a Python script and the C preprocessor to build a complete mapfile from a set of templates and styling information.

Use the branch corresponding to your mapserver version, e.g.
 - branch-6-2 for mapserver versions 6.2.X
 - master for development (unreleased) mapserver versions

The build process uses the gcc preprocessor extensively, you should have it installed on your system. On linux, check that the `cpp` command is present. On OSX, the provided `cpp` program is a shell wrapper that is not suitable: the Makefile is coded to call `cpp-4.2`, which you can change in case you have another version installed.

## Usage

### Data

#### PostGIS database

The mapfiles rely on a Postgresql database schema as created by a recent version of imposm with the `imposm3-mapping.json` file provided by Basemaps.

See the [Imposm documentation]( https://imposm.org/docs/imposm3/latest/) for information on how to import OpenStreetMap data into Postgresql.

Until recently imposm did not create the landusages_gen and waterareas_gen tables. Since 2.3.0 this is not the case anymore.

If you do not have the generalized tables, you can change the landusage_data and waterareas_data entries in `styles/default.py` so that it queries the non-generalized tables on the lower zoom levels (this will be slower for the lower zoom levels).

The generated mapfile can also be made to query an osm database created with osm2pgsql rather than imposm.

This setup is not recommended as it will be much slower. To use the osm2pgsql schema, you should add the `osm2pgsql` entry to the list of styles for an entry of `style_aliases` in `generate_style.py`, e.g:

    "bingosm2pgsql":"default,outlined,bing,osm2pgsql"

Then run `make STYLE=bingosm2pgsql` to create the osm-bingosm2pgsql.map

#### OSM coastline data shapefiles

The generated mapfiles also use OpenStreetMap coastline data for rendering low zoom maps. They can be downloaded by running `make data` or from https://osmdata.openstreetmap.de/.

#### Boundaries data shapefiles

The generated mapfiles use the boundaries shapefile provided in the `data/` directory.

#### Fonts

DejaVuSans fonts are used by the generated mapfile and provided in the `fonts/` directory.

### Makefile parameters

Some parameters such as the output `STYLE` can be passed as arguments when generating the make files, eg:

    make STYLE=michelin

### Data path locations

The mapfile is generated with relative paths for data files.

The `fonts.lst` file needs to be in the same directory as the mapfile.

The `fonts/` directory, containing DejaVuSans fonts, needs to be in the same directory as the mapfile.

The `data/` directory, containing the coastline and border data, needs to be in the same directory as the mapfile.

The `styles/` directory, containing named styles as Python modules.

Of course these can be symlinks/hardlinks.

## Further configuration

Styling configuration and tweaks should be done in the `styles/` directory.

The `style_aliases` dictionary in `generate_style.py` provides possible combinations of styles to apply, styles ordered later will shadow earlier ones.

Documentation as to how to edit styles to adapt the rendering has yet to be done, but is simple.

Check https://github.com/mapserver/basemaps/wiki/Tweaking-Map-Styles for a preliminary tutorial.
