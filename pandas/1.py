import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt


# series (int64 - arrays de numpy)
edades = pd.Series(
    # data=
    [25, 30, 22, 35],
    # index= (si no agrego índice, pandas genera una secuencia)
    ['Ana', 'Luis', 'Carlos', 'Sofía']
)

#print(edades)

#print('-'*20)

#dict
data = {
    'Nombre': ['Ana', 'Luis', 'Carlos', 'Sofía'],
    'Edad': [25, 30, 22, 35],
    'Ciudad': ['Madrid', 'Barcelona', 'Valencia', 'Sevilla']
}

#print(type(data))

# DataFrame (pandas.DataFrame)
# cada columna es una serie
# además genera un índice de una secuencia
df = pd.DataFrame(
    #data=
    data
    #, index=['uno', 'dos', 'tres', 'cuatro'] (se podría personalizar el índice de ser necesario)
)

#print(df)
#print(type(df))

#print('-'*20)

cols = ['PassengerId', 'Survived', 'Pclass', 'Name', 'Sex', 'Age', 'Fare', 'Cabin', 'Ticket', 'Embarked']

nulls = ['NA', 'N/A', 'missing', '', '-']

# crear un DataFrame desde un archivo csv
# se puede especificar el tipo de separador (, sep=';')
# se puede especificar las columnas que usaremos para el análisis
# se puede especificar la lista de posibles valores a considerarse como nulos
# se puede especificar el número de filas que queremos leer con nrows
# se puede especificar si se desea saltar filas con skiprows
titanic = pd.read_csv(
    'Titanic-Dataset.csv'
    , usecols=cols
    , na_values=nulls
    , nrows=100
    # , skiprows=2
)

#print(type(titanic))

# total de filas y columnas
#print(titanic.shape)

# primeras 5 filas (NaN = nulos)
#print(titanic.head())

# estructura del DataFrame (tipo columnas, conteo de no nulos, etc)
#print(titanic.info())

# resumen de estadísticas de cada columna
#print(titanic.describe())

# Análisis de datos

#sobrevivieron = titanic['Survived']

#tasa = round(sobrevivieron.mean() * 100, 2)

#print(f'sobrevivieron {tasa} %')

#print(titanic.head(3))

# obtener la suma de todos los nulos de cada columna
#print(titanic.isna().sum())


# leer desde un archivo xlsx (requiere instalar la librería openxls pero sin importala)
# openxls sólo sirve para los formatos modernos xlsx y no los anteriores
# para los anteriores podemos usar python-calamine que es inclusive más rápido
# df_excel = pd.read_excel('Titanic-Dataset.xls', engine='calamine')

# print(df_excel.shape)

# print(df_excel.head())


# leer últimas 5 filas
#print(titanic.tail())

# otro tipo de descripción usando un parámetro include=
# nos da datos muy valiosos para el análisis
#print(titanic.describe(include='str'))

# otra forma de referenciar una columna por su nombre
edades = titanic.Age.head()

#print(edades)

# estadísticas básicas de la columna Age
# print(f'Media de edad: {titanic.Age.mean():.1f}')
# print(f'Edad máxima: {titanic.Age.max()}')
# print(f'Edad mínima: {titanic.Age.min()}')
# print(f'Mediana: {titanic.Age.median()}')

# multiplicar toda una columna (matriz por escalar)
fare_euros = titanic.Fare * 0.85
#print(f'\nPrecio medio en euros: {fare_euros.mean():.2f}')

# agregar una nueva columna calculada
titanic['Fare_EUR'] = titanic.Fare * 1.18

# mostrar las 2 columnas, la limitamos a los primeros 5 resultados
#print(titanic[['Fare_EUR', 'Fare']].head())

# generamos un nuevo .csv con los datos modificados (limpieza)
# usamos index=Flase para que no agregue otra columna de indices, ya que tenemos una columna en el csv original con los ids
#titanic.to_csv('titanic_euros.csv', index=False)

# borrar una columna que no nos sirve para el análisis
# usamos axis=1 para decir que efectivamente es una columna lo que queremos borrar
#titanic = titanic.drop('Cabin', axis=1)

