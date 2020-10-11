#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os
import icu
import shutil
import json

from libdata import *

DEST="../docs/feats/"
DATA="../../../foundry/foundryvtt-pathfinder2-fr/data/"
SOURCE="../../../../.local/share/FoundryVTT/Data/systems/pf2e/packs/"

# delete (cleanup)
if os.path.exists(DEST):
  shutil.rmtree(DEST)
os.makedirs(DEST)


dirpath= "%s/feats" % (DATA)


#
# Lecture des données source (anglophone)
#
source = readCompendium(SOURCE + "feats.db")

#
# Lecture de tous les fichiers de dons
#

files = [f for f in os.listdir(dirpath) if os.path.isfile(os.path.join(dirpath, f))]
files = sorted(files, key=str.casefold)

list = []
for f in files:
  data = fileToData(os.path.join(dirpath,f))
  if isValid(data):
    if data['id'] in source:
      # add metadata
      data['metadata'] = []
      data['metadata'].append( { 'title': "Nom d'origine", 'value': data['nameEN'] } )
      data['metadata'].append( { 'title': "Niveau", 'value': int(getValue(source[data['id']], "data.level.value", False, "01")) } )
      list.append(data)
    else:
      print("Not found: %s" % data['id'])
      continue

collator = icu.Collator.createInstance(icu.Locale('fr_FR.UTF-8'))
list = sorted(list, key=lambda x: collator.getSortKey(x['nameFR']))


#
# Génération de la liste de dons pour le site
#

content = "# Dons de PF2\n\n"

for f in list:
  filename = getFilename(f['nameFR'])
  content += " * [%s](%s.md)\n" % (f['nameFR'], filename)
  dataToFile(f, "%s%s.md" % (DEST, filename))

with open("%slist.md" % DEST, 'w') as df:
  df.write(content)
