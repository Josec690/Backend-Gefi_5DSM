from flask import jsonify, request
import os
import time
from datetime import datetime
import httpx
import yfinance as yf

# Cache em memória
_CACHE = {}
_CACHE_TTL = int(os.getenv("INVEST_CACHE_TTL", "300"))  # 5 minutos padrão

# URLs das APIs
BRAPI_BASE_URL = "https://brapi.dev/api"
TESOURO_API_URL = (
    "https://www.tesourotransparente.gov.br/api-de-dados/titulos-tesouro-direto"
)


def _set_cache(key: str, data, ttl: int = None):
    """Armazena dados no cache com TTL"""
    now = time.time()
    _CACHE[key] = {
        "data": data,
        "expires_at": now + (ttl if ttl is not None else _CACHE_TTL),
    }


def _get_cache(key: str):
    """Recupera dados do cache se válidos"""
    now = time.time()
    entry = _CACHE.get(key)
    if entry and entry.get("expires_at", 0) > now:
        return entry.get("data")
    return None


def _get_brapi_quotes(tickers: list):
    """Busca cotações via Brapi (fonte primária)"""
    if not tickers:
        return {}

    cache_key = f'brapi:quotes:{",".join(sorted(tickers))}'
    cached = _get_cache(cache_key)
    if cached:
        return cached

    try:
        tickers_str = ",".join(tickers)
        url = f"{BRAPI_BASE_URL}/quote/{tickers_str}"

        with httpx.Client(timeout=10.0) as client:
            response = client.get(url, params={"token": os.getenv("BRAPI_TOKEN", "")})

            if response.status_code == 200:
                data = response.json()
                results = {}

                for stock in data.get("results", []):
                    ticker = stock.get("symbol", "")
                    results[ticker] = {
                        "preco": stock.get("regularMarketPrice"),
                        "variacao": stock.get("regularMarketChange"),
                        "variacao_percentual": stock.get("regularMarketChangePercent"),
                        "timestamp": datetime.utcnow().isoformat() + "Z",
                        "nome": stock.get("shortName") or stock.get("longName"),
                        "fonte": "brapi",
                    }

                _set_cache(cache_key, results)
                return results
    except Exception as e:
        print(f"Erro ao buscar Brapi: {e}")

    return {}


def _get_yfinance_fallback(ticker: str):
    """Fallback desabilitado - Yahoo Finance bloqueia requisições constantemente"""
    # yfinance não é confiável para uso em produção (rate limits agressivos)
    # Brapi é a fonte primária e suficiente para o mercado brasileiro
    return None


