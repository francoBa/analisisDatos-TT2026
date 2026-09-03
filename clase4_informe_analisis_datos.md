# Informe de hallazgos sobre la calidad de los datos

## 1. Objetivo

El presente informe documenta los principales hallazgos identificados en el archivo [Primer análisis: informe de calidad de datos](./datos_ventas_para_auditoria.csv)
.

El análisis se enfocó en revisar la consistencia, integridad y coherencia general de los registros, sin aplicar procesos de limpieza, transformación o corrección. Por lo tanto, los resultados reflejan el estado original de los datos recibidos.

## 2. Resumen del conjunto de datos

- **Cantidad de registros analizados:** 120
- **Cantidad de columnas:** 10
- **Identificador principal esperado:** `ID_Transaccion`
- **Rango nominal de identificadores:** desde `TXN-1000` hasta `TXN-1119`
- **Cantidad de identificadores únicos:** 118
- **Período declarado en las fechas:** enero y febrero de 2026
- **Campos categóricos principales:** categoría de producto, método de pago y estatus de auditoría

El conjunto presenta una estructura aparentemente transaccional, pero contiene repetición de patrones, inconsistencias de formato, valores faltantes y registros que no resultan coherentes con las reglas habituales de una venta.

## 3. Hallazgos principales

### 3.1 Inconsistencias en los formatos de fecha

La columna `Fecha_Venta` presenta múltiples formatos para representar fechas:

| Formato o tipo de valor | Ejemplo | Cantidad aproximada |
|---|---|---:|
| `AAAA-MM-DD` válido | `2026-01-15` | 60 |
| `AAAA/MM/DD` | `2026/01/16` | 12 |
| `DD-MM-AAAA` | `17-01-2026` | 12 |
| `AAAA.MM.DD` | `2026.01.18` | 12 |
| Fecha calendario inválida | `2026-02-31` | 12 |
| Texto no interpretable como fecha | `INVALID_DATE` | 12 |

Se identificaron **60 registros con fechas en formatos alternativos o inválidos**. Además, `2026-02-31` utiliza una estructura similar al formato ISO, pero representa una fecha inexistente en el calendario.

La presencia de `INVALID_DATE` impide interpretar directamente la fecha de venta, mientras que las fechas con separadores distintos pueden producir resultados diferentes dependiendo de la herramienta utilizada para importar el archivo.

### 3.2 Registros duplicados y problemas con la clave única

El campo `ID_Transaccion` no se comporta como una clave única en todos los registros.

Se observó que:

- `TXN-1005` aparece **tres veces**.
- Existen identificadores esperados que no aparecen, entre ellos `TXN-1015` y `TXN-1028`.
- La cantidad total de registros es 120, pero solo se identifican 118 valores únicos en `ID_Transaccion`.

La repetición de `TXN-1005` es especialmente relevante porque aparece asociado a datos diferentes en una de sus ocurrencias. En un registro se relaciona con un cliente sin nombre, mientras que en otras apariciones se vincula con `Empresa ACME S.A.`.

También se observan bloques de transacciones que repiten la misma combinación de cliente, fecha, categoría, cantidades, precios y método de pago. Aunque los identificadores sean diferentes, esta repetición puede dificultar la distinción entre transacciones realmente independientes y registros replicados.

### 3.3 Problemas de estandarización de nombres y espacios

La columna `Cliente_Nombre` presenta diferencias de formato y escritura para clientes que aparentemente podrían representar a la misma persona o empresa.

Ejemplos observados:

- ` Juan Pérez ` contiene espacios al inicio y al final.
- `Juan Perez` aparece sin tilde.
- `MARIA GOMEZ` está completamente escrito en mayúsculas.
- `Carlos López` y `carlos lopez` presentan diferencias de mayúsculas, minúsculas y acentuación.
- `Empresa ACME S.A.` y `Empresa ACME` representan variantes del nombre de una misma empresa.
- `Empresa ACME` seguido de `SA` aparece separado por un salto de línea.
- `Ana` y `Martínez` también aparecen separados por un salto de línea.

Estas diferencias generan múltiples representaciones textuales para clientes que podrían ser equivalentes. Como consecuencia, los conteos por cliente podrían quedar fragmentados y producir una cantidad de clientes aparentemente superior a la real.

### 3.4 Valores atípicos en cantidades, precios y totales

