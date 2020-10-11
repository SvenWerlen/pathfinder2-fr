#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os
import icu
import shutil

from libdata import *

DEST="../docs/feats/"
DATA="../../../foundry/foundryvtt-pathfinder2-fr/data/"

# delete (cleanup)
if os.path.exists(DEST):
  shutil.rmtree(DEST)
os.makedirs(DEST)


dirpath= "%s/feats" % (DATA)

files = [f for f in os.listdir(dirpath) if os.path.isfile(os.path.join(dirpath, f))]
files = sorted(files, key=str.casefold)

list = []
for f in files:
  data = fileToData(os.path.join(dirpath,f))
  if isValid(data):
    list.append(data)

collator = icu.Collator.createInstance(icu.Locale('fr_FR.UTF-8'))
list = sorted(list, key=lambda x: collator.getSortKey(x['nameFR']))


#
# Génération de la liste de dons
#

content = "# Dons de PF2\n\n"

for f in list:
  filename = getFilename(f['nameFR'])
  content += " * [%s](%s.md)\n" % (f['nameFR'], filename)
  dataToFile(f, "%s%s.md" % (DEST, filename))

with open("%slist.md" % DEST, 'w') as df:
  df.write(content)
