import os
from pathlib import Path
from abc import ABC, abstractmethod
from bs4 import BeautifulSoup
import requests

class Scraping(ABC):
  def __init__(self, config):
    self.base_url = config['base_url']
    self.url = config['base_url'] + '/' + config['list_uri']
    self.identifier = config['name']
    super().__init__()

    #Get HTML page content
    page_response = requests.get(self.url, timeout=5)
    self.page_content = BeautifulSoup(page_response.content, 'html.parser')

  @abstractmethod
  def getInfoList(self):
    """Obtiene la estructura HTML de los items en el listado

    Returns:
    array:Listado
    """
    pass

  @abstractmethod
  def extractData(self):
    """Extrae la info del item dado
    
    Returns:
    dict:Info
    """
    pass

  @abstractmethod
  def saveDataToCsv(self, data, file_name):
    """Almacena la data en un csv
    
    Parameters:
    data (array): Info a almacenar
    filename (string): Nombre de archivo

    Returns:
    void
    """
    pass

  def getDataSavePath(self):
    """Obtiene la ruta dónde se almacenarán los archivos de data
    En caso de que no existan, los crea

    Returns:
    string:path
    """
    # Ruta de almacenamiento
    file_path = os.sep.join(__file__.split(os.sep)[:-2]) + os.sep + 'data' + os.sep
    # Si no existe, la creo
    if not os.path.exists(file_path):
      os.makedirs(file_path)

    return file_path