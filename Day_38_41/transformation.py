import os
import pandas as pd
from utils import get_time

def transform_and_load(df, load_csv=False, output_to_local=False):
    service_info = df.loc[:,['servicecode', 'servicecodedescription', 'servicetypecodedescription', 'organizationacronym']]
    service_info.drop_duplicates(subset="servicecode", inplace=True)
    service_info = service_info.reset_index(drop=True)

    # 
    start_date = df['adddate'].min() - pd.DateOffset(years= 1)
    end_date = df['serviceduedate'].max() + pd.DateOffset(years= 1)

    request_date = pd.DataFrame(pd.date_range(start=start_date,
                            end=end_date, freq='1H', normalize=True), columns=['Date']) #df['serviceduedate'].max()

    request_date['year'] = request_date['Date'].dt.year
    request_date['months'] = request_date['Date'].dt.month
    request_date['day'] = request_date['Date'].dt.day
    request_date['week'] = request_date['Date'].dt.isocalendar().week
    request_date['dayofweek'] = request_date['Date'].dt.dayofweek
    request_date['quarter'] = request_date['Date'].dt.quarter
    request_date['is_weekend'] = request_date['dayofweek'].apply(lambda x: True if x in [5,6] else False)
    request_date['hour'] = request_date['Date'].dt.hour
    request_date['time_of_day'] = request_date['hour'].apply(lambda x: get_time(x))

    
    #
    status_col = ['priority', 'serviceorderstatus', 'status_code',]
    service_status = df.loc[:,status_col]
    service_status.drop_duplicates(subset=["priority", "serviceorderstatus"], inplace=True)
    service_status.dropna(subset=['priority'], inplace=True)
    service_status = service_status.reset_index(drop=True).reset_index()
    service_status['index'] = service_status['index'].apply(lambda x : x+1)
    service_status.rename(columns={'index':'status_id'}, inplace=True)

    
    #
    address_col = ['streetaddress', 'xcoord', 'ycoord', 'latitude', 'longitude', 'city', 'state', 'zipcode', 'maraddressrepositoryid', 'ward']
    address_details = df.loc[:, address_col]
    address_details.drop_duplicates(subset=["streetaddress"], inplace=True)
    address_details = address_details.reset_index(drop=True).reset_index()
    address_details['index'] = address_details['index'].apply(lambda x : x+1)
    address_details.rename(columns={'index':'address_id'}, inplace=True)

    # 
    serviceFacts = df.drop(['servicecodedescription', 'servicetypecodedescription', 'organizationacronym'], axis=1)
    serviceFacts = serviceFacts.merge(service_status, left_on=['serviceorderstatus', 'priority'], right_on=['serviceorderstatus','priority'])
    serviceFacts.drop(['serviceorderstatus', 'priority','status_code_y','status_code_x'], axis=1, inplace=True)
    address_col.remove('streetaddress') # removes streetaddress from the list, because it would be used for merging the two dataframe
    serviceFacts.drop(address_col, axis=1, inplace=True)
    serviceFacts = serviceFacts.merge(address_details, left_on=['streetaddress'], right_on=['streetaddress'])
    address_col.insert(0,'streetaddress') # insertng the streetaddress so the column could be droppped
    serviceFacts.drop(address_col, axis=1, inplace=True)

    # below code changes the time to nearest hour
    serviceFacts.loc[:,['adddate', 'resolutiondate', 'serviceduedate', 'serviceorderdate']] = \
                serviceFacts[['adddate', 'resolutiondate', 'serviceduedate', 'serviceorderdate']].apply(lambda x: x.round('H'))

    # serviceFacts
    serviceFacts = serviceFacts[['servicerequestid','servicecode', 'status_id', 'address_id', 'adddate', \
                                'resolutiondate','serviceduedate', 'serviceorderdate', 'details', 'servicecallcount']]

    if output_to_local:
        directory = 'output'
        if not os.path.exists(directory):
            os.makedirs(directory)
        if load_csv:
            address_details.to_csv('output/dimLocation.csv', index=False)
            service_status.to_csv('output/dimServiceStatus.csv', index=False)
            service_info.to_csv('output/dimServiceType.csv', index=False)
            request_date.to_csv('output/dimDate.csv', index=False)
            serviceFacts.to_csv('output/serviceFacts.csv', index=False)
        else:
            address_details.to_json('output/dimLocation.json', orient='records')
            service_status.to_json('output/dimServiceStatus.json', orient='records')
            service_info.to_json('output/dimServiceType.json', orient='records')
            request_date.to_json('output/dimDate.json', orient='records')
            serviceFacts.to_json('output/serviceFacts.json', orient='records')

        # files = glob(f"./output/*.csv")
        # files
    # if load_csv:
    #     load_format='csv'
    # else:
    load_format='json'
    data_to_upload = {f'dimLocation.{load_format}' : address_details,
                f'dimDate.{load_format}' :  request_date,
                f'serviceFacts.{load_format}' : serviceFacts,
                f'dimServiceType.{load_format}' : service_info,
                f'dimServiceStatus.{load_format}' : service_status}
    return data_to_upload
    
if __name__=='__main__':
    transform_and_load()
