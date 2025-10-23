from datetime import datetime
from app.models.financial_model import EntradaCreate, SaidaCreate
from app.utils.helpers import get_month_range
from bson import ObjectId

class FinancialController:
    """Controller para operações financeiras"""
    
    def __init__(self, db):
        self.db = db
    
    def create_entrada(self, user_id: str, entrada_data: dict):
        """Cria nova entrada financeira"""
        try:
            entrada = EntradaCreate(**entrada_data)
            
            entrada_dict = {
                "user_id": user_id,
                "valor": entrada.valor,
                "entry_data": datetime.utcnow(),
                "tipo": entrada.tipo,
                "descricao": entrada.descricao,
                "future_entry": entrada.future_entry
            }
            
            result = self.db.entradas.insert_one(entrada_dict)
            
            return {
                "id": str(result.inserted_id),
                "user_id": user_id,
                "valor": entrada.valor,
                "entry_data": entrada_dict["entry_data"].isoformat(),
                "tipo": entrada.tipo,
                "message": "Entrada criada com sucesso"
            }, 201
        
        except Exception as e:
            return {"error": str(e)}, 500
    
    def get_entradas(self, user_id: str, skip: int = 0, limit: int = 100):
        """Lista entradas do usuário"""
        try:
            cursor = self.db.entradas.find({"user_id": user_id}).skip(skip).limit(limit).sort("entry_data", -1)
            entradas = []
            
            for entrada in cursor:
                entrada["_id"] = str(entrada["_id"])
                entrada["entry_data"] = entrada["entry_data"].isoformat()
                entradas.append(entrada)
            
            return {"entradas": entradas, "total": len(entradas)}, 200
        
        except Exception as e:
            return {"error": str(e)}, 500
    
    def create_saida(self, user_id: str, saida_data: dict):
        """Cria nova saída financeira"""
        try:
            saida = SaidaCreate(**saida_data)
            
            saida_dict = {
                "user_id": user_id,
                "valor": saida.valor,
                "out_data": datetime.utcnow(),
                "tipo": saida.tipo,
                "descricao": saida.descricao,
                "future_out": saida.future_out
            }
            
            result = self.db.saidas.insert_one(saida_dict)
            
            return {
                "id": str(result.inserted_id),
                "user_id": user_id,
                "valor": saida.valor,
                "out_data": saida_dict["out_data"].isoformat(),
                "tipo": saida.tipo,
                "message": "Saída criada com sucesso"
            }, 201
        
        except Exception as e:
            return {"error": str(e)}, 500
    
    def get_resumo_financeiro(self, user_id: str, mes: int = None, ano: int = None):
        """Gera resumo financeiro do usuário"""
        try:
            start_date, end_date = get_month_range(mes, ano)
            
            # Entradas
            entrada_pipeline = [
                {"$match": {
                    "user_id": user_id,
                    "entry_data": {"$gte": start_date, "$lt": end_date}
                }},
                {"$group": {"_id": None, "total": {"$sum": "$valor"}}}
            ]
            
            # Saídas
            saida_pipeline = [
                {"$match": {
                    "user_id": user_id,
                    "out_data": {"$gte": start_date, "$lt": end_date}
                }},
                {"$group": {"_id": None, "total": {"$sum": "$valor"}}}
            ]
            
            entradas = list(self.db.entradas.aggregate(entrada_pipeline))
            saidas = list(self.db.saidas.aggregate(saida_pipeline))
            
            total_entradas = entradas[0]["total"] if entradas else 0
            total_saidas = saidas[0]["total"] if saidas else 0
            saldo = total_entradas - total_saidas
            
            return {
                "mes": start_date.month,
                "ano": start_date.year,
                "total_entradas": total_entradas,
                "total_saidas": total_saidas,
                "saldo": saldo
            }, 200
        
        except Exception as e:
            return {"error": str(e)}, 500