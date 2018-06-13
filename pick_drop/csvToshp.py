# csv data  to from_epsg(4269) 坐标
# import libraries
import shapefile, csv
import urllib
import os
top_dir = 'D:/shi0001/myfile/python/NYC-taxiAnalysis'
os.chdir(top_dir)

# funtion to generate a .prj file
def getWKT_PRJ(epsg_code):
	wkt = urllib.urlopen("http://spatialreference.org/ref/epsg/{0}/prettywkt/".format(epsg_code))
	remove_spaces = wkt.read().replace(" ", "")
	output = remove_spaces.replace("\n", "")
	return output


# create a point shapefile
trees_shp = shapefile.Writer(shapefile.POINT)

# for every record there must be a corresponding geometry.
trees_shp.autoBalance = 1

# create the field names and data type for each.
trees_shp.field("medallion", "C")
trees_shp.field("hack_license", "C")
trees_shp.field("vendor_id", "C")
trees_shp.field("rate_code", "I")
trees_shp.field("store_and_fwd_flag", "C")
trees_shp.field("pickup_datetime", "D")
trees_shp.field("dropoff_datetime", "D")
trees_shp.field("passenger_count", "N")
trees_shp.field("trip_time_in_secs", "N")
trees_shp.field("trip_distance", "F")
trees_shp.field("payment_type", "C")
trees_shp.field("fare_amount", "F")
trees_shp.field("surcharge", "F")
trees_shp.field("mta_tax", "F")
trees_shp.field("tip_amount", "F")
trees_shp.field("tolls_amount", "F")
trees_shp.field("total_amount", "F")

# pickup_longitude	pickup_latitude	dropoff_longitude	dropoff_latitude	payment_type	fare_amount	surcharge	mta_tax	tip_amount	tolls_amount	total_amount


# count the features
counter = 1

# access the CSV file
with open("./TaxiData/sample_data/trip_data_2013_1.csv", 'rb') as csvfile:
	reader = csv.reader(csvfile, delimiter=',')
	# skip the header
	# next(reader, None)
	# loop through each of the rows and assign the attributes to variables
	for row in reader:
		medallion = row[0]
		hack_license = row[1]
		vendor_id = row[2]
		rate_code = row[3]
		store_and_fwd_flag = row[4]
		pickup_datetime = row[5]
		dropoff_datetime = row[6]
		passenger_count = row[7]
		trip_time_in_secs = row[8]
		trip_distance = row[9]
		pickup_longitude = row[10]
		pickup_latitude = row[11]
		dropoff_longitude = row[12]
		dropoff_latitude = row[13]
		payment_type = row[14]
		fare_amount = row[15]
		surcharge = row[16]
		mta_tax = row[17]
		tip_amount = row[18]
		tolls_amount = row[19]
		total_amount = row[20]

		# create the point geometry
		trees_shp.point(float(pickup_longitude), float(pickup_latitude))
		trees_shp.point(float(dropoff_longitude), float(dropoff_latitude))
		# add attribute data
		trees_shp.record(medallion, hack_license, vendor_id, rate_code, store_and_fwd_flag,
						 pickup_datetime, dropoff_datetime, passenger_count,trip_time_in_secs,
						 trip_distance, payment_type, fare_amount, surcharge, mta_tax, tip_amount,
						 tolls_amount, total_amount
						 )
		# medallion	hack_license	vendor_id	rate_code	store_and_fwd_flag	pickup_datetime	dropoff_datetime	passenger_count	trip_time_in_secs	trip_distance	pickup_longitude	pickup_latitude	dropoff_longitude	dropoff_latitude	payment_type	fare_amount	surcharge	mta_tax	tip_amount	tolls_amount	total_amount

		print("Feature " + str(counter) + " added to Shapefile.")
		counter = counter + 1

# save the Shapefile
trees_shp.save("./TaxiData/sample_data/trip_data_2013_1_shp")

# create a projection file
prj = open("./TaxiData/sample_data/trip_data_2013_1_shp.prj", "w")
epsg = getWKT_PRJ("4269")
prj.write(epsg)
prj.close()
