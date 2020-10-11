#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os
import re
import unidecode


#
# cette fonction extrait l'information d'un fichier
#
def fileToData(filepath):

  data = {}
  if os.path.isfile(filepath):
    
    # read all lines in f
    with open(filepath, 'r') as f:
      content = f.readlines()
      
    nameEN = ""
    nameFR = ""
    descrEN = ""
    descrFR = ""
    status = ""
    isDescEN = False  
    isDescFR = False  
    
    match = re.search('(\w{16})\.htm', filepath)
    if not match:
      print("Invalid filename %s" % filepath)
      exit(1)
    data['id'] = match.group(1)  
    
    for line in content:
      if line.startswith("Name:"):
        data['nameEN'] = line[5:].strip()
      elif line.startswith("Nom:"):
        data['nameFR'] = line[4:].strip()
      elif line.startswith("État:"):
        data['status'] = line[5:].strip()
      elif line.startswith("État d'origine:"):
        data['oldstatus'] = line[15:].strip()
      elif line.startswith("------ Description (en) ------"):
        isDescEN = True
        isDescFR = False
        continue
      elif line.startswith("------ Description (fr) ------"):
        isDescFR = True
        isDescEN = False
        continue
      
      if isDescEN:
        descrEN += line
      elif isDescFR:
        descrFR += line
      
      
    data['descrEN'] = descrEN.strip()
    data['descrFR'] = descrFR.strip()
    
  else:
    print("Invalid path: %s" % filepath)
    exit(1)
  
  if not 'nameEN' in data or not 'descrEN' in data:
    print("Invalid data: %s" % filepath)
    exit(1)
  
  return data


#
# retourne vrai si l'entrée est valide
#
def isValid(data):
  return data['nameFR'] and len(data['nameFR']) > 0

    
#
# génère un nom de fichier valide à partir d'un nom
#
def getFilename(name):
  name = unidecode.unidecode(name).replace(" ", "-").lower()
  name = re.sub('[^0-9a-zA-Z\\-]+', '', name)
  return name


#
# cette fonction extrait l'information d'un fichier
#
def dataToFile(data, filepath):
  
  with open(filepath, 'w') as df:
    df.write("# %s\n\n" % data['nameFR'])
    df.write(data['descrFR'])
    
  return data
