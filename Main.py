from lib.ZonaProp import ZonaProp
from lib.MongoDBClient import MongoDBClient
from Helper import *

# Cargo archivo de configuración de sitios
config_sites = get_sites_config()

# Procesamiento de ZonaProp
config_zonaprop = config_sites.get('zonaprop')
if(config_zonaprop):
  zonaprop = ZonaProp(config_zonaprop)

  _filters = dict({  
    'tipo_operacion': 'venta', # venta | alquiler | alquiler-temporal | emprendimientos
    'orden': {
      'criterio': 'precio', # publicado | precio | variacionporcentual (bajaron de precio) | area-normalizada (amplios / pequeños en m2) | antiguedad | precio-m2
      'sentido': 'ascendente' # ascendente | descendente
    },
    'ubicacion': '[slug-nombre-ubicacion]', # Lo suele agregar al final
    'precio': { # Si hay solo mínimo la busqueda será "Desde", Si hay sólo máximo será "Hasta", si están ambos será rango de precios
      'minimo': 100,
      'maximo': False,
      'moneda': 'pesos' # pesos | dolar
    },
    'expensas': { # Si hay solo mínimo la busqueda será "Desde", Si hay sólo máximo será "Hasta", si están ambos será rango de precios
      'minimo': 100,
      'maximo': False,
      'moneda': 'pesos' # pesos | dolar
    },
    'ambientes': {
      'cantidad': 4,
      'tope': 5 # Si el valor es mayor o igual a esto, a la URL se le agrega "mas"
    },
    'tipo_vivienda': 'departamentos', # departamentos | casas | terrenos | locales-comerciales | oficinas-comerciales | cocheras
    'dormitorios': {
      'cantidad': 4,
      'tope': 5 # Si el valor es mayor o igual a esto, a la URL se le agrega "mas"
    },
    'superficie': { # Si hay solo mínimo la busqueda será "Desde", Si hay sólo máximo será "Hasta", si están ambos será rango de precios
      'minimo': 100,
      'maximo': False,
      'unidad': 'm2' # m2
    },
    'fecha_publicacion': 'hace-menos-de-1-dia' # hace-menos-de-1-dia (hoy) | hace-menos-de-2-dias (ayer) | hace-menos-de-1-semana | hace-menos-de-15-dias | hace-menos-de-1-mes | hace-menos-de-45-dias
  })
  filters = dict({
    'tipo_operacion': 'venta',
    'orden': {
      'criterio': 'precio',
      'sentido': 'ascendente'
    },
    'ubicacion': 'caballito',
    'tipo_vivienda': 'departamentos'
  })
  zp_info = zonaprop.getInfoList(5, filters)

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
    """
    for data in zp_info:
      condition = { 'site_id': data['site_id'] }
      mc.update('inmuebles', data, condition)
    """
    
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