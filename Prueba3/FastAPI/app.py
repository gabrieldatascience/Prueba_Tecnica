from fastapi import FastAPI, HTTPException
import pandas as pd

app = FastAPI()

# Ruta GET para descargar el archivo en formato CSV
@app.get("/ejercicio/descarga/")
def descargar_archivo_get(formato: str = "csv"):
    if formato.lower() != "csv" and formato.lower() != "json":
        raise HTTPException(status_code=400, detail="El formato especificado no es válido. Solo se admiten formatos CSV y JSON.")
    
    # Leer el archivo CSV (suponiendo que se llama "data.csv")
    try:
        df = pd.read_csv("data.csv")
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="El archivo CSV no se encontró.")
    
    if formato.lower() == "csv":
        # Descargar el archivo CSV
        response = df.to_csv(index=False)
        return Response(content=response, media_type="text/csv", headers={"Content-Disposition": "attachment; filename=data.csv"})
    if formato.lower() == "json":
        # Convertir el DataFrame a JSON
        response = df.to_json(orient="records")
        return Response(content=response, media_type="application/json")
    else:
        return TTPException(status_code=404, detail="El archivo CSV no se encontró.")

# Ruta POST para descargar el archivo en formato CSV o JSON
@app.post("/ejercicio/descarga/")
def descargar_archivo_post(payload: dict):
    if "formato" not in payload:
        raise HTTPException(status_code=400, detail="El campo 'formato' es obligatorio en el payload.")
    
    formato = payload["formato"]
    
    if formato.lower() != "csv" and formato.lower() != "json":
        raise HTTPException(status_code=400, detail="El formato especificado no es válido. Solo se admiten formatos CSV y JSON.")
    
    # Leer el archivo CSV (suponiendo que se llama "data.csv")
    try:
        df = pd.read_csv("data.csv")
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="El archivo CSV no se encontró.")
    
    if formato.lower() == "csv":
        # Descargar el archivo CSV
        response = df.to_csv(index=False)
        return Response(content=response, media_type="text/csv", headers={"Content-Disposition": "attachment; filename=data.csv"})
    if formato.lower() == "json":
        # Convertir el DataFrame a JSON
        response = df.to_json(orient="records")
        return Response(content=response, media_type="application/json")
    else:
        return TTPException(status_code=404, detail="El archivo CSV no se encontró.")

