from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains.retrieval import create_retrieval_chain
from utils.logger_config import logger

def chatbot(vector_store,llm,prompt,question):
    try:
        # Adicionar um print para depurar objetos
        # print(f"bedrock_llm: {bedrock_llm}")
        # print(f"vector_store as retriever: {vector_store.as_retriever}")

        # Configurar o retriever
        retriever = vector_store.as_retriever(search_type="similarity", search_kwargs={"k": 20})

        # Criar a cadeia de documentos combinados
        combine_docs_chain = create_stuff_documents_chain(
            llm, prompt
        )

        # Criar a cadeia de recuperação
        retrieval_chain = create_retrieval_chain(
            retriever, combine_docs_chain
        )

        try:
            # Obter a resposta final
            result=retrieval_chain.run({"input": "Oque é um documento de agravo?"})
            logger.info(f'Resultado da consulta: {result}')
        except Exception as e:
            print(dir(retrieval_chain))
            logger.error(f"Erro no invoke: {e}")
    
        response = result.get('answer', 'Não consegui encontrar uma resposta adequada.')
        return response

        # source_documents = result.get("context", [])
        # if source_documents:
        #     for i, doc in enumerate(source_documents):
        #         source = doc.metadata.get("source", "Arquivo desconhecido")
        #         print(f"Documento {i+1} (Fonte: {source}):\n{doc.page_content[:500]}...\n")
        # else:
        #     print("Nenhum documento fonte encontrado.")

    except Exception as e:
        # print(f"Erro: {e}, Detalhes: {e.__traceback__}")
        logger.error(f"Erro: {e}, Detalhes: {e.__traceback__}")
