import pandas as pd
import datetime as dt
from shapely import geometry
from shapely.geometry import MultiPolygon,shape
from sqlalchemy import create_engine
import geopandas
import os
import fiona
from fiona.crs import from_epsg
def find_zone(row, cols):
	lon = row[cols[0]]
	lat = row[cols[1]]
	# print(lon, lat)
	point = geometry.Point(lon, lat)  # longitude, latitude  每个trip上下车地点
	print(point)
	for i in idx_shape:
		bound = list(df_bound.loc[i,["minx", "miny", "maxx", "maxy"]])
		# print(bound)
		# (minx = bound[0], miny = bound[1], maxx = bound[2], maxy = bound[3])
		# 在该范围值外，则下一个i
		if lon < bound[0] or lon > bound[2] or lat < bound[1] or lat > bound[3]:
			continue
		# polygon = geometry.Polygon(df_shape.loc[i, ["geometry"]].item())
		if multipolyShape[i].contains(point):
			return df_zones.loc[i,'LocationID'].item()
def add_pickup_dropoff_zones(df):
	dfs = [df]
	#add pickup_LocationID column
	pickup_cols = ['pickup_longitude', 'pickup_latitude']
	dfs.append(df[pickup_cols].round(3).
			   apply(lambda cell: pd.Series(find_zone(cell, pickup_cols), index=['pickup_LocationID']), axis=1))

	dropoff_cols = ['dropoff_longitude', 'dropoff_latitude']
	dfs.append(df[dropoff_cols].round(3).
			   apply(lambda cell: pd.Series(find_zone(cell, dropoff_cols), index=['dropoff_LocationID']), axis=1))
	return pd.concat(dfs, axis=1)

if __name__ == '__main__':
	# Set this to top directory
	top_dir = 'D:/shi0001/myfile/python/NYC-taxiAnalysis'
	os.chdir(top_dir)
	shp = "./TaxiData/taxi_zones.shp"
	shp_df = geopandas.GeoDataFrame.from_file(shp)
	# 转换到经纬度坐标 GCS_North_American_1983
	shp_df_change = shp_df.to_crs(from_epsg(4269))
	# shp_df_change.plot(column="Shape_Area",colormap='Set1')
	df_zones = shp_df_change[['LocationID']]
	# df_shape = shp_df_change[['geometry']]
	multipolyShape = MultiPolygon([shape(poly['geometry']) for poly in fiona.open(shp)])
	# geometric Manipulations
	df_bound = shp_df_change[['geometry']].bounds.round(3)
	idx_shape = range(0, df_zones.shape[0])
	start = dt.datetime.now()
	chunksize = 20000
	j = 0
	job_id = 1
	disk_engine = create_engine("mysql+pymysql://root:SHI800810888@localhost:3306/sample", echo=False)
	for df in pd.read_csv('./TaxiData/sample_data/trip_data_2013_' +
						  str(job_id) + '.csv', header=0, chunksize=chunksize, iterator=True):
		df = add_pickup_dropoff_zones(df)
		df.to_sql("trip_data_" + str(job_id), disk_engine, if_exists='append')
		j += 1
		print('{} seconds: completed {} rows'.format((dt.datetime.now() - start).seconds, j * chunksize))