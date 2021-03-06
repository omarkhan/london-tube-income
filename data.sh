#!/bin/sh

# This script takes our source data and turns it into the big json we use for the visualization.

set -eo pipefail
cd "$(dirname $0)"
export PYTHONUNBUFFERED='true'

cat source-data/stations.csv |                # List of stations
  ./bin/stations.py |                         # Fetch postcodes for each station
  ./bin/areas.py |                            # Map station postcodes to ONS super output areas
  ./bin/incomes.py source-data/incomes.csv |  # Map station areas to income data
  ./bin/lines.py source-data/lines.json > templates/data.json # Generate json data for each tube line
