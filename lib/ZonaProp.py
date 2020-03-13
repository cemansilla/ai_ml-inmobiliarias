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
      'tipo_operacion',
      'ubicacion',
      'tipo_vivienda'
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
      'fecha_publicacion'
    ]
  })

  # Initializer / Instance Attributes
  def __init__(self, config):
    super().__init__(config)

    # Cargo archivo de configuración de sitios
    self.config_sites = get_sites_config()

  """
  def proccessFiltersParameters(self, filters, key):
    # https://www.zonaprop.com.ar/departamentos-alquiler-caballito-mas-de-2-banos-3-habitaciones-2-ambientes-mas-de-1-garage-10-35-m2-cubiertos-publicado-hace-menos-de-1-semana-100-10000-pesos-100-500-expensas.html
    #[base_url]-[tipo_operacion]-[zona]-[banos]-[habitaciones]-[ambientes]-[garage]-[mts]-[fecha_publicacion]-[precio]-[expensas]

    pattern_string = self.__filters_map[key]
    uri_pattern = filters[key]
    uri_separator = '-'
    value = filters[key]

    return dict({
      'pattern_string': pattern_string,
      'uri_pattern': uri_pattern, 
      'uri_separator': uri_separator,
      'value': value
    })
  """

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
    _base_url =  self.base_url
    _tipo_operacion =  ''
    _zona =  ''
    _banos =  ''
    _habitaciones =  ''
    _ambientes =  ''
    _garage =  ''
    _mts =  ''
    _fecha_publicacion =  ''
    _precio =  ''
    _expensas =  ''
    # ./Inicializo variables

    for key in filters:
      if key in self.__filters_values_map['single']:
        tmp_uri.append(filters[key])
      else:        
        if key == 'orden':
          tmp_uri.append(filters[key]['criterio'] + '-' + filters[key]['sentido'])
        elif key == 'precio':
          pass
        elif key == 'expensas':
          pass
        elif key == 'ambientes':
          pass      
        elif key == 'dormitorios':
          pass
        elif key == 'superficie':
          pass
        elif key == 'fecha_publicacion':
          pass

      print('filter', key, filters[key])

    url_template = '{base_url}{tipo_operacion}{zona}{banos}{habitaciones}{ambientes}{garage}{mts}{fecha_publicacion}{precio}{expensas}'.format(
      base_url = _base_url,
      tipo_operacion = _tipo_operacion,
      zona = _zona,
      banos = _banos,
      habitaciones = _habitaciones,
      ambientes = _ambientes,
      garage = _garage,
      mts = _mts,
      fecha_publicacion = _fecha_publicacion,
      precio = _precio,
      expensas = _expensas
    )
    print('url_template', url_template)

    """
    print('tmp_url', tmp_url) 
    print('tmp_uri', tmp_uri)
    parameters = '-'.join(tmp_uri) if tmp_uri else ''
    if(parameters):
      tmp_url += '/' + parameters + '.html'
    
    print('tmp_url despues', tmp_url)
    """
    
    """
    for key in filters:
      if(key in self.__filters_map):
        params_dict = self.proccessFiltersParameters(filters, key)
        print('params_dict', params_dict)

        url = modify_url_string(url, params_dict['pattern_string'], params_dict['uri_pattern'], params_dict['uri_separator'], params_dict['value'])

    #print('self.url', self.url)
    print('url procesada', url)
    """

    sys.exit()
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