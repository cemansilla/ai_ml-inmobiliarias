from lib.ZonaProp import ZonaProp
from lib.MongoDBClient import MongoDBClient
from Helper import *

from bson.objectid import ObjectId

# Cargo archivo de configuración de sitios
config_sites = get_sites_config()

# Procesamiento de ZonaProp
config_zonaprop = config_sites.get('zonaprop')
if(config_zonaprop):
  zonaprop = ZonaProp(config_zonaprop)
  #zp_info = zonaprop.getInfoList()

  #zonaprop.saveDataToCsv(zp_info)
  #zonaprop.saveDataToXlsx(zp_info)

  mc = MongoDBClient()
  if(mc.isConnected()):
    """
    #Desde scraping
    for data in zp_info:
      condition = { 'site_id': data['site_id'] }
      mc.update('inmuebles', data, condition)
    """

    """
    #Desde Excel
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

    # Delete
    #filters = { 'many': { '$regex': 'array' } }
    #mc.delete('inmuebles', filters)
    #print('borrados', mc.deleted_rows())

    # Insert
    #mc.insert('inmuebles', [{'many': 'array 2 b'},{'many': 'array 2 c'}])
    #print('insertados 1', mc.affected_rows())
    #mc.insert('inmuebles', {'many': 'dict 2 b'})
    #print('insertados 2', mc.affected_rows())

    # Update
    #data = { 'key': 'actualizado by value', 'nueva_key': ':)', 'todos': '...' }
    #condition = { 'title': { '$regex': 'ipsum' } }
    #condition = { '_id': ObjectId('5e63af1141f68b2a481ce30f') }
    #condition = {}    
    #mc.update('inmuebles', data, condition)
    #print('afectados', mc.affected_rows())

    # Consulta
    """
    filters = { 'key': { '$regex': 'valu' } }
    order = [('key',1)]
    filters = {}
    order = {}
    mc.query('inmuebles', filters, order)
    if(mc.num_rows() > 0):
      print(mc.get_rows())
    else:
      print('no hay datos')
    """
  else:
    print('Error de conexión')
else:
  print('Es requerida la configuración para ZonaProp')