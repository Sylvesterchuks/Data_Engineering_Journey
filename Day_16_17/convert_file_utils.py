
def get_dict_rows(filename='countries.csv'):
    with open(filename,'r',encoding='utf-8') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        line_count = 0
        country_dict = {}
        for row in csv_reader:
            if line_count == 0:
                print(f'Column names are {", ".join(row)}')
                line_count += 1
            country_dict[str(line_count)] = row
            print(country_dict)
            line_count += 1
        print(f'Processed {line_count} lines.')
        return country_dict

def open_json(filename='countries.json'):
    with open(filename,'r+', encoding='utf-8') as f:
        country_dict = json.load(f)
    return country_dict

def open_csv(filename='countries.csv'):
    with open(filename,'r+') as f:
        txt = f.readlines()
    return txt, len(txt)


def get_json(filename='mycountries.json', csv_filename='countries.csv'):
    with open(filename,'w+', encoding='utf-8') as f:
        country_dict = get_dict_rows(csv_filename)
        json_string = json.dumps(country_dict,
                                 indent = 4)
        f.write(json_string)


def csv_row(val):
    row = []
    if isinstance(val,dict):
        for j in val.values():
            if isinstance(j,dict):
                row.append(','.join(list(j.values())))
            else:
                row.append(j)
    else:
        row.append(','.join(val))
        print(row)
    return row

def convert_to_csv(x):
    
    file_len = 0
    result = []
    if not isinstance(x, dict):
        # print('if statement')
        for val in x:
            row = []
            if file_len == 0:
                result.append(list(i.keys()))
                file_len += 1
            result.append(csv_row(i))
    else:
        # print('The else statement')
        for i in x.values():
            row = []
            if file_len == 0:
                result.append(list(i.keys()))
                print(f'Column names are {", ".join(i.keys())}')
                file_len += 1
            result.append(csv_row(i))
    print(f'Processed {file_len} lines.')
    return result

def get_csv_file(filename='mycountries.csv', json_filename='countries.json'):
    with open(filename,'w',encoding='utf-8') as file:
        json_file = open_json(json_filename)
        dic = convert_to_csv(json_file)

        country_writer = csv.writer(file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

        for value in dic:
            country_writer.writerow(value)

def convert_excel_file_with_pandas(sheetname): 
    movie_details = []
    single = []
    line_count = 0
    for row in range(0, dataframe[sheetname].max_row):
        for col in dataframe[sheetname].iter_cols(1, dataframe[sheetname].max_column):
            single.append(col[row].value)
            # print(dataframe[sheetname].iter_cols(1)[0].value)
        single = [r.replace('\ufeff', '').replace('\xa0', '') if isinstance(r,str) else r for r in single]
        movie_details.append(single)
        single = []

    print(f'Movies Info {sheetname} was successfully transformed')
    df  = pd.DataFrame(movie_details)
    df.columns = df.iloc[0] 
    df = df[1:]
    df.to_csv(f'{sheetname}_cleaned.csv', index=False)
    print(f'Movies Info {sheetname} was successfully saved as csv file')
    return movie_details

def convert_excel_file(sheetname): 
    movie_details = []
    single = []
    line_count = 1
    for row in range(0, dataframe[sheetname].max_row):
        for col in dataframe[sheetname].iter_cols(1, dataframe[sheetname].max_column):
            single.append(col[row].value)
            # print(dataframe[sheetname].iter_cols(1)[0].value)
        single = [r.replace('\ufeff', '').replace('\xa0', '') if isinstance(r,str) else r for r in single]
        movie_details.append(single)
        single = []

    print(f'Movies Info {sheetname} was successfully transformed')
    
    with open(f'{sheetname}_cleaned.csv', 'w') as f:
        csv_writer = csv.writer(f, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        if line_count==0:
            print('if ran')
            csv_writer.writerow(['timestamp','severity_level','message'])
            line_count += 1
        for info in movie_details:
            csv_writer.writerow(info)
    print(f'Movies Info {sheetname} was successfully saved as csv file')
    return movie_details


def read_logs(filename='log.log', delimiter=' - '):
    with open(filename, 'r') as f:
        logs = f.readlines()
        log_list = []
        for log in logs:
            log_split = log.split(delimiter)
            log_list.append(log_split)
    return log_list
       
def convert_log_file(filename='log.csv', log_filename='log.log', line_count=0):
    with open(filename, 'w') as f:
        log_list = read_logs(log_filename)
        log_writer = csv.writer(f, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        if line_count==0:
            log_writer.writerow(['timestamp','severity_level','message'])
            line_count += 1
        for log in log_list:
            log_writer.writerow(log)
