# função para carregar as variaveis de ambiente usadas
import os
from dotenv import load_dotenv


def env_func():
    try:
        # Especifique o caminho do .env um diretório acima
        dotenv_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), '.env')
        dotenv_path = os.path.join('config', '.env') 
        load_dotenv(dotenv_path)  # Carrega as variáveis do .env

        bucket_name = os.getenv('BUCKET_NAME')
        profile_user_name= os.getenv('SESSION_NAME')
    except Exception as e:
        # print(f"Erro de carregamento de env {e}")
        from utils.logger_config import logger
        logger.error(f"Erro de carregamento de env {e}")
    
    return bucket_name, profile_user_name

def env_func_telegram():
    try:
        # Especifique o caminho do .env um diretório acima
        dotenv_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), '.env')
        dotenv_path = os.path.join('config', '.env') 
        load_dotenv(dotenv_path)  # Carrega as variáveis do .env

        token = os.getenv('TOKEN_TELEGRAM')
    except Exception as e:
        # print(f"Erro de carregamento de env {e}")
        from utils.logger_config import logger
        logger.error(f"Erro de carregamento de env {e}")
    
    return token   