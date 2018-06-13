import pandas as pd
import datetime as dt
import fiona
from shapely import geometry
from sqlalchemy import create_engine
import os

def find_zone(row, cols):
    lon = row[cols[0]]
    lat = row[cols[1]]
    point = geometry.Point(lon, lat)# longitude, latitude
    for i in idx_shape:
        bound = bounds[i]
        if lon < bound[0] or lon > bound[2] or lat < bound[1] or lat > bound[3]:
            continue
        # Alternative: if point.within(shape)
        if shapes[i].contains(point):
            return zones[i]
    return

def add_pickup_dropoff_zones(df):
    dfs = [df]

    pickup_cols = ['pickup_longitude', 'pickup_latitude']
    dfs.append(df[pickup_cols].apply(
            lambda cell: pd.Series(find_zone(cell, pickup_cols), index=['pickup_LocationID']), axis=1))

    dropoff_cols = ['dropoff_longitude', 'dropoff_latitude']
    dfs.append(df[dropoff_cols].apply(
            lambda cell: pd.Series(find_zone(cell, dropoff_cols), index=['dropoff_LocationID']), axis=1))

    return pd.concat(dfs, axis=1)

if __name__ == "__main__":
    shapes = []
    bounds = []
    zones = []
    top_dir = 'D:/shi0001/myfile/python/NYC-taxiAnalysis'
    os.chdir(top_dir)
    with fiona.open("./TaxiData/taxi_zones_new/taxi_zones_new.shp") as fiona_collection:
        for zone in fiona_collection:
            # Use Shapely to create the polygon
            shape = geometry.asShape(zone['geometry'])
            shapes.append(shape)
            bounds.append(shape.bounds)
            zones.append(zone['properties']['LocationID'])

    idx_shape = range(len(shapes))

    start = dt.datetime.now()
    chunksize = 20000
    j = 0
    job_id = 1
    disk_engine = create_engine("mysql+pymysql://root:SHI800810888@localhost:3306/sample", echo=False)

    for df in pd.read_csv('./TaxiData/original_data/tidy_data/trip_data_2013_'+str(job_id)+'.csv', header=0, chunksize=chunksize, iterator=True, encoding='utf-8'):
        df = add_pickup_dropoff_zones(df)

        df.to_sql("trip_data_"+str(job_id), disk_engine, if_exists='append')

        j+=1
        print('{} seconds: completed {} rows'.format((dt.datetime.now() - start).seconds, j*chunksize))
