import requests
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import csv

def api(api_url):
    response = requests.get(url= api_url)

    result = response.json()
    records = result.get('records', [])
    
    return records

def main():

    Co2url = 'https://api.energidataservice.dk/dataset/CO2Emis?start=2017-01-03T00:00&limit=0&filter={%22PriceArea%22:[%22DK1%22]}'
    Coalurl = 'https://api.energidataservice.dk/dataset/ElectricityBalanceNonv?start=2017-01-02T00:00&limit=0&filter={%22PriceArea%22:[%22DK1%22]}'

    x_date = []
    x_num = 0
    x = []
    Co2_y = []
    El_y = []

    Co2 = api(Co2url)
    Coal = api(Coalurl)

    with open("Co2.csv", 'w', encoding='utf-8') as csv_file:
        csv_writer = csv.DictWriter(csv_file, fieldnames=Co2[0].keys(), quotechar="'")
        csv_writer.writerows(Co2)

    with open("El.csv", 'w', encoding='utf-8') as csv_file:
        csv_writer = csv.DictWriter(csv_file, fieldnames=Coal[0].keys(), quotechar="'") # assuming that all features has the same
        csv_writer.writerows(Coal)        

    for record in Co2:
        if '07:00:00' in record['Minutes5DK']:
            x_num += 1
            test = record['Minutes5DK'].split('T')
            test = " ".join(test)
            x_date.append(test)
            x.append(test)
            Co2_y.append(record['CO2Emission'])

    for record in Coal:
        if '07:00' in record['HourDK']:
            El_y.append(record['FossilHardCoal'])

    fig, ax = plt.subplots(1, 2, figsize=(12, 6))

    x = np.asarray(x, dtype='datetime64[s]')

    ax[0].set_title('Co2 Emesions')
    ax[0].plot(x, Co2_y, label="Line1")

    ax[1].set_title('Coal Bunred')
    ax[1].plot(x, El_y, label="Line 2")

    plt.show()

if __name__ == '__main__':
    main()
