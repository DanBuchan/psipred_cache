import requests
import csv
import pprint
import sys

pp = pprint.PrettyPrinter(indent=2)

taxa_query_uri = "http://www.uniprot.org/proteomes/?sort=&desc=&compress=no&"+\
                 "fil=&force=no&preview=true&format=list&" + \
                 "query=redundant:no organism:"

HIV_query_uri = "http://www.uniprot.org/proteomes/?sort=&desc=&compress=no&"+\
                 "fil=&force=no&preview=true&format=list&" + \
                 "query=redundant:no taxonomy:"


proteome_uri = "http://www.uniprot.org/uniprot/?" + \
               "force=no&include=true&format=fasta&" + \
               "query=proteome:"

with open('/Users/dbuchan/Code/psipred_cache/hash_submission_lookup/'
          'common_organisms.csv') as infile:
    strings = csv.reader(infile, delimiter=',', quotechar='"')
    next(strings)
    for row in strings:
        if float(row[10]) > 0.05:
            taxa_url = ''
            if row[0] == "11676":
                taxa_url = HIV_query_uri+row[0]
            else:
                taxa_url = taxa_query_uri+row[0]
            print("Getting: " + taxa_url, file=sys.stderr)
            try:
                r = requests.post(taxa_url)
                ids = r.text.strip()
                proteome_ids = ids.split("\n")
                for p_id in proteome_ids:
                    proteome_url = proteome_uri+p_id
                    print(proteome_url, file=sys.stderr)
                    try:
                        p = requests.post(proteome_url)
                        print(p.text)
                    except:
                        print("FAILED: "+proteome_url, file=sys.stderr)
            except:
                print("FAILED: "+taxa_url, file=sys.stderr)
