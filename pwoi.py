import csv

# Creating s function called get_data to extract data from the given csv file
def get_data(csv_file):
    '''This function extracts the data from the given csv file'''

    # Creating a List named records so that it stores all the records
    records=[]

    # Opening the CSV file and reading it
    with open(csv_file,'r') as f:
        reader=csv.reader(f)

        for record in reader:
            records.append(record)
        f.close()
        
    return records
