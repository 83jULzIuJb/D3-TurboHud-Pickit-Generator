"""
    OLD ORIGINAL FILE
"""

import json
from collections import OrderedDict

statlist = OrderedDict()
with open('statlist.json', 'r') as f:
     statlist = {int(k):v for k,v in json.load(f).items()}

i=1
while i < 220:
    statlist[i].pop(3)
    statlist[i].pop(0)
    print(statlist[i])
    i += 1

with open('statlist2.json', 'w') as outfile:
    json.dump(statlist, outfile, indent=2)
print('INFO | save successful')