La columna `Cantidad` contiene valores que se apartan del comportamiento esperado para una venta:

- **12 registros con cantidad negativa:** `-3.0`.
- **12 registros con cantidad igual a cero:** `0.0`.
- **1 registro con cantidad faltante.**
- **12 registros con cantidad igual a `10000.0`**, considerablemente superior al resto de las cantidades observadas.

La cantidad `10000.0` genera un total calculado de `150000.0`, convirtiéndose en un valor extremo dentro del conjunto.

También se observa un precio unitario de `1200.0`, que produce un total de `12000.0` para una cantidad de 10 unidades. Este valor se encuentra por encima de la mayoría de los precios unitarios registrados.

Los valores atípicos identificados no necesariamente representan errores por sí mismos, pero requieren una revisión porque pueden modificar significativamente los análisis de ventas, promedios y distribución de importes.

### 3.5 Valores faltantes, nulos y marcadores de ausencia

Se identificaron valores faltantes o equivalentes a información ausente en varias columnas:

| Columna | Situación identificada | Cantidad |
|---|---|---:|
| `Cliente_Nombre` | Campo vacío | 1 |
| `RFC_NIT` | Campo vacío | 1 |
| `RFC_NIT` | Valor `N/A` | 12 |
| `Cantidad` | Campo vacío | 1 |
| `Precio_Unitario` | Campo vacío | 12 |

Además de los campos vacíos, se utilizan expresiones como `N/A` para indicar ausencia de información. Esto implica que la falta de datos no está representada de una única manera.

El registro asociado con `Pedro Picapiedra` presenta simultáneamente:

- `RFC_NIT = N/A`
- `Precio_Unitario` vacío
- `Metodo_Pago = Desconocido`
- `Categoria_Producto = ERROR_CAT`

La concentración de varias anomalías en los mismos registros aumenta su nivel de riesgo para análisis posteriores.

### 3.6 Categorías de producto no autorizadas o inconsistentes

Las categorías esperadas parecen ser:

- `Electrónica`
- `Hogar`
- `Ropa`
- `Alimentos`

Sin embargo, se encontraron las siguientes variantes:

| Valor observado | Tipo de inconsistencia |
|---|---|
| `Hogar ` | Espacio al final |
| `hogar` | Uso de minúsculas |
| `ROPA` | Uso de mayúsculas |
| ` Alimentos` | Espacio al inicio |
| `ERROR_CAT` | Categoría no autorizada o de error |

La categoría `ERROR_CAT` aparece en 12 registros, por lo que no se trata de un caso aislado.

Estas variaciones hacen que una misma categoría pueda ser contabilizada como si fueran varias categorías diferentes. Además, `ERROR_CAT` no pertenece al conjunto de categorías comerciales esperado y debe considerarse un hallazgo explícito del análisis.

### 3.7 Inconsistencias en los métodos de pago

La columna `Metodo_Pago` presenta diferencias de escritura y valores fuera del conjunto habitual:

| Valor observado | Cantidad aproximada |
|---|---:|
| `Tarjeta` | 24 |
| `tarjeta` | 12 |
| `Efectivo` | 24 |
| `EFECTIVO` | 12 |
| `Transferencia` | 24 |
| `BTC_CRYPTO` | 12 |
| `Desconocido` | 12 |

Los métodos `tarjeta` y `EFECTIVO` representan variantes de escritura de métodos ya existentes. Además, `BTC_CRYPTO` y `Desconocido` no forman parte del grupo principal de medios de pago observados.

La existencia de `Desconocido` es consistente con un dato no identificado, mientras que `BTC_CRYPTO` introduce una categoría adicional que debería confirmarse contra las reglas del negocio.

### 3.8 Inconsistencias entre cantidad, precio unitario y total calculado

En la mayoría de los registros, el campo `Total_Calculado` coincide con la multiplicación de `Cantidad` por `Precio_Unitario`. Sin embargo, existen situaciones que requieren atención:

- Para una cantidad de `-3.0` y un precio unitario de `50.0`, el total informado es `150.0`. Desde el punto de vista aritmético, la multiplicación directa produciría `-150.0`.
- Para una cantidad de `4.0` y un precio unitario faltante, el total informado es `0.0`.
- Para una cantidad de `0.0`, el total informado es `0.0`, aunque la existencia de la operación puede resultar atípica.
- El precio `"150,00"` utiliza coma decimal dentro de un campo numérico, mientras que el resto de los valores usa punto decimal.

