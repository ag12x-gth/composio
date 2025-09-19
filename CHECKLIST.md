
# ✅ CHECKLIST DE CONFIGURAÇÃO - META ADS AUTOMATION

## 📋 ANTES DE FAZER O DEPLOY

### 1. Arquivos do Projeto
- [ ] run_composio.py (script principal)
- [ ] .github/workflows/composio_metaads.yml (workflow)
- [ ] requirements.txt (dependências)
- [ ] README.md (documentação)
- [ ] .env.example (exemplo de configuração)
- [ ] .gitignore (arquivos ignorados)

### 2. Configuração do Composio
- [ ] Conta criada em app.composio.dev
- [ ] Integração Meta Ads ativa e autenticada
- [ ] Integração Google Sheets ativa e autenticada
- [ ] Token Composio obtido (Settings > API Keys)

### 3. Configuração do Google Sheets
- [ ] Planilha criada no Google Sheets
- [ ] ID da planilha copiado (da URL)
- [ ] Permissões adequadas configuradas

### 4. Configuração do GitHub
- [ ] Repositório criado
- [ ] GitHub Actions habilitado
- [ ] Secret COMPOSIO_TOKEN configurado
- [ ] Secret SPREADSHEET_ID configurado

### 5. Teste Local (Recomendado)
- [ ] Arquivo .env criado com as configurações
- [ ] Dependências instaladas (pip install -r requirements.txt)
- [ ] Script executado com sucesso (python run_composio.py)

## 🚀 APÓS O DEPLOY

### 1. Monitoramento
- [ ] Primeiro workflow executado com sucesso
- [ ] Dados aparecendo no Google Sheets
- [ ] Logs verificados na aba Actions

### 2. Validação
- [ ] Agendamento funcionando corretamente
- [ ] Dados atualizando a cada 2 minutos
- [ ] Sem erros nos logs

## 🔧 CONFIGURAÇÕES AVANÇADAS (Opcional)

- [ ] Ajustar frequência de execução
- [ ] Configurar notificações de erro
- [ ] Adicionar métricas customizadas
- [ ] Configurar backup dos dados

---
Data da configuração: 19/09/2025 07:25
