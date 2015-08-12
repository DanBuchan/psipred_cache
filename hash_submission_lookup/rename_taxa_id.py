import requests
import csv
import xmltodict
import pprint
pp = pprint.PrettyPrinter(indent=2)
uri = "http://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=taxonomy&id="
# phylo_levels = ('superkingdom', 'phylum', 'class',
#                 'subclass', 'order', 'family', 'genus', 'species')
phylo_levels = ('superkingdom',)

with open('taxa_id_counts.csv') as infile:
    strings = csv.reader(infile, delimiter=',', quotechar='"')
    for row in strings:
        try:
            url = uri + row[0]
            r = requests.post(url)
            data = xmltodict.parse(r.text)
            #pp.pprint(data)

            superkingdom = ''
            phylogeny_array = data["TaxaSet"]["Taxon"]["LineageEx"]['Taxon']
            for level in phylo_levels:
                name = "-"
                #pp.pprint(level)
                for rank in phylogeny_array:
                    if rank['Rank'] == level:
                        name = rank['ScientificName']
                superkingdom = name+","

            scientific_name = data["TaxaSet"]["Taxon"]["ScientificName"]
            superkingdom += scientific_name+","+row[0]+","+row[1]
            print(superkingdom)
        except:
            print("Nope" + row[0])
