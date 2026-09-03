# Análisis de datos

Repositorio correspondiente a los ejercicios y análisis realizados durante el curso de análisis de datos.

## Estructura del proyecto

La estructura actual del proyecto incluye los informes, los datos utilizados, el script de análisis y los archivos de configuración necesarios:

~~~text
.
├── README.md
├── requirements.txt
├── .gitignore
├── analisis_calidad.py
├── clase4_informe_analisis_datos.md
└── datos_ventas_para_auditoria.csv
~~~

Para visualizar el árbol de archivos desde la terminal, se puede utilizar el siguiente comando:

~~~bash
tree
~~~

En Windows, si el comando `tree` está disponible, se puede mostrar también el contenido de los archivos con:

~~~bash
tree /F
~~~

En macOS o Linux, si el comando `tree` no está instalado, puede instalarse con:

~~~bash
# macOS
brew install tree

# Ubuntu o Debian
sudo apt install tree
~~~

## Análisis realizados

### 1. Primer análisis: calidad de datos

Este documento presenta un análisis exploratorio de la calidad de los datos contenidos en el archivo de ventas.

Se documentan inconsistencias relacionadas con:

- Formatos de fecha.
- Registros duplicados y problemas con identificadores únicos.
- Valores faltantes o nulos.
- Categorías no autorizadas.
- Métodos de pago desconocidos.
- Valores atípicos.
- Diferencias de mayúsculas, minúsculas y espacios.
- Inconsistencias entre cantidades, precios y totales.
- Posibles problemas estructurales en el archivo.
- Diferencias entre el estatus de auditoría y las anomalías encontradas.

El análisis se enfoca exclusivamente en la identificación y documentación de hallazgos, sin aplicar procesos de limpieza o corrección de los datos.

- [Ver informe del primer análisis](./clase4_informe_analisis_datos.md)
- [Ver archivo de datos analizado](./datos_ventas_para_auditoria.csv)

### 2. Script de análisis

El archivo [Ver archivo de script](./analisis_calidad.py) contiene un análisis reproducible realizado con Python.

El script utiliza las siguientes librerías:

- **Pandas:** lectura, exploración y análisis de los datos.
- **NumPy:** cálculo de valores atípicos mediante el rango intercuartílico.
- **Polars:** verificación rápida de la estructura del archivo.

El script no modifica el archivo original. Solo genera indicadores y conteos para respaldar los hallazgos incluidos en el informe.

Para ejecutar el análisis:

~~~bash
python analisis_calidad.py
~~~

## Instalación

Se recomienda utilizar un entorno virtual para instalar las dependencias del proyecto.

### Crear el entorno virtual

~~~bash
python -m venv .venv
~~~

### Activar el entorno virtual en Windows

~~~bash
.\.venv\Scripts\activate
~~~

### Activar el entorno virtual en macOS o Linux

~~~bash
source .venv/bin/activate
~~~

### Instalar las dependencias

Las librerías utilizadas se encuentran detalladas en el archivo `requirements.txt`.

Para instalarlas, ejecutar:

~~~bash
pip install -r requirements.txt
~~~

Las principales dependencias del proyecto son:

- `pandas`
- `numpy`
- `polars`

## Archivos de configuración

El archivo `.gitignore` contiene las reglas para evitar subir al repositorio:

- Entornos virtuales como `.venv/`, `venv/` y `env/`.
- Archivos temporales de Python.
- Carpetas de caché.
- Archivos con variables de entorno.
- Configuraciones específicas de editores.

## Aplicación interactiva con Streamlit

Como futura etapa del proyecto, se prevé incorporar una aplicación interactiva desarrollada con Streamlit. El objetivo será visualizar los resultados del análisis de calidad de datos mediante métricas, tablas, gráficos y filtros dinámicos.

La aplicación permitirá consultar de forma más visual algunos de los principales hallazgos, como:

- Cantidad total de registros.
- Identificadores duplicados.
- Valores faltantes.
- Categorías no autorizadas.
- Métodos de pago registrados.
- Valores atípicos en cantidades y precios.
- Estado de auditoría de las transacciones.

La aplicación se ejecutará localmente mediante el siguiente comando:

```bash
streamlit run app.py
