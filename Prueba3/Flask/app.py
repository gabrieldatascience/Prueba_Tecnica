from flask import Flask, request, Response
import pandas as pd

app = Flask(__name__)

@app.route('/ejercicio/descarga/', methods=['GET', 'POST'])
def descargar_archivo():
    formato = request.args.get('formato', 'csv') if request.method == 'GET' else request.json.get('formato', 'csv')
    
    if formato.lower() != 'csv' and formato.lower() != 'json':
        return 'El formato especificado no es válido. Solo se admiten formatos CSV y JSON.', 400
    
    # Leer el archivo CSV (suponiendo que se llama "data.csv")
    try:
        df = pd.read_csv("data.csv")
    except FileNotFoundError:
        return 'El archivo CSV no se encontró.', 404
    
    if formato.lower() == 'csv':
        # Descargar el archivo CSV
        response = Response(content_type='text/csv')
        response.headers['Content-Disposition'] = 'attachment; filename="data.csv"'
        df.to_csv(response, index=False)
        return response
    if formato.lower() == 'json':
        # Convertir el DataFrame a JSON
        response = Response(content_type='application/json')
        response.headers['Content-Disposition'] = 'attachment; filename="data.json"'
        df.to_json(response, orient='records')
        return response
    else:
        return 'El formato especificado no es válido. Solo se admiten formatos CSV y JSON.', 400

if __name__ == '__main__':
    app.run()

