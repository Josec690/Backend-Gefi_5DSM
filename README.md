# 🔧 GeFi Backend - API REST

Backend do sistema de gestão financeira desenvolvido com Flask (Python) e MongoDB.

---

## 📋 Pré-requisitos

Antes de começar, certifique-se de ter instalado:

- **Python 3.8+** ([Download](https://www.python.org/downloads/))
- **MongoDB** rodando localmente ou acesso a um cluster MongoDB Atlas
- **Git** (opcional, para clonar o repositório)

---

## 🚀 Instalação e Execução

### 🔹 Clonar o repositório

```bash
git clone https://github.com/seu-usuario/seu-repo.git

```

---

### Método 1: Script Automático (Windows)

```bash
cd seu-repo
.\start.bat
```

O script irá:
1. Criar um ambiente virtual Python (se não existir)
2. Ativar o ambiente virtual
3. Instalar todas as dependências
4. Iniciar o servidor Flask

### Método 2: Manual

```bash
# 1. Navegue até o diretório do backend
cd Backend

# 2. Crie um ambiente virtual
python -m venv venv

# 3. Ative o ambiente virtual
# Windows PowerShell:
.\venv\Scripts\Activate.ps1
# Windows CMD:
venv\Scripts\activate.bat
# Linux/Mac:
source venv/bin/activate

# 4. Instale as dependências
pip install -r requirements.txt

# 5. Inicie o servidor
python app.py
```

---

## 🌐 Endpoints Disponíveis

O servidor estará rodando em: **http://localhost:5000**

### Autenticação
- `POST /api/auth/cadastro` - Cadastrar novo usuário
- `POST /api/auth/login` - Fazer login
- `POST /api/auth/solicitar-codigo` - Solicitar código de recuperação
- `POST /api/auth/redefinir-senha` - Redefinir senha

### Usuário (requer autenticação)
- `GET /api/usuario/perfil` - Obter dados do perfil
- `PUT /api/usuario/perfil` - Atualizar perfil
- `PUT /api/usuario/alterar-senha` - Alterar senha

### Entradas (requer autenticação)
- `GET /api/entradas` - Listar entradas
- `POST /api/entradas` - Criar entrada
- `PUT /api/entradas/<id>` - Atualizar entrada
- `DELETE /api/entradas/<id>` - Deletar entrada

### Saídas (requer autenticação)
- `GET /api/saidas` - Listar saídas
- `POST /api/saidas` - Criar saída
- `PUT /api/saidas/<id>` - Atualizar saída
- `DELETE /api/saidas/<id>` - Deletar saída

### Análises (requer autenticação)
- `GET /api/analise/balanco` - Obter balanço financeiro
- `GET /api/analise/proximas-saidas` - Próximas saídas recorrentes

### Investimentos
- `GET /api/investimentos` - Lista investimentos recomendados (requer autenticação)
- `GET /api/investimentos/cotacao?ticker=VALE3` - Cotação em tempo real
- `GET /api/investimentos/em-alta` - Ações em alta do dia
- `GET /api/investimentos/tesouro` - Títulos do Tesouro Direto
- `GET /api/investimentos/historico?ticker=VALE3&periodo=1M` - Histórico de preços

---

## 📦 Dependências Principais

```
Flask==3.1.0              # Framework web
flask-cors==5.0.0         # CORS para comunicação com frontend
PyJWT==2.10.1             # Autenticação JWT
pymongo==4.10.1           # Driver MongoDB
bcrypt==4.2.1             # Hash de senhas
httpx==0.28.1             # Cliente HTTP para APIs externas
yfinance==0.2.50          # Dados financeiros do Yahoo Finance
pandas==2.2.3             # Manipulação de dados
python-dotenv==1.0.1      # Variáveis de ambiente
```

---

## ⚙️ Configuração



### Configuração do MongoDB

O backend se conecta ao MongoDB em `mongodb://localhost:27017/gefi` por padrão. Para usar MongoDB Atlas ou outro servidor:

1. Edite o arquivo `config/database.py`
2. Altere a `MONGO_URI` para sua conexão

---

## 🗂️ Estrutura do Projeto

```
Backend/
├── app.py                  # Entrada principal
├── config/
│   └── database.py         # Configuração MongoDB
├── controllers/            # Lógica de negócio
│   ├── analise_controller.py
│   ├── auth_controller.py
│   ├── entrada_controller.py
│   ├── investimento_controller.py
│   ├── saida_controller.py
│   └── user_controller.py
├── models/                 # Modelos de dados
│   ├── entrada_model.py
│   ├── saida_model.py
│   └── usuario_model.py
├── routes/                 # Rotas da API
│   ├── analise_routes.py
│   ├── auth_routes.py
│   ├── entrada_routes.py
│   ├── investimento_routes.py
│   ├── saida_routes.py
│   └── user_routes.py
├── utils/                  # Utilitários
│   ├── auth.py            # Decoradores de autenticação
│   └── validators.py      # Validações
├── requirements.txt        # Dependências Python
└── start.bat              # Script de inicialização
```

---

## 🐛 Troubleshooting

### Erro: "MongoDB connection failed"
- Verifique se o MongoDB está rodando: `mongod --version`
- Confirme a URI de conexão em `config/database.py`

### Erro: "Port 5000 is already in use"
- Pare outros processos na porta 5000:
  ```bash
  # Windows
  netstat -ano | findstr :5000
  taskkill /PID <PID> /F
  ```

### Erro: "Module not found"
- Certifique-se de que o ambiente virtual está ativado
- Reinstale as dependências: `pip install -r requirements.txt`

### APIs de investimento não retornam dados
- **Brapi** (fonte primária): Gratuita, sem necessidade de token
- **yfinance** (fallback): Pode ter rate limits, use com moderação

---

## 🔒 Segurança

- Senhas são criptografadas com **bcrypt**
- Autenticação via **JWT tokens**
- CORS configurado para aceitar requisições do frontend
- Validações de entrada em todos os endpoints

---

## 📊 Recursos de Investimentos

- **Brapi**: Cotações em tempo real do mercado brasileiro
- **yfinance**: Histórico de preços com fallback automático
- **Tesouro Direto**: API oficial do governo
- **Cache inteligente**: 5 minutos para otimizar performance

---

## 🤝 Contribuindo

1. Faça um fork do projeto
2. Crie uma branch para sua feature (`git checkout -b feature/nova-feature`)
3. Commit suas mudanças (`git commit -m 'Adiciona nova feature'`)
4. Push para a branch (`git push origin feature/nova-feature`)
5. Abra um Pull Request

---

## 📝 Licença

Este projeto é parte do trabalho acadêmico do curso de Desenvolvimento de Software Multiplataforma.

---

## 📧 Suporte

Para dúvidas ou problemas, abra uma issue no repositório do projeto.

**🎉 Backend pronto para uso!**