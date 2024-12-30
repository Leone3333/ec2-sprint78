import os
import boto3
from langchain_community.vectorstores import Chroma
from utils.env_func import env_func
from utils.indexing.s3_base_rag import s3_pull
from utils.logger_config import logger

# carrega o banco chroma com os embeddings, 
# recebe o diretorio do chromadb e os embeddings
def vectore_store_louder(persist_directory,bedrock_embeddings_from_docs):
    # Verifica se o banco já existe
    if os.path.exists(persist_directory):
        # print("Carregando banco de dados existente...")
        logger.info("Carregando banco de dados existente...")
        try:
            vector_store = Chroma(persist_directory=persist_directory, embedding_function=bedrock_embeddings_from_docs)
            # print("Banco vetorial para llm carregado")
            logger.info("Banco de Dados Vetorial ChromaDB carregado")
            return vector_store
        except Exception as e:
            # print(f"ERRO: Banco vetorial não carregado {e}")
            logger.error(f"ERRO: Banco vetorial não carregado {e}")
    else:
        # Configuração da sessão AWS
        try:
            bucket_name, profile_user_name = env_func()
            session = boto3.Session(profile_name=profile_user_name)
            s3 = session.client('s3')

            # Chama função que puxa os dados do bucket e separa em chunks
            docs_juridcs = s3_pull(s3=s3, bucket_name=bucket_name)

            # Criar a base de dados vetorial com Chroma
            vector_store = Chroma.from_documents(
                documents=docs_juridcs,
                embedding=bedrock_embeddings_from_docs,
                persist_directory="vector_store/chroma/"
            )
            # print("Armazenado usando ChromaDB")
            logger.info("Banco de Dados Vetorial ChromaDB carregado")
            return vector_store
        except Exception as e:
            logger.error(f"Erro na criação do BD vetorial {e}")
