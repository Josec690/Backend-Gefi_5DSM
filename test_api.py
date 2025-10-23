import requests
import json
from datetime import datetime

BASE_URL = "http://localhost:8000"

class GeFiAPITester:
    def __init__(self):
        self.access_token = None
        self.user_data = {
            "cpf_user": "12345678901",
            "full_name": "João da Silva",
            "email": "joao@exemplo.com",
            "password": "Senha@123"
        }
    
    def test_user_registration(self):
        """Testa cadastro de usuário"""
        print("=== Testando Cadastro de Usuário ===")
        
        response = requests.post(
            f"{BASE_URL}/auth/register",
            json=self.user_data
        )
        
        if response.status_code == 201:
            print("✅ Usuário cadastrado com sucesso!")
            print(f"Dados: {response.json()}")
        else:
            print(f"❌ Erro no cadastro: {response.status_code} - {response.text}")
    
    def test_user_login(self):
        """Testa login do usuário"""
        print("\n=== Testando Login ===")
        
        response = requests.post(
            f"{BASE_URL}/auth/login",
            json={
                "email": self.user_data["email"],
                "password": self.user_data["password"]
            }
        )
        
        if response.status_code == 200:
            data = response.json()
            self.access_token = data["access_token"]
            print("✅ Login realizado com sucesso!")
            print(f"Token: {self.access_token[:50]}...")
        else:
            print(f"❌ Erro no login: {response.status_code} - {response.text}")
    
    def test_create_entrada(self):
        """Testa criação de entrada"""
        print("\n=== Testando Criação de Entrada ===")
        
        if not self.access_token:
            print("❌ Token necessário para esta operação")
            return
        
        headers = {"Authorization": f"Bearer {self.access_token}"}
        entrada_data = {
            "valor": 2500.00,
            "tipo": "Salário"
        }
        
        response = requests.post(
            f"{BASE_URL}/financial/entrada",
            json=entrada_data,
            headers=headers
        )
        
        if response.status_code == 201:
            print("✅ Entrada criada com sucesso!")
            print(f"Dados: {response.json()}")
        else:
            print(f"❌ Erro ao criar entrada: {response.status_code} - {response.text}")
    
    def test_create_saida(self):
        """Testa criação de saída"""
        print("\n=== Testando Criação de Saída ===")
        
        if not self.access_token:
            print("❌ Token necessário para esta operação")
            return
        
        headers = {"Authorization": f"Bearer {self.access_token}"}
        saida_data = {
            "valor": 350.00,
            "tipo": "Supermercado"
        }
        
        response = requests.post(
            f"{BASE_URL}/financial/saida",
            json=saida_data,
            headers=headers
        )
        
        if response.status_code == 201:
            print("✅ Saída criada com sucesso!")
            print(f"Dados: {response.json()}")
        else:
            print(f"❌ Erro ao criar saída: {response.status_code} - {response.text}")
    
    def test_get_resumo(self):
        """Testa obtenção de resumo financeiro"""
        print("\n=== Testando Resumo Financeiro ===")
        
        if not self.access_token:
            print("❌ Token necessário para esta operação")
            return
        
        headers = {"Authorization": f"Bearer {self.access_token}"}
        
        response = requests.get(
            f"{BASE_URL}/financial/resumo",
            headers=headers
        )
        
        if response.status_code == 200:
            print("✅ Resumo obtido com sucesso!")
            print(f"Dados: {json.dumps(response.json(), indent=2)}")
        else:
            print(f"❌ Erro ao obter resumo: {response.status_code} - {response.text}")
    
    def test_stock_data(self):
        """Testa obtenção de dados de ação"""
        print("\n=== Testando Dados de Ação (PETR4) ===")
        
        if not self.access_token:
            print("❌ Token necessário para esta operação")
            return
        
        headers = {"Authorization": f"Bearer {self.access_token}"}
        
        response = requests.get(
            f"{BASE_URL}/market/stock/PETR4.SA",
            headers=headers
        )
        
        if response.status_code == 200:
            print("✅ Dados de ação obtidos com sucesso!")
            data = response.json()
            print(f"Ação: {data.get('name', 'N/A')}")
            print(f"Preço atual: R$ {data.get('current_price', 0):.2f}")
            print(f"Variação: {data.get('change_percent', 0):.2f}%")
        else:
            print(f"❌ Erro ao obter dados da ação: {response.status_code} - {response.text}")
    
    def test_health_check(self):
        """Testa health check"""
        print("=== Testando Health Check ===")
        
        response = requests.get(f"{BASE_URL}/health")
        
        if response.status_code == 200:
            print("✅ API está saudável!")
            print(f"Dados: {response.json()}")
        else:
            print(f"❌ Erro no health check: {response.status_code}")
    
    def run_all_tests(self):
        """Executa todos os testes"""
        print("🚀 Iniciando testes da API GeFi\n")
        
        self.test_health_check()
        self.test_user_registration()
        self.test_user_login()
        
        if self.access_token:
            self.test_create_entrada()
            self.test_create_saida()
            self.test_get_resumo()
            self.test_stock_data()
        
        print("\n🎉 Testes concluídos!")

if __name__ == "__main__":
    tester = GeFiAPITester()
    tester.run_all_tests()