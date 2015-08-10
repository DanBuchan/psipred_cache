import collections
import pprint
import hashlib

pp = pprint.PrettyPrinter(indent=2)
m = hashlib.md5()

counts = {}
with open('/Users/dbuchan/Projects/query_hashes.txt') as infile:
    counts = collections.Counter(l.strip() for l in infile)
    # pp.pprint(counts)

current_header = ''
seq = ''
final = {}
i = 0
with open('/Users/dbuchan/Projects/uniref100.fasta') as infile:
    for l in infile:
        l = l.strip()
        if l.startswith(">"):
            # print(current_header)
            #print(seq)
            seq_hash = m.update(seq.encode('utf-8'))
            if seq_hash in counts:
                final[seq_hash] = current_header
            seq = ''
            current_header = l
            # i += 1
            # if i == 3:
            #     break
        else:
            seq += l

for key in final:
    print(final[key])
