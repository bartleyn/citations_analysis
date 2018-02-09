import xml.etree.cElementTree as ET
import pandas as pd
import datetime
import sys
import csv

#tree = ET.ElementTree(file=sys.argv[1])
with open(sys.argv[1], 'r') as fp:
    
    tree = ET.fromstring(fp.read())


cited_dict = {}

with open('output/new_citing_cited.csv', 'r') as fp:
    csv_reader = csv.reader(fp)
    for row in csv_reader:
        try:
            # used for measuring inbound citations
            #cited_dict[row[2]] += [row[0]]
            # used for measuring outbound citations 
            cited_dict[row[1]] += [row[0]]
        except:
            # used for measuring inbound citations
            #cited_dict[row[2]] = [row[0]]
            # used for measuring outbound citations
            cited_dict[row[1]] = [row[0]]

    


#TODO: Counting external citations at every timeslice for each journal




#datetime.datetime.strptime(string_date, "%Y-%m-%d %H:%M:%S.%f")

#for elem in tree.iterfind('branch/sub-branch')

year_count_dict = {}
articles_per_year = {}
citing_year_dict = {}
cur_pubdate = 0
ctr = 0
co_author_tracker = {}


for article in tree.iterfind('article'):
    pubdate = None
    for issue in article.iterfind('issue'):
        try:
            pubdate = int(datetime.datetime.strptime(issue.attrib["printdate"], '%Y-%m-%d').year)
        except:
            try:
                pubdate = int(issue.attrib["printdate"][:4])
            except:
                pass
    if pubdate is None:
        print(article)  
        continue
    if pubdate not in year_count_dict:
        year_count_dict[pubdate] = 0
        co_author_tracker[pubdate] = {}
    if pubdate > cur_pubdate:
        cur_pubdate = pubdate
        author_name_dict = {}
    try:
        citing_year_dict[pubdate] += [article.attrib['doi']]
    except:
        citing_year_dict[pubdate] = [article.attrib['doi']]    
    #citing_year_dict[article.attrib['doi']] = pubdate
    ctr += 1
print("total number of articles: {}".format(ctr))

for year in sorted(citing_year_dict):
    count_in_year = 0
    for doi in citing_year_dict[year]:
        if doi in cited_dict:
            count_in_year += len([x for x in cited_dict[doi]])

    print(year, count_in_year)

with open('output/outgoing_citations_per_year.csv', 'a') as fp:
    csv_writer = csv.writer(fp)
    csv_writer.writerow(['Year', 'Journal', 'Count'])
    for year in sorted(citing_year_dict):
        count_in_year = 0
        for doi in citing_year_dict[year]:
            if doi in cited_dict:
                #count_in_year += len([x for x in cited_dict[doi] if int(x) == int(year)])
                # count the number of citations
                count_in_year += len([x for x in cited_dict[doi]])
        csv_writer.writerow([year, sys.argv[1][:-4], count_in_year])


