import xml.etree.cElementTree as ET
import pandas as pd
import datetime
import sys
import csv
import networkx as nx


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
    
    for authgrp in article.iterfind('authgrp'):
        author_names = [] 
        for author in authgrp.iterfind('author'):

            author_name = "_".join([elem.text.lower().strip(' .,') for elem in author.iter() if elem.text])
            if author_name not in author_name_dict:
                author_name_dict[author_name] = ""
            author_names += [author_name]
        #for author_name in author_names:
            #co_author_tracker[author_name] = [other_name for other_name in author_names if not other_name == author_name and not author_name in co_author_tracker[ot
        for author_name in author_names:
            if author_name not in co_author_tracker:
                co_author_tracker[author_name] = {}
            ix = author_names.index(author_name)
            for other_name in author_names[ix:]:
                if other_name == author_name:
                    continue
                co_author_tracker[author_name][other_name] = 1
                #co_author_tracker[pubdate] += "{}-{}".format(author_name, other_name)
    ctr += 1
print("total number of articles: {}".format(ctr))
print("total number of authors: {}".format(len(co_author_tracker)))

nx_graph = nx.Graph(co_author_tracker)
nx.readwrite.adjlist.write_adjlist(nx_graph, "/nfs/topaz/nbartley/data/aps_networks/{}".format(sys.argv[1]))

#for key in sorted(year_count_dict.keys()):
#    print("{}:\tunique authors - {}\tnum articles - {}\tnum coauthors - {}".format(key, year_count_dict[key], articles_per_year[key], co_author_dict[key]))
