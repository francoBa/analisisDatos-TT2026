from pathlib import Path
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import streamlit as st

# =====================================================================
# CONFIGURACIÓN INICIAL DE LA PÁGINA
# =====================================================================
st.set_page_config(
    page_title="SynthData 2024 | Executive Analytics Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Estilos CSS personalizados para tarjetas KPI de lujo
st.markdown("""
<style>
    div[data-testid="metric-container"] {
        background-color: #ffffff;
        border: 1px solid #e2e8f0;
        padding: 16px 20px;
        border-radius: 12px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
        border-left: 5px solid #2563eb;
    }
    .header-banner {
        background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
        padding: 24px 30px;
        border-radius: 12px;
        color: white;
        margin-bottom: 20px;
    }
</style>
""", unsafe_allow_html=True)

# =====================================================================
# CARGA Y PREPROCESAMIENTO DE DATOS
# =====================================================================
CARPETA_FILES = Path(__file__).parent / "files"
ARCHIVO_AUDITORIA = Path(__file__).parent / "datos_ventas_para_auditoria.csv"

@st.cache_data
def cargar_y_limpiar_datos():
    try:
        df_clientes = pd.read_csv(CARPETA_FILES / "clientes.csv")
        df_marketing = pd.read_csv(CARPETA_FILES / "marketing.csv")
        df_ventas = pd.read_csv(CARPETA_FILES / "ventas.csv")

        # Limpieza idéntica a la Etapa 2 del Notebook (3.035 -> 2.998 registros)
        df_v = df_ventas.drop_duplicates().dropna(subset=['precio', 'cantidad']).copy()
        df_v['precio'] = df_v['precio'].astype(str).str.replace('$', '', regex=False).str.strip().astype(float)
        df_v['cantidad'] = df_v['cantidad'].astype(int)
        df_v['ingreso_total'] = df_v['precio'] * df_v['cantidad']
        df_v['fecha_venta'] = pd.to_datetime(df_v['fecha_venta'], format='%d/%m/%Y')
        df_v['mes'] = df_v['fecha_venta'].dt.to_period('M').astype(str)
        df_v['trimestre'] = df_v['fecha_venta'].dt.to_period('Q').astype(str)

        # Limpieza Marketing
        df_m = df_marketing.copy()
        df_m['fecha_inicio'] = pd.to_datetime(df_m['fecha_inicio'], format='%d/%m/%Y')
        df_m['fecha_fin'] = pd.to_datetime(df_m['fecha_fin'], format='%d/%m/%Y')

        # Dataset Consolidado (Ventas + Marketing)
        resumen_v = df_v.groupby(['producto', 'categoria'], as_index=False).agg(
            ingreso_generado=('ingreso_total', 'sum'),
            unidades_vendidas=('cantidad', 'sum'),
            operaciones=('id_venta', 'count'),
            precio_promedio=('precio', 'mean')
        )
        resumen_m = df_m.groupby('producto', as_index=False).agg(
            costo_marketing_total=('costo', 'sum'),
            canales=('canal', lambda x: ", ".join(sorted(x.unique()))),
            campanhas=('id_campanha', 'count')
        )
        df_consolidado = pd.merge(resumen_v, resumen_m, on='producto', how='inner')
        df_consolidado['relacion_ingreso_costo'] = df_consolidado['ingreso_generado'] / df_consolidado['costo_marketing_total']

        return df_clientes, df_m, df_v, df_ventas, df_consolidado
    except Exception:
        return None, None, None, None, None

@st.cache_data
def cargar_datos_auditoria():
    if ARCHIVO_AUDITORIA.exists():
        return pd.read_csv(ARCHIVO_AUDITORIA, keep_default_na=False)
    return pd.DataFrame()

df_clientes, df_marketing, df_v_limpio, df_v_crudo, df_consolidado = cargar_y_limpiar_datos()
df_auditoria = cargar_datos_auditoria()

# Función formato moneda argentina
def fmt_ar(valor):
    return f"$ {valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

# =====================================================================
# ENCABEZADO EJECUTIVO
# =====================================================================
st.markdown("""
<div class="header-banner">
    <h1 style="margin:0; font-size: 28px;">📊 SYNTHDATA — EXECUTIVE INTELLIGENCE DASHBOARD</h1>
    <p style="margin:6px 0 0 0; color: #cbd5e1; font-size: 15px;">
        <b>Autor:</b> Franco Barreto &nbsp;|&nbsp; <b>Proyecto Final:</b> Data Analytics 2026 &nbsp;|&nbsp; <b>Stack:</b> Python, Pandas, Plotly & Streamlit
    </p>
</div>
""", unsafe_allow_html=True)

# =====================================================================
# SISTEMA DE PESTAÑAS PRINCIPALES
# =====================================================================
pestana_principal, pestana_estadistica, pestana_preentrega, pestana_auditoria = st.tabs([
    "🏠 Dashboard Ejecutivo (Etapa 4)",
    "📐 Estadística y Correlación (Etapa 3)",
    "📈 Preprocesamiento e Integración (Etapa 2)",
    "🔍 Auditoría de Calidad (Etapa 1)"
])
if df_v_limpio is not None and not df_v_limpio.empty:
    # --- BARRA LATERAL DE FILTROS GLOBALES ---
    st.sidebar.header("🎛️ Filtros Interactivos")
    categorias_disp = sorted(df_v_limpio['categoria'].unique())
    trimestres_disp = sorted(df_v_limpio['trimestre'].unique())

    cat_sel = st.sidebar.selectbox("📂 Categoría Comercial:", ["Todas"] + categorias_disp)
    trim_sel = st.sidebar.selectbox("📅 Período Trimestral:", ["Todos"] + trimestres_disp)

    st.sidebar.divider()
    st.sidebar.info("💡 Los filtros actualizan dinámicamente los KPIs y gráficos del tablero ejecutivo.")

    # Aplicar filtros
    df_view = df_v_limpio.copy()
    if cat_sel != "Todas":
        df_view = df_view[df_view['categoria'] == cat_sel]
    if trim_sel != "Todos":
        df_view = df_view[df_view['trimestre'] == trim_sel]

    # =================================================================
    # PESTAÑA 1: DASHBOARD EJECUTIVO (ETAPA 4)
    # =================================================================
    with pestana_principal:
        # 1. Fila de 4 KPIs Principales
        k1, k2, k3, k4 = st.columns(4)
        k1.metric("💰 Facturación Total", fmt_ar(df_view['ingreso_total'].sum()))
        k2.metric("📦 Unidades Vendidas", f"{df_view['cantidad'].sum():,} uds".replace(",", "."))
        k3.metric("🧾 Ticket Promedio", fmt_ar(df_view['ingreso_total'].mean() if len(df_view) else 0))
        k4.metric("🛒 Operaciones Válidas", f"{len(df_view):,}".replace(",", "."))

        st.write("")

        # 2. Fila 1 de Gráficos: Evolución Temporal + Dona de Participación
        col1, col2 = st.columns([2, 1])
        with col1:
            df_mes = df_view.groupby('mes', as_index=False)['ingreso_total'].sum()
            fig_linea = px.area(
                df_mes, x='mes', y='ingreso_total', markers=True,
                title="<b>Evolución Mensual de la Facturación ($)</b>",
                labels={'mes': 'Mes', 'ingreso_total': 'Ingresos ($)'},
                template='plotly_white'
            )
            fig_linea.update_traces(line_color='#2563eb', line_width=3, fillcolor='rgba(37, 99, 235, 0.15)')
            fig_linea.update_layout(height=360, margin=dict(t=50, b=30, l=20, r=20))
            st.plotly_chart(fig_linea, use_container_width=True)

        with col2:
            grupo_dona = 'categoria' if cat_sel == "Todas" else 'producto'
            df_dona = df_view.groupby(grupo_dona, as_index=False)['ingreso_total'].sum().nlargest(5, 'ingreso_total')
            titulo_dona = "<b>Participación por Categoría</b>" if cat_sel == "Todas" else f"<b>Top 5 en {cat_sel}</b>"
            fig_dona = px.pie(
                df_dona, names=grupo_dona, values='ingreso_total', hole=0.55,
                title=titulo_dona,
                color_discrete_sequence=['#2563eb', '#0d9488', '#f59e0b', '#7c3aed', '#ec4899'],
                template='plotly_white'
            )
            fig_dona.update_layout(height=360, margin=dict(t=50, b=30, l=10, r=10), legend=dict(orientation="h", y=-0.15))
            st.plotly_chart(fig_dona, use_container_width=True)

        # 3. Fila 2 de Gráficos: Top 8 Productos + Impacto Marketing vs Ventas
        col3, col4 = st.columns(2)
        with col3:
            df_top = df_view.groupby('producto', as_index=False)['ingreso_total'].sum().nlargest(8, 'ingreso_total').sort_values('ingreso_total')
            fig_barras = px.bar(
                df_top, x='ingreso_total', y='producto', orientation='h',
                title="<b>Top 8 Productos con Mayor Facturación ($)</b>",
                labels={'ingreso_total': 'Ingresos Totales ($)', 'producto': ''},
                color='ingreso_total', color_continuous_scale='Blues',
                template='plotly_white'
            )
            fig_barras.update_layout(height=380, margin=dict(t=50, b=30, l=10, r=20), coloraxis_showscale=False)
            st.plotly_chart(fig_barras, use_container_width=True)

        with col4:
            df_mkt_view = df_consolidado if cat_sel == "Todas" else df_consolidado[df_consolidado['categoria'] == cat_sel]
            fig_roas = px.scatter(
                df_mkt_view, x='costo_marketing_total', y='ingreso_generado',
                size='unidades_vendidas', color='categoria', hover_name='producto',
                title="<b>Impacto Marketing: Costo Pauta vs. Ingresos Anuales</b>",
                labels={'costo_marketing_total': 'Costo Total Marketing ($)', 'ingreso_generado': 'Ingresos Generados ($)'},
                color_discrete_sequence=['#2563eb', '#0d9488', '#f59e0b'],
                template='plotly_white'
            )
            fig_roas.update_layout(height=380, margin=dict(t=50, b=30, l=20, r=20), legend=dict(orientation="h", y=-0.2))
            st.plotly_chart(fig_roas, use_container_width=True)

        # 4. Conclusiones Estratégicas
        st.subheader("📋 Insights y Conclusiones Estratégicas (SynthData)")
        st.success("""
        * **Estabilidad Operativa Anual:** La demanda se mantuvo sólida durante todo el año 2024, superando las 19.400 unidades vendidas tras la depuración de registros.
        * **Diversificación y Mitigación de Riesgos:** Las tres categorías (*Electrodomésticos* 34,4%, *Electrónica* 32,9% y *Decoración* 32,7%) aportan de manera equilibrada a la facturación global.
        * **Eficiencia Publicitaria (ROAS):** Las campañas multicanal (Email, RRSS y TV) impulsaron con alto retorno a los productos líderes (*Lámpara de mesa*, *Auriculares* y *Microondas*).
        * **Independencia Precio-Volumen:** La cantidad de unidades por compra no se ve penalizada por un mayor precio unitario, habilitando estrategias de venta cruzada y paquetes por volumen.
        """)
    # =================================================================
    # PESTAÑA 2: ESTADÍSTICA DESCRIPTIVA Y CORRELACIÓN (ETAPA 3)
    # =================================================================
    with pestana_estadistica:
        st.subheader("📐 Medidas de Tendencia Central y Dispersión")
        cols_num = ['precio', 'cantidad', 'ingreso_total']
        df_est = df_view[cols_num].agg(['mean', 'median', 'min', 'max', 'var', 'std']).T
        df_est.columns = ['Media', 'Mediana', 'Mínimo', 'Máximo', 'Varianza', 'Desvío Estándar']
        df_est['Moda'] = df_view[cols_num].mode().iloc
        df_est['Rango'] = df_est['Máximo'] - df_est['Mínimo']
        df_est['RIC (IQR)'] = df_view[cols_num].quantile(0.75) - df_view[cols_num].quantile(0.25)
        st.dataframe(df_est.round(2), use_container_width=True)

        # Gráfico combinado Boxplot + Histograma de Ingresos
        fig_dist = make_subplots(rows=2, cols=1, shared_xaxes=True, row_heights=[0.25, 0.75], vertical_spacing=0.05)
        fig_dist.add_trace(go.Box(x=df_view['ingreso_total'], name='Dispersión (IQR)', marker_color='#2563eb'), row=1, col=1)
        fig_dist.add_trace(go.Histogram(x=df_view['ingreso_total'], nbinsx=30, name='Frecuencia', marker_color='#60a5fa'), row=2, col=1)
        fig_dist.add_vline(x=df_view['ingreso_total'].mean(), line_dash="dash", line_color="red", annotation_text="Media", row=2, col=1)
        fig_dist.add_vline(x=df_view['ingreso_total'].median(), line_dash="solid", line_color="green", annotation_text="Mediana", row=2, col=1)
        fig_dist.update_layout(title="<b>Distribución y Dispersión de Ingresos por Ticket ($)</b>", height=420, showlegend=False, template='plotly_white')
        st.plotly_chart(fig_dist, use_container_width=True)

        st.divider()
        st.subheader("🔬 Matriz de Correlación de Pearson y Dispersión")
        c_corr1, c_corr2 = st.columns(2)
        with c_corr1:
            corr_matrix = df_view[cols_num].corr().round(2)
            fig_heat = px.imshow(
                corr_matrix, text_auto=True, color_continuous_scale='RdBu_r', zmin=-1, zmax=1,
                title="<b>Mapa de Calor: Correlación entre Variables</b>"
            )
            fig_heat.update_layout(height=380)
            st.plotly_chart(fig_heat, use_container_width=True)

        with c_corr2:
            corr_val = df_view['precio'].corr(df_view['cantidad'])
            fig_scat = px.scatter(
                df_view.sample(min(len(df_view), 400), random_state=42),
                x='precio', y='cantidad', color='categoria',
                title=f"<b>Precio vs. Cantidad (Pearson r = {corr_val:.4f})</b>",
                labels={'precio': 'Precio Unitario ($)', 'cantidad': 'Unidades Vendidas'},
                template='plotly_white'
            )
            fig_scat.update_layout(height=380)
            st.plotly_chart(fig_scat, use_container_width=True)

    # =================================================================
    # PESTAÑA 3: PREPROCESAMIENTO E INTEGRACIÓN (ETAPA 2)
    # =================================================================
    with pestana_preentrega:
        st.subheader("📈 Consolidación Final: Ventas + Categorías + Marketing")
        st.write("Tabla maestra resultante de la limpieza de duplicados/nulos y el cruce interno (`inner merge`) por producto.")

        st.dataframe(df_consolidado.sort_values(by='ingreso_generado', ascending=False).round(2), hide_index=True, use_container_width=True)

        # Botón para descargar el CSV consolidado
        csv_data = df_consolidado.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 Descargar Dataset Consolidado Final (CSV)",
            data=csv_data,
            file_name="df_consolidado_final.csv",
            mime="text/csv"
        )

    # =================================================================
    # PESTAÑA 4: AUDITORÍA DE CALIDAD (ETAPA 1)
    # =================================================================
    with pestana_auditoria:
        st.subheader("🔍 Diagnóstico Inicial de Calidad de Datos")
        m1, m2, m3 = st.columns(3)
        m1.metric("Registros Crudos (ventas.csv)", f"{len(df_v_crudo):,}".replace(",", "."))
        m2.metric("Duplicados Exactos Detectados", f"{df_v_crudo.duplicated().sum()} filas (1,15%)")
        m3.metric("Registros con Nulos Removidos", "2 filas (IDs 627 y 2171)")

        if not df_auditoria.empty:
            st.markdown("### Registro Detallado de Auditoría")
            st.dataframe(df_auditoria, use_container_width=True)
else:
    st.error("❌ No se encontraron los archivos CSV dentro de la carpeta `files/`. Verifica la estructura del repositorio.")
