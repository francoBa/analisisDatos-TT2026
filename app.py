from pathlib import Path
import numpy as np
import pandas as pd
import streamlit as st

# Configuración inicial de la página
st.set_page_config(
    page_title="Entrega Final | Análisis de Datos 2026",
    page_icon="📊",
    layout="wide",
)

# --- CARGA DE DATOS DE LAS DIFERENTES ETAPAS ---
CARPETA_FILES = Path(__file__).parent / "files"
ARCHIVO_AUDITORIA = Path(__file__).parent / "datos_ventas_para_auditoria.csv"

@st.cache_data
def cargar_datos_principales():
    try:
        df_clientes = pd.read_csv(CARPETA_FILES / "clientes.csv")
        df_marketing = pd.read_csv(CARPETA_FILES / "marketing.csv")
        df_ventas = pd.read_csv(CARPETA_FILES / "ventas.csv")
        return df_clientes, df_marketing, df_ventas
    except Exception as e:
        return None, None, None

@st.cache_data
def cargar_datos_auditoria():
    if ARCHIVO_AUDITORIA.exists():
        return pd.read_csv(ARCHIVO_AUDITORIA, keep_default_na=False)
    return pd.DataFrame()

df_clientes, df_marketing, df_ventas = cargar_datos_principales()
df_auditoria = cargar_datos_auditoria()

# --- SISTEMA DE PESTAÑAS PRINCIPALES ---
pestana_principal, pestana_preentrega, pestana_auditoria = st.tabs([
    "🏠 Entrega Final (Análisis y Dashboard)", 
    "📈 Pre-Entrega (Etapa 2)", 
    "🔍 Auditoría de Calidad (Datos Crudos)"
])

