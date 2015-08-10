import os
import requests
import csv
import sys
import xmltodict
import pprint

pp = pprint.PrettyPrinter(indent=1)
print("Superkingdom,Phylum,Class,Subclass,Order,Family,Genus,Species,"
      "ProteomeID,Description,taxaID,ReleaseDate,ProteinCount")
uri = "http://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=taxonomy&id="

phylo_levels = ('superkingdom', 'phylum', 'class',
                'subclass', 'order', 'family')
total_proteins = 0
with open('/cs/research/bioinf/home1/green/dbuchan/Projects/psipred_cache/'
          'uniprot_proteome_info_single_genus.csv', newline='') as csvfile:
    genomes = csv.reader(csvfile, delimiter=',', quotechar='"')
    next(genomes)
    for row in genomes:
        try:
            url = uri + row[4]
            # print(url)
            phylo_string = ""
            r = requests.post(url)
            data = xmltodict.parse(r.text)
            phylogeny_array = data["TaxaSet"]["Taxon"]["LineageEx"]['Taxon']

            for level in phylo_levels:
                name = "-"
                for rank in phylogeny_array:
                    if rank['Rank'] == level:
                        name = rank['ScientificName']
                phylo_string += name+","

            phylo_string += row[0]+","+row[1]+","+row[2]+","+row[3]+"," + \
                                   row[4]+","+row[5]+","+row[6]
            total_proteins += int(row[6])
            print(phylo_string)
        except:
            print(row[0]+","+row[1]+","+row[2]+","+row[3]+","+row[4]+"," +
                  row[5]+","+row[6], file=sys.stderr)

print(total_proteins, file=sys.stderr)
