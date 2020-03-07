from Helper import *
import pymongo
#import dns # required for connecting with SRV

class MongoDBClient():
  collection_name = ''
  db = ''
  __rs = False
  __affected = 0

  # Initializer / Instance Attributes
  def __init__(self):
    # Obtengo la configuración
    config_atlas = get_global_config_by_section('MongodbAtlas')

    # Realizo la conexión
    self.client = pymongo.MongoClient("mongodb+srv://"+config_atlas['user']+":"+config_atlas['pass']+"@"+config_atlas['host']+"/"+config_atlas['name']+"?retryWrites=true&w=majority")
    
    # Configuro la colección activa
    database_name = config_atlas['name']
    self.useDatabase(database_name)
    

  def useDatabase(self, database_name):
    """
    Setea la base de datos activa

    Parameters:
    database_name (string): Nombre de la base de datos
    """
    self.db = self.client[database_name]

  def query(self, collection_name, filters = {}, order = {}):
    """
    Ejecuta una consulta y almacena internamente el result set para ser utilizado en métodos posteriores

    Parameters:
    collection_name (string): Nombre de la colección
    filters (dict): Opcional. Filtros.

    Return:
    void
    """    
    self.__rs = self.db[collection_name].find(filters)

    if(order):
      self.__rs = self.__rs.sort(order)

  def delete(self, collection_name, filters = {}):
    """
    Elimina documentos de la colección

    Parameters:
    collection_name (string): Nombre de la colección
    data (mixed): Objetos y array de documentos a insertar
    """
    self.__rs = self.db[collection_name].delete_many(filters)

  def insert(self, collection_name, data):
    """
    Inserta un documento en la colección

    Parameters:
    collection_name (string): Nombre de la colección
    data (mixed): Objetos y array de documentos a insertar
    """
    if(type(data) is dict):
      self.__rs = self.db[collection_name].insert(data)
    else:
      self.__rs = self.db[collection_name].insert_many(data)

  def update(self, collection_name, data, condition):
    """
    Actualiza un documento a partir de la condición especificada

    Parameters:
    collection_name (string): Nombre de la colección
    data (mixed): Objetos y array de documentos a insertar
    condition (mixed): Objetos y array de condiciones
    """
    self.__rs = self.db[collection_name].update_many(condition, {
      '$set': data,
      '$currentDate': { 'lastModified': True }
    })
    self.__last_query = 'update'

  def num_rows(self):
    """
    Retorna el número de documentos encontrado en la consulta

    Return:
    integer
    """
    return self.__rs.count()

  def affected_rows(self):
    """
    Retorna la cantidad de documentos afectados

    Return:
    int
    """
    num = 0

    try:
      num = self.__rs.modified_count
    except:
      pass

    return num

  def deleted_rows(self):
    """
    Retorna la cantidad de documentos eliminados

    Return:
    int
    """
    num = 0

    try:
      num = self.__rs.deleted_count
    except:
      pass

    return num

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