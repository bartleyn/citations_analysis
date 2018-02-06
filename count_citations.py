import xml.etree.cElementTree as ET
import pandas as pd
import datetime
import sys
import csv

#tree = ET.ElementTree(file=sys.argv[1])
with open(sys.argv[1], 'r') as fp:
    
    tree = ET.fromstring(fp.read())


citing_dict = {}

with open('aps_2010_citing_cited.csv', 'r') as fp:
    csv_reader = csv.reader(fp)
    for row in csv_reader:
        try:
            citing_dict[row[0]] += [row[1]]
        except:
            citing_dict[row[0]] = [row[1]]






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
    
    citing_year_dict[article.attrib['doi']] = pubdate
    ctr += 1
print("total number of articles: {}".format(ctr))

with open('output/new_citing_cited.csv', 'a') as fp:
    csv_writer = csv.writer(fp)
    csv_writer.writerow(['Year', 'CitingDOI', 'CitedDOI'])
    for key in sorted(citing_dict.keys()):
        try: # Citing_dict is bound to be bigger than the citing_year_dict of this current journal
            for cited_doc in citing_dict[key]:
                csv_writer.writerow([citing_year_dict[key], key, cited_doc])
        except:
            pass
#for key in sorted(year_count_dict.keys()):
#    print("{}:\tunique authors - {}\tnum articles - {}\tnum coauthors - {}".format(key, year_count_dict[key], articles_per_year[key], co_author_dict[key]))
