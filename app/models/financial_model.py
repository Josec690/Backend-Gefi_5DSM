from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class EntradaCreate(BaseModel):
    """Model para criação de entrada"""
    valor: float = Field(..., gt=0)
    tipo: str = Field(..., min_length=1, max_length=50)
    descricao: Optional[str] = Field(None, max_length=200)
    future_entry: Optional[datetime] = None

class EntradaResponse(BaseModel):
    """Model para resposta de entrada"""
    id: str
    user_id: str
    valor: float
    entry_data: str  # ISO format string
    tipo: str
    descricao: Optional[str] = None
    future_entry: Optional[str] = None  # ISO format string
    
    class Config:
        arbitrary_types_allowed = True
        extra = 'ignore'

class SaidaCreate(BaseModel):
    """Model para criação de saída"""
    valor: float = Field(..., gt=0)
    tipo: str = Field(..., min_length=1, max_length=50)
    descricao: Optional[str] = Field(None, max_length=200)
    future_out: Optional[datetime] = None

class SaidaResponse(BaseModel):
    """Model para resposta de saída"""
    id: str
    user_id: str
    valor: float
    out_data: str  # ISO format string
    tipo: str
    descricao: Optional[str] = None
    future_out: Optional[str] = None  # ISO format string
    
    class Config:
        arbitrary_types_allowed = True
        extra = 'ignore'

class ResumoFinanceiro(BaseModel):
    """Model para resumo financeiro"""
    mes: int
    ano: int
    total_entradas: float
    total_saidas: float
    saldo: float