# eliminar varias columnas
#titanic = titanic.drop(['Ticket', 'PassengerId'], axis=1)

# mostrar los nombres de las columnas
#print(titanic.columns)

# ver cuantas columnas tenemos (el 2do valor de la tupla que devuelve shape)
#print(titanic.shape[1])

# ver cuantas filas tenemos
#print(titanic.shape[0])

# eliminar una fila, axis=0 nos dice que son filas las que queremos borrar
#titanic = titanic.drop(0, axis=0)

# eliminar varias filas (usamos los índices)
#titanic = titanic.drop([1, 2, 3], axis=0)
# también podemos eliminar usando un rango
#titanic = titanic.drop(range(4, 90, 5), axis=0)

#print(titanic.head())
#print(titanic.shape)

# nuevo orden (mover una columna)
nuevo_orden = ['Survived', 'Name', 'Sex', 'Age', 'Pclass', 'Fare', 'Embarked']

titanic_reord = titanic[nuevo_orden]

#print(titanic_reord.head(3))

# usando loc para obtener los valores de un rango
#print(titanic_reord.loc[0, 'Name'])
# usamos slice pero en este caso pandas si toma en cuenta el último índice, no como python
#print(titanic_reord.loc[0:4, 'Name'])
# vemos más columnas
# print(titanic_reord.loc[0:4, ['Name', 'Age']])

# buscamos un nombre específico en lugar de índices
pasajero = titanic_reord.loc[titanic_reord.Name == 'Braund, Mr. Owen Harris']

# especificar que columnas queremos de la fila encontrada
pasajero = pasajero[['Survived', 'Pclass', 'Age', 'Sex']]

#print(pasajero)

supervivientes = titanic_reord.loc[titanic_reord['Survived'] == 1, ['Name', 'Sex', 'Age', 'Fare']]
#print(f'Supervivientes: {len(supervivientes)}')
#print(supervivientes.head(4))

murieron = titanic_reord.loc[titanic_reord['Survived'] == 0, ['Name', 'Sex', 'Age']]
#print(f'Muertos: {len(murieron)}')
#print(murieron.head())

# modificar datos con loc
#print(f'Edad fila 5 antes: {titanic_reord.loc[5, 'Age']}')

titanic_reord.loc[5, 'Age'] = 30.0

#print(f'Edad fila 5 después: {titanic_reord.loc[5, 'Age']}')

# usando iloc (índice en memoria, no etiqueta de índice)
#print(titanic_reord.head())
titanic_reord =  titanic_reord.drop(0, axis=0)
# este comando restablece el índice de etiquetas luego del borrado anterior para poder usar loc y la posición 0
titanic_reord = titanic_reord.reset_index(drop=True)
#print(titanic_reord.head())
#print(titanic_reord.iloc[0]) # lee el primer registro, sin importar que el índice sea 0 o 1
#print(titanic_reord.loc[0]) # error porque indice 0 ya se eliminó

# buscando valores
mujeres = titanic_reord[titanic_reord['Sex'] == 'female']
#print(f'Mujeres en el titanic: {len(mujeres)}')
#print(mujeres[['Name', 'Sex', 'Age']].head(3))

mayores = titanic_reord[titanic_reord['Age'] > 60]
# print(f'Pasajeros mayores de 60 años: {len(mayores)}')
# print(mayores[['Name', 'Age', 'Survived']].head())

primera_segunda = titanic_reord[titanic_reord['Pclass'].isin([1, 2])]
# print(f'Pasajeros de 1ra o 2da clase: {len(primera_segunda)}')
# print(primera_segunda['Pclass'].value_counts()) # agrupa

# print(f'Total supervivientes: {len(supervivientes)}')
# print(supervivientes.head(4))

mujeres_sobrevivieron = titanic_reord[(titanic_reord['Sex'] == 'female') & (titanic_reord['Survived'] == 1)]
# print(f'Mujeres sobrevivieron: {len(mujeres_sobrevivieron)}')
# print(mujeres_sobrevivieron[['Name', 'Sex', 'Survived']].head())

