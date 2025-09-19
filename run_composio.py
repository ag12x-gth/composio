#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de Automação Meta Ads para Google Sheets
Desenvolvido para execução via GitHub Actions com Composio SDK

Funcionalidades:
- Extração de dados de campanhas do Meta Ads
- Processamento e formatação dos dados
- Atualização automática do Google Sheets
- Logging detalhado e tratamento de erros
"""

import os
import sys
import logging
import json
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
import traceback

try:
    from composio import Composio, Action
    print("✅ Composio SDK importado com sucesso")
except ImportError as e:
    print(f"❌ Erro ao importar Composio SDK: {e}")
    print("Execute: pip install composio-core")
    sys.exit(1)

# Configuração de logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler('composio_automation.log', encoding='utf-8')
    ]
)
logger = logging.getLogger(__name__)

class MetaAdsAutomation:
    """Classe principal para automação Meta Ads -> Google Sheets"""

    def __init__(self):
        """Inicializa a classe com configurações do ambiente"""
        self.composio_token = os.getenv('COMPOSIO_TOKEN')
        self.spreadsheet_id = os.getenv('SPREADSHEET_ID')
        self.composio_client = None

        # Validar variáveis de ambiente
        if not self.composio_token:
            raise ValueError("❌ COMPOSIO_TOKEN não encontrado nas variáveis de ambiente")

        if not self.spreadsheet_id:
            raise ValueError("❌ SPREADSHEET_ID não encontrado nas variáveis de ambiente")

        logger.info("🚀 Iniciando automação Meta Ads")
        logger.info(f"📊 Spreadsheet ID: {self.spreadsheet_id}")

    def initialize_composio(self) -> bool:
        """Inicializa o cliente Composio"""
        try:
            self.composio_client = Composio(api_key=self.composio_token)
            logger.info("✅ Cliente Composio inicializado com sucesso")
            return True
        except Exception as e:
            logger.error(f"❌ Erro ao inicializar Composio: {str(e)}")
            return False

    def get_meta_ads_campaigns(self) -> Optional[List[Dict]]:
        """Extrai dados das campanhas do Meta Ads"""
        try:
            logger.info("📱 Extraindo dados das campanhas Meta Ads...")

            # Configurar parâmetros para busca de campanhas
            campaign_params = {
                "fields": [
                    "id",
                    "name", 
                    "status",
                    "objective",
                    "created_time",
                    "updated_time",
                    "daily_budget",
                    "lifetime_budget",
                    "budget_remaining",
                    "start_time",
                    "stop_time"
                ],
                "limit": 100,
                "effective_status": ["ACTIVE", "PAUSED"]
            }

            # Executar ação para obter campanhas
            campaigns_response = self.composio_client.execute_action(
                action=Action.METAADS_GET_CAMPAIGNS,
                params=campaign_params,
                entity_id="metaads-hiwull"
            )

            if campaigns_response and 'data' in campaigns_response:
                campaigns = campaigns_response['data']
                logger.info(f"✅ {len(campaigns)} campanhas encontradas")
                return campaigns
            else:
                logger.warning("⚠️ Nenhuma campanha encontrada")
                return []

        except Exception as e:
            logger.error(f"❌ Erro ao extrair campanhas Meta Ads: {str(e)}")
            logger.error(traceback.format_exc())
            return None

    def get_campaign_insights(self, campaign_id: str) -> Optional[Dict]:
        """Obtém insights/métricas de uma campanha específica"""
        try:
            # Data range - últimos 7 dias
            end_date = datetime.now()
            start_date = end_date - timedelta(days=7)

            insights_params = {
                "level": "campaign",
                "fields": [
                    "campaign_id",
                    "campaign_name",
                    "impressions",
                    "clicks",
                    "spend",
                    "reach",
                    "frequency",
                    "ctr",
                    "cpc",
                    "cpm",
                    "cpp",
                    "conversions",
                    "cost_per_conversion",
                    "conversion_rate"
                ],
                "time_range": {
                    "since": start_date.strftime("%Y-%m-%d"),
                    "until": end_date.strftime("%Y-%m-%d")
                },
                "breakdowns": ["device_platform"],
                "time_increment": 1
            }

            insights_response = self.composio_client.execute_action(
                action=Action.METAADS_GET_INSIGHTS,
                params={
                    "campaign_id": campaign_id,
                    **insights_params
                },
                entity_id="metaads-hiwull"
            )

            if insights_response and 'data' in insights_response:
                return insights_response['data']

            return None

        except Exception as e:
            logger.error(f"❌ Erro ao obter insights da campanha {campaign_id}: {str(e)}")
            return None

    def process_campaign_data(self, campaigns: List[Dict]) -> List[List]:
        """Processa dados das campanhas para formato Google Sheets"""
        try:
            logger.info("🔄 Processando dados das campanhas...")

            # Cabeçalho da planilha
            headers = [
                "Data/Hora Atualização",
                "ID Campanha", 
                "Nome Campanha",
                "Status",
                "Objetivo",
                "Orçamento Diário",
                "Orçamento Total",
                "Orçamento Restante",
                "Data Criação",
                "Data Início",
                "Data Fim",
                "Impressões",
                "Cliques", 
                "Gastos (R$)",
                "Alcance",
                "Frequência",
                "CTR (%)",
                "CPC (R$)",
                "CPM (R$)",
                "Conversões",
                "Custo por Conversão (R$)",
                "Taxa de Conversão (%)"
            ]

            processed_data = [headers]
            current_time = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

            for campaign in campaigns:
                try:
                    # Dados básicos da campanha
                    campaign_id = campaign.get('id', '')
                    campaign_name = campaign.get('name', '')
                    status = campaign.get('status', '')
                    objective = campaign.get('objective', '')
                    daily_budget = campaign.get('daily_budget', 0)
                    lifetime_budget = campaign.get('lifetime_budget', 0)
                    budget_remaining = campaign.get('budget_remaining', 0)
                    created_time = campaign.get('created_time', '')
                    start_time = campaign.get('start_time', '')
                    stop_time = campaign.get('stop_time', '')

                    # Obter insights da campanha
                    insights = self.get_campaign_insights(campaign_id)

                    # Valores padrão para métricas
                    impressions = 0
                    clicks = 0
                    spend = 0
                    reach = 0
                    frequency = 0
                    ctr = 0
                    cpc = 0
                    cpm = 0
                    conversions = 0
                    cost_per_conversion = 0
                    conversion_rate = 0

                    # Processar insights se disponíveis
                    if insights and len(insights) > 0:
                        # Agregar métricas de todos os insights
                        for insight in insights:
                            impressions += int(insight.get('impressions', 0))
                            clicks += int(insight.get('clicks', 0))
                            spend += float(insight.get('spend', 0))
                            reach += int(insight.get('reach', 0))
                            frequency += float(insight.get('frequency', 0))
                            conversions += int(insight.get('conversions', 0))

                        # Calcular métricas derivadas
                        if impressions > 0:
                            ctr = (clicks / impressions) * 100
                            cpm = (spend / impressions) * 1000

                        if clicks > 0:
                            cpc = spend / clicks

                        if conversions > 0:
                            cost_per_conversion = spend / conversions
                            conversion_rate = (conversions / clicks) * 100 if clicks > 0 else 0

                        # Média da frequência
                        if len(insights) > 0:
                            frequency = frequency / len(insights)

                    # Formatação de datas
                    created_date = self.format_date(created_time)
                    start_date = self.format_date(start_time)
                    end_date = self.format_date(stop_time)

                    # Linha de dados
                    row_data = [
                        current_time,
                        campaign_id,
                        campaign_name,
                        status,
                        objective,
                        f"R$ {daily_budget/100:.2f}" if daily_budget else "N/A",
                        f"R$ {lifetime_budget/100:.2f}" if lifetime_budget else "N/A", 
                        f"R$ {budget_remaining/100:.2f}" if budget_remaining else "N/A",
                        created_date,
                        start_date,
                        end_date,
                        f"{impressions:,}",
                        f"{clicks:,}",
                        f"R$ {spend:.2f}",
                        f"{reach:,}",
                        f"{frequency:.2f}",
                        f"{ctr:.2f}%",
                        f"R$ {cpc:.2f}",
                        f"R$ {cpm:.2f}",
                        f"{conversions:,}",
                        f"R$ {cost_per_conversion:.2f}",
                        f"{conversion_rate:.2f}%"
                    ]

                    processed_data.append(row_data)
                    logger.info(f"✅ Processada campanha: {campaign_name}")

                except Exception as e:
                    logger.error(f"❌ Erro ao processar campanha {campaign.get('name', 'Unknown')}: {str(e)}")
                    continue

            logger.info(f"✅ {len(processed_data)-1} campanhas processadas com sucesso")
            return processed_data

        except Exception as e:
            logger.error(f"❌ Erro no processamento dos dados: {str(e)}")
            logger.error(traceback.format_exc())
            return []

    def format_date(self, date_string: str) -> str:
        """Formata string de data para formato brasileiro"""
        if not date_string:
            return "N/A"

        try:
            # Parse ISO format
            if 'T' in date_string:
                date_obj = datetime.fromisoformat(date_string.replace('Z', '+00:00'))
                return date_obj.strftime("%d/%m/%Y %H:%M")
            else:
                return date_string
        except:
            return date_string

    def update_google_sheets(self, data: List[List]) -> bool:
        """Atualiza Google Sheets com os dados processados"""
        try:
            logger.info("📊 Atualizando Google Sheets...")

            if not data or len(data) <= 1:
                logger.warning("⚠️ Nenhum dado para atualizar")
                return False

            # Limpar planilha primeiro
            clear_params = {
                "spreadsheet_id": self.spreadsheet_id,
                "range": "A:Z"  # Limpar colunas A até Z
            }

            clear_response = self.composio_client.execute_action(
                action=Action.GOOGLESHEETS_CLEAR_VALUES,
                params=clear_params,
                entity_id="googlesheets-metaads"
            )

            logger.info("🧹 Planilha limpa com sucesso")

            # Atualizar com novos dados
            update_params = {
                "spreadsheet_id": self.spreadsheet_id,
                "range": "A1",  # Começar da célula A1
                "values": data,
                "value_input_option": "RAW"
            }

            update_response = self.composio_client.execute_action(
                action=Action.GOOGLESHEETS_UPDATE_VALUES,
                params=update_params,
                entity_id="googlesheets-metaads"
            )

            if update_response:
                logger.info(f"✅ Google Sheets atualizado com {len(data)-1} campanhas")
                return True
            else:
                logger.error("❌ Falha na atualização do Google Sheets")
                return False

        except Exception as e:
            logger.error(f"❌ Erro ao atualizar Google Sheets: {str(e)}")
            logger.error(traceback.format_exc())
            return False

    def run_automation(self) -> bool:
        """Executa o processo completo de automação"""
        try:
            logger.info("🚀 Iniciando processo de automação...")

            # 1. Inicializar Composio
            if not self.initialize_composio():
                return False

            # 2. Extrair campanhas Meta Ads
            campaigns = self.get_meta_ads_campaigns()
            if campaigns is None:
                logger.error("❌ Falha na extração de campanhas")
                return False

            if len(campaigns) == 0:
                logger.info("ℹ️ Nenhuma campanha encontrada")
                return True

            # 3. Processar dados
            processed_data = self.process_campaign_data(campaigns)
            if not processed_data:
                logger.error("❌ Falha no processamento dos dados")
                return False

            # 4. Atualizar Google Sheets
            success = self.update_google_sheets(processed_data)
            if not success:
                logger.error("❌ Falha na atualização do Google Sheets")
                return False

            logger.info("🎉 Automação concluída com sucesso!")
            return True

        except Exception as e:
            logger.error(f"❌ Erro na execução da automação: {str(e)}")
            logger.error(traceback.format_exc())
            return False

def main():
    """Função principal"""
    try:
        # Criar instância da automação
        automation = MetaAdsAutomation()

        # Executar automação
        success = automation.run_automation()

        if success:
            logger.info("✅ Processo finalizado com sucesso")
            sys.exit(0)
        else:
            logger.error("❌ Processo finalizado com erros")
            sys.exit(1)

    except Exception as e:
        logger.error(f"❌ Erro crítico: {str(e)}")
        logger.error(traceback.format_exc())
        sys.exit(1)

if __name__ == "__main__":
    main()
