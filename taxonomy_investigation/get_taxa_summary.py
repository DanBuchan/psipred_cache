import os
import requests
import csv
import sys

# 1. Get the proteom ID by making a proteomes query.
# http://www.uniprot.org/proteomes/?query=taxonomy:9606&format=tab
# parse this for the protein counts and Proteome ID

uri = "http://www.uniprot.org/proteomes/?format=tab&query=taxonomy:"
genomes = ""
gene_total = 0
print("Genus\tSpecies\tProteomeID\tDescription\ttaxaID\tReleaseDate\tProteinCount")
with open('/cs/research/bioinf/home1/green/dbuchan/'
          'Projects/psipred_cache/oma-species.txt', newline='') as csvfile:
    genomes = csv.reader(csvfile, delimiter=',', quotechar='"')
    for row in genomes:
        try:
            url = uri+row[1]
            r = requests.post(url)
            proteome_data = r.text.splitlines()
            details = proteome_data[1].split("\t")
            gene_total += int(details[4])
            print(row[2]+"\t"+row[3]+"\t"+proteome_data[1])
        except:
            print(row[0]+","+row[1]+","+row[2]+","+row[3], file=sys.stderr)

print(gene_total, file=sys.stderr)
