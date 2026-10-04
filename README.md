# Análisis de Datos - Talento Tech 2026

[![Validar y Ejecutar Notebook](https://github.com/francoBa/analisisDatos-TT2026/actions/workflows/test_notebook.yml/badge.svg)](https://github.com/francoBa/analisisDatos-TT2026/actions/workflows/test_notebook.yml)
[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/francoBa/analisisDatos-TT2026/blob/main/pre_entrega.ipynb)

Repositorio correspondiente a los proyectos, auditorías y ejercicios prácticos desarrollados durante el curso de **Análisis de Datos**.

> **Acceso directo:** Haz clic en el botón superior **"Open In Colab"** para ejecutar interactivamente el cuaderno principal en Google Colaboratory.

---

## Estructura del Proyecto

```text
.
├── .github/
│   └── workflows/
│       └── test_notebook.yml             # Pipeline de CI/CD (GitHub Actions)
├── files/
│   ├── clientes.csv                      # Dataset demográfico y económico
│   ├── marketing.csv                     # Inversión y canales publicitarios
│   └── ventas.csv                        # Registro transaccional anual
├── README.md
├── requirements.txt                      # Dependencias del proyecto
├── .gitignore
├── pre_entrega.ipynb                     # Cuaderno principal (Etapas 1 y 2)
├── app.py                                # Tablero interactivo con Streamlit
├── analisis_calidad.py                   # Script de análisis exploratorio previo
├── clase4_informe_analisis_datos.md      # Informe de calidad de la Clase 4
└── datos_ventas_para_auditoria.csv       # Dataset previo de auditoría
```

---

## Contenido de la Pre-Entrega (`pre_entrega.ipynb`)

El cuaderno principal consolida dos fases completas de trabajo sobre los datos reales del negocio:

### Etapa 1: Recopilación y Preparación de Datos (Clases 1 a 4)
* **Actividad 1:** Carga dinámica de los conjuntos de datos en DataFrames de Pandas.
* **Actividad 2:** Cálculo dinámico de ventas mensuales de todo el año 2024 utilizando variables y operadores de Python nativo (con formato regional argentino `$ 1.234,56`).
* **Actividad 3:** Programa modular de almacenamiento de transacciones en memoria (`AlmacenVentas`) fundamentando la elección de una **Lista de Diccionarios (`list[dict]`)**.
* **Actividad 4:** Análisis Exploratorio de Datos (EDA) sobre las 3 fuentes con identificación de métricas de dispersión, tipos y outliers.
* **Actividad 5:** Auditoría formal de calidad: detección de 35 filas duplicadas y 2 registros nulos en `ventas.csv`.

### Etapa 2: Preprocesamiento y Limpieza de Datos (Clases 5 a 8)
* **Actividad 1:** Limpieza y depuración: remoción de duplicados (de 3.035 a 2.998 filas limpias), sanitización del caracter `$` en precios y casteo a tipos correctos (`datetime`, `float`, `int`).
* **Actividad 2:** Identificación de **Productos de Alto Rendimiento** que superan la media de facturación del catálogo.
* **Actividad 3:** Agregación por categorías de producto y análisis de participación porcentual en los ingresos.
* **Actividad 4:** Integración de fuentes (`Ventas + Marketing`) mediante un Merge relacional para calcular el retorno publicitario (ROAS / Ratio Ingreso-Costo).

---

## Aplicación Interactiva (Dashboard con Streamlit)

El proyecto incluye un tablero visual desarrollado en Streamlit (`app.py`), que permite:
* Consultar la auditoría general de inconsistencias y valores atípicos.
* Registrar nuevas ventas interactivamente en memoria mediante un formulario web.
* Visualizar métricas ejecutivas, gráficos de barras por categoría y tablas de retorno sobre la inversión en marketing.

### Ejecución de la aplicación:

```bash
streamlit run app.py
```

---

## Instalación y Entorno Local

Se recomienda utilizar un entorno virtual para instalar y ejecutar el proyecto.

### 1. Clonar el repositorio
```bash
git clone https://github.com/francoBa/analisisDatos-TT2026.git
cd analisisDatos-TT2026
```

### 2. Crear y activar el entorno virtual
```bash
# Crear entorno
python -m venv .venv

# Activar en Windows
.\.venv\Scripts\activate

# Activar en macOS o Linux
source .venv/bin/activate
```

### 3. Instalar las dependencias
```bash
pip install -r requirements.txt
```

Las dependencias principales incluyen: `pandas`, `numpy`, `streamlit`, `jupyter`, `nbconvert` e `ipykernel`.

---

## Integración Continua (CI/CD)

El repositorio cuenta con un flujo automatizado de pruebas mediante **GitHub Actions** (`.github/workflows/test_notebook.yml`).  
En cada `push` o `pull request`, una máquina virtual ejecuta de forma desatendida todas las celdas de `pre_entrega.ipynb` para garantizar que el código se mantenga libre de errores y reproducible.