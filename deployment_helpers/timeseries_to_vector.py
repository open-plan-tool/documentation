import csv
import json

timeseries_vector = list()

with open('inputs/time_series/pv_solar_input.csv') as csv_file:
    csv_data = csv.reader(csv_file, delimiter='\n')
    csv_header = next(csv_data)  # skip header

    [timeseries_vector.append(float(row[0])) for row in csv_data]


with open('inputs/time_series/data2json.json', 'w') as json_file:
    json.dump(timeseries_vector, json_file)
# or just 
print(timeseries_vector)
