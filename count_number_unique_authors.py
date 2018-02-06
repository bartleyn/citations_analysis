import xml.etree.cElementTree as ET
import pandas as pd
import datetime
import sys
import csv

#tree = ET.ElementTree(file=sys.argv[1])
with open(sys.argv[1], 'r') as fp:
    
    tree = ET.fromstring(fp.read())


#datetime.datetime.strptime(string_date, "%Y-%m-%d %H:%M:%S.%f")

#for elem in tree.iterfind('branch/sub-branch')

year_count_dict = {}
articles_per_year = {}
author_name_dict = {}
co_author_dict = {}
cur_pubdate = 0
ctr = 0
co_author_tracker = {}


for article in tree.iterfind('article'):
    pubdate = None
    for issue in article.iterfind('issue'):
        try:
            pubdate = int(datetime.datetime.strptime(issue.attrib["printdate"], '%Y-%m-%d').year)
        except:
            pubdate = int(issue.attrib["printdate"][:4])
    if pubdate is None:
        print(article)  
        continue
    if pubdate not in year_count_dict:
        year_count_dict[pubdate] = 0
        co_author_dict[pubdate] = 0
        co_author_tracker[pubdate] = {}
    if pubdate > cur_pubdate:
        cur_pubdate = pubdate
        author_name_dict = {}
    
    for authgrp in article.iterfind('authgrp'):
        author_names = [] 
        for author in authgrp.iterfind('author'):
            co_author_dict[pubdate] += 1
            author_name = "_".join([elem.text.lower().strip(' .,') for elem in author.iter() if elem.text])
            if author_name not in author_name_dict:
                author_name_dict[author_name] = ""
                year_count_dict[pubdate] += 1
            author_names += author_name
        #for author_name in author_names:
            #co_author_tracker[author_name] = [other_name for other_name in author_names if not other_name == author_name and not author_name in co_author_tracker[ot
        for author_name in author_names:
            if author_name not in co_author_tracker[pubdate]:
                co_author_tracker[pubdate][author_name] = {}
            ix = author_names.index(author_name)
            for other_name in author_names[ix:]:
                if other_name == author_name:
                    continue
                co_author_tracker[pubdate][author_name][other_name] = 0
                #co_author_tracker[pubdate] += "{}-{}".format(author_name, other_name)
        co_author_dict[pubdate] -= 1

    ctr += 1
    if pubdate not in articles_per_year:
        articles_per_year[pubdate] = 1
    else:
        articles_per_year[pubdate] += 1
print("total number of articles: {}".format(ctr))

with open('output/{}.csv'.format(sys.argv[1][:-4]), 'w') as fp:
    csv_writer = csv.writer(fp)
    csv_writer.writerow(['Year', 'Num_Articles', 'Num_Unique_Authors', 'Total_Num_Co_Authors', 'Num_Unique_Co_Authors'])
    for key in sorted(year_count_dict.keys()):
        csv_writer.writerow([key, articles_per_year[key], year_count_dict[key], co_author_dict[key], sum(len(co_author_tracker[key][author_name]) for author_name in co_author_tracker[key])])
#for key in sorted(year_count_dict.keys()):
#    print("{}:\tunique authors - {}\tnum articles - {}\tnum coauthors - {}".format(key, year_count_dict[key], articles_per_year[key], co_author_dict[key]))