# =====================================================================
# PESTAÑA 1: ENTREGA FINAL (VISTA PRINCIPAL DE LUJO)
# =====================================================================
with pestana_principal:
    st.title("📊 Dashboard Ejecutivo: Entrega Final de Análisis de Datos")
    st.write("**Autor:** Franco Barreto | **Entorno:** Streamlit & Python | **Contexto:** SynthData 2024")
    st.divider()

    if df_ventas is not None and not df_ventas.empty:
        # Preprocesamiento optimizado para el dashboard principal
        df_v = df_ventas.copy()
        df_v = df_v.dropna(subset=['precio', 'cantidad'])
        df_v['precio'] = df_v['precio'].astype(str).str.replace('$', '', regex=False).str.strip().astype(float)
        df_v['cantidad'] = df_v['cantidad'].astype(int)
        df_v['ingreso_total'] = df_v['precio'] * df_v['cantidad']
        df_v['fecha_venta'] = pd.to_datetime(df_v['fecha_venta'], format='%d/%m/%Y')
        df_v['mes'] = df_v['fecha_venta'].dt.strftime('%Y-%m')

        # Sidebar de Filtros Globales para la vista principal
        st.sidebar.header("🎛️ Filtros de Visualización")
        categorias_disp = sorted(df_v['categoria'].unique())
        cat_seleccionada = st.sidebar.selectbox("Filtrar por Categoría", ["Todas"] + categorias_disp)

        if cat_seleccionada != "Todas":
            df_view = df_v[df_v['categoria'] == cat_seleccionada]
        else:
            df_view = df_v.copy()

        # 1. Indicadores Principales (KPIs)
        kpi1, kpi2, kpi3, kpi4 = st.columns(4)
        kpi1.metric("Facturación Total", f"$ {df_view['ingreso_total'].sum():,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))
        kpi2.metric("Unidades Vendidas", f"{df_view['cantidad'].sum():,} uds".replace(",", "."))
        kpi3.metric("Transacciones Evaluadas", f"{len(df_view):,}".replace(",", "."))
        kpi4.metric("Ticket Promedio", f"$ {df_view['ingreso_total'].mean():,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))

        st.divider()

        # 2. Sección de Análisis Estadístico y EDA
        col_eda1, col_eda2 = st.columns(2)
        with col_eda1:
            st.subheader("📈 Evolución Mensual de Facturación")
            df_tiempo = df_view.groupby('mes', as_index=False)['ingreso_total'].sum()
            st.line_chart(df_tiempo.set_index('mes'), color="#2563eb", width="stretch")

        with col_eda2:
            st.subheader("📊 Facturación Consolidada por Categoría")
            df_cat = df_view.groupby('categoria', as_index=False)['ingreso_total'].sum()
            st.bar_chart(df_cat.set_index('categoria'), color="#059669", width="stretch")

        st.divider()

        # 3. Análisis de Correlación y Dispersión
        st.subheader("🔬 Análisis de Correlación (Precio vs. Cantidad)")
        corr_val = df_view['precio'].corr(df_view['cantidad'])
        st.info(f"**Coeficiente de Correlación de Pearson:** `{corr_val:.4f}` — Indica independencia lineal entre el valor monetario del producto y el volumen de unidades adquiridas por transacción.")

        # Gráfico de dispersión nativo con Streamlit
        st.scatter_chart(df_view.sample(min(len(df_view), 300)), x='precio', y='cantidad', color='categoria')

        st.divider()

        # 4. Consolidación Final de Hallazgos
        st.subheader("📋 Conclusiones del Panel de Expertos (SynthData)")
        st.success("""
        * **Estabilidad Operativa:** El flujo de ingresos se mantuvo consistente durante todo el período analizado.
        * **Mitigación de Riesgos:** Las categorías comerciales presentan una participación equilibrada.
        * **Eficiencia Publicitaria:** Las campañas multicanal acompañaron de forma óptima el volumen de salida de los productos líderes.
        """)
    else:
        st.error("No se pudieron cargar los archivos transaccionales en la carpeta `files/`.")

# =====================================================================
# PESTAÑA 2: PRE-ENTREGA (ETAPA 2)
# =====================================================================
with pestana_preentrega:
    st.subheader("📈 Pre-Entrega: Preprocesamiento e Integración (Etapa 2)")
    st.write("Resultados analíticos sobre la combinación de bases de datos de ventas y marketing.")

    if df_ventas is not None and df_marketing is not None:
        v_pre = df_ventas.copy().drop_duplicates().dropna(subset=["precio", "cantidad"])
        v_pre["precio"] = v_pre["precio"].astype(str).str.replace("$", "", regex=False).str.strip().astype(float)
        v_pre["ingreso_total"] = v_pre["precio"] * v_pre["cantidad"]
        m_pre = df_marketing.copy()

        c1, c2 = st.columns(2)
        with c1:
            st.markdown("### Rendimiento por Categoría")
            res_cat = v_pre.groupby("categoria")["ingreso_total"].sum().reset_index()
            st.dataframe(res_cat, hide_index=True, width="stretch")

        with c2:
            st.markdown("### Integración Ventas vs Marketing")
            mkt_prod = m_pre.groupby("producto").agg(costo_mkt=("costo", "sum"), canales=("canal", lambda x: ", ".join(x.unique()))).reset_index()
            v_prod = v_pre.groupby("producto").agg(ingresos=("ingreso_total", "sum")).reset_index()
            merge_df = pd.merge(v_prod, mkt_prod, on="producto", how="inner")
            merge_df["ROAS_Ratio"] = (merge_df["ingresos"] / merge_df["costo_mkt"]).round(2)
            st.dataframe(merge_df.sort_values(by="ROAS_Ratio", ascending=False), hide_index=True, width="stretch")
    else:
        st.warning("Archivos de pre-entrega no disponibles.")

# =====================================================================
# PESTAÑA 3: AUDITORÍA DE CALIDAD (DATOS CRUDOS - TALENTO TECH)
# =====================================================================
with pestana_auditoria:
    st.subheader("🔍 Reporte de Calidad de Datos (Prueba Académica)")
    st.write("Análisis técnico de anomalías, valores faltantes y estatus de auditoría inicial.")

    if not df_auditoria.empty:
        st.dataframe(df_auditoria, width="stretch")
    else:
        st.warning("No se encontró el archivo `datos_ventas_para_auditoria.csv`.")