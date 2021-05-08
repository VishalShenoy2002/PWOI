import csv
import matplotlib.pyplot as plt

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
    
    with open(file_to_write,'a',newline='') as f:
        writer=csv.DictWriter(f,fieldnames=field_names)
        writer.writeheader()
        writer.writerows(data)
        f.close()
    print('File Written')

# ======================================================= #
#            BUGY FUNCTION Below (plot_graph)             #
# ======================================================= #


def plot_graph(info_file):
    information=get_data(info_file)
    data=[]
    for record in information:
        if record['Client Type'] != 'TOTAL':
            data.append([record['Client Type'],record['Index Net Long']])
    positive_data=[value[1] for value in data if int(value[1])>0 else 0]
    negative_data=[value[1] for value in data if int(value[1])<0]
    x = range(4)
    fig = plt.figure()
    ax = plt.subplot()
    ax.bar(x, negative_data, width=1, color='r')
    ax.bar(x, positive_data, width=1, color='b')
    plt.show()
    # print(positive_data,negative_data)
# write_data(r"E:\Programs\Application\PWOI\PWOI\fao_participant_oi_30042021.csv",r'test.csv')
plot_graph(r'test.csv')