#Modelo de Identificación
###Utiliza delito y mes_hecho para el modelo
###Dataset: https://datos.cdmx.gob.mx/dataset/carpetas-de-investigacion-fgj-de-la-ciudad-de-mexico


import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score, confusion_matrix
import matplotlib.pyplot as plt

dataset_path = "datos_delitos.csv"
data = pd.read_csv(dataset_path)

# Explorar los datos
print(data.head())

# Eliminar columnas innecesarias o irrelevantes
data = data.drop(['ao_hechos',	'fecha_hechos',	'hora_hechos',	'ao_inicio',	'mes_inicio',	'fecha_inicio',	'hora_inicio
], axis=1)



# Manejar valores faltantes o nulos
data = data.dropna()

# Convertir la variable objetivo en números usando LabelEncoder
le = LabelEncoder()
data['mes_hechos'] = le.fit_transform(data['mes_hechos'])

# Separar características y variable objetivo
X = data.drop('delito', axis=1)
y = data['mes_hechos']

# Dividir los datos en conjuntos de entrenamiento y prueba
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Crear un modelo de clasificación, como un árbol de decisión
model = DecisionTreeClassifier()

# Entrenar el modelo utilizando los datos de entrenamiento
model.fit(X_train, y_train)

y_pred = model.predict(X_test)

# Calcular la precisión del modelo
accuracy = accuracy_score(y_test, y_pred)
print("Precisión del modelo:", accuracy)

# Calcular y mostrar la matriz de confusión
conf_matrix = confusion_matrix(y_test, y_pred)
print("Matriz de confusión:")
print(conf_matrix)

# Mostrar la matriz de confusión en forma de gráfico
plt.imshow(conf_matrix, cmap='Blues')
plt.title("Matriz de Confusión")
plt.colorbar()
plt.xlabel("Clases Predichas")
plt.ylabel("Clases Verdaderas")
plt.show()