class InvestimentoController:

    @staticmethod
    def listar():
        """Lista investimentos sugeridos com cotações reais"""
        investimentos = [
            {
                "id": "1",
                "nome": "Tesouro Selic",
                "tipo": "Renda Fixa",
                "rendimento": "12.5% ao ano",
                "risco": "Baixo",
                "liquidez": "Diária",
            },
            {
                "id": "2",
                "nome": "CDB",
                "tipo": "Renda Fixa",
                "rendimento": "13% ao ano",
                "risco": "Baixo",
                "liquidez": "90 dias",
            },
            {
                "id": "3",
                "nome": "Fundo Imobiliário KNRI11",
                "ticker": "KNRI11",
                "tipo": "Renda Variável",
                "rendimento": "8% ao ano + valorização",
                "risco": "Médio",
                "liquidez": "2 dias úteis",
            },
            {
                "id": "4",
                "nome": "Ações VALE3",
                "ticker": "VALE3",
                "tipo": "Renda Variável",
                "rendimento": "Variável",
                "risco": "Alto",
                "liquidez": "2 dias úteis",
            },
        ]

        # Buscar cotações para investimentos com ticker
        tickers = [inv["ticker"] for inv in investimentos if "ticker" in inv]

        if tickers:
            # Tentar Brapi primeiro (fonte confiável)
            quotes = _get_brapi_quotes(tickers)

            # Fallback para yfinance APENAS se Brapi falhou E não estamos em rate limit
            rate_limit_active = _get_cache("yfinance:rate_limit")
            if not rate_limit_active:
                for ticker in tickers:
                    if ticker not in quotes or quotes[ticker].get("preco") is None:
                        fallback = _get_yfinance_fallback(ticker)
                        if fallback:
                            quotes[ticker] = fallback

            # Anexar dados aos investimentos
            for inv in investimentos:
                ticker = inv.get("ticker")
                if ticker and ticker in quotes:
                    quote = quotes[ticker]
                    inv["preco"] = quote.get("preco")
                    inv["variacao"] = quote.get("variacao")
                    inv["variacao_percentual"] = quote.get("variacao_percentual")
                    inv["timestamp"] = quote.get("timestamp")
                    inv["fonte"] = quote.get("fonte", "brapi")

        return jsonify(investimentos), 200

    @staticmethod
    def cotacao():
        """Busca cotação de um ou mais tickers"""
        ticker = request.args.get("ticker", "").strip().upper()
        tickers_param = request.args.get("tickers", "").strip()

        if not ticker and not tickers_param:
            return (
                jsonify({"erro": 'Parâmetro "ticker" ou "tickers" é obrigatório.'}),
                400,
            )

        # Múltiplos tickers
        if tickers_param:
            tickers = [t.strip().upper() for t in tickers_param.split(",") if t.strip()]
        else:
            tickers = [ticker]

        # Tentar Brapi primeiro (sempre)
        quotes = _get_brapi_quotes(tickers)

        # Fallback para yfinance APENAS se necessário e sem rate limit
        rate_limit_active = _get_cache("yfinance:rate_limit")
        if not rate_limit_active:
            for t in tickers:
                if t not in quotes or quotes[t].get("preco") is None:
                    fallback = _get_yfinance_fallback(t)
                    if fallback:
                        quotes[t] = fallback

        # Se único ticker, retornar objeto simples
        if len(tickers) == 1:
            t = tickers[0]
            if t in quotes:
                result = {
                    "ticker": t,
                    "preco": quotes[t].get("preco"),
                    "variacao": quotes[t].get("variacao"),
                    "variacao_percentual": quotes[t].get("variacao_percentual"),
                    "timestamp": quotes[t].get("timestamp"),
                    "fonte": quotes[t].get("fonte"),
                }
                return jsonify(result), 200
            return jsonify({"erro": f"Não foi possível obter dados para {t}"}), 404

        # Múltiplos tickers
        return jsonify(quotes), 200

    @staticmethod
    def em_alta():
        """Retorna ações em alta (maior variação positiva do dia)"""
        cache_key = "investimentos:em_alta"
        cached = _get_cache(cache_key)
        if cached:
            return jsonify(cached), 200

        try:
            # Usar endpoint da Brapi para ações mais negociadas
            url = f"{BRAPI_BASE_URL}/quote/list"

            with httpx.Client(timeout=15.0) as client:
                response = client.get(
                    url,
                    params={
                        "sortBy": "change",
                        "sortOrder": "desc",
                        "limit": 10,
                        "token": os.getenv("BRAPI_TOKEN", ""),
                    },
                )

                if response.status_code == 200:
                    data = response.json()
                    em_alta = []

                    for stock in data.get("stocks", []):
                        # Filtrar apenas ações com variação positiva
                        change_pct = stock.get("change")
                        if change_pct and change_pct > 0:
                            em_alta.append(
                                {
                                    "ticker": stock.get("stock"),
                                    "nome": stock.get("name"),
                                    "preco": stock.get("close"),
                                    "variacao_percentual": change_pct,
                                    "volume": stock.get("volume"),
                                    "timestamp": datetime.utcnow().isoformat() + "Z",
                                }
                            )

                    _set_cache(cache_key, em_alta, ttl=600)  # Cache de 10 minutos
                    return jsonify(em_alta), 200
        except Exception as e:
            print(f"Erro ao buscar ações em alta: {e}")

        return jsonify({"erro": "Não foi possível buscar investimentos em alta"}), 500

    @staticmethod
    def listar_tesouro():
        """Lista títulos do Tesouro Direto disponíveis (API oficial)"""
        cache_key = "tesouro:titulos"
        cached = _get_cache(cache_key)
        if cached:
            return jsonify(cached), 200

        try:
            with httpx.Client(timeout=15.0) as client:
                response = client.get(TESOURO_API_URL)

                if response.status_code == 200:
                    data = response.json()
                    titulos = []

                    # Processar resposta da API do Tesouro
                    for item in data.get("response", {}).get("data", []):
                        titulos.append(
                            {
                                "codigo": item.get("NomeTitulo", ""),
                                "nome": item.get("NomeTitulo", ""),
                                "vencimento": item.get("DataVencimento", ""),
                                "taxa_compra": item.get("TaxaCompra"),
                                "taxa_venda": item.get("TaxaVenda"),
                                "preco_unitario": item.get("PrecoUnitario"),
                                "valor_minimo": item.get("ValorMinimo"),
                                "tipo": "Tesouro Direto",
                            }
                        )

                    _set_cache(cache_key, titulos, ttl=3600)  # Cache de 1 hora
                    return jsonify(titulos), 200
        except Exception as e:
            print(f"Erro ao buscar Tesouro Direto: {e}")

        # Fallback: dados estáticos
        tesouro_fallback = [
            {
                "codigo": "Tesouro Selic 2029",
                "nome": "Tesouro Selic 2029",
                "vencimento": "2029-03-01",
                "taxa_compra": "SELIC + 0.0585%",
                "tipo": "Tesouro Direto",
                "valor_minimo": "R$ 30,00",
            },
            {
                "codigo": "Tesouro IPCA+ 2035",
                "nome": "Tesouro IPCA+ 2035",
                "vencimento": "2035-05-15",
                "taxa_compra": "IPCA + 6.20%",
                "tipo": "Tesouro Direto",
                "valor_minimo": "R$ 30,00",
            },
        ]

        return jsonify(tesouro_fallback), 200
