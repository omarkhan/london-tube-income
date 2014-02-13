# MIND THE GAP

## Household income by London Underground station

Based on [this feature][1] in the New Yorker and [this project][2] by [Dan
Grover][3].

Source data consists of a [csv of tube station coordinates][4] from Chris Bell,
an [adjacency list representation of the tube network graph][5] from wikimedia,
and the latest [MSOA-level model-based income estimates][6] from the
neighbourhood statistics website.  Data from 2007/08.

Thanks to [Ben Barnett][7] for the [original version][8] of the SVG tube map
used above, and to [John Galantini][9] for the tube map font taken from his
[CSS tube map][10] project.

### Hacking

First, run

    pip install -r requirements.txt
    npm install -g coffee-script uglify-js

This project uses [Cactus][11] to generate a static site from a bunch of django
templates and other source files. Data processing scripts are in `bin/`,
templates are in `pages/` and `templates/`, static assets are in `static/`.
Pretty straightforward.

To build the frontend:

    make

This will put everything in `.build/`.

To re-run the data processing scripts:

    make data

To serve the frontend at `localhost:8000` for development:

    make serve

[1]: http://www.newyorker.com/sandbox/business/subway.html
[2]: http://dangrover.com/
[3]: http://dangrover.github.io/sf-transit-inequality/
[4]: http://www.doogal.co.uk/london_stations.php
[5]: http://commons.wikimedia.org/wiki/London_Underground_geographic_maps/CSV
[6]: http://www.neighbourhood.statistics.gov.uk/dissemination/Info.do?page=analysisandguidance/analysisarticles/income-small-area-model-based-estimates-200708.htm
[7]: http://www.benbarnett.net/
[8]: https://github.com/benbarnett/SVG-Tube-Map
[9]: http://www.johngalantini.com/
[10]: http://www.csstubemap.co.uk/
[11]: https://github.com/koenbok/Cactus
