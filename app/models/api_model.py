from pydantic import BaseModel, Field
from typing import Dict, Any, Optional
from datetime import datetime

class ApiCallCreate(BaseModel):
    """Model para criação de chamada de API"""
    nome_api: str
    endpoint: str
    parametros: Dict[str, Any]

class ApiCallResponse(BaseModel):
    """Model para resposta de chamada de API"""
    id: Optional[str] = Field(default=None, alias="_id")
    user_id: str
    nome_api: str
    endpoint: str
    parametros: Dict[str, Any]
    resposta: Dict[str, Any]
    data_call: datetime
    
    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True