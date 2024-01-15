from utils import pd, time, od, flat_items

# dataset_url = 'https://opendata.arcgis.com/api/v3/datasets/14faf3d4bfbe4ca4a713bf203a985151_0/downloads/data?format=geojson&spatialRefId=4326&where=1%3D1'

def retrieve_data(dataset_url):
    url_name = dataset_url.split('/')[-1]
    od.download(dataset_url, 'data', filename='service.json')

    # Source
    # src = f'data/{url_name}'

    # Destination
    dest = 'data/All_311_City_Service_Requests_-_Last_30_Days.geojson'

    data = pd.read_json(f'./{dest}', orient='index').T.to_dict()

    service_req_df_combine = []
    serviec_req_cols = []
    strt = time.time()

    for item in data['features'][0]:
        if len(serviec_req_cols) < 1:
            serviec_req_cols = [k for k,_ in list(flat_items(item, key_separator='.'))]
        service_req_df_combine.append([v for _,v in list(flat_items(item, key_separator='.'))])

    service_req_df_json = pd.DataFrame(service_req_df_combine, columns=serviec_req_cols)
    endt = time.time()
    print(f'Data successfully downloaded to {dest}')
    print('Time Taken: ', endt - strt)
    return service_req_df_json

# if __name__=="__main__":
#     retrieve_data(dataset_url)
