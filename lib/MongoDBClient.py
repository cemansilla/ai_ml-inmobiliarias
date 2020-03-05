from Helper import *
import pymongo
#import dns # required for connecting with SRV

class MongoDBClient():
  # Initializer / Instance Attributes
  def __init__(self):
    config_atlas = get_global_config_by_section('MongodbAtlas')
    self.client = pymongo.MongoClient("mongodb+srv://"+config_atlas['user']+":"+config_atlas['pass']+"@"+config_atlas['host']+"/"+config_atlas['name']+"?retryWrites=true&w=majority")

  def isConnected(self):
    try:
      self.client.server_info()
      return True
    except:
      return False