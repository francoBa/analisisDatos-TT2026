# Análisis de Datos — Entrega Final (Talento Tech 2026)

[![Validar y Ejecutar Notebook](https://github.com/francoBa/analisisDatos-TT2026/actions/workflows/test_notebook.yml/badge.svg)](https://github.com/francoBa/analisisDatos-TT2026/actions/workflows/test_notebook.yml)
[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/francoBa/analisisDatos-TT2026/blob/main/entrega_final.ipynb)

Repositorio oficial correspondiente al proyecto integral, auditorías y desarrollo analítico del curso de **Análisis de Datos**.

> **Acceso interactivo:** Haz clic en el botón **Open In Colab** para ejecutar el cuaderno principal en Google Colaboratory.

---

## Estructura del Proyecto

```text
.
├── .github/
│   └── workflows/
│       └── test_notebook.yml             # Pipeline de CI/CD (GitHub Actions)
├── .streamlit/
│   └── config.toml                       # Configuración de Streamlit
├── files/
│   ├── clientes.csv                      # Dataset demográfico y económico
│   ├── marketing.csv                     # Inversión y canales publicitarios
│   └── ventas.csv                        # Registro transaccional anual
├── README.md
├── requirements.txt                      # Dependencias del proyecto
├── .gitignore
├── pre_entrega.ipynb                     # Cuaderno principal (Etapas 1 y 2)
├── entrega_final.ipynb                   # Cuaderno principal (Etapas 3 y 4)
├── app.py                                # Aplicación web multipestaña (Streamlit)
├── analisis_calidad.py                   # Análisis exploratorio previo
├── clase4_informe_analisis_datos.md      # Informe de calidad de la Clase 4
└── datos_ventas_para_auditoria.csv       # Dataset previo de auditoría
```

---

## Contenido Académico (`pre_entrega.ipynb`)

El cuaderno principal consolida el ciclo de vida completo del dato (*Data Lifecycle*), estructurado en cuatro etapas fundamentales.

### Etapa 1: Recopilación y Preparación de Datos (Clases 1 a 4)

- **Actividad 1:** Carga dinámica de los conjuntos de datos en DataFrames de Pandas.
- **Actividad 2:** Cálculo dinámico de ventas mensuales de todo el año 2024 utilizando variables y operadores de Python nativo, con formato regional argentino (`$ 1.234,56`).
- **Actividad 3:** Programa modular de almacenamiento de transacciones en memoria (`AlmacenVentas`), fundamentando la elección de una **Lista de Diccionarios (`list[dict]`)**.
- **Actividades 4 y 5:** Análisis Exploratorio Inicial y auditoría formal de calidad, con detección de 35 filas duplicadas y 2 valores nulos en `ventas.csv`.

### Etapa 2: Preprocesamiento y Limpieza de Datos (Clases 5 a 8)

- **Actividad 1:** Limpieza y depuración estructural, reduciendo el dataset de 3.035 a 2.998 filas limpias. Sanitización de monedas y conversión a tipos de datos adecuados (`datetime`, `float`, `int`).
- **Actividades 2 y 3:** Identificación de **Productos de Alto Rendimiento** y agregación analítica por categorías de producto, incluyendo su participación porcentual.
- **Actividad 4:** Integración de fuentes (`Ventas + Marketing`) mediante un cruce relacional (*Merge*) para calcular el rendimiento publicitario (**ROAS** y retorno por peso invertido).

### Etapa 3: Análisis de Datos (Clase 8 en adelante)

- **Actividad 1:** Estadística descriptiva avanzada mediante el cálculo de medidas de tendencia central y dispersión: Media, Mediana, Desvío Estándar y Rango Intercuartil.
- **Actividad 2:** Análisis Exploratorio de Datos (EDA) orientado a identificar patrones y tendencias de consumo.
- **Actividad 3:** Evaluación de correlación lineal de Pearson entre el precio unitario y la cantidad de unidades demandadas.
- **Actividad 4:** Consolidación analítica de todas las métricas en un dataset maestro de cierre.

### Etapa 4: Visualización de Datos y Dashboard Interactivo

- **Actividades 1 y 2:** Visualizaciones estáticas mediante **Matplotlib** (evolución temporal mensual) y **Seaborn** (`boxplot` estadístico de precios por categoría).
- **Actividades 3 y 4:** Construcción de un dashboard interactivo avanzado con **Plotly** y presentación de conclusiones de negocio ante el panel de expertos simulados (*SynthData*).

---

## Aplicación Web Interactiva (`app.py` con Streamlit)

El proyecto incorpora una aplicación web multipestaña desarrollada con **Streamlit**, orientada a la presentación y exploración ejecutiva de los resultados.

### Secciones de la aplicación

1. **Entrega Final (Vista Principal):** Dashboard ejecutivo con indicadores clave de rendimiento (KPIs): Facturación, Unidades, Transacciones y Ticket Promedio. Incluye filtros laterales por categoría y gráficos dinámicos de evolución e ingresos.
2. **Pre-Entrega (Etapa 2):** Resumen del preprocesamiento, tablas de análisis por categorías y cálculo del retorno publicitario (ROAS).
3. **Auditoría de Calidad:** Reporte técnico de control de anomalías, valores nulos y registros duplicados, en el contexto de las actividades de Talento Tech.

### Ejecución local

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
# Crear entorno virtual
python -m venv .venv
```

**Windows:**

```powershell
.venv\Scripts\activate
```

**macOS / Linux:**

```bash
source .venv/bin/activate
```

### 3. Instalar las dependencias

```bash
pip install -r requirements.txt
```

Las principales dependencias del proyecto incluyen:

- `pandas`
- `numpy`
- `streamlit`
- `jupyter`
- `nbconvert`
- `ipykernel`
- `plotly`
- `matplotlib`
- `seaborn`
- `dash`
- `dash-bootstrap-components`

---

## Integración Continua (CI/CD)

El repositorio incorpora un flujo automatizado de pruebas mediante **GitHub Actions**, definido en `.github/workflows/test_notebook.yml`.

En cada evento `push` o `pull_request`, un entorno de ejecución automatizado ejecuta las celdas de `pre_entrega.ipynb` para verificar que el cuaderno pueda ejecutarse correctamente y mantener la reproducibilidad del análisis.

Este proceso permite detectar errores de ejecución y problemas de reproducibilidad antes de integrar nuevos cambios en la rama principal.

---

## Objetivos del Proyecto

Este trabajo integra los conocimientos adquiridos durante el curso de Análisis de Datos de Talento Tech 2026, aplicando herramientas y metodologías de Python para:

- Recopilar y estructurar información proveniente de distintas fuentes.
- Detectar y corregir problemas de calidad de datos.
- Transformar y combinar conjuntos de datos.
- Aplicar técnicas estadísticas y análisis exploratorio.
- Identificar patrones, tendencias y relaciones entre variables.
- Comunicar resultados mediante visualizaciones y dashboards interactivos.
- Automatizar controles de ejecución y reproducibilidad mediante integración continua.

El resultado es un proyecto integral que combina análisis técnico, interpretación de datos y presentación de información orientada a la toma de decisiones.

---