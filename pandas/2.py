import pandas as pd

titanic = pd.read_csv('Titanic-Dataset.csv')

# Ver nulos iniciales
print('INICIALES')
print(titanic[['Age', 'Embarked', 'Fare']].isna().sum())

# Diccionario de relleno
valores_relleno = {
    'Age': titanic.Age.median(),
    'Embarked': 'S',
    'Fare': titanic.Fare.mean()
}

titanic_limpio = titanic.fillna(valores_relleno)

print('\nNULOS DESPUÉS')
print(titanic_limpio[['Age', 'Embarked', 'Fare']].isna().sum())