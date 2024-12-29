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
    # Cria uma sessão boto3 com a região configurada
    session = boto3.Session(region_name='us-east-1')
    
    # Configura o CloudWatch LogHandler com a região
    cloudwatch_handler = watchtower.CloudWatchLogHandler(
        log_group="CHAT-RAG-GROUP-5",  # Nome do grupo de logs no CloudWatch
        stream_name="CHAT-RAG-GROUP-5",  # Nome do stream de logs
        boto3_session=session  # Passa a sessão boto3 configurada
    )
    logger.addHandler(cloudwatch_handler)
    logger.info("CloudWatch Logs configurado com sucesso.")
except NoCredentialsError as e:
    logger.error("Credenciais da AWS não configuradas corretamente.")
    raise e
except Exception as e:
    logger.error(f"Erro ao configurar o CloudWatch Logs: {str(e)}")
    raise e
