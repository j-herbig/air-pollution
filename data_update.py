import numpy as np
import pandas as pd
import datetime 
import glob

# 1. make sure to run "download_Deutscher_Wetterdienst.ipynb" and "download_sensor_community_update_data.ipynb" before this. 
# 2. do not forget to delete "data/DeutscherWetterdienst" before running "download_Deutscher_Wetterdienst.ipynb"
# 3. lastly, 

# define needed functions 

def import_sensor_data(sensor):
    '''
    imports the data for a given sensor type (sds, bme, bmp, dht)
    returns list with DataFrames with one entry per sensor
    '''
    path = r'data/SensorCommunity' # use your path
    all_files = glob.glob(path + "/*.csv") # list with paths to data files

    li = []
    # select data files for chosen sensor, read it to DataFrame and save it in list
    for filename in all_files: 
        if sensor in filename:
            df = pd.read_csv(filename, index_col=None, header=0)
            li.append(df)

    return pd.concat(li, axis=0, ignore_index=True)

def process_timestamps(df):
    # add columns with date and hour
    df.timestamp = pd.to_datetime(df.timestamp) # string to datetime
    df['hour'] = df.timestamp.dt.hour
    df['date'] = pd.to_datetime(df.timestamp.dt.date)
    df['timestamp'] = pd.array(df.timestamp).floor(freq='H')   #
    #pd.to_datetime(df['date'].astype(str) + '_' + df_sds['hour'].astype(str), format='%Y-%m-%d_%H')
    
def label_cities(lat, lon):
    if (lat >= 50.030681) and (lat <= 50.205692) and (lon >= 8.430634) and (lon <= 8.919868):
        return 'Frankfurt'
    else:
        return 'Bremen'


# Calculate a dynamic median per hour for all sensors in a city.
def clean_pm(df: pd.DataFrame, cols: list=['PM10', 'PM2p5'], factor: int = 3) -> pd.DataFrame:
    """deletes outliers for the given columns and considerung their timestamps and cities which are larger than factor times the median

    Args:
        df (pd.DataFrame): input dataframe
        cols (list): columns to clean
        factor (int, optional): factor that is used to calculate the threshold for keeping or deleting data. Defaults to 3.

    Returns:
        pd.DataFrame: cleaned dataframe
    """

    for col in df.columns:
        if 'threshold' in col:
            df.drop(col, axis=1, inplace=True)
    
    # define a list for saving the thresholds
    thresholds = []

    # for each city in the dataframe make a dataframe with timestamps
    for city in df['city'].unique():
        df_cur = df[df['city'] == city]
        df_threshold = pd.DataFrame(
            data={
                'timestamp': df_cur['timestamp'].unique(), 
                'city': city
            }
        )

        # for each timestamp calculate the median and threshold (factor * median)
        for col in cols:
            df_threshold[col+'_median'] = df_threshold.apply(lambda x: df_cur[(df_cur['timestamp'] == x['timestamp'])][col].median(), axis=1)
            df_threshold[col+'_threshold'] = factor * df_threshold[col+'_median']
        thresholds.append(df_threshold)

    # concatenate all thresholds
    df_thresholds = pd.DataFrame()
    for df_threshold in thresholds:
        df_thresholds = pd.concat([df_thresholds, df_threshold])
    
    # merge thresholds with original dataframe on timestamp and city 
    df = df.merge(df_thresholds, how='left', on=['timestamp', 'city'])
    
    # delete values if they are above the threshold and print number of deleted values
    for col in cols:
        nan_before = df[col].isna().sum()
        df[col] = df.apply(lambda x: x[col] if x[col] <= x[col+'_threshold'] else np.nan, axis=1)
        print(f"{df[col].isna().sum() - nan_before} NaNs added in {col}")

    # for col in cols:
    #     df.drop([col+'_threshold'], axis=1, inplace=True)
    return df



# Drop sensors with only few data in the past year
def get_share_of_missing_values(df: pd.DataFrame, start_time: str):
    # Get the total number of observations possible in the past year
    observations_of_interest = df[(df['location_id'] == df['location_id'].unique()[0]) & (df['timestamp'] >= pd.to_datetime(start_time))].shape[0]

    # make a dataframe to store missing values per location
    missing_values = pd.DataFrame(columns=['location_id', 'city', 'PM10_missing', 'PM2p5_missing'])

    # get missing values for every location
    for location in df['location_id'].unique():
        # filter for location
        df_cur = df[(df['location_id'] == location) & (df['timestamp'] >= '2021-01-01')][['city', 'PM10', 'PM2p5']]
        
        # create a new entry in the dataframe containing location_id, city and share of missing values
        new_entry = {
            'location_id': int(location),
            'city': df_cur['city'].iloc[0],
            'PM10_missing': df_cur['PM10'].isna().sum() / observations_of_interest,
            'PM2p5_missing': df_cur['PM2p5'].isna().sum() / observations_of_interest,
        }
        missing_values = missing_values.append(new_entry, ignore_index=True)

    # cast location_id to int
    missing_values['location_id'] = missing_values['location_id'].astype(int) 
    return missing_values


