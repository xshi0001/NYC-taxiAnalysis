![TLC Trip Record Data. - from http://www.nyc.gov](http://upload-images.jianshu.io/upload_images/7255718-941cdf3e853ff447.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)


Data:
This project is using the NYC taxi data from the period before July 2016 described and available[nyc.gov](http://www.nyc.gov/html/tlc/html/about/trip_record_data.shtml), also available either through  [GoogleBiqQuery](https://bigquery.cloud.google.com/table/bigquery-public-data:new_york.tlc_green_trips_2013?pli=1) or in [smaller samples ](http://www.andresmh.com/nyctaxitrips/) or from [archive.org](https://archive.org/details/nycTaxiTripData2013)


#### step1  clean_data
You need to deal with the raw data and find out that the columns names need to be stripped, concat the trip data and fare data in one csv and remove rows with unreasonable values.
#### step2  pick_drop_locationID
 the original taxi zone shp projected coordinate system is defined by [EPSG:2263(NAD_1983_StatePlane_New_York_Long_Island_FIPS_3104_Feet)](https://developers.arcgis.com/javascript/3/jshelp/gcs.htm). However, longitude, latitude in the csv data
 are achieved by geographic coordinate systems [ESPG:4326(GCS_WGS_1984)](https://developers.arcgis.com/javascript/3/jshelp/gcs.htm) So you need to make an coordinate transformation between them to find the locationID for picking and dropping.
 you can use python packages here:
 * [Shapely](https://shapely.readthedocs.io/en/latest/manual.html) - a python package for set-theoretic analysis and manipulation of planar features using (via Python’s ctypes module) functions from the well known and widely deployed GEOS library.
* [GeoPandas](http://geopandas.org/index.html) -  an open source project to make working with geospatial data in python easier. GeoPandas extends the datatypes used by pandas to allow spatial operations on geometric types.
 * [fiona](https://github.com/Toblerity/Fiona) -  It focuses on reading and writing data in standard Python IO style and relies upon familiar Python types and protocols.

#### Reference:
* [Generate a Projection File (.prj) using Python ](https://glenbambrick.com/2015/08/09/prj/)
* [CSV to Shapefile with pyshp](https://glenbambrick.com/2016/01/09/csv-to-shapefile-with-pyshp/)
* [Reproject a Polygon Shapefile using PyShp and PyProj](https://glenbambrick.com/2016/01/24/reproject-shapefile/)