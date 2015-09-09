import pprint
import re

header = ""
seq = ""
i = 0
with open('/cs/research/bioinf/home1/green/dbuchan/Code/psipred_cache/get_proteomes/proteomes_greater_than_ten_percent.fasta') as infile:
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

# 22279.out
