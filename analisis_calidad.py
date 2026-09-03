import numpy as np
import pandas as pd
import polars as pl


ARCHIVO = "datos_ventas_para_auditoria.csv"


# Pandas: herramienta principal para el análisis exploratorio
df = pd.read_csv(ARCHIVO, keep_default_na=False)

print("\n=== RESUMEN GENERAL ===")
print(f"Registros: {len(df)}")
print(f"Columnas: {len(df.columns)}")
print(f"IDs únicos: {df['ID_Transaccion'].nunique()}")
print(f"IDs duplicados: {df['ID_Transaccion'].duplicated().sum()}")

print("\n=== FECHAS ===")
fecha = df["Fecha_Venta"].astype(str).str.strip()

print(f"Fechas no interpretables: {(fecha == 'INVALID_DATE').sum()}")
print(f"Fechas calendario inválidas: {(fecha == '2026-02-31').sum()}")
print(f"Fechas con formato AAAA/MM/DD: {fecha.str.match(r'^\\d{4}/\\d{2}/\\d{2}$').sum()}")
print(f"Fechas con formato DD-MM-AAAA: {fecha.str.match(r'^\\d{2}-\\d{2}-\\d{4}$').sum()}")
print(f"Fechas con formato AAAA.MM.DD: {fecha.str.match(r'^\\d{4}\\.\\d{2}\\.\\d{2}$').sum()}")

print("\n=== VALORES FALTANTES ===")
for columna in ["Cliente_Nombre", "RFC_NIT", "Cantidad", "Precio_Unitario"]:
    vacios = df[columna].astype(str).str.strip().eq("").sum()
    print(f"{columna}: {vacios}")

print(f"RFC/NIT con N/A: {(df['RFC_NIT'].str.upper() == 'N/A').sum()}")

print("\n=== CATEGORÍAS ===")
categorias_autorizadas = {
    "Electrónica",
    "Hogar",
    "Ropa",
    "Alimentos",
}

categorias = df["Categoria_Producto"].astype(str)
no_autorizadas = ~categorias.isin(categorias_autorizadas)

print(f"Categorías no autorizadas: {no_autorizadas.sum()}")
print("Valores encontrados:")
print(df["Categoria_Producto"].value_counts(dropna=False).to_string())

print("\n=== MÉTODOS DE PAGO ===")
metodos_autorizados = {
    "Tarjeta",
    "Efectivo",
    "Transferencia",
}

metodos = df["Metodo_Pago"].astype(str)
no_habituales = ~metodos.isin(metodos_autorizados)

print(f"Métodos no habituales o desconocidos: {no_habituales.sum()}")
print(df["Metodo_Pago"].value_counts(dropna=False).to_string())

print("\n=== CANTIDADES Y VALORES ATÍPICOS ===")
cantidad = pd.to_numeric(df["Cantidad"], errors="coerce")
precio = pd.to_numeric(
    df["Precio_Unitario"].astype(str).str.replace(",", ".", regex=False),
    errors="coerce",
)

print(f"Cantidades negativas: {(cantidad < 0).sum()}")
print(f"Cantidades iguales a cero: {(cantidad == 0).sum()}")
print(f"Cantidad faltante: {cantidad.isna().sum()}")
print(f"Cantidad igual a 10000: {(cantidad == 10000).sum()}")
print(f"Precio unitario faltante: {precio.isna().sum()}")

# NumPy: detección de valores atípicos mediante el rango intercuartílico
valores = cantidad.dropna().to_numpy()
q1, q3 = np.percentile(valores, [25, 75])
iqr = q3 - q1
limite_superior = q3 + 1.5 * iqr
atipicos = valores > limite_superior

print(f"Valores atípicos según IQR: {atipicos.sum()}")

print("\n=== ESTATUS DE AUDITORÍA ===")
print(df["Estatus_Auditoria"].value_counts(dropna=False).to_string())

# Polars: resumen rápido de la estructura del archivo
df_polars = pl.read_csv(ARCHIVO)

print("\n=== RESUMEN CON POLARS ===")
print(f"Filas: {df_polars.height}")
print(f"Columnas: {df_polars.width}")