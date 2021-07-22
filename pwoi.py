import csv
from os import path,listdir
import requests
import datetime

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

def create_date_range(from_,to_=datetime.date.today()):
    '''Creates a Date Range'''

    date_range=[]
    year,month,day=from_
    from_date=datetime.date(year,month,day)
    no_of_days=to_-from_date

    for days in range(no_of_days.days):
        date=from_date+datetime.timedelta(days)

        if date.isoweekday()!=6 and date.isoweekday()!=7:
            formated_date=date.strftime('%d%m%Y')
            date_range.append(formated_date)

    return date_range 


def download_fao_file(date):
    '''Downloads the F&O file from nseindia
    :param date DDMMYYYY'''

    # Downloading the Data File from the web
    print("Downloading Data...")
    url="https://www1.nseindia.com/content/nsccl/fao_participant_oi_{}.csv".format(date)
    web_content=requests.get(url,allow_redirects=True)
    file_data=web_content.content.decode()
    records=[]

    filename=url.split('/')[-1]

    # Saving the file with the web data
    with open(filename,'a',newline='') as f:
        f.write(file_data)
        f.close()
    

    with open(filename,'r') as f:
        reader=csv.reader(f)
        for row in reader:
            records.append(row)
        f.close()

    print("Writing the Data...")
    with open(filename,'w',newline='') as f:
        writer=csv.writer(f)
        for index in range(1,len(records)):
            writer.writerow(records[index])
        f.close()
        

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
    dates=create_date_range((2020,1,1))
    for date in dates:
        print('Processing Data for {}'.format(date))
        download_fao_file(date)
    for file in listdir():
        try:
            if file.endswith(".csv"):
                write_data(file,'test.csv')
        except Exception:
            continue