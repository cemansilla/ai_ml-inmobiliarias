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

  db = MongoDBClient()
  print(db.isConnected())
else:
  print('Es requerida la configuración para ZonaProp')