import os
import uuid
from langchain_community.document_loaders import PyPDFLoader
from utils.config_bedrock import text_splitter_text
from utils.logger_config import logger


def s3_pull(s3,bucket_name,):
    try:
        # Criar diretório temporário
        os.makedirs("tmp", exist_ok=True)

        # Carregar arquivos do bucket S3
        files_from_bucket = s3.list_objects_v2(Bucket=bucket_name)
        if 'Contents' in files_from_bucket:
            docs = []
            count = 0
            for obj_bucket in files_from_bucket['Contents']:
                file_key = obj_bucket['Key']
                if file_key.endswith('.pdf'):
                    count += 1 
                    local_file_path = f"tmp/{uuid.uuid4()}_{file_key.split('/')[-1]}"                           
                    s3.download_file(bucket_name, file_key, local_file_path)
                                     
                    # chama a função abaixo para extrair conteudo do pdf e separar o texto em chucks
                    text_extractor(docs,local_file_path,file_key,text_splitter_text())
        logger.info(f"{count} Documentos extraídos do bucket {bucket_name} com sucesso")
        return docs
    except Exception as e:
        # print(f"Erro ao salvar arquivos do s3 {e}")
        logger.error(f"Erro ao extrair arquivos do s3 {e}")
            

def text_extractor(docs,local_file_path,file_key, text_to_split):
    try:
        # Carregar e processar documentos
        loader = PyPDFLoader(local_file_path)
        local_docs = loader.load()
                
        chunks_from_document = text_to_split.split_documents(local_docs)

        # Adicionar o nome do arquivo como metadado a cada chunk
        for chunk in chunks_from_document:
            chunk.metadata["source"] = file_key
        docs.extend(chunks_from_document)
        logger.info(f"{file_key} dividido em Chunks com sucesso")
    except Exception as e:
        # print(f"Erro no text spliter {e}")
        logger.error(f"Erro no text spliter {e}")
    finally:
        os.remove(local_file_path)  # Remove o arquivo local

        # Validar chunks, na verdade apenas verifica, util para testes
        # for i, chunk in enumerate(docs[:5]):  # Exibir os primeiros 5 chunks
        #     print(f"Chunk {i+1} (Arquivo: {chunk.metadata['source']}):\n{chunk.page_content[:200]}...\n")
        