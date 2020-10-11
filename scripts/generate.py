#!/usr/bin/python3
# -*- coding: utf-8 -*-

import json
import yaml
import os
import datetime

from libdata import *


DATA="../../foundry/foundryvtt-pathfinder2-fr/data/"

dirpath= "%s/feats" % (DATA)

content = "# Dons de PF2\n\n"

files = [f for f in os.listdir(dirpath) if os.path.isfile(os.path.join(dirpath, f))]
files = sorted(files, key=str.casefold)

for f in files:
  data = fileToData(os.path.join(dirpath,f))
  print(data["nameFR"])
  