# get the data of those good sensors
def use_good_sensors_only(df, good_sensors):
    df_good_sensors = df[df['location_id'].\
        isin(good_sensors)].\
            drop([col for col in df.columns if ('median' in col or 'threshold' in col)], axis=1)
    return df_good_sensors


if __name__ == "__main__":
    # day of download of data files
    day = datetime.datetime.now().date()

    # load data and drop unnecessary columns
    df_sds = import_sensor_data('sds').drop(['durP1', 'durP2', 'ratioP1', 'ratioP2', 'sensor_type', 'sensor_id', 'location'], axis=1)

    dataframes = [df_sds]
    # Make date and hour columns
    for df in dataframes:
        process_timestamps(df)

    # PM sensors
    df_sds_grouped = df_sds.groupby(['hour', 'date', 'lat', 'lon', 'timestamp']).mean().reset_index() # mean
    df_sds_grouped_std = df_sds.groupby(['hour', 'date', 'lat', 'lon', 'timestamp']).std().reset_index() # std
    df_sds_grouped_std.rename(columns={'P1': 'PM10_std', 'P2': 'PM2p5_std'}, inplace=True)
    df_sds_grouped.rename(columns={'P1': 'PM10', 'P2': 'PM2p5'}, inplace=True)
    df = df_sds_grouped.merge(df_sds_grouped_std, how='left', on=['hour', 'date', 'lat', 'lon', 'timestamp'])
    # add city column (Frankfurt, Bremen)
    df['city'] = df.apply(lambda x: label_cities(x.lat, x.lon), axis=1)

    # create list of distinct lat/long positions of sensor data
    data_area_location = df[['lat', 'lon', 'city']].drop_duplicates()

    # create data area of all possible timestamps
    data_area_time = pd.DataFrame()
    data_area_time['timestamp'] = pd.date_range(start=df['timestamp'].min(), end=df['timestamp'].max(), freq='H')

    # create complete data area over all timestamps and locations
    data_area = data_area_location.merge(data_area_time, how='cross')

    # join data to data area
    full_sensor_df = data_area.merge(df, how='left', on=['lat','lon','timestamp', 'city'])

    # Merge sensor data and dwd data
    # load dwd data
    dwd_df = pd.read_csv(f'data/processed_deutscher_wetterdienst_{day}.csv', index_col=0)
    dwd_df['date'] = pd.to_datetime(dwd_df.date)
    dwd_df.rename(columns={'date': 'timestamp'}, inplace=True)


    # replace error value of -999 with NaN
    for col in dwd_df.columns:
        dwd_df[col] = dwd_df[col].replace(-999, np.nan)

    # merge dwd and sensor
    sensor_dwd_df = full_sensor_df.merge(dwd_df, how='left', on=['timestamp','city'])

    # add sensor IDs
    df_location = sensor_dwd_df.groupby(['lat', 'lon']).count().reset_index()[['lat', 'lon']]
    df_location['location_id'] = df_location.index+1
    sensor_dwd_df = sensor_dwd_df.merge(df_location, on=['lat', 'lon'], how='left')

    # define lists with columns
    no_data_cols = ['location_id', 'timestamp', 'city', 'lat', 'lon']
    sc_cols = sorted(['PM10', 'PM2p5', 'PM10_std', 'PM2p5_std'])
    sc_cols_wo_std = [col for col in sc_cols if 'std' not in col]
    dwd_cols = sorted([col for col in dwd_df.columns if (col not in no_data_cols and col not in sc_cols)])
    std_cols = [col for col in sc_cols if 'std' in col]
    data_cols_wo_std = sc_cols_wo_std + dwd_cols
    data_cols = sc_cols + dwd_cols

    # reorganize columns: first non-data columns, then sorted data columns
    sensor_dwd_df = sensor_dwd_df.reindex(columns=no_data_cols + sc_cols + dwd_cols)

    # apply cleaning function
    sensor_dwd_df = clean_pm(sensor_dwd_df)
    
    missing_values = get_share_of_missing_values(sensor_dwd_df, '2021-01-01')

    # get the IDs of good sensors having less than 25 % missing values in PM2.5
    good_sensors = missing_values.query("PM2p5_missing < 0.25")['location_id']

    df_good_sensors = use_good_sensors_only(sensor_dwd_df, good_sensors=good_sensors)

    # export data 
    # all data for final prediction
    df_good_sensors.to_csv(f"data/cleaned_sensors_dwd_{day}.csv")

    # Train test split for model evaluation
    split_time = '2022-01-31 23:00'
    df_train = df_good_sensors[df_good_sensors.timestamp <= split_time]
    df_train.to_csv(f"data/cleaned_sensors_dwd_train_{day}.csv")

    df_test = df_good_sensors[df_good_sensors.timestamp > split_time]
    df_test.to_csv(f"data/cleaned_sensors_dwd_test_{day}.csv")
