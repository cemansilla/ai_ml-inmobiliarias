import json
import os
from pathlib import Path
import yaml
import configparser
import re

def modify_url_string(url, pattern_string, uri_pattern, uri_separator, value):
  """
  Modifica la URL de navegación para agregar filtros o paginado

  Parameters:
  url (string)
  pattern_string (string): expresión regular
  uri_pattern (string): porcion variable en el string
  uri_separator (string)
  value (mixed)
  """
  pattern = re.compile(pattern_string)
  _re = pattern.findall(url)
  if(_re):
    url = pattern.sub(uri_pattern + uri_separator + str(value), url)
  else:
    position = url.find('.html')
    url = url[:position] + uri_separator + uri_pattern + uri_separator + str(value) + url[position:]

  return url

def get_sites_config():
  """
  Obtiene la info de configuración de sitios

  Returns:
  array
  """
  data = []

  file_path = os.sep.join(__file__.split(os.sep)[:-1]) + os.sep + 'config' + os.sep

  with open(file_path + 'sites.yaml') as f:    
    data = yaml.load(f, Loader=yaml.FullLoader)

  return data

def get_global_config_by_section(key):
  """
  Obtiene data de configuración de una sección dada en el archivo config/config.ini

  Parameters:
  key (string): Nombre de la sección dentro del archivo

  Returns:
  dict: data
  """
  data = dict()

  config = configparser.ConfigParser()
  config.read('config/config.ini')

  if(config.has_section(key)):
    for name, value in config.items(key):
      data.update({name:value})

  return data

def clean_text_string(text):
  """
  Elimina saltos de línea y tabulaciones en strings

  Parameters:
  text (string): Texto a limpiar

  Returns:
  String
  """
  return text.replace('\n', '').replace('\t', '')

def d(data):
  """
  Impresión de dump formateado

  Parameters:
  data (object|array): Elemento a imprimir

  Returns:
  void
  """
  print(json.dumps(data, indent=2))