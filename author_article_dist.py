import csv

name_dict = {}
with open('/nfs/topaz/nbartley/data/aps-dataset-metadata-2010/author_ctr.csv', 'r') as fp:
    csv_reader = csv.reader(fp)

    fp.readline()
    for row in csv_reader:
        try:
            name_dict[row[0]] += int(row[1])
        except:
            name_dict[row[0]] = int(row[1])


with open('/nfs/topaz/nbartley/data/aps-dataset-metadata-2010/unique_author_ctr.csv', 'w') as fp:

    csv_writer = csv.writer(fp)
    csv_writer.writerow(['Name', 'Count'])
    for key in name_dict:
        csv_writer.writerow([key, name_dict[key]])