jovenes_o_ancianos = titanic_reord[(titanic_reord['Age'] < 18) | (titanic_reord['Age'] > 60)]
# print(jovenes_o_ancianos[['Name', 'Age', 'Survived']].head(10))

no_primera = titanic_reord[ ~ (titanic_reord['Pclass'] == 1)]
# print(f'Pasajeros que no eran de 1ra clase: {len(no_primera)}')
# print(no_primera[['Name', 'Pclass']].head())

# consulta compleja
filtro = (
    (
        (titanic_reord['Sex'] == 'female') 
        & (titanic_reord['Survived'] == 1) 
        & (titanic_reord['Pclass'] != 1)
    ) 
    | (titanic_reord['Age'] < 10)
)

resultado = titanic_reord[filtro]
# print(f'Resultado: {len(resultado)} pasajeros')
# print(resultado[['Name', 'Sex', 'Age', 'Pclass', 'Survived']].head(10))


# nulos
nulos = titanic_reord.isna()
# print(nulos.head()) # lo que figura como True tiene en el campo NaN
# print(nulos.sum())
# print(round(titanic_reord.isna().sum() / len(titanic_reord) * 100, 2))

# sacando los nulos
titanic_sin_nulos = titanic_reord.dropna()
# print(f'Filas después del dropna: {len(titanic_sin_nulos)}')

# eliminar si tienen nulos en 'Age' o 'Embarked'
titanic_filtrado = titanic.dropna(subset=['Age', 'Embarked'])
# print(f'1. dropna(subset=["Age", "Embarked"]): {len(titanic_filtrado)} filas')

# eliminar si todas las columnas son nulas
titanic_todos_nulos = titanic.dropna(how='all')
# print(f'2. dropna(how="all"): {len(titanic_todos_nulos)} filas')

# Mantener filas con al menos 10 valores no nulos
titanic_thresh = titanic.dropna(thresh=10)
# print(f'3. dropna(thresh=10): {len(titanic_thresh)} filas')

# muestra todas las filas
pd.set_option('display.max_rows', None)

mapa_nulos = titanic[['Embarked', 'Cabin', 'Age']].isna()

# print('---- MAPA COMPLETO ----')
# print(mapa_nulos)

# print('\n---- FILAS CON 3 NULOS ----')
# print(mapa_nulos[mapa_nulos.sum(axis=1) == 3])

# heatmap de nulos
plt.figure(figsize=(10, 6))
sns.heatmap(titanic.isna(), yticklabels=False, cbar=True, cmap='viridis')
plt.title('Mapa de valores nulos en Titanic (amarillo = nulo)')
plt.tight_layout()
# plt.show()

nulos_info = titanic.isna().sum()
nulos_info = nulos_info[nulos_info > 0].sort_values(ascending=False)
# for col, count in nulos_info.items():
#     print(f'    {col}: {count} nulos ({ count / len(titanic) * 100:.1f}%)')


# rellenar valor nulos
# print('\nAntes\n')
# print(f'Embarked - nulos: {titanic['Embarked'].isna().sum()}')
# print(titanic.Embarked.value_counts())

# rellenar nulos con 'S' (Southampton - el más común)
titanic.Embarked = titanic['Embarked'].fillna('S')

# print('\nDespués\n')
# print(f'Embarked - nulos: {titanic['Embarked'].isna().sum()}')
# print(titanic.Embarked.value_counts())

# estadística
# print('EDADES (Age)')
# print(f'Nulos antes: {titanic.Age.isna().sum()}')
# print(f'Media de edad: {titanic.Age.mean():.1f}')
# print(f'Mediana de edad: {titanic.Age.median():.1f}')

# rellenar con la media
titanic['Age_media'] = titanic.Age.fillna(titanic.Age.mean())

# rellenar con la mediana
titanic['Age_mediana'] = titanic.Age.fillna(titanic.Age.median())

# print('COMPARATIVA')
# print(titanic[['Age', 'Age_media', 'Age_mediana']].head(10))