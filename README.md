# 🚀 Automação Meta Ads para Google Sheets

Automação completa para extrair dados de campanhas do Meta Ads e enviar para Google Sheets usando Composio SDK e GitHub Actions.

## 📋 Pré-requisitos

1. **Conta Composio** configurada em [app.composio.dev](https://app.composio.dev)
2. **Integrações ativas** no Composio:
   - Meta Ads (Facebook Ads)
   - Google Sheets
3. **Repositório GitHub** com GitHub Actions habilitado

## 🔧 Configuração Rápida

### 1. Clone e Configure o Repositório

```bash
git clone <seu-repositorio>
cd <nome-do-repositorio>
cp .env.example .env
```

### 2. Configure as Variáveis de Ambiente

Edite o arquivo `.env`:
```bash
COMPOSIO_TOKEN=your_composio_token_here
SPREADSHEET_ID=your_spreadsheet_id_here
```

### 3. Configure os Secrets no GitHub

Acesse: `Seu Repositório > Settings > Secrets and variables > Actions`

Adicione os seguintes **Repository secrets**:
- `COMPOSIO_TOKEN`: Token obtido em [Composio Settings](https://app.composio.dev/settings)
- `SPREADSHEET_ID`: ID da sua planilha Google Sheets

### 4. Execute o Teste Local (Opcional)

```bash
pip install -r requirements.txt
python run_composio.py
```

## ⚙️ Funcionamento

- **Agendamento**: A cada 2 minutos (configurável em `.github/workflows/composio_metaads.yml`)
- **Dados extraídos**: Campanhas ativas, métricas de performance, insights
- **Destino**: Google Sheets especificado no `SPREADSHEET_ID`

## 📁 Estrutura do Projeto

```
├── .github/
│   └── workflows/
│       └── composio_metaads.yml    # Workflow GitHub Actions
├── run_composio.py                 # Script principal
├── requirements.txt                # Dependências Python
├── .env.example                    # Exemplo de configuração
├── .gitignore                      # Arquivos ignorados
└── README.md                       # Esta documentação
```

## 🔍 Monitoramento

- **Logs de execução**: Disponíveis na aba "Actions" do repositório
- **Erros**: Salvos automaticamente como artifacts
- **Execução manual**: Disponível via "workflow_dispatch"

## 🛠️ Personalização

### Alterar Frequência de Execução

Edite o arquivo `.github/workflows/composio_metaads.yml`:
```yaml
schedule:
  - cron: '*/5 * * * *'  # A cada 5 minutos
```

### Adicionar Novas Métricas

Modifique o arquivo `run_composio.py` na função de extração de dados.

## 🆘 Solução de Problemas

### Erro de Autenticação
- Verifique se o `COMPOSIO_TOKEN` está correto
- Confirme se as integrações estão ativas no Composio

### Erro no Google Sheets
- Verifique se o `SPREADSHEET_ID` está correto
- Confirme se a planilha tem permissões adequadas

### Workflow não executa
- Verifique se os secrets estão configurados corretamente
- Confirme se o GitHub Actions está habilitado no repositório

## 📞 Suporte

Para dúvidas sobre:
- **Composio SDK**: [Documentação oficial](https://docs.composio.dev)
- **GitHub Actions**: [Documentação GitHub](https://docs.github.com/actions)

---

**✅ Status**: Pronto para produção
**🔄 Última atualização**: 19/09/2025
