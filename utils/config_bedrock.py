import boto3
from langchain_aws import BedrockEmbeddings, ChatBedrock
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_core.prompts import ChatPromptTemplate
from utils.env_func import env_func
from utils.logger_config import logger
bucket_name, profile_user_name = env_func() 

# Configuração do Bedrock LLM
def bedrock_llm():
    try:
        client = boto3.client('bedrock', region_name='us-east-1') # Especificar a região correta
        llm = ChatBedrock(
            model_id="meta.llama3-70b-instruct-v1:0",
            #max_tokens=3072,
            #temperature=0.7
            model_kwargs={
                    "prompt": "",  # Prompt inicial vazio
                    "max_gen_len": 300,  # Comprimento máximo da geração
                    "temperature": 0.1,  # Controle de aleatoriedade na geração de texto
                    "top_p": 0.5  # Amostragem de núcleo para considerar os tokens mais prováveis
                }   
        )
        logger.info(f'LLM {llm.model_id} carregada com sucesso')
        return llm
    except Exception as e:
        logger.error(f'Erro: {e}')


# Configuração de embeddings
def bedrock_embeddings():
    try: 
        client = boto3.client('bedrock', region_name='us-east-1') # Especificar a região correta
        embeddings = BedrockEmbeddings(
            model_id="amazon.titan-embed-text-v1"
        )
        logger.info(f'Gerando embbedings com {embeddings.model_id}')
        return embeddings
    except Exception as e:
        logger.error(f'Erro: {e}')


# configurações do separador de texto
def text_splitter_text():
    try:
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=500,
            chunk_overlap=150,
            add_start_index=True,
            separators=["\n\n", "\n", " "]
            )
        return text_splitter
    except Exception as e:
        logger.error(f'Erro: {e}')

# configuração do prompt para unir com a llm 
def prompt_template():
    try:
        prompt = ChatPromptTemplate.from_template("""
            You are a legal assistant who specializes in analyzing legal documents. 
            Try to answer the following question based solely on the context provided. 
            If the context provided is not useful, perform a new search in the vector database.
            Try to make a summary of no more than 250 words, ensuring that your explanation is complete.
            **Requirements:** 
            1. Answer in Brazilian Portuguese. 
            2. Identify and cite clauses, articles, restrictions, and specific references, for example: “e-STJ Fl.1680”. 
            3. Explain the meaning and importance of these elements in the context of the question. 
            4. Provide a detailed and accurate analysis based on the specified information. 
            5. Cite the sources of the documents, including the PDF document or other relevant files. 
            <context>
            {context}
            </context>
            Question: {input}""")
        return prompt
    except Exception as e:
        logger.error(f'Erro: {e}')


        #Fragmento retirado para teste
            # Answer the following question based only on the provided context. 
            # Think step by step before providing a detailed answer. 
            # Cite the sources, including the source PDF document   
            # Answer in Portuguese.   
            #  Você é um assistente jurídico especializado em analisar documentos jurídicos. 
            #    Responda à seguinte pergunta com base apenas no contexto fornecido. 
            #    **Requisitos:** 
            #    1. Identifique e cite cláusulas, artigos, seções, e referências específicas, por exemplo: "e-STJ Fl.1680". 
            #    2. Explique o significado e a importância desses elementos no contexto da pergunta. 
            #    3. Forneça uma análise detalhada e precisa com base nas informações identificadas. 
            #    4. Cite as fontes dos documentos, incluindo o documento PDF ou outros arquivos relevantes. 
            #    5. Responda em português.   

            #  You are a legal assistant who specializes in analyzing legal documents. 
            # Answer the following question based solely on the context provided. 
            # Try to make a summary of no more than 250 words, ensuring that your explanation is complete.
            #    **Requirements:** 
            #    1. Identify and cite clauses, articles, restrictions, and specific references, for example: “e-STJ Fl.1680”. 
            #    2. Explain the meaning and importance of these elements in the context of the question. 
            #    3. Provide a detailed and accurate analysis based on the specified information. 
            #    4. Cite the sources of the documents, including the PDF document or other relevant files. 
            #    5. Answer in Brazilian Portuguese.
