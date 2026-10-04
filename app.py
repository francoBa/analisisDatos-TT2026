from pathlib import Path

import numpy as np
import pandas as pd
import streamlit as st


ARCHIVO = Path(__file__).parent / "datos_ventas_para_auditoria.csv"

st.set_page_config(
    page_title="Análisis de calidad de datos",
    page_icon="📊",
    layout="wide",
)

st.title("Análisis de calidad de datos")
st.write("Proyecto académico desarrollado durante Talento Tech 2026.")

# Lectura del archivo
df = pd.read_csv(ARCHIVO, keep_default_na=False)

# Conversión temporal para el análisis (Series de Pandas)
cantidad = pd.to_numeric(df["Cantidad"], errors="coerce")

precio = pd.to_numeric(
    df["Precio_Unitario"]
    .astype(str)
    .str.replace(",", ".", regex=False),
    errors="coerce",
)

fecha = df["Fecha_Venta"].astype(str).str.strip()

# Reglas de análisis
categorias_autorizadas = {
    "Electrónica",
    "Hogar",
    "Ropa",
    "Alimentos",
}

metodos_autorizados = {
    "Tarjeta",
    "Efectivo",
    "Transferencia",
}

categorias_no_autorizadas = (
    ~df["Categoria_Producto"].isin(categorias_autorizadas)
).sum()

metodos_no_habituales = (
    ~df["Metodo_Pago"].isin(metodos_autorizados)
).sum()

ids_duplicados = df["ID_Transaccion"].duplicated(keep=False).sum()
ids_repetidos = df["ID_Transaccion"].duplicated().sum()

fechas_invalidas = (
    fecha.eq("INVALID_DATE") |
    fecha.eq("2026-02-31")
).sum()

fechas_formato_alternativo = (
    fecha.str.match(r"^\d{4}/\d{2}/\d{2}$", na=False) |
    fecha.str.match(r"^\d{2}-\d{2}-\d{4}$", na=False) |
    fecha.str.match(r"^\d{4}\.\d{2}\.\d{2}$", na=False)
).sum()

campos_faltantes = (
    df.replace(r"^\s*$", np.nan, regex=True)
    .isna()
    .sum()
    .sort_values(ascending=False)
)

cantidad_negativa = (cantidad < 0).sum()
cantidad_cero = (cantidad == 0).sum()
cantidad_extrema = (cantidad == 10000).sum()

# Detección de valores atípicos mediante IQR
cantidad_valida = cantidad.dropna()

if len(cantidad_valida) > 0:
    q1, q3 = np.percentile(cantidad_valida, [25, 75])
    iqr = q3 - q1
    limite_superior = q3 + 1.5 * iqr
    valores_atipicos = (cantidad > limite_superior).sum()
else:
    valores_atipicos = 0

# Filtros laterales
st.sidebar.header("Filtros")

categorias_disponibles = sorted(
    df["Categoria_Producto"].astype(str).unique()
)

categorias_seleccionadas = st.sidebar.multiselect(
    "Categoría",
    categorias_disponibles,
    default=categorias_disponibles,
)

metodos_disponibles = sorted(
    df["Metodo_Pago"].astype(str).unique()
)

metodos_seleccionados = st.sidebar.multiselect(
    "Método de pago",
    metodos_disponibles,
    default=metodos_disponibles,
)

estatus_disponibles = sorted(
    df["Estatus_Auditoria"].astype(str).unique()
)

estatus_seleccionados = st.sidebar.multiselect(
    "Estatus de auditoría",
    estatus_disponibles,
    default=estatus_disponibles,
)

df_filtrado = df[
    df["Categoria_Producto"].isin(categorias_seleccionadas)
    & df["Metodo_Pago"].isin(metodos_seleccionados)
    & df["Estatus_Auditoria"].isin(estatus_seleccionados)
]

# Indicadores principales
st.subheader("Resumen general")

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Registros",
    len(df_filtrado),
    f"de {len(df)} totales",
)

col2.metric(
    "Columnas",
    len(df.columns),
)

col3.metric(
    "IDs únicos",
    df["ID_Transaccion"].nunique(),
)

col4.metric(
    "IDs duplicados",
    ids_duplicados,
)

# Hallazgos principales
st.subheader("Principales hallazgos")

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Valores faltantes",
    int(campos_faltantes.sum()),
)

col2.metric(
    "Categorías no autorizadas",
    categorias_no_autorizadas,
)

col3.metric(
    "Métodos no habituales",
    metodos_no_habituales,
)

col4.metric(
    "Valores atípicos",
    int(valores_atipicos),
)

