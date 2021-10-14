from fastapi import FastAPI, status
from typing import List, Optional
from pydantic import EmailStr
from pydantic.main import BaseModel
from starlette.responses import JSONResponse
import uvicorn
import uuid

app = FastAPI()

class GatewayResponse(BaseModel):
    Id: int  # TODO: Armar este modelo

@app.get('/', response_model = List[GatewayResponse], status_code=status.HTTP_200_OK)
async def getTestGateway():  # TODO: Filtros
    return [{'Id': 1}]  # Hardcoded para probar

if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8002)