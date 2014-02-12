## Methodology

Starting points: a [csv of tube station coordinates][1] from Chris Bell, an
[adjacency list representation of the tube network graph][2] from wikimedia,
and the latest [MSOA-level model-based income estimates][3] from the
neighbourhood statistics website.  Data from 2007/08.

Station coordinates are matched up with [MSOAs][4] by first converting them to
postcodes using the [UK Postcodes API][5]. These postcodes are then matched up
with MSOA names using the [neighbourhood statistics API][6]. Some
distance-calculating guesswork is used when the API fails for no apparent
reason.

Once each station has been mapped to a MSOA, we can map the income data.
This is then combined with our graph of stations, which we walk using
depth-first search to find all branches on each line.

The end result is a big JSON that is displayed using SVG with [d3][7]. No other
frameworks are used. Source code for the visualization and the data processing
[available on github][8]. Thanks to [Ben Barnett][9] for the [original
version][10] of the SVG tube map used above, and to [John Galantini][11] for
the tube map font taken from his [CSS tube map][12] project.

My name is Omar, I'm a programmer. Get in touch:
[![linkedin](./static/img/webicon-linkedin.svg)][13]
[![github](./static/img/webicon-github.svg)][14]

[1]: http://www.doogal.co.uk/london_stations.php
[2]: http://commons.wikimedia.org/wiki/London_Underground_geographic_maps/CSV
[3]: http://www.neighbourhood.statistics.gov.uk/dissemination/Info.do?page=analysisandguidance/analysisarticles/income-small-area-model-based-estimates-200708.htm
[4]: http://www.ons.gov.uk/ons/guide-method/geography/beginner-s-guide/census/super-output-areas--soas-/index.html
[5]: http://uk-postcodes.com/api
[6]: http://www.neighbourhood.statistics.gov.uk/dissemination/Info.do?page=nde.htm
[7]: http://d3js.org/
[8]: https://github.com/omarkhan/london-tube-income
[9]: http://www.benbarnett.net/
[10]: https://github.com/benbarnett/SVG-Tube-Map
[11]: http://www.johngalantini.com/
[12]: http://www.csstubemap.co.uk/
[13]: http://www.linkedin.com/pub/omar-khan/28/797/530
[14]: https://github.com/omarkhan
