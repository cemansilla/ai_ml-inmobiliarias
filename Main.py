from lib.ZonaProp import ZonaProp
from lib.MongoDBClient import MongoDBClient
from Helper import *

# Cargo archivo de configuración de sitios
config_sites = get_sites_config()

# Procesamiento de ZonaProp
config_zonaprop = config_sites.get('zonaprop')
if(config_zonaprop):
  #zonaprop = ZonaProp(config_zonaprop)
  #zp_info = zonaprop.getInfoList()

  #zonaprop.saveDataToCsv(zp_info)
  #zonaprop.saveDataToXlsx(zp_info)

  mc = MongoDBClient()
  if(mc.isConnected()):
    #print('list_collection_names', mc.db.list_collection_names())
    #print('list inmuebles', mc.db['inmuebles'].find())

    # Ejecuto query
    mc.query('inmuebles')
    if(mc.num_rows() > 0):
      print(mc.get_rows())
    else:
      print('no hay datos')
  else:
    print('Error de conexión')
else:
  print('Es requerida la configuración para ZonaProp')