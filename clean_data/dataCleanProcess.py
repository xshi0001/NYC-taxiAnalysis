import pandas as pd
def trip_merge_fare(df_trip, df_fare):
	df = pd.concat([df_trip, df_fare], axis=1, join="inner")
	df = df.loc[:, ~df.columns.duplicated()]
	return df


def drop_wrong_data(df):
	''' Remove rows with unreasonable values in passenger_count, trip_time, trip_distance,
		total_amount, fare_amount, tip_amount, toll_amount, etc. '''

	# number of passenger: 208 is way too large to be true, 0 is also not for a valid ride
	df = df[df.passenger_count != 208]
	df = df[df.passenger_count != 0]

	# trip time should be non-negative and less than one day
	df = df[df.trip_time >= 0.0]
	df = df[df.trip_time <= 86400]

	# trip distance larger than 100 miles is unreasonably far
	df = df[df.trip_distance < 100]

	# any amount paid should be non-negative
	df = df[df.total_amount >= 0.0]
	df = df[df.fare_amount >= 0.0]
	df = df[df.surcharge >= 0.0]
	df = df[df.tolls_amount >= 0.0]
	return

if __name__ == '__main__':
	i= "1"
	path = "D:/shi0001/myfile/python/TaxiData/sample_data/"
	# path = "D:/shi0001/myfile/python/TaxiData/original_data/"
	df_trip = pd.read_csv(path + "trip_data_{0}.csv".format(i), low_memory=False)
	df_fare = pd.read_csv(path + "trip_fare_{0}.csv".format(i), low_memory=False)
	df_fare.columns = [i.strip() for i in df_fare.columns]
	df_trip.columns = [i.strip() for i in df_trip.columns]
	df = trip_merge_fare(df_trip, df_fare)
	# drop_wrong_data(df)
	df.to_csv(path + "/trip_data_2013_{0}.csv".format(i))



