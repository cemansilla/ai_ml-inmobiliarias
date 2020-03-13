# ML / AI en sitios de inmobiliarias - borrador
Juntando 3 inquietudes actuales surge este proyecto.

Por un lado, estoy incursionando en machine learning e inteligencia artificial, incorporando conceptos, practicando y lo que es más importante, disfrutando el proceso.

Por otro lado, veo la necesidad de aprender Python (vengo de PHP).

Y por último tengo planeado mudarme a fines de este año.

Con todo esto pienso armar un programa que busque en sitios de inmobiliarias en base a determinados parámetros y me envie alertas de aquellos que sean relevantes para lo que quiero (por ejemplo que me quede en un punto central entre la universidad, el trabajo y la casa de mi hija), acepte seguro de cacución o determinado tipo de garantía (tendría que interpretar texto).

Cuando tenga esta base quisiera incorporar paneles con info en un dashboard, armar gráficos, empezar a procesar data.

## Dependencias
Recomiendo usar [pip](https://pip.pypa.io/en/stable/installing/).

- YAML
- BeautifulSoup
- Pandas
- Selenium
- PyMongo
- dnspython

## Ideas / Pendientes
- ~~Aplicar filtros en listados~~
- ~~Procesar páginas. Establecer límites~~
- Convertir en webservice
- ~~Incorporar Selenium~~ (Descartado. Se procesará el mapa con la API.)
- ~~Obtener info de Google Maps~~
  - Calcular distancia
- ~~Almacenar / Actualizar info en DB~~
- Procesar de lenguaje en descripciones (NLP)
- Incorporar otros sitios
- Envío de alertas de oportunidades
  - Plantear distintas vías
    - Whatsapp
    - Mail
    - Messenger
    - SMS
    - Notificación push

## ZonaProp filtros
```python
filters = dict({  
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
```

### Temporal
```python
"""
### Paginado ###
https://www.zonaprop.com.ar/departamentos-pagina-2.html
https://www.zonaprop.com.ar/departamentos-2-ambientes-orden-precio-ascendente-pagina-2.html

### Filtros ###

# Tipo de operación
https://www.zonaprop.com.ar/inmuebles-alquiler-orden-precio-m2-descendente.html
https://www.zonaprop.com.ar/emprendimientos-orden-precio-m2-descendente.html

# Orden
https://www.zonaprop.com.ar/inmuebles-orden-publicado-descendente.html
https://www.zonaprop.com.ar/inmuebles-orden-precio-ascendente.html
https://www.zonaprop.com.ar/inmuebles-orden-area-normalizada-ascendente.html

# Zona
https://www.zonaprop.com.ar/departamentos-alquiler-caballito.html
https://www.zonaprop.com.ar/departamentos-alquiler-villa-crespo.html

# Rango de precios
https://www.zonaprop.com.ar/departamentos-alquiler-villa-crespo-5000-15000-pesos.html
https://www.zonaprop.com.ar/departamentos-alquiler-villa-crespo-mas-5000-pesos.html
https://www.zonaprop.com.ar/departamentos-alquiler-villa-crespo-menos-15000-pesos.html

# Expensas
https://www.zonaprop.com.ar/departamentos-alquiler-villa-crespo-menos-15000-pesos-100-200-expensas.html
https://www.zonaprop.com.ar/departamentos-alquiler-villa-crespo-menos-15000-pesos-mas-100-expensas.html
https://www.zonaprop.com.ar/departamentos-alquiler-villa-crespo-menos-15000-pesos-menos-200-expensas.html

# Ambientes
https://www.zonaprop.com.ar/departamentos-alquiler-villa-crespo-2-ambientes-menos-15000-pesos-mas-100-expensas.html

# Tipo de vivienda
https://www.zonaprop.com.ar/casas-alquiler-villa-crespo-2-ambientes-menos-15000-pesos-mas-100-expensas.html

# Habitaciones
https://www.zonaprop.com.ar/casas-alquiler-villa-crespo-1-habitacion-2-ambientes-menos-15000-pesos-mas-100-expensas.html
https://www.zonaprop.com.ar/casas-alquiler-villa-crespo-2-habitaciones-2-ambientes-menos-15000-pesos-mas-100-expensas.html

# Superficie
https://www.zonaprop.com.ar/casas-alquiler-villa-crespo-2-habitaciones-2-ambientes-mas-15-m2-cubiertos-menos-15000-pesos-mas-100-expensas.html
https://www.zonaprop.com.ar/casas-alquiler-villa-crespo-2-habitaciones-2-ambientes-menos-35-m2-cubiertos-menos-15000-pesos-mas-100-expensas.html
https://www.zonaprop.com.ar/casas-alquiler-villa-crespo-2-habitaciones-2-ambientes-15-35-m2-cubiertos-menos-15000-pesos-mas-100-expensas.html

# Fecha de publicación
https://www.zonaprop.com.ar/casas-alquiler-villa-crespo-2-habitaciones-2-ambientes-menos-35-m2-cubiertos-publicado-hace-menos-de-2-dias-menos-15000-pesos-mas-100-expensas.html
https://www.zonaprop.com.ar/casas-alquiler-villa-crespo-2-habitaciones-2-ambientes-menos-35-m2-cubiertos-publicado-hace-menos-de-1-dia-menos-15000-pesos-mas-100-expensas.html
https://www.zonaprop.com.ar/casas-alquiler-villa-crespo-2-habitaciones-2-ambientes-menos-35-m2-cubiertos-publicado-hace-menos-de-1-semana-menos-15000-pesos-mas-100-expensas.html
https://www.zonaprop.com.ar/casas-alquiler-villa-crespo-2-habitaciones-2-ambientes-menos-35-m2-cubiertos-publicado-hace-menos-de-45-dias-menos-15000-pesos-mas-100-expensas.html
"""
```