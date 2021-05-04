import csv

# Creating s function called get_data to extract data from the given csv file
def get_data(csv_file):
    '''This function extracts the data from the given csv file'''

    datestring=csv_file.split('.')[0]
    # Creating a List named records to store all the dictionaries
    records=[]

    # Opening the CSV file and reading it
    with open(csv_file,'r') as f:
        reader=csv.DictReader(f)

        for record in reader:
            dict_record={}
            dict_record['Date']='{}-{}-{}'.format(datestring[53:55],datestring[55:57],datestring[57:])
            for key,value in record.items():
                dict_record[key]=value
            records.append(dict_record)
        
        f.close()
    return records

def write_data(file_to_read,file_to_write=''):
    '''Writes the data into csv files'''

    # Extracting the data to write
    data=get_data(file_to_read)

    # Getting the keys from the first record and storing it in field_names variable
    field_names=[]

    for i in range(1):
        keys=data[i].keys()

    for key in keys:
        field_names.append(key)
    
    with open(file_to_write,'a',newline='') as f:
        writer=csv.DictWriter(f,fieldnames=field_names)
        writer.writeheader()
        writer.writerows(data)
        f.close()
    print('File Written')


