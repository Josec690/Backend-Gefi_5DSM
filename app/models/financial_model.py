from pydantic import BaseModel, Field, validator
from typing import Optional
from datetime import datetime

class EntradaCreate(BaseModel):
    """Model para criação de entrada"""
    valor: float
    tipo: str
    descricao: Optional[str] = None
    future_entry: Optional[datetime] = None

    @validator('valor')
    def validate_valor(cls, v):
        if v <= 0:
            raise ValueError('Valor deve ser maior que zero')
        return v

    @validator('tipo')
    def validate_tipo(cls, v):
        if not v or len(v) < 1 or len(v) > 50:
            raise ValueError('Tipo deve ter entre 1 e 50 caracteres')
        return v

    @validator('descricao')
    def validate_descricao(cls, v):
        if v and len(v) > 200:
            raise ValueError('Descrição deve ter no máximo 200 caracteres')
        return v

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
    valor: float
    tipo: str
    descricao: Optional[str] = None
    future_out: Optional[datetime] = None

    @validator('valor')
    def validate_valor(cls, v):
        if v <= 0:
            raise ValueError('Valor deve ser maior que zero')
        return v

    @validator('tipo')
    def validate_tipo(cls, v):
        if not v or len(v) < 1 or len(v) > 50:
            raise ValueError('Tipo deve ter entre 1 e 50 caracteres')
        return v

    @validator('descricao')
    def validate_descricao(cls, v):
        if v and len(v) > 200:
            raise ValueError('Descrição deve ter no máximo 200 caracteres')
        return v

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