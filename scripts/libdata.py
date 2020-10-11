#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os
import re
import unidecode
import json


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
# cette fonction lit un compendium Foundry et ajoute les entrées dans un dict
#
def readCompendium(path):
  entries = {}
  with open(path, 'r') as f:
    content = f.readlines()

  for line in content:
    try:
      obj = json.loads(line)
    except:
      continue
    
    if '$$deleted' in obj:
      continue
    
    entries[obj['_id']] = obj
    
  return entries


#
# cette fonction extrait l'information d'un fichier
#
def dataToFile(data, filepath):
  
  with open(filepath, 'w') as df:
    df.write("[Revenir à la liste](..)\n\n")
    df.write("# %s\n\n" % data['nameFR'])
    
    if 'metadata' in data:
      for m in data['metadata']:
        df.write(" * **%s** : %s\n" % (m["title"], m["value"]))
      df.write("\n\n")
    
    df.write(data['descrFR'])
    
  return data

#
# cette fonction tente une extraction d'une valeur dans un objet
# Ex: data.level.value => obj["data"]["level"]["value"]
#
def getValue(obj, path, exitOnError = True, defaultValue = None):
  element = obj
  for p in path.split('.'):
    if p in element:
      element = element[p]
    elif exitOnError:
      print("Error with path %s in %s" % (path, obj))
      exit(1)
    else:
      print("Path %s not found for %s!" % (path, obj['name']))
      return defaultValue
  
  if element is None:
    return defaultValue
  elif isinstance(element, int):
    return "%02d" % element
  elif isinstance(element, list):
    if len(element) == 0:
      return defaultValue
    if len(element) > 1:
      print("List has more than 1 element for '%s'! %s" % (element, path))
      exit(1)
    return element[0]
  elif element.isdigit():
    return "%02d" % int(element)
  else:
    return element
