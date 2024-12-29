import os
import time
import random
# import boto3
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
from utils.env_func import env_func_telegram
from utils.chatbot import chatbot
# from utils.indexing.s3_base_rag import s3_pull
from utils.indexing.chromadb import vectore_store_louder
from utils.config_bedrock import *
from utils.logger_config import logger

# Lista para armazenar o histórico de mensagens
chat_history = []

# Função de configuração do Telegram
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Olá! Sou o assistente jurídico. Pergunte sobre documentos ou informações específicas.")

# Função para retry com backoff exponencial
def retry_with_backoff(function, max_retries=4):
    retries = 0
    while retries < max_retries:
        try:
            return function()
        except Exception as e:
            if "ThrottlingException" in str(e):
                wait_time = (2 ** retries) + random.uniform(0, 1)
                print(f"Throttled. Waiting {wait_time:.2f} seconds before retrying...")
                time.sleep(wait_time)
                retries += 1
            else:
                raise e
    raise Exception("Max retries exceeded")

# Função que vai processar as mensagens do Telegram
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text
    
    # Verifica se a mensagem não está vazia
    if not user_message or user_message.strip() == "":
        await update.message.reply_text("Por favor, envie uma pergunta válida.")
        return
    
    try:
        #print(f"Mensagem recebida: {user_message}")
        logger.info(f"Mensagem recebida: {user_message}")

        # Adiciona a mensagem do usuário ao histórico
        chat_history.append(f"Usuário: {user_message}")

        # Limita o histórico a 10 mensagens
        context_messages = "\n".join(chat_history[-4:])# 4 mensagens no max

        # Imprime o contexto concatenado para verificação 
        print("\n\n")
        print("Contexto do chat:") 
        print(context_messages)
        print("\n\n\n")

        #Atribuindo as funções às variáveis
        persist_directory = os.path.join("vector_store", "chroma")
        bedrock_embeddings_from_docs = bedrock_embeddings()
        llm = bedrock_llm()
        prompt = prompt_template()
        vector_store = vectore_store_louder(persist_directory, bedrock_embeddings_from_docs)
                
        try:
            # carrega a resposta do chatbot
            # response = chatbot(vector_store,llm,prompt, f"Contexto do chat: {context_messages}\nPergunta: {user_message}")
            def get_chatbot_response():
                return chatbot(vector_store, llm, prompt, f'Contexto do chat: {context_messages}\nPergunta: {user_message}')
 
            # Chama a função com retry
            response = retry_with_backoff(get_chatbot_response)
            
             #print(response)
            logger.info(response)
 
            # Adiciona a resposta do bot ao histórico
            chat_history.append(f"Bot: {response}")
            await update.message.reply_text(response)
        except Exception as e:
            #print(f"Erro ao carregar resposta do chatbot: {e}")
            logger.error(f"Erro ao carregar resposta do chatbot: {e}")


    except Exception as e:
        await update.message.reply_text(f"Desculpe, ocorreu um erro: {e}")
        # print(f"Erro: {e}")
        logger.error(f"Erro: {e}")

# Função para iniciar o bot do Telegram
def main():
    token = env_func_telegram()

    try:
        # Configura o bot
        app = ApplicationBuilder().token(token).build()

    except Exception as e:
        print(f"Erro ao configurar o bot: {e} + {token}")
        logger.error(f"Erro ao configurar o bot: {e} + {token}")
    
    # Adiciona os handlers de comandos
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    logger.info("Bot está rodando...")
    app.run_polling()

if __name__ == "__main__":
    main()