# Pestañas del análisis
tab1, tab2, tab3, tab4, tab5, tab_almacen, tab_etapa2 = st.tabs(
    [
        "Vista de datos",
        "Fechas",
        "Valores faltantes",
        "Categorías y pagos",
        "Valores atípicos",
        "Pre Entrega - Carga",
        "Pre Entrega - Resultados (Etapa 2)"
    ]
)

with tab1:
    st.subheader("Datos filtrados")
    st.dataframe(df_filtrado, width="stretch")

with tab2:
    st.subheader("Hallazgos en fechas")

    fechas_df = pd.DataFrame(
        {
            "Tipo de hallazgo": [
                "Fechas explícitamente inválidas",
                "Fechas con formatos alternativos",
                "Fechas en formato AAAA-MM-DD",
            ],
            "Cantidad": [
                fechas_invalidas,
                fechas_formato_alternativo,
                len(df) - fechas_invalidas - fechas_formato_alternativo,
            ],
        }
    )

    st.dataframe(fechas_df, hide_index=True, width="stretch")
    st.bar_chart(fechas_df.set_index("Tipo de hallazgo"))

with tab3:
    st.subheader("Valores faltantes por columna")

    faltantes_df = (
        campos_faltantes
        .rename("Cantidad")
        .reset_index()
        .rename(columns={"index": "Columna"})
    )

    st.dataframe(faltantes_df, hide_index=True, width="stretch")
    st.bar_chart(faltantes_df.set_index("Columna"))

with tab4:
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Categorías")
        categorias = df_filtrado["Categoria_Producto"].value_counts()
        st.bar_chart(categorias)
        st.dataframe(
            categorias.rename("Cantidad").reset_index(),
            hide_index=True,
            width="stretch",
        )

    with col2:
        st.subheader("Métodos de pago")
        metodos_pago = df_filtrado["Metodo_Pago"].value_counts()
        st.bar_chart(metodos_pago)
        st.dataframe(
            metodos_pago.rename("Cantidad").reset_index(),
            hide_index=True,
            width="stretch",
        )

with tab5:
    st.subheader("Cantidades y valores atípicos")

    atipicos_df = pd.DataFrame(
        {
            "Tipo de hallazgo": [
                "Cantidades negativas",
                "Cantidades iguales a cero",
                "Cantidad igual a 10000",
                "Precios unitarios faltantes",
            ],
            "Cantidad": [
                cantidad_negativa,
                cantidad_cero,
                cantidad_extrema,
                int(precio.isna().sum()),
            ],
        }
    )

    st.dataframe(atipicos_df, hide_index=True, width="stretch")
    st.bar_chart(atipicos_df.set_index("Tipo de hallazgo"))

    st.write(
        f"El límite superior calculado mediante IQR para la columna "
        f"`Cantidad` es: **{limite_superior:.2f}**."
    )

with tab_almacen:
    st.subheader("Programa de Registro y Almacenamiento de Ventas")
    st.markdown("**Estructura utilizada:** Lista de Diccionarios (`list[dict]`) en `st.session_state`.")

    # Inicializar la lista en memoria si no existe
    if "almacen_ventas" not in st.session_state:
        st.session_state.almacen_ventas = []

    # Formulario interactivo para almacenar datos (variables renombradas para evitar colisión)
    with st.form("form_nueva_venta", clear_on_submit=True):
        col_p, col_pr, col_c = st.columns(3)
        input_prod = col_p.text_input("Producto")
        input_prec = col_pr.number_input("Precio ($)", min_value=0.01, step=1.0)
        input_cant = col_c.number_input("Cantidad", min_value=1, step=1)

        btn_guardar = st.form_submit_button("Almacenar Venta")

        if btn_guardar:
            if input_prod.strip():
                # Se almacena en la estructura elegida
                nueva_venta = {
                    "producto": input_prod.strip(),
                    "precio": float(input_prec),
                    "cantidad": int(input_cant),
                }
                st.session_state.almacen_ventas.append(nueva_venta)
                st.success(f"Venta de '{input_prod}' almacenada con éxito.")
            else:
                st.error("El nombre del producto no puede estar vacío.")

    # Mostrar la estructura almacenada
    if st.session_state.almacen_ventas:
        df_almacen = pd.DataFrame(st.session_state.almacen_ventas)
        df_almacen["Subtotal"] = df_almacen["precio"] * df_almacen["cantidad"]
        st.dataframe(df_almacen, width="stretch")
        st.metric("Total Almacenado", f"${df_almacen['Subtotal'].sum():,.2f}")


