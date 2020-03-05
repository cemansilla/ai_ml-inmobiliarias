import json
import os
from pathlib import Path
import yaml
import configparser

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