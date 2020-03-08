from .MongoDBClient import MongoDBClient
from .Scraping import Scraping
from bs4 import BeautifulSoup
import requests
from Helper import *
import pandas as pd

class ZonaProp(Scraping):
  # Initializer / Instance Attributes
  def __init__(self, config):
    super().__init__(config)

    # Cargo archivo de configuración de sitios
    self.config_sites = get_sites_config()

  def getInfoList(self):
    """Obtiene la estructura HTML de los items en el listado

    Returns:
    array: Listado
    """
    property_html = self.page_content.find_all('div', {'class': ['posting-card', 'super-highlighted']})

    a_info = []
    for item in property_html:
      a_info.append(self.extractData(item))

    return a_info

    
  def extractData(self, item):
    """Extrae la info del item dado
    
    Parameters:
    item (object): Nodo HTML del cual extraer la data

    Returns:
    dict: Info
    """
    #ID
    _id = item.get('data-id')

    #Link
    _href = item.get('data-to-posting')

    #Título
    _title = clean_text_string(item.find('h2', {'class': ['posting-title']}).find('a').text)

    #Dirección
    _address = item.find('span', {'class': ['posting-location']})
    _address = clean_text_string(_address.text) if _address else ''

    #Características
    tmp_features = item.find('ul', {'class': ['main-features']})
    tmp_features = tmp_features.find_all('li') if tmp_features else []

    _features = []
    for _prop in tmp_features:
      _features.append(clean_text_string(_prop.text))

    #Descripción corta
    _short_description = item.find('div', {'class': ['posting-description']})
    _short_description = clean_text_string(_short_description.text) if _short_description else ''

    #Precio
    _price = item.find('span', {'class': ['first-price']})
    _price = clean_text_string(_price.text) if _price else ''

    #Expensas
    _expenses = item.find('span', {'class': ['expenses']})
    _expenses = clean_text_string(_expenses.text) if _expenses else ''

    #Data extraida desde la interna
    child_page_response = requests.get(self.base_url + _href, timeout=5)
    child_page_html_content = BeautifulSoup(child_page_response.content, 'html.parser')

    #Descripción extendida    
    child_page_content = child_page_html_content.find('div', {'class': ['description-container']})
    _description = clean_text_string(child_page_content.getText()) if child_page_content else ''

    #Fecha publicacion
    child_page_content = child_page_html_content.find('h5', {'class': ['section-date']})
    _publish_date = clean_text_string(child_page_content.getText()) if child_page_content else ''

    info = dict({
      'site_id': _id,
      'href': _href,
      'address': _address,
      'title': _title,
      'features': _features,
      'short_description': _short_description,
      'description': _description,
      'publish_date': _publish_date,
      'price': _price,
      'expenses': _expenses
    })

    return info

  def saveDataToCsv(self, data, file_name = 'zonaprop_data'):
    """Almacena la data en un csv
    
    Parameters:
    data (array): Info a almacenar
    filename (string): Nombre de archivo

    Returns:
    void
    """
    df = pd.DataFrame(data)
    df.to_csv(self.getDataSavePath() + file_name + '.csv', encoding='utf-8-sig')

  def saveDataToXlsx(self, data, file_name = 'zonaprop_data'):
    """Almacena la data en un Excel
    
    Parameters:
    data (array): Info a almacenar
    filename (string): Nombre de archivo

    Returns:
    void
    """
    df = pd.DataFrame(data)
    df.to_excel(self.getDataSavePath() + file_name + '.xlsx', sheet_name=self.identifier)

  def saveDataToMongoDB(self, collection_name, data):
    """Almacena la data en MongoDB
    
    Parameters:
    collection_name (string): Nombre de la colección
    data (array): Info a almacenar

    Returns:
    void
    """
    mc = MongoDBClient()

    if(mc.isConnected()):
      pass
    
  def getDataFromCsv(self, file_name = 'zonaprop_data'):
    """
    Lee la data desde un csv

    Parameters:
    filename (string): Nombre de archivo

    Retuns:
    mixed: Dataframe | False
    """
    try:
      return pd.read_csv(self.getDataSavePath() + file_name + '.csv')
    except:
      return False

  def getDataFromXls(self, file_name = 'zonaprop_data'):
    """
    Lee la data desde un Excel

    Parameters:
    filename (string): Nombre de archivo

    Retuns:
    mixed: Dataframe | False
    """
    try:
      return pd.read_excel(self.getDataSavePath() + file_name + '.xlsx')
    except:
      return False

  def getDataFromMongo(self, collection_name, filters = {}, order = {}):
    """
    Consulta la data de inmuebles almacenada en Mongo

    Parameters:
    collection_name (string): Nombre de la colección

    Returns:
    array
    """
    documents = []

    mc = MongoDBClient()
    
    if(mc.isConnected()):
      order = [('last_modified',1)]
      mc.query('inmuebles', filters, order)

      if(mc.num_rows() > 0):
        documents = mc.get_rows()
    
    return documents