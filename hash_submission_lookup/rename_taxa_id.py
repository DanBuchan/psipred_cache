import requests
import csv
import xmltodict
import pprint
pp = pprint.PrettyPrinter(indent=2)
uri = "http://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=taxonomy&id="
# phylo_levels = ('superkingdom', 'phylum', 'class',
#                 'subclass', 'order', 'family', 'genus', 'species')
phylo_levels = ('genus', 'species')

with open('test.csv') as infile:
    strings = csv.reader(infile, delimiter=',', quotechar='"')
    for row in strings:
        try:
            url = uri + row[0]
            r = requests.post(url)
            data = xmltodict.parse(r.text)
            # pp.pprint(data)
            scientific_name = data["TaxaSet"]["Taxon"]["ScientificName"]
            scientific_name += ","+row[0]+","+row[1]
            print(scientific_name)
        except:
            print("Nope" + row[0])
