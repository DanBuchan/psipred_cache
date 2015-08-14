import pprint
import re

header = ""
seq = ""
i = 0
with open('/Users/dbuchan/Code/psipred_cache/get_proteomes/'
          'cache_proteomes.fasta') as infile:
    for line in infile:
        line = line.strip()
        if line.startswith(">"):
            if i > 0:
                print(header)
                print(seq)
            seq = ""
            header = line
            i += 1
        else:
            seq += line

print(header)
print(seq)
