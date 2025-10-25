"""
Script de testes para validar todos os endpoints da API GeFi
Execute: python test_api.py
"""

import requests
import json
from datetime import datetime

# Configuração
BASE_URL = "http://localhost:5000/api"
token = None
usuario_id = None
entrada_id = None
saida_id = None

def print_resultado(titulo, response):
    """Imprime resultado formatado"""
    print(f"\n{'='*60}")
    print(f"🧪 {titulo}")
    print(f"{'='*60}")
    print(f"Status: {response.status_code}")
    try:
        print(f"Resposta: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
    except:
        print(f"Resposta: {response.text}")
    print(f"{'='*60}\n")

def test_1_cadastro():
    """Teste 1: Cadastro de novo usuário"""
    global token, usuario_id
    
    url = f"{BASE_URL}/cadastro"
    dados = {
        "nome": "Teste GeFi",
        "email": f"teste_{datetime.now().timestamp()}@gefi.com",
        "cpf": "12345678900",
        "senha": "senha123"
    }
    
    response = requests.post(url, json=dados)
    print_resultado("CADASTRO DE USUÁRIO", response)
    
    if response.status_code == 201:
        data = response.json()
        token = data.get('token')
        usuario_id = data.get('usuario_id')
        print(f"✅ Token salvo: {token[:50]}...")
        print(f"✅ ID do usuário: {usuario_id}")
    else:
        print("❌ Erro no cadastro!")
    
    return response.status_code == 201

def test_2_login():
    """Teste 2: Login com usuário existente"""
    global token
    
    url = f"{BASE_URL}/login"
    dados = {
        "email": "teste@gefi.com",
        "senha": "senha123"
    }
    
    response = requests.post(url, json=dados)
    print_resultado("LOGIN", response)
    
    if response.status_code == 200:
        token = response.json().get('token')
        print(f"✅ Novo token obtido: {token[:50]}...")

def test_3_buscar_usuario():
    """Teste 3: Buscar dados do usuário"""
    if not token:
        print("❌ Token não disponível. Execute o teste de cadastro primeiro.")
        return
    
    url = f"{BASE_URL}/usuario"
    headers = {"Authorization": f"Bearer {token}"}
    
    response = requests.get(url, headers=headers)
    print_resultado("BUSCAR DADOS DO USUÁRIO", response)

def test_4_salvar_questionario():
    """Teste 4: Salvar respostas do questionário"""
    if not token:
        print("❌ Token não disponível.")
        return
    
    url = f"{BASE_URL}/questionario"
    headers = {"Authorization": f"Bearer {token}"}
    dados = {
        "respostas": {
            "q1": "Sim",
            "q2": "Aposentadoria",
            "q3": "Iniciante"
        }
    }
    
    response = requests.post(url, json=dados, headers=headers)
    print_resultado("SALVAR QUESTIONÁRIO", response)

def test_5_criar_entrada():
    """Teste 5: Criar entrada financeira"""
    global entrada_id
    
    if not token:
        print("❌ Token não disponível.")
        return
    
    url = f"{BASE_URL}/entrada"
    headers = {"Authorization": f"Bearer {token}"}
    dados = {
        "descricao": "Salário Teste",
        "valor": 5000.00,
        "categoria": "Trabalho",
        "data": datetime.now().isoformat()
    }
    
    response = requests.post(url, json=dados, headers=headers)
    print_resultado("CRIAR ENTRADA", response)
    
    if response.status_code == 201:
        entrada_id = response.json().get('id')
        print(f"✅ ID da entrada: {entrada_id}")

def test_6_listar_entradas():
    """Teste 6: Listar todas as entradas"""
    if not token:
        print("❌ Token não disponível.")
        return
    
    url = f"{BASE_URL}/entradas"
    headers = {"Authorization": f"Bearer {token}"}
    
    response = requests.get(url, headers=headers)
    print_resultado("LISTAR ENTRADAS", response)

def test_7_criar_saida():
    """Teste 7: Criar saída financeira"""
    global saida_id
    
    if not token:
        print("❌ Token não disponível.")
        return
    
    url = f"{BASE_URL}/saida"
    headers = {"Authorization": f"Bearer {token}"}
    dados = {
        "descricao": "Aluguel Teste",
        "valor": 1500.00,
        "categoria": "Moradia",
        "data": datetime.now().isoformat(),
        "eh_recorrente": True
    }
    
    response = requests.post(url, json=dados, headers=headers)
    print_resultado("CRIAR SAÍDA", response)
    
    if response.status_code == 201:
        saida_id = response.json().get('id')
        print(f"✅ ID da saída: {saida_id}")

def test_8_listar_saidas():
    """Teste 8: Listar todas as saídas"""
    if not token:
        print("❌ Token não disponível.")
        return
    
    url = f"{BASE_URL}/saidas"
    headers = {"Authorization": f"Bearer {token}"}
    
    response = requests.get(url, headers=headers)
    print_resultado("LISTAR SAÍDAS", response)

def test_9_atualizar_entrada():
    """Teste 9: Atualizar entrada"""
    if not token or not entrada_id:
        print("❌ Token ou ID da entrada não disponível.")
        return
    
    url = f"{BASE_URL}/entrada/{entrada_id}"
    headers = {"Authorization": f"Bearer {token}"}
    dados = {
        "descricao": "Salário Atualizado",
        "valor": 5500.00
    }
    
    response = requests.put(url, json=dados, headers=headers)
    print_resultado("ATUALIZAR ENTRADA", response)

def test_10_atualizar_saida():
    """Teste 10: Atualizar saída"""
    if not token or not saida_id:
        print("❌ Token ou ID da saída não disponível.")
        return
    
    url = f"{BASE_URL}/saida/{saida_id}"
    headers = {"Authorization": f"Bearer {token}"}
    dados = {
        "descricao": "Aluguel Atualizado",
        "valor": 1600.00
    }
    
    response = requests.put(url, json=dados, headers=headers)
    print_resultado("ATUALIZAR SAÍDA", response)

def test_11_calcular_balanco():
    """Teste 11: Calcular balanço mensal"""
    if not token:
        print("❌ Token não disponível.")
        return
    
    mes = datetime.now().month
    ano = datetime.now().year
    
    url = f"{BASE_URL}/balanco?mes={mes}&ano={ano}"
    headers = {"Authorization": f"Bearer {token}"}
    
    response = requests.get(url, headers=headers)
    print_resultado("CALCULAR BALANÇO", response)

def test_12_proximas_saidas():
    """Teste 12: Buscar próximas saídas recorrentes"""
    if not token:
        print("❌ Token não disponível.")
        return
    
    url = f"{BASE_URL}/proximas-saidas"
    headers = {"Authorization": f"Bearer {token}"}
    
    response = requests.get(url, headers=headers)
    print_resultado("PRÓXIMAS SAÍDAS", response)

def test_13_categorias_gastos():
    """Teste 13: Agrupar gastos por categoria"""
    if not token:
        print("❌ Token não disponível.")
        return
    
    mes = datetime.now().month
    ano = datetime.now().year
    
    url = f"{BASE_URL}/categorias-gastos?mes={mes}&ano={ano}"
    headers = {"Authorization": f"Bearer {token}"}
    
    response = requests.get(url, headers=headers)
    print_resultado("GASTOS POR CATEGORIA", response)

def test_14_listar_investimentos():
    """Teste 14: Listar investimentos sugeridos"""
    if not token:
        print("❌ Token não disponível.")
        return
    
    url = f"{BASE_URL}/investimentos"
    headers = {"Authorization": f"Bearer {token}"}
    
    response = requests.get(url, headers=headers)
    print_resultado("LISTAR INVESTIMENTOS", response)

def test_15_mudar_senha():
    """Teste 15: Mudar senha do usuário"""
    if not token:
        print("❌ Token não disponível.")
        return
    
    url = f"{BASE_URL}/mudar-senha"
    headers = {"Authorization": f"Bearer {token}"}
    dados = {
        "senha_atual": "senha123",
        "senha_nova": "novaSenha456"
    }
    
    response = requests.put(url, json=dados, headers=headers)
    print_resultado("MUDAR SENHA", response)

def test_16_deletar_entrada():
    """Teste 16: Deletar entrada"""
    if not token or not entrada_id:
        print("❌ Token ou ID da entrada não disponível.")
        return
    
    url = f"{BASE_URL}/entrada/{entrada_id}"
    headers = {"Authorization": f"Bearer {token}"}
    
    response = requests.delete(url, headers=headers)
    print_resultado("DELETAR ENTRADA", response)

def test_17_deletar_saida():
    """Teste 17: Deletar saída"""
    if not token or not saida_id:
        print("❌ Token ou ID da saída não disponível.")
        return
    
    url = f"{BASE_URL}/saida/{saida_id}"
    headers = {"Authorization": f"Bearer {token}"}
    
    response = requests.delete(url, headers=headers)
    print_resultado("DELETAR SAÍDA", response)

def test_18_recuperar_senha():
    """Teste 18: Recuperar senha"""
    url = f"{BASE_URL}/recuperar-senha"
    dados = {
        "email": "teste@gefi.com"
    }
    
    response = requests.post(url, json=dados)
    print_resultado("RECUPERAR SENHA", response)

def test_19_token_invalido():
    """Teste 19: Testar com token inválido"""
    url = f"{BASE_URL}/usuario"
    headers = {"Authorization": "Bearer token_invalido_123"}
    
    response = requests.get(url, headers=headers)
    print_resultado("TESTE COM TOKEN INVÁLIDO (deve falhar)", response)

def test_20_sem_token():
    """Teste 20: Testar sem token"""
    url = f"{BASE_URL}/entradas"
    
    response = requests.get(url)
    print_resultado("TESTE SEM TOKEN (deve falhar)", response)

def run_all_tests():
    """Executa todos os testes"""
    print("\n" + "="*60)
    print("🚀 INICIANDO TESTES DA API GEFI")
    print("="*60 + "\n")
    
    try:
        # Testes básicos
        print("📋 FASE 1: AUTENTICAÇÃO")
        test_1_cadastro()
        input("\n⏸️  Pressione ENTER para continuar...")
        
        test_2_login()
        input("\n⏸️  Pressione ENTER para continuar...")
        
        # Testes de usuário
        print("\n📋 FASE 2: DADOS DO USUÁRIO")
        test_3_buscar_usuario()
        input("\n⏸️  Pressione ENTER para continuar...")
        
        test_4_salvar_questionario()
        input("\n⏸️  Pressione ENTER para continuar...")
        
        # Testes de entradas
        print("\n📋 FASE 3: ENTRADAS FINANCEIRAS")
        test_5_criar_entrada()
        input("\n⏸️  Pressione ENTER para continuar...")
        
        test_6_listar_entradas()
        input("\n⏸️  Pressione ENTER para continuar...")
        
        test_9_atualizar_entrada()
        input("\n⏸️  Pressione ENTER para continuar...")
        
        # Testes de saídas
        print("\n📋 FASE 4: SAÍDAS FINANCEIRAS")
        test_7_criar_saida()
        input("\n⏸️  Pressione ENTER para continuar...")
        
        test_8_listar_saidas()
        input("\n⏸️  Pressione ENTER para continuar...")
        
        test_10_atualizar_saida()
        input("\n⏸️  Pressione ENTER para continuar...")
        
        # Testes de análises
        print("\n📋 FASE 5: ANÁLISES FINANCEIRAS")
        test_11_calcular_balanco()
        input("\n⏸️  Pressione ENTER para continuar...")
        
        test_12_proximas_saidas()
        input("\n⏸️  Pressione ENTER para continuar...")
        
        test_13_categorias_gastos()
        input("\n⏸️  Pressione ENTER para continuar...")
        
        # Testes de investimentos
        print("\n📋 FASE 6: INVESTIMENTOS")
        test_14_listar_investimentos()
        input("\n⏸️  Pressione ENTER para continuar...")
        
        # Testes de segurança
        print("\n📋 FASE 7: SEGURANÇA E VALIDAÇÕES")
        test_15_mudar_senha()
        input("\n⏸️  Pressione ENTER para continuar...")
        
        test_18_recuperar_senha()
        input("\n⏸️  Pressione ENTER para continuar...")
        
        test_19_token_invalido()
        input("\n⏸️  Pressione ENTER para continuar...")
        
        test_20_sem_token()
        input("\n⏸️  Pressione ENTER para continuar...")
        
        # Testes de deleção (por último)
        print("\n📋 FASE 8: DELEÇÃO DE DADOS")
        test_16_deletar_entrada()
        input("\n⏸️  Pressione ENTER para continuar...")
        
        test_17_deletar_saida()
        
        print("\n" + "="*60)
        print("✅ TODOS OS TESTES CONCLUÍDOS!")
        print("="*60 + "\n")
        
    except KeyboardInterrupt:
        print("\n\n❌ Testes interrompidos pelo usuário.")
    except Exception as e:
        print(f"\n\n❌ Erro durante os testes: {e}")

def menu_interativo():
    """Menu interativo para escolher testes"""
    while True:
        print("\n" + "="*60)
        print("🧪 MENU DE TESTES - API GEFI")
        print("="*60)
        print("1.  Cadastro de usuário")
        print("2.  Login")
        print("3.  Buscar dados do usuário")
        print("4.  Salvar questionário")
        print("5.  Criar entrada")
        print("6.  Listar entradas")
        print("7.  Criar saída")
        print("8.  Listar saídas")
        print("9.  Atualizar entrada")
        print("10. Atualizar saída")
        print("11. Calcular balanço")
        print("12. Próximas saídas")
        print("13. Gastos por categoria")
        print("14. Listar investimentos")
        print("15. Mudar senha")
        print("16. Deletar entrada")
        print("17. Deletar saída")
        print("18. Recuperar senha")
        print("19. Teste token inválido")
        print("20. Teste sem token")
        print("="*60)
        print("0.  Executar TODOS os testes")
        print("Q.  Sair")
        print("="*60)
        
        escolha = input("\n🔹 Escolha uma opção: ").strip().upper()
        
        if escolha == 'Q':
            print("\n👋 Até logo!")
            break
        elif escolha == '0':
            run_all_tests()
        elif escolha == '1':
            test_1_cadastro()
        elif escolha == '2':
            test_2_login()
        elif escolha == '3':
            test_3_buscar_usuario()
        elif escolha == '4':
            test_4_salvar_questionario()
        elif escolha == '5':
            test_5_criar_entrada()
        elif escolha == '6':
            test_6_listar_entradas()
        elif escolha == '7':
            test_7_criar_saida()
        elif escolha == '8':
            test_8_listar_saidas()
        elif escolha == '9':
            test_9_atualizar_entrada()
        elif escolha == '10':
            test_10_atualizar_saida()
        elif escolha == '11':
            test_11_calcular_balanco()
        elif escolha == '12':
            test_12_proximas_saidas()
        elif escolha == '13':
            test_13_categorias_gastos()
        elif escolha == '14':
            test_14_listar_investimentos()
        elif escolha == '15':
            test_15_mudar_senha()
        elif escolha == '16':
            test_16_deletar_entrada()
        elif escolha == '17':
            test_17_deletar_saida()
        elif escolha == '18':
            test_18_recuperar_senha()
        elif escolha == '19':
            test_19_token_invalido()
        elif escolha == '20':
            test_20_sem_token()
        else:
            print("❌ Opção inválida!")
        
        input("\n⏸️  Pressione ENTER para voltar ao menu...")

if __name__ == "__main__":
    print("\n🎯 Certifique-se de que o servidor está rodando em http://localhost:5000\n")
    
    # Verifica se o servidor está rodando
    try:
        response = requests.get("http://localhost:5000/")
        if response.status_code == 200:
            print("✅ Servidor está online!\n")
            menu_interativo()
        else:
            print("❌ Servidor retornou status inesperado.")
    except requests.exceptions.ConnectionError:
        print("❌ ERRO: Não foi possível conectar ao servidor.")
        print("   Certifique-se de que está executando: python app.py")
    except Exception as e:
        print(f"❌ Erro: {e}")