from .MongoDBClient import MongoDBClient
from .Scraping import Scraping
from bs4 import BeautifulSoup
from urllib import parse
import requests
from Helper import *
import pandas as pd
import re

import sys

class ZonaProp(Scraping):
  __filters_values_map = dict({
    'single': [ # Valor que se usa directamente
      'tipo_vivienda',
      'tipo_operacion',
      'ubicacion',
      'fecha_publicacion'
    ],
    'key_value': [ # Par clave / valor que se usa directamente
      'orden'
    ],
    'min_max': [ # Valores mínimos / máximos
      'precio',
      'expensas',
      'superficie'
    ],
    'quantity': [ # Cantidades
      'ambientes',
      'dormitorios'
    ],
    'proccess': [ # Procesados de formas particulares
      #'fecha_publicacion' # De momento lo pongo como valor fijo
    ]
  })

  # Initializer / Instance Attributes
  def __init__(self, config):
    super().__init__(config)

    # Cargo archivo de configuración de sitios
    self.config_sites = get_sites_config()

  def getInfoList(self, limit_pages = 3, filters = dict()):
    """Obtiene la estructura HTML de los items en el listado

    Returns:
    array: Listado
    """
    current_page = 1    
    a_info = []

    ### Procesamiento de filtros
    # Temporal para no afectar en desarrollo a self.url
    tmp_url = self.base_url
    tmp_uri = []

    # Inicializo variables
    filters_dict = dict({
      'tipo_vivienda': 'departamentos',
      'tipo_operacion': '',
      'ubicacion': '',
      'banos': '',
      'dormitorios': '',
      'ambientes': '',
      'garage': '',
      'superficie': '',
      'fecha_publicacion': '',
      'precio': '',
      'expensas': '',
      'orden': ''
    })
    # ./Inicializo variables    

    for key in filters:
      if key in self.__filters_values_map['single']:
        filters_dict[key] = '-' + filters[key]
      elif key in self.__filters_values_map['min_max']:
        _min_max = ''
        if filters[key]['minimo'] and filters[key]['maximo']:
          _min_max = str(filters[key]['minimo']) + '-' + str(filters[key]['maximo']) + '-' + filters[key]['unidad']
        else:
          if filters[key]['minimo']:
            _min_max = 'mas-' + str(filters[key]['minimo']) + '-' + str(filters[key]['unidad'])
          elif filters[key]['maximo']:
            _min_max = 'menos-' + str(filters[key]['maximo']) + '-' + str(filters[key]['unidad'])

        filters_dict[key] = '-' + _min_max if _min_max else ''
      elif key in self.__filters_values_map['quantity']:
        _quantity = ''
        _slug_start = 'mas-de-' if(filters[key]['cantidad'] >= filters[key]['tope']) else ''
        _slug_end = filters[key]['slug_plural'] if filters[key]['cantidad'] > 1 else filters[key]['slug_singular']
        
        _quantity = _slug_start + str(filters[key]['cantidad']) + '-' + _slug_end

        filters_dict[key] = '-' + _quantity if _quantity else ''
      else:        
        if key == 'orden':
          filters_dict['orden'] = '-' + filters[key]['criterio'] + '-' + filters[key]['sentido']

    url_template = '{tipo_vivienda}{tipo_operacion}{ubicacion}{banos}{dormitorios}{ambientes}{garage}{superficie}{fecha_publicacion}{precio}{expensas}{orden}.html'.format_map(filters_dict)
    url_template = url_template[1:] if url_template[0] == '-' else url_template    
    self.url = '{}/{}'.format(self.base_url, url_template)
    ### ./Procesamiento de filtros

    while True:
      # Modifico URL dependiendo de página actual
      if(current_page > 1):
        self.url = modify_url_string(self.url, 'pagina-\d', 'pagina', '-', current_page)

      # Obtengo contenido de la página actual
      page_response = requests.get(self.url, timeout=5)
      self.page_content = BeautifulSoup(page_response.content, 'html.parser')
      property_html = self.page_content.find_all('div', {'class': ['posting-card', 'super-highlighted']})
    
      for item in property_html:
        a_info.append(self.extractData(item))

      current_page += 1
      if(current_page > limit_pages):
        break

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

    #Latitud / Longitud
    child_page_content = child_page_html_content.find('img', {'id': 'static-map'})
    _lat_lng = child_page_content['src'] if child_page_content and child_page_content.has_attr('src') else False
    if(_lat_lng):
      _, query_string = parse.splitquery(_lat_lng)
      query = parse.parse_qs(query_string)
      if query['center']:
        str_center = query['center'][0].split(',')
        _lat_lng = {
          'lat': str_center[0],
          'lng': str_center[1]
        }

    info = dict({
      'site_id': _id,
      'href': _href,
      'address': _address,
      'lat_lng': _lat_lng,
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
      mc.query(collection_name, filters, order)

      if(mc.num_rows() > 0):
        documents = mc.get_rows()
    
    return documents