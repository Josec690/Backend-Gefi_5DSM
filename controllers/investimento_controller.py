from flask import jsonify

class InvestimentoController:
    
    @staticmethod
    def listar():
        """Lista investimentos sugeridos (dados estáticos para MVP)"""
        investimentos = [
            {
                'id': '1',
                'nome': 'Tesouro Selic',
                'tipo': 'Renda Fixa',
                'rendimento': '12.5% ao ano',
                'risco': 'Baixo',
                'liquidez': 'Diária'
            },
            {
                'id': '2',
                'nome': 'CDB',
                'tipo': 'Renda Fixa',
                'rendimento': '13% ao ano',
                'risco': 'Baixo',
                'liquidez': '90 dias'
            },
            {
                'id': '3',
                'nome': 'Fundo Imobiliário',
                'tipo': 'Renda Variável',
                'rendimento': '8% ao ano + valorização',
                'risco': 'Médio',
                'liquidez': '2 dias úteis'
            },
            {
                'id': '4',
                'nome': 'Ações',
                'tipo': 'Renda Variável',
                'rendimento': 'Variável',
                'risco': 'Alto',
                'liquidez': '2 dias úteis'
            }
        ]
        
        return jsonify(investimentos), 200