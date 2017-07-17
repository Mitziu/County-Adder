import numpy as np
import pandas as pd
import argparse

# Creates new CSV file
def create_csv_file(input_file, output_file, county_dict):
    df = pd.read_csv(input_file)
    df = df.replace(np.nan, '', regex=True)
    ctr = 0

    new_csv_file = open(output_file, 'w')


    for column in df.columns.tolist():
        new_csv_file.write(column + ',')

    new_csv_file.write('US Counties' + '\n')

    for index, row in df.iterrows():
        zip_code = str(row['Zip Code'])
        if '-' in zip_code:
            zip_code = zip_code.split('-')[0]

        county = ''

        try:
            county = county_dict[zip_code]['state'] + '-' + county_dict[zip_code]['county']
            print zip_code, county
        except:
            county = ''
            print zip_code, county

        for column in df.columns.tolist():
            line = str(row[column])

            if ',' in line:
                new_csv_file.write('"' + str(row[column]) + '"' + ',')
            else:
                new_csv_file.write(str(row[column]) + ',')

        new_csv_file.write(county + '\n')

        ctr += 1

    print ctr
    print df.columns.tolist()

# Reads in County CSV file
def read_county_csv_file(county_csv_file):

    county_dict = {}

    with open(county_csv_file) as csv_file:
        for line in csv_file.readlines()[1:]:
            zip_code, city, _, state, county, _, _, _ = line.split(',')
            county_dict[zip_code] = {}
            county_dict[zip_code]['city'] = city
            county_dict[zip_code]['state'] = state
            county_dict[zip_code]['county'] = county

    return county_dict

# Parse arguments
def parse_args():
    parser = argparse.ArgumentParser(description='Creates CSV file identical to original one with US County')
    parser.add_argument('--input_file', dest='input_file', help='Original CSV file',
                        default='./Sky_Factory_import.csv')
    parser.add_argument('--output_file', dest='output_file', help='Output CSV file',
                        default='./Sky_Factory_import_with_County.csv')

    return parser.parse_args()

def main():
    args = parse_args()
    csv_dict = read_county_csv_file('Counties.csv')
    create_csv_file(args.input_file, args.output_file, csv_dict)

if __name__ == '__main__':
    main()