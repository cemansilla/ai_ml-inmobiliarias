import json
import os
from pathlib import Path
import yaml

# Obtiene la info de congiguración
def get_config_info():
  data = []

  file_path = os.sep.join(__file__.split(os.sep)[:-1]) + os.sep + 'config' + os.sep

  with open(file_path + 'sites.yaml') as f:    
    data = yaml.load(f, Loader=yaml.FullLoader)

  return data

# Elimina saltos de línea y tabulaciones en strings
def clean_text_string(text):
  return text.replace('\n', '').replace('\t', '')

# Dump formateado
def d(data):
  print(json.dumps(data, indent=2))