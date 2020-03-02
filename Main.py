from lib.ZonaProp import ZonaProp
from Helper import *

# Cargo archivo de configuración
config = get_config_info()

# Procesamiento de ZonaProp
config_zonaprop = config.get('zonaprop')
if(config_zonaprop):
  zonaprop = ZonaProp(config_zonaprop)
  zp_info = zonaprop.getInfoList()
  zonaprop.saveDataToCsv(zp_info)
  zonaprop.saveDataToXlsx(zp_info)
else:
  print('Es requerida la configuración para ZonaProp')