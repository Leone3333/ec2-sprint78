import logging
import boto3
import watchtower
from botocore.exceptions import NoCredentialsError
from utils.env_func import env_func

bucket_name, profile_user_name = env_func()

# Configura o logger
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Adiciona um StreamHandler para o console
console_handler = logging.StreamHandler()
logger.addHandler(console_handler)

try:
    # Configura o CloudWatch LogHandler com a região explicitamente
    cloudwatch_handler = watchtower.CloudWatchLogHandler(
        log_group="CHAT-RAG-GROUP-5",
        stream_name="CHAT-RAG-GROUP-5",
        region_name="us-east-1"  # Região explícita
    )
    logger.addHandler(cloudwatch_handler)
    logger.info("CloudWatch Logs configurado com sucesso.")
except NoCredentialsError as e:
    logger.error("Credenciais da AWS não configuradas corretamente.")
    raise e
except Exception as e:
    logger.error(f"Erro ao configurar o CloudWatch Logs: {str(e)}")
    raise e
