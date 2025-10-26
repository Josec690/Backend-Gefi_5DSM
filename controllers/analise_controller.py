from flask import request, jsonify
from models.entrada_model import EntradaModel
from models.saida_model import SaidaModel
from datetime import datetime

class AnaliseController:
    
    @staticmethod
    def calcular_balanco(usuario_id):
        """Calcula o balanço financeiro do usuário"""
        try:
            # Pega parâmetros ou usa mês atual
            mes = request.args.get('mes', datetime.utcnow().month, type=int)
            ano = request.args.get('ano', datetime.utcnow().year, type=int)
            
            # Define início e fim do mês
            inicio_mes = datetime(ano, mes, 1)
            if mes == 12:
                fim_mes = datetime(ano + 1, 1, 1)
            else:
                fim_mes = datetime(ano, mes + 1, 1)
            
            # Buscar entradas e saídas do período
            entradas = EntradaModel.buscar_por_periodo(usuario_id, inicio_mes, fim_mes)
            saidas = SaidaModel.buscar_por_periodo(usuario_id, inicio_mes, fim_mes)
            
            total_entradas = sum(e['valor'] for e in entradas)
            total_saidas = sum(s['valor'] for s in saidas)
            balanco = total_entradas - total_saidas
            
            return jsonify({
                'mes': mes,
                'ano': ano,
                'total_entradas': total_entradas,
                'total_saidas': total_saidas,
                'balanco': balanco,
                'quantidade_entradas': len(entradas),
                'quantidade_saidas': len(saidas)
            }), 200
            
        except Exception as e:
            return jsonify({'erro': f'Erro ao calcular balanço: {str(e)}'}), 500
    
    @staticmethod
    def proximas_saidas(usuario_id):
        """Lista as próximas saídas recorrentes"""
        try:
            hoje = datetime.utcnow()
            fim_mes = datetime(hoje.year, hoje.month + 1 if hoje.month < 12 else 1, 1)
            
            saidas = SaidaModel.buscar_recorrentes_proximas(usuario_id, hoje, fim_mes)
            
            saidas_formatadas = []
            for saida in saidas:
                saidas_formatadas.append({
                    'id': str(saida['_id']),
                    'descricao': saida['descricao'],
                    'valor': saida['valor'],
                    'categoria': saida['categoria'],
                    'data': saida['data'].isoformat()
                })
            
            return jsonify(saidas_formatadas), 200
            
        except Exception as e:
            return jsonify({'erro': f'Erro ao buscar próximas saídas: {str(e)}'}), 500
    
    @staticmethod
    def categorias_gastos(usuario_id):
        """Agrupa gastos por categoria no mês"""
        try:
            mes = request.args.get('mes', datetime.utcnow().month, type=int)
            ano = request.args.get('ano', datetime.utcnow().year, type=int)
            
            inicio_mes = datetime(ano, mes, 1)
            if mes == 12:
                fim_mes = datetime(ano + 1, 1, 1)
            else:
                fim_mes = datetime(ano, mes + 1, 1)
            
            resultados = SaidaModel.agrupar_por_categoria(usuario_id, inicio_mes, fim_mes)
            
            categorias = []
            for r in resultados:
                categorias.append({
                    'categoria': r['_id'],
                    'total': r['total'],
                    'quantidade': r['quantidade']
                })
            
            return jsonify(categorias), 200
            
        except Exception as e:
            return jsonify({'erro': f'Erro ao agrupar categorias: {str(e)}'}), 500