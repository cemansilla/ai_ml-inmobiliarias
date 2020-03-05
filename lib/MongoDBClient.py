from Helper import *
import pymongo
#import dns # required for connecting with SRV

class MongoDBClient():
  collection_name = ''
  db = ''
  __rs = False

  # Initializer / Instance Attributes
  def __init__(self):
    config_atlas = get_global_config_by_section('MongodbAtlas')
    self.client = pymongo.MongoClient("mongodb+srv://"+config_atlas['user']+":"+config_atlas['pass']+"@"+config_atlas['host']+"/"+config_atlas['name']+"?retryWrites=true&w=majority")
    self.collection_name = config_atlas['name']
    self.db = self.client[self.collection_name]

  def query(self, collection_name, filters = {}):
    """
    Ejecuta una consulta y almacena internamente el result set para ser utilizado en métodos posteriores

    Parameters:
    collection_name (string): Nombre de la colección
    filters (dict): Opcional. Filtros.

    Return:
    void
    """    
    self.__rs = self.db[collection_name].find(filters)

  def num_rows(self):
    """
    Retorna el número de documentos encontrado en la consulta

    Return:
    integer
    """
    return self.__rs.count()

  def get_rows(self):
    """
    Retorna los documentos encontrados en la consulta

    Return:
    array
    """
    data = []

    for doc in self.__rs:
      data.append(doc)

    return data

  def get_row(self):
    """
    Retorna el primer documento encontrado en la consulta

    Return:
    array
    """
    data = []

    for doc in self.__rs:
      data = doc
      break

    return data

  def isConnected(self):
    """
    Valida si la conexión se extableció correctamente

    Returns:
    boolean
    """
    try:
      self.client.server_info()
      return True
    except:
      return False