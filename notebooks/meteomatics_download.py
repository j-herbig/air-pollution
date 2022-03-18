import pandas as pd
import meteomatics.api as api
import datetime as dt

parameters_ts = ['t_2m:C', 'msl_pressure:hPa', 'precip_1h:mm', 'wind_speed_10m:ms', 'wind_dir_10m:d']

now = dt.datetime.utcnow().replace(minute=0, second=0, microsecond=0)
startdate_ts = now
enddate_ts = startdate_ts + dt.timedelta(days=9)
interval_ts = dt.timedelta(hours=1)

username = 'neuefischegmbh_rankovic'
password = '2Fsy8O2NzQ'

coordinates_ts, city = [(50.0259, 8.5213)], 'Frankfurt' 
coordinates_ts_1, city_1 = [(53.0451, 8.7981)], 'Bremen'

try:
    df_ts = api.query_time_series(coordinates_ts, startdate_ts, enddate_ts, interval_ts,
                                  parameters_ts, username, password)
    df_ts_1 = api.query_time_series(coordinates_ts_1, startdate_ts, enddate_ts, interval_ts,
                                  parameters_ts, username, password)
except Exception as e:
    print("Failed, the exception is {}".format(e))

df_ts = df_ts.reset_index()
df_ts['city'] = city
df_ts = df_ts.rename(columns={'validdate': 'timestamp', 't_2m:C': 'temperature', 'msl_pressure:hPa': 'pressure', 'precip_1h:mm': 'precip', 'wind_speed_10m:ms': 'wind_speed', 'wind_dir_10m:d': 'wind_direction'})

df_ts_1 = df_ts_1.reset_index()
df_ts_1['city'] = city_1
df_ts_1 = df_ts_1.rename(columns={'validdate': 'timestamp', 't_2m:C': 'temperature', 'msl_pressure:hPa': 'pressure', 'precip_1h:mm': 'precip', 'wind_speed_10m:ms': 'wind_speed', 'wind_dir_10m:d': 'wind_direction'})

df_ts['timestamp'] = df_ts['timestamp'].dt.tz_localize(None)
df_ts_1['timestamp'] = df_ts_1['timestamp'].dt.tz_localize(None)

df_ts.to_csv(f'/Users/filip/neuefische/air-pollution/data/Meteomatics/auto_processed_weather_forecast_{city}_{now.date()}.csv', index=False)
df_ts_1.to_csv(f'/Users/filip/neuefische/air-pollution/data/Meteomatics/auto_processed_weather_forecast_{city_1}_{now.date()}.csv', index=False)