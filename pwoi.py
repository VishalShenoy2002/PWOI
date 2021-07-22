import csv
import matplotlib.pyplot as plt
from os import path

# ==== FORMULA ==== #

# INDEX 
# ------

# Index Future Net = Future Long + Future Short
# Index Call Net = Call Long + Call Short
# Index Put Net = Put Long - Put Short

# STOCK
# ------

# Stock Future Net = Future Long + Future Short
# Stock Call Net = Call Long + Call Short
# Stock Put Net = Put Long - Put Short


# Creating s function called get_data to extract data from the given csv file

def get_data(csv_file):
    '''This function extracts the data from the given csv file'''

    datestring=path.splitext(csv_file)[0].split('_')[-1]
    # Creating a List named records to store all the dictionaries
    records=[]

    # Opening the CSV file and reading it
    with open(csv_file,'r') as f:
        reader=csv.DictReader(f)

        for record in reader:
            dict_record={}
            dict_record['Date']='{}-{}-{}'.format(datestring[0:2],datestring[2:4],datestring[4:])
            for key,value in record.items():
                dict_record[key.strip()]=value

            # Adding New Fields :  Index Future Net, Index Call Net, Index Put Net, Index Net Long

            dict_record['Index Future Net']=str(int(dict_record["Future Index Long"])-int(dict_record["Future Index Short"]))
            dict_record['Index Call Net']=str(int(dict_record["Option Index Call Long"])-int(dict_record["Option Index Call Short"]))
            dict_record['Index Put Net']=str(int(dict_record["Option Index Put Long"])-int(dict_record["Option Index Put Short"]))
            dict_record['Index Net Long']=str(int(dict_record["Index Future Net"])+int(dict_record["Index Call Net"])-int(dict_record['Index Put Net']))
            
            # Adding New Fields :  Stock Future Net, Stock Call Net, Stock Put Net, Stock Net Long

            dict_record['Stock Future Net']=str(int(dict_record["Future Stock Long"])-int(dict_record["Future Stock Short"]))
            dict_record['Stock Call Net']=str(int(dict_record["Option Stock Call Long"])-int(dict_record["Option Stock Call Short"]))
            dict_record['Stock Put Net']=str(int(dict_record["Option Stock Put Long"])-int(dict_record["Option Stock Put Short"]))
            dict_record['Stock Net Long']=str(int(dict_record["Stock Future Net"])+int(dict_record["Stock Call Net"])-int(dict_record['Stock Put Net']))
            
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
    
    if path.isfile(file_to_write)==False:
        with open(file_to_write,'a',newline='') as f:
            writer=csv.DictWriter(f,fieldnames=field_names)
            writer.writeheader()
            f.close()

    with open(file_to_write,'a',newline='') as f:
        writer=csv.DictWriter(f,fieldnames=field_names)
        writer.writerows(data)
        f.close()
        
        print('File Written')


# Starting the Main Program

if __name__=="__main__":
    data_files=['fao_participant_oi_30042021.csv','fao_participant_oi_03052021.csv']
    for file in data_files:
        print('Working on {}'.format(file))
        write_data(file,'test.csv')
        