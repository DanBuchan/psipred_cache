import pprint
import re

header = ""
seq = ""
with open('/Users/dbuchan/Code/psipred_cache/get_proteomes/'
          'cache_proteomes.fasta') as infile:
    for line in infile:
        line = line.strip()
        if line.startswith(">"):
            print(header)
            print(seq)
            seq = ""
            header = line
        else:
            seq += line

print(header)
print(seq)
