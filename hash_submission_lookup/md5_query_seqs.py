import pprint
import csv
import hashlib


class MyFilter:
    def __init__(self, instr, errstr):
        self.instr = instr
        self.errstr = errstr

    def __enter__(self):
        # print("ENTERING filter")
        return self

    def __exit__(self, a, b, c):
        # print("EXITING filter")
        self.instr.close()
        self.errstr.close()
        return False

    def __next__(self):
        line = next(self.instr)
        while True:
            try:
                t = line.decode('utf8')
                return t.strip()
            except UnicodeDecodeError:
                self.errstr.write(line)
                line = next(self.instr)
        return line

    def __iter__(self):
        return self

    def next(self):
        return self.__next__()

pp = pprint.PrettyPrinter(indent=1)
m = hashlib.md5()
test_seq = 'MLELLPTAVEGVSQAQITGRPEWIWLALGTALMGLGTLYFLVKGMGVSDPDAKKFYAITT' + \
           'LVPAIAFTMYLSMLLGYGLTMVPFGGEQNPIYWARYADWLFTTPLLLLDLALLVDADQGT' + \
           'ILALVGADGIMIGTGLVGALTKVYSYRFVWWAISTAAMLYILYVLFFGFTSKAESMRPEV' + \
           'ASTFKVLRNVTVVLWSAYPVVWLIGSEGAGIVPLNIETLLFMVLDVSAKVGFGLILLRSR' + \
           'AIFGEAEAPEPSAGDGAAATSD'
test_hash = m.update(test_seq.encode('utf-8'))

with open('/cs/research/bioinf/home1/green/dbuchan/Projects/psipred_cache/'
          'hash_submission_lookup/string.csv', 'rb') as istream, \
            open("err.txt", 'wb') as err, MyFilter(istream, err) as fd:
    strings = csv.reader(fd, delimiter='\t', quotechar='"')
    for row in strings:
        try:
            seq = "".join(row[2].split())
            m.update(seq.encode('utf-8'))
            if m.hexdigest != test_hash:
                print(m.hexdigest())
        except:
            pass
