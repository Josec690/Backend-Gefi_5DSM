# 🚀 Guia de Teste - Integração Brapi + Tesouro Direto

## ✅ O que foi implementado

### Backend (Python/Flask)
1. **Brapi** como fonte primária de cotações (gratuita, sem necessidade de token)
2. **Fallback para yfinance** quando Brapi não retornar dados
3. **API oficial do Tesouro Direto** para títulos públicos
4. **Cache em memória** (TTL de 5 minutos padrão)
5. **3 novos endpoints**:
   - `GET /api/investimentos/cotacao?ticker=VALE3` - Cotação individual
   - `GET /api/investimentos/em-alta` - Top ações em alta
   - `GET /api/investimentos/tesouro` - Títulos do Tesouro Direto

### Frontend (React Native)
1. **3 seções na tela de Investimentos**:
   - 🔥 Investimentos em Alta
   - 🏛️ Tesouro Direto
   - 📊 Investimentos Recomendados
2. **Pull-to-refresh** para atualizar dados
3. **Exibição de preços e variação percentual** em tempo real

---

## 🧪 Como testar

### 1. Instalar dependência (se necessário)
```powershell
cd "c:\Users\user\Desktop\PI-Gefi_5DSM\Backend"
pip install httpx
```

### 2. Iniciar o backend
```powershell
cd "c:\Users\user\Desktop\PI-Gefi_5DSM\Backend"
python app.py
```

### 3. Testar endpoints no PowerShell

#### Teste 1: Cotação individual (Brapi)
```powershell
Invoke-WebRequest -Uri "http://localhost:5000/api/investimentos/cotacao?ticker=VALE3" -Method GET | ConvertFrom-Json | ConvertTo-Json -Depth 5
```

**Resultado esperado:**
```json
{
  "ticker": "VALE3",
  "preco": 58.75,
  "variacao": 1.23,
  "variacao_percentual": 2.14,
  "timestamp": "2025-11-16T...",
  "fonte": "brapi"
}
```

#### Teste 2: Investimentos em alta
```powershell
Invoke-WebRequest -Uri "http://localhost:5000/api/investimentos/em-alta" -Method GET | ConvertFrom-Json | ConvertTo-Json -Depth 5
```

**Resultado esperado:** Lista de 5-10 ações com maior valorização do dia

#### Teste 3: Tesouro Direto
```powershell
Invoke-WebRequest -Uri "http://localhost:5000/api/investimentos/tesouro" -Method GET | ConvertFrom-Json | ConvertTo-Json -Depth 5
```

**Resultado esperado:** Lista de títulos públicos disponíveis

#### Teste 4: Lista geral (autenticado)
Primeiro, faça login e pegue o token:
```powershell
$login = Invoke-WebRequest -Uri "http://localhost:5000/api/login" -Method POST -ContentType "application/json" -Body '{"email":"seu@email.com","senha":"suasenha"}' | ConvertFrom-Json
$token = $login.token

# Agora teste a lista com autenticação
$headers = @{"Authorization" = "Bearer $token"}
Invoke-WebRequest -Uri "http://localhost:5000/api/investimentos" -Method GET -Headers $headers | ConvertFrom-Json | ConvertTo-Json -Depth 5
```

---

## 📱 Testar no App (React Native)

### 1. Registrar tela no App.js
Adicione ao `App.js`:
```javascript
import TelaInvestimento from './screens/TelaInvestimento';

// Dentro do Stack.Navigator:
<Stack.Screen name="Investimentos" component={TelaInvestimento} />
```

### 2. Navegar para a tela
De qualquer tela autenticada:
```javascript
navigation.navigate('Investimentos');
```

### 3. O que você verá:
- 🔥 **Investimentos em Alta**: Top 5 ações com maior valorização
- 🏛️ **Tesouro Direto**: Títulos públicos disponíveis com taxas
- 📊 **Recomendados**: Seus investimentos com preços atualizados
- **Pull down to refresh** para atualizar dados

---

## 🔧 Configurações opcionais

### Token Brapi (aumenta limite de requisições)
Crie conta gratuita em https://brapi.dev e adicione no `.env`:
```
BRAPI_TOKEN=seu_token_aqui
```

### Ajustar TTL do cache
No `.env`:
```
INVEST_CACHE_TTL=300  # 5 minutos (padrão)
```

---

## 🐛 Troubleshooting

### Erro: "httpx não encontrado"
```powershell
pip install httpx
```

### Erro: "Não foi possível buscar investimentos em alta"
- Brapi pode estar temporariamente indisponível
- Sistema usa fallback automático para dados estáticos

### Preços aparecem como "null"
- Normal em horários fora do pregão (mercado fechado)
- Fim de semana/feriados não retornam cotações
- Sistema tenta yfinance como fallback

### Frontend não conecta
Verifique o IP no `Frontend/services/api.js`:
```javascript
return 'http://localhost:5000/api';  // Ajuste para seu IP
```

---

## 📊 Arquitetura da solução

```
┌─────────────────┐
│   Frontend      │
│  (React Native) │
└────────┬────────┘
         │ HTTP/JSON
┌────────▼────────┐
│   Backend Flask │
│   Controller    │
└────────┬────────┘
         │
    ┌────┴─────────────┐
    │                  │
┌───▼────┐      ┌─────▼──────┐
│ Brapi  │      │  Tesouro   │
│ (1º)   │      │  Direto    │
└───┬────┘      │  (Oficial) │
    │ falha     └────────────┘
┌───▼────┐
│yfinance│
│ (2º)   │
└────────┘
```

---

## ✅ Checklist de validação

- [ ] Backend inicia sem erros
- [ ] Endpoint `/cotacao` retorna dados da Brapi
- [ ] Endpoint `/em-alta` retorna ações valorizadas
- [ ] Endpoint `/tesouro` retorna títulos
- [ ] Frontend exibe 3 seções corretamente
- [ ] Pull-to-refresh funciona
- [ ] Preços aparecem formatados (R$ XX.XX)
- [ ] Variação aparece colorida (verde/vermelho)

---

## 🎯 Próximos passos sugeridos

1. **Adicionar gráficos** (react-native-chart-kit)
2. **Histórico de preços** (usar endpoint Brapi `/quote/{ticker}/history`)
3. **Alertas de preço** (notificar quando atingir meta)
4. **Comparar investimentos** (side-by-side)
5. **Simulador de rentabilidade**

---


