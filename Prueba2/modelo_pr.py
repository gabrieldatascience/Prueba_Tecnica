
# NLP - Modelo Pregunta-Respuesta
###Dataset: https://rajpurkar.github.io/SQuAD-explorer/


import wikipedia as wiki

k = 5
question = "What are the tourist hotspots in Mexico?"

results = wiki.search(question, results=k)
print('Question:', question)
print('Pages:  ', results)

import json
import numpy as np
import pandas as pd

# Importar el módulo os para manipulación de archivos y directorios
import os

# Listar los datos disponibles
# Recorre todos los directorios y archivos dentro de '/kaggle/input'
for dirname, _, filenames in os.walk('/kaggle/input'):
    for filename in filenames:
        # Imprimir la ruta completa de cada archivo encontrado
        print(os.path.join(dirname, filename))

import json
import pandas as pd
import numpy as np

def squad_json_to_dataframe(file_path, record_path=['data', 'paragraphs', 'qas', 'answers']):
    """
    file_path: ruta al archivo JSON de SQuAD.
    record_path: ruta hasta el nivel más profundo en el archivo JSON, el valor predeterminado es
    ['data', 'paragraphs', 'qas', 'answers']
    """
    # Cargar el archivo JSON
    archivo = json.loads(open(file_path).read())

    # Analizar los diferentes niveles del archivo JSON
    js = pd.json_normalize(archivo, record_path)
    m = pd.json_normalize(archivo, record_path[:-1])
    r = pd.json_normalize(archivo, record_path[:-2])

    # Combinar todo en un solo dataframe
    idx = np.repeat(r['context'].values, r.qas.str.len())
    m['context'] = idx
    data = m[['id', 'question', 'context', 'answers']].set_index('id').reset_index()
    data['c_id'] = data['context'].factorize()[0]

    return data

# Cargar los datos
file_path = '/kaggle/input/stanford-question-answering-dataset/train-v1.1.json'
data = squad_json_to_dataframe(file_path)
data

# Cuantos datos son unicos?
data['c_id'].unique().size

documents = data[['context', 'c_id']].drop_duplicates().reset_index(drop=True)
documents

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.neighbors import NearestNeighbors

# Definir la configuración para TF-IDF
tfidf_configs = {
    'lowercase': True,  # Convertir todo a minúsculas
    'analyzer': 'word',  # Analizar a nivel de palabras
    'stop_words': 'english',  # Remover palabras comunes en inglés
    'binary': True,  # Usar representación binaria para contar términos
    'max_df': 0.9,  # Descartar palabras que aparecen en más del 90% de los documentos
    'max_features': 10_000  # Limitar el número máximo de características a 10,000
}

# Definir el número de documentos a recuperar
retriever_configs = {
    'n_neighbors': 10,  # Número de vecinos más cercanos a buscar
    'metric': 'cosine'  # Métrica de similitud a utilizar (coseno en este caso)
}

# Definir nuestra pipeline
embedding = TfidfVectorizer(**tfidf_configs)  # Instanciar el vectorizador TF-IDF con la configuración dada
retriever = NearestNeighbors(**retriever_configs)  # Instanciar el algoritmo de búsqueda de vecinos más cercanos con la configuración dada

# Vamos a entrenar el modelo para recuperar el identificador del documento 'c_id':
X = embedding.fit_transform(documents['context'])
retriever.fit(X, documents['c_id'])

def transform_text(vectorizer, text):
    '''
    Print the text and the vector[TF-IDF]
    vectorizer: sklearn.vectorizer
    text: str
    '''
    print('Text:', text)
    vector = vectorizer.transform([text])
    vector = vectorizer.inverse_transform(vector)
    print('Vect:', vector)

# vectorizar la pregunta
transform_text(embedding, question)

X = embedding.transform([question])  # Transformar la pregunta en una representación numérica usando el vectorizador TF-IDF
c_id = retriever.kneighbors(X, return_distance=False)[0][0]  # Obtener el índice del documento más similar a la pregunta
selected = documents.iloc[c_id]['context']  # Obtener el contexto del documento seleccionado

# Vectorizar el documento seleccionado
transform_text(embedding, selected)

# Commented out IPython magic to ensure Python compatibility.
# %%time
# # Predecir un documento para cada pregunta
# X = embedding.transform(data['question'])  # Transformar las preguntas en representaciones numéricas utilizando el vectorizador TF-IDF
# y_test = data['c_id']  # Obtener los identificadores de los documentos de prueba
# y_pred = retriever.kneighbors(X, return_distance=False)  # Realizar predicciones de los documentos más similares a las preguntas

#Mostrar los documentos principales predichos para cada pregunta:
y_pred

def top_accuracy(y_true, y_pred) -> float:
#Calcula la precisión superior (top accuracy) de las predicciones.

#y_true: Lista de valores verdaderos de los documentos.
#y_pred: Lista de listas con los documentos predichos para cada pregunta.

#Retorna el valor de precisión superior.
    right, count = 0, 0
    for i, y_t in enumerate(y_true):
        count += 1
        if y_t in y_pred[i]:
            right += 1
    return right / count if count > 0 else 0

# Calcular y mostrar la precisión superior, cantidad de predicciones correctas y total de predicciones
acc = top_accuracy(y_test, y_pred)
print('Accuracy:', f'{acc:.4f}')
print('Quantity:', int(acc*len(y_pred)), 'from', len(y_pred))