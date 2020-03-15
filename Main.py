from lib.ZonaProp import ZonaProp
from lib.MongoDBClient import MongoDBClient
from Helper import *

# Cargo archivo de configuración de sitios
config_sites = get_sites_config()

# Procesamiento de ZonaProp
config_zonaprop = config_sites.get('zonaprop')
if(config_zonaprop):
  zonaprop = ZonaProp(config_zonaprop)
  
  """
  # Ejemplo de filtros completo
  # Se debería procesar un formulario o query params en una petición REST para armar esta estructura
  filters = dict({
    'tipo_operacion': 'venta',
    'orden': {
      'criterio': 'precio',
      'sentido': 'ascendente'
    },
    'ubicacion': 'caballito',
    'tipo_vivienda': 'locales-comerciales',
    'precio': {
      'minimo': 100,
      'maximo': 500,
      'unidad': 'pesos'
    },
    'expensas': {
      'minimo': 120,
      'maximo': 520,
      'unidad': 'expensas'
    },
    'superficie': {
      'minimo': 150,
      'maximo': 550,
      'unidad': 'm2'
    },
    'ambientes': {
      'cantidad': 1,
      'tope': 5,
      'slug_singular': 'ambiente',
      'slug_plural': 'ambientes'
    },
    'dormitorios': {
      'cantidad': 5,
      'tope': 5,
      'slug_singular': 'habitacion',
      'slug_plural': 'habitaciones'
    },
    'fecha_publicacion': 'hace-menos-de-1-dia'
  })
  """
  filters = {
    'tipo_operacion': 'alquiler',
    'ubicacion': 'caballito'
  }
  zp_info = zonaprop.getInfoList(10, filters)

  # Almacenamiento en CSV / Excel
  """
  zonaprop.saveDataToCsv(zp_info)
  zonaprop.saveDataToXlsx(zp_info)
  """

  # Conexión a MongoDB
  mc = MongoDBClient()
  if(mc.isConnected()):
    # Borro documentos
    # ATENCIÓN: si el parámetro filters está vacio borrará todos los documentos
    """
    filters = {}
    mc.delete('inmuebles', filters)
    print('borrados', mc.deleted_rows())
    """

    # Inserto / Actualizo en MongoDB desde scraping
    for data in zp_info:
      condition = { 'site_id': data['site_id'] }
      mc.update('inmuebles', data, condition)
    
    # Inserto / Actualizo en MongoDB desde Excel
    """
    zp_info = zonaprop.getDataFromXls()
    for index, row in zp_info.iterrows():
      #Convierto a diccionario
      data = row.to_dict()

      #Remuevo la primer columna del dataset
      data.pop('Unnamed: 0', None)

      #Clave primaria
      condition = { 'site_id': data['site_id'] }
      mc.update('inmuebles', data, condition)
    """

    # Consulto documentos de inmuebles almacenados en MongoDB
    """
    filters = { 'address': { '$regex': 'belgrano', '$options': 'i' } }
    zp_info = zonaprop.getDataFromMongo('inmuebles', filters)
    if zp_info:
      print(zp_info)
    else:
      print('no hay datos')
    """
  else:
    print('Error de conexión')
else:
  print('Es requerida la configuración para ZonaProp')