Estos casos dificultan determinar si el total representa un cálculo automático, un importe ajustado manualmente o una cifra cargada independientemente de los demás campos.

### 3.9 Inconsistencias en los identificadores RFC/NIT

La columna `RFC_NIT` contiene valores con características diferentes:

- Identificadores alfanuméricos aparentemente estructurados, como `ABC123456XYZ`.
- Un valor numérico de nueve dígitos: `999999999`.
- El marcador `N/A`.
- Un campo vacío.

El valor `999999999` aparece asociado a `Empresa ACME`, mientras que en otros registros de la misma empresa se utiliza `ACM900101AAA`. Esta diferencia podría indicar un identificador inválido, genérico o perteneciente a otra estructura.

También se identifican registros en los que el mismo RFC/NIT aparece asociado a distintas variantes de escritura del nombre del cliente.

### 3.10. Inconsistencias en el estatus de auditoría

Todos los registros presentan el valor:

~~~text
Estatus_Auditoria = Aprobado
~~~

Esto incluye registros con:

- Fechas inválidas o no interpretables.
- Cantidades negativas.
- Cantidades iguales a cero.
- Campos obligatorios faltantes.
- Categorías no autorizadas.
- Métodos de pago desconocidos.
- Identificadores duplicados.
- Precios unitarios ausentes.
- Valores extremos.

La uniformidad del estatus resulta inconsistente con la cantidad de anomalías detectadas. Esto sugiere que el estado de auditoría no estaría reflejando efectivamente la calidad o validez de cada transacción.

## 4. Resumen cuantitativo de anomalías

| Tipo de hallazgo | Registros afectados o casos observados |
|---|---:|
| Formatos de fecha alternativos o inválidos | 60 |
| Fechas explícitamente no interpretables | 12 |
| Fechas calendario inválidas | 12 |
| Identificadores de transacción duplicados | 1 identificador repetido |
| Registros con `ID_Transaccion` no únicos | 2 registros adicionales |
| Cantidades negativas | 12 |
| Cantidades iguales a cero | 12 |
| Cantidades faltantes | 1 |
| Cantidades extremas de `10000.0` | 12 |
| Precios unitarios faltantes | 12 |
| RFC/NIT informado como `N/A` | 12 |
| RFC/NIT faltante | 1 |
| Categoría `ERROR_CAT` | 12 |
| Métodos de pago no habituales o desconocidos | 24 |
| Variantes de mayúsculas, minúsculas o espacios | Varias columnas |
| Registros con estatus `Aprobado` pese a presentar anomalías | 120 |

## 5. Consideraciones sobre la estructura del archivo

Además de los valores anómalos, se observaron saltos de línea dentro de algunos nombres de clientes, por ejemplo:

~~~text
Empresa ACME
SA
~~~

También se observó el siguiente caso:

~~~text
Ana
Martínez
~~~

Esto puede afectar la interpretación del archivo como CSV o texto delimitado, ya que un salto de línea interno puede confundirse con el inicio de un nuevo registro si no se encuentra correctamente encapsulado.

También se observa un precio unitario con coma decimal y entre comillas:

~~~text
"150,00"
~~~

Esto introduce una representación numérica distinta a la utilizada en el resto de la columna.

## 6. Conclusión

El archivo presenta problemas en varias dimensiones de calidad de datos:

- **Consistencia:** se utilizan diferentes formatos para fechas, nombres, categorías y métodos de pago.
- **Integridad:** existen campos vacíos, valores `N/A` y precios faltantes.
- **Validez:** se observan fechas inexistentes, cantidades negativas, categorías no autorizadas y métodos de pago desconocidos.
- **Unicidad:** el identificador de transacción `TXN-1005` se encuentra repetido.
- **Coherencia:** algunos totales no coinciden con la interpretación aritmética directa de cantidad y precio unitario.
- **Estructura:** existen posibles saltos de línea embebidos dentro de los nombres.
- **Control de auditoría:** todos los registros están marcados como `Aprobado`, incluso aquellos que contienen anomalías evidentes.

En su estado actual, los datos pueden utilizarse para identificar patrones de calidad y documentar incidencias, pero los resultados de análisis agregados —como ventas por cliente, categoría, método de pago o período— podrían verse afectados por estas inconsistencias.