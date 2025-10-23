import yfinance as yf
import httpx
from datetime import datetime
from bson import ObjectId

class MarketController:
    """Controller para dados de mercado"""
    
    def __init__(self, db):
        self.db = db
    
    def get_stock_data(self, symbol: str, user_id: str):
        """Obtém dados de ação via Yahoo Finance"""
        try:
            stock = yf.Ticker(symbol)
            info = stock.info
            hist = stock.history(period="5d")
            
            response_data = {
                "symbol": symbol,
                "name": info.get("longName", "N/A"),
                "current_price": info.get("currentPrice", 0),
                "previous_close": info.get("previousClose", 0),
                "change": 0,
                "change_percent": 0,
                "currency": info.get("currency", "BRL"),
                "market_cap": info.get("marketCap", 0),
                "volume": info.get("volume", 0),
                "historical_prices": []
            }
            
            if info.get("currentPrice") and info.get("previousClose"):
                change = info["currentPrice"] - info["previousClose"]
                response_data["change"] = change
                response_data["change_percent"] = (change / info["previousClose"]) * 100
            
            if not hist.empty:
                response_data["historical_prices"] = [
                    {
                        "date": date.strftime("%Y-%m-%d"),
                        "close": float(row["Close"]),
                        "volume": int(row["Volume"])
                    }
                    for date, row in hist.iterrows()
                ]
            
            # Salvar chamada da API
            api_call = {
                "user_id": user_id,
                "nome_api": "Yahoo Finance",
                "endpoint": f"/stock/{symbol}",
                "parametros": {"symbol": symbol},
                "resposta": response_data,
                "data_call": datetime.utcnow()
            }
            
            self.db.apis.insert_one(api_call)
            
            return response_data, 200
        
        except Exception as e:
            return {"error": f"Erro ao buscar dados da ação: {str(e)}"}, 500
    
    def get_b3_indices(self, user_id: str):
        """Obtém índices da B3"""
        try:
            indices = ["^BVSP", "IFIX.SA"]
            indices_data = []
            
            for index in indices:
                try:
                    ticker = yf.Ticker(index)
                    info = ticker.info
                    hist = ticker.history(period="1d")
                    
                    if not hist.empty:
                        current_price = float(hist["Close"].iloc[-1])
                        previous_close = info.get("previousClose", current_price)
                        change = current_price - previous_close
                        change_percent = (change / previous_close) * 100 if previous_close != 0 else 0
                        
                        indices_data.append({
                            "symbol": index,
                            "name": info.get("longName", index),
                            "current_price": current_price,
                            "previous_close": previous_close,
                            "change": change,
                            "change_percent": change_percent,
                            "volume": int(hist["Volume"].iloc[-1]) if not hist["Volume"].empty else 0
                        })
                except:
                    continue
            
            response_data = {
                "fonte": "B3 via Yahoo Finance",
                "data_atualizacao": datetime.utcnow().isoformat(),
                "indices": indices_data
            }
            
            # Salvar chamada da API
            api_call = {
                "user_id": user_id,
                "nome_api": "B3",
                "endpoint": "/b3-indices",
                "parametros": {"indices": indices},
                "resposta": response_data,
                "data_call": datetime.utcnow()
            }
            
            self.db.apis.insert_one(api_call)
            
            return response_data, 200
        
        except Exception as e:
            return {"error": f"Erro ao buscar índices da B3: {str(e)}"}, 500
    
    def get_tesouro_direto(self, user_id: str):
        """Obtém dados do Tesouro Direto"""
        try:
            url = "https://www.tesourotransparente.gov.br/ckan/api/3/action/datastore_search"
            params = {
                "resource_id": "796d2059-14e9-44e3-80c9-2d9e30b405c1",
                "limit": 10
            }
            
            response = httpx.get(url, params=params, timeout=10.0)
            response.raise_for_status()
            data = response.json()
            
            tesouro_data = []
            if data.get("success") and data.get("result", {}).get("records"):
                for record in data["result"]["records"]:
                    tesouro_data.append({
                        "titulo": record.get("Tipo Titulo"),
                        "vencimento": record.get("Data Vencimento"),
                        "taxa_compra": record.get("Taxa Compra Manha"),
                        "taxa_venda": record.get("Taxa Venda Manha"),
                        "pu_compra": record.get("PU Compra Manha"),
                        "pu_venda": record.get("PU Venda Manha")
                    })
            
            response_data = {
                "fonte": "Tesouro Direto",
                "data_atualizacao": datetime.utcnow().isoformat(),
                "titulos": tesouro_data
            }
            
            # Salvar chamada da API
            api_call = {
                "user_id": user_id,
                "nome_api": "Tesouro Direto",
                "endpoint": "/tesouro-direto",
                "parametros": params,
                "resposta": response_data,
                "data_call": datetime.utcnow()
            }
            
            self.db.apis.insert_one(api_call)
            
            return response_data, 200
        
        except Exception as e:
            return {"error": f"Erro ao buscar dados do Tesouro Direto: {str(e)}"}, 500
    
    def get_api_calls_history(self, user_id: str, limit: int = 50):
        """Obtém histórico de chamadas de API"""
        try:
            cursor = self.db.apis.find(
                {"user_id": user_id}
            ).sort("data_call", -1).limit(limit)
            
            api_calls = []
            for call in cursor:
                call["_id"] = str(call["_id"])
                call["data_call"] = call["data_call"].isoformat()
                api_calls.append(call)
            
            return {"api_calls": api_calls, "total": len(api_calls)}, 200
        
        except Exception as e:
            return {"error": str(e)}, 500