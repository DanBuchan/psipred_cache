import pprint
import requests
import re

id_re = ">UniRef100_(.+?)\s"
count_re = "COUNT=(.+)"
taxa_re = "OX\s+NCBI_TaxID=(\d+)\D+"
uniprot_uri = "http://www.uniprot.org/uniprot/"  # A0A024RDF4.txt

totals = {}
i = 0
with open('hash_matches.txt') as infile:
    for l in infile:
        i++
        seq_id = ''
        count = 0
        for match in re.findall(id_re, l):
            seq_id = match
            for match2 in re.findall(count_re, l):
                count = int(match2)
                try:
                    r = requests.post(uniprot_uri+seq_id+".txt")
                except:
                    print("Missed " + seq_id)
                for match3 in re.findall(taxa_re, r.text):
                    if match3 in totals:
                        totals[match3] += match2
                    else:
                        totals[match3] = match2
        if i % 1000 == 0:
            print(str(i))

for taxa_id in totals:
    print(taxa_id+","+totals[taxa_id])
