# Api Gateway

## Instalación

Para instalar la Gateway de APIs existen 2 posibilidades:

### Usar Python

Utilizando Python pueden instalarse las dependencias a partir del siguiente comando:

```
pip install -r requirements.txt
```

Y el servidor una vez que las dependencias estén completamente instaladas puede correrse con el comando:

```
uvicorn gateway.Gateway:app --reload
```

De esta forma, la terminal nos lanzará un enlace con el cual podremos acceder al servidor corrido con Uvicorn, y podemos visualizar el API Docs concatenando a ese link "/docs".

Ejemplo:

Si nos retorna el enlace 

https://127.0.0.1:8000

Entonces la API Docs puede accederse en:

https://127.0.0.1:8000/docs



### Usar Docker

Para utilizar Docker se poseen 2 scripts. Por un lado, primero se deben correr los comandos (Parados en el directorio raíz):

* En Windows:

```
CompileImage.bat
RunServer.bat
```

* En Linux:

```
chmod +x CompileImage.sh
chmod +x RunServer.sh
./CompileImage.sh
./RunServer.sh
```

Finalmente, la imagen estará corriendo debido a los comandos de RunServer, y podrá accederse a la API Docs desde la URL:

https://127.0.0.1:8002/docs
