# Compatibilidade Pydantic v1
try:
    from pydantic.v1 import BaseModel, Field, EmailStr, validator
except ImportError:
    from pydantic import BaseModel, Field, EmailStr, validator

__all__ = ['BaseModel', 'Field', 'EmailStr', 'validator']