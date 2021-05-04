import csv

# Creating s function called get_data to extract data from the given csv file
def get_data(csv_file):
    '''This function extracts the data from the given csv file'''

    records=[]

    with open(csv_file,'r') as f:
        data=csv.DictReader(f)
        records.append(['Date', 'Open', 'High', 'Low', 'Close'])

        for element in data:
            records.append([element['Date'].strip(),element['Open'].strip(),element['High'].strip(),element['Low'].strip(),element['Close'].strip()])
        
        f.close()
    
    return records
