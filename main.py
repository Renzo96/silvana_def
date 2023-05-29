from fastapi import FastAPI, Request, Response,Depends, HTTPException
from tests2 import *
from fastapi.responses import PlainTextResponse, FileResponse,HTMLResponse, JSONResponse
from fastapi import Response, Depends, HTTPException, FastAPI, Form 
from fastapi.security import HTTPBasic, HTTPBasicCredentials
import pandas as pd
import pymysql
from starlette import responses

app = FastAPI()
security = HTTPBasic()

users = {
    "Admin": "password123",
    "Silvana": "password456"
}

@app.get("/")
def home():
    html = leer_html('home.html')
    return responses.HTMLResponse(content=html, status_code=200)

sessions = {}

@app.post("/login")
async def login(credentials: HTTPBasicCredentials = Depends(security)):
    username = credentials.username
    password = credentials.password

    # Checking valid username and password
    if username not in users or users[username] != password:
        raise HTTPException(status_code=401, detail="Incorrect username or password")

    sessions[username] = True
    return {"Message": "Login successful"}

@app.get("/network_map")
def network_map(credentials: HTTPBasicCredentials = Depends(security)):
    username = credentials.username

    if username not in sessions:
        raise HTTPException(status_code=401, detail="You need to log in to execute this request.")

    # Fragmento para poder descargar info en txt
    interfaz_info = get_interface_info()
    interfaz_info_str = "\n".join([f"{k}: {v}" for k, v in interfaz_info.items()])
    response = Response(content=interfaz_info_str, media_type="text")
    response.headers["Content-Disposition"] = "attachment; filename=mapa_red.txt"

    return response


@app.get("/network_map")
def network_map(request: Request, credentials: HTTPBasicCredentials = Depends(security)):
    username = credentials.username
    
    if username not in sessions:
        return {"Message": "You need to log in to execute this request."}
    
    #Fragmento para poder descargar info en txt
    interfaz_info = get_interface_info()
    interfaz_info_str = "\n".join([f"{k}: {v}" for k, v in interfaz_info.items()])
    response = Response(content=interfaz_info_str, media_type="text")
    response.headers["Content-Disposition"] = "attachment; filename=mapa_red.txt"
    
    return response


@app.get("/scan_ports")
def scan_ports(credentials: HTTPBasicCredentials = Depends(security)):
    username = credentials.username

    if username not in sessions:
        return {"Message": "You need to log in to execute this request."}
    
    #Fragmento para poder descargar info en txt
    scan_info = port_scan(get_local_ip())
    scan_info_str = "\n".join([f"{k}: {v}" for k, v in scan_info.items()])

    response = Response(content=scan_info_str, media_type="text")
    response.headers["Content-Disposition"] = "attachment; filename=información_interfaz.txt"
    
    return response
    

@app.get("/system_information")
def system_information(request: Request,response: Response,credentials: HTTPBasicCredentials = Depends(security)):
    username = credentials.username
    if username not in sessions:
        return {"Message": "You need to log in to execute this request."}
    
    #Fragmento para poder descargar info en txt
    system_info = get_system_info()
    system_info_str = "\n".join([f"{k}: {v}" for k, v in system_info.items()])
    response = Response(content=system_info_str, media_type="text")
    response.headers["Content-Disposition"] = "attachment; filename=información_sistema.txt"
    
    return response

    
    
# @app.get("/antivirus_information")
# def antivirus_information(request: Request, response: Response, credentials: HTTPBasicCredentials = Depends(security)):
#     username = credentials.username
#     if username not in sessions:
#         return {"Message": "You need to log in to execute this request."}
    
#     #Fragmento para poder descargar info en txt
#     antivirus_info =  get_antivirus()
#     antivirus_info_str = "\n".join([f"{k}: {v}" for k, v in antivirus_info.items()])
#     response = Response(content=antivirus_info_str, media_type="text")
#     response.headers["Content-Disposition"] = "attachment; filename=información_antivirus.txt"
    
#     return response


@app.get("/internet_speed_information")
def internet_speed_information(request: Request,response: Response,credentials: HTTPBasicCredentials = Depends(security)):
    username = credentials.username
    if username not in sessions:
        return {"message": "You need to log in to execute this request."}
    
    internet_info = speed_connection()
    internet_info_str = "\n".join([f"{k}: {v}" for k, v in internet_info.items()])
    response = Response(content=internet_info_str, media_type="text")
    response.headers["Content-Disposition"] = "attachment; filename=información_internet.txt"
    
    return response


@app.get("/user_wifi")
def user_wifi(credentials: HTTPBasicCredentials = Depends(security)):
    username = credentials.username

    if username not in sessions:
        return {"Message": "You need to log in to execute this request."}
    
    #Fragmento para poder descargar info en txt
    user_info = user_conect_wifi(get_local_ip())
    user_info_str = "\n".join([f"{k}: {v}" for k, v in user_info.items()])

    response = Response(content=user_info_str, media_type="text")
    response.headers["Content-Disposition"] = "attachment; filename=usuarios_wifi.txt"
    
    return response


@app.post("/logout")
async def logout(credentials: HTTPBasicCredentials = Depends(security)):
    username = credentials.username
    if username in sessions:
        del sessions[username]
    return {"message": "Logged out successfully."}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)