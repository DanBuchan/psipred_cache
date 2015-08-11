import collections
import pprint
import hashlib

pp = pprint.PrettyPrinter(indent=2)

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
        m = hashlib.md5()
        l = l.strip()
        if l.startswith(">"):
            # print(current_header)
            # print(seq)
            m.update(seq.encode('utf-8'))
            seq_hash = m.hexdigest()
            # print(seq_hash)
            if seq_hash in counts:
                final[seq_hash] = current_header
            seq = ''
            current_header = l
            # i += 1
            # if i == 3:
            #     break
        else:
            seq += l

m.update(seq.encode('utf-8'))
seq_hash = m.hexdigest()
if seq_hash in counts:
    final[seq_hash] = current_header

for key in final:
    print(final[key] + " COUNT=" + str(counts[key]))