with tab_etapa2:
    st.subheader("Resultados Consolidados: Preprocesamiento e Integración")
    st.markdown("Consolidación analítica de la **Etapa 2** sobre los datasets `ventas.csv` y `marketing.csv`.")

    ruta_v = Path(__file__).parent / "files" / "ventas.csv"
    ruta_m = Path(__file__).parent / "files" / "marketing.csv"

    if ruta_v.exists() and ruta_m.exists():
        # Carga y limpieza directa para la vista ejecutiva
        v_df = pd.read_csv(ruta_v).drop_duplicates().dropna(subset=["precio", "cantidad"])
        v_df["precio"] = v_df["precio"].astype(str).str.replace("$", "", regex=False).str.strip().astype(float)
        v_df["cantidad"] = v_df["cantidad"].astype(int)
        v_df["ingreso_total"] = v_df["precio"] * v_df["cantidad"]

        m_df = pd.read_csv(ruta_m)

        # 1. Métricas de impacto de la limpieza
        m1, m2, m3 = st.columns(3)
        m1.metric("Transacciones Depuradas", f"{len(v_df):,}", "35 duplicados y 2 nulos removidos")
        m2.metric("Facturación Neta Total", f"$ {v_df['ingreso_total'].sum():,.2f}")
        m3.metric("Unidades Totales Vendidas", f"{v_df['cantidad'].sum():,} uds")

        st.divider()

        # 2. Gráfico y tabla: Ventas por Categoría
        st.subheader("1. Ventas por Categoría de Producto")
        cat_df = v_df.groupby("categoria")["ingreso_total"].sum().reset_index()
        cat_df.columns = ["Categoría", "Ingresos Totales ($)"]

        col_g1, col_g2 = st.columns([3, 2])
        with col_g1:
            st.bar_chart(cat_df.set_index("Categoría"), color="#29b5e8", width="stretch")
        with col_g2:
            st.dataframe(cat_df, width="stretch", hide_index=True)

        st.divider()

        # 3. Productos de Alto Rendimiento
        st.subheader("2. Productos de Alto Rendimiento (Por encima de la media)")
        prod_df = v_df.groupby("producto").agg(
            ingreso_total=("ingreso_total", "sum"),
            unidades=("cantidad", "sum"),
            operaciones=("id_venta", "count")
        ).reset_index()

        umbral = prod_df["ingreso_total"].mean()
        alto_rendimiento = prod_df[prod_df["ingreso_total"] > umbral].sort_values(by="ingreso_total", ascending=False)
        st.caption(f"Umbral de corte (media de facturación por producto): **${umbral:,.2f}**")
        st.dataframe(alto_rendimiento, width="stretch", hide_index=True)

        st.divider()

        # 4. Integración: Ventas vs Marketing (ROAS)
        st.subheader("3. Integración Comercial vs. Inversión en Marketing")
        mkt_prod = m_df.groupby("producto").agg(
            costo_marketing=("costo", "sum"),
            canales=("canal", lambda x: ", ".join(sorted(x.unique())))
        ).reset_index()

        integrado = pd.merge(prod_df, mkt_prod, on="producto", how="inner")
        integrado["retorno_por_peso"] = integrado["ingreso_total"] / integrado["costo_marketing"]
        integrado = integrado.sort_values(by="retorno_por_peso", ascending=False)

        st.dataframe(
            integrado[["producto", "canales", "ingreso_total", "costo_marketing", "retorno_por_peso"]],
            width="stretch",
            hide_index=True
        )
    else:
        st.warning("No se encontraron los archivos en la carpeta `files/`. Verifica que existan `files/ventas.csv` y `files/marketing.csv`.")


# Resumen de auditoría
st.subheader("Estatus de auditoría")

auditoria = df["Estatus_Auditoria"].value_counts()

st.bar_chart(auditoria)
st.dataframe(
    auditoria.rename("Cantidad").reset_index(),
    hide_index=True,
    width="stretch",
)

if len(auditoria) == 1 and auditoria.index[0] == "Aprobado":
    st.warning(
        "Todos los registros presentan el estatus 'Aprobado', "
        "incluidos aquellos que contienen anomalías."
    )

# Registros duplicados
st.subheader("Registros con identificadores duplicados")

duplicados = df[
    df["ID_Transaccion"].duplicated(keep=False)
].sort_values("ID_Transaccion")

if duplicados.empty:
    st.success("No se encontraron identificadores duplicados.")
else:
    st.dataframe(duplicados, hide_index=True, width="stretch")
    st.info(
        f"Se encontraron {ids_repetidos} identificador(es) repetido(s) "
        f"y {ids_duplicados} registro(s) involucrado(s)."
    )