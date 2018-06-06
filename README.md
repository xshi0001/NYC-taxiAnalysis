# The Data Science of NYC Taxi Trips: An Analysis & Visualization

This repo provides scripts to download, process, and analyze data for NYC Taxi Trips before July 2016(described and available here: http://www.nyc.gov/html/tlc/html/about/trip_record_data.shtml, also available either through BiqQuery https://bigquery.cloud.google.com/table/imjasonh-storage:nyctaxi.trip_data, or in smaller samples from http://www.andresmh.com/nyctaxitrips/). 
The data is stored in a [MySQL](http://www.MySQL.org/) database, 
and uses [PostGIS](http://postgis.net/) for spatial calculations, in particular mapping latitude/longitude coordinates to census tracts.