# Pipo bot V1.02
# Importação de bibliotecas	
import discord
import google.generativeai as genai
from discord.ext import commands
import os
from dotenv import load_dotenv
import asyncio
import gifs
import random

def run_bot():
    load_dotenv()
    # Carregando chaves das APIs
    DISCORD_TOKEN = os.getenv('discord_token')
    GEMINI_API_KEY = os.getenv('gemini_api_key')

    # Inicializando o bot
    intents = discord.Intents.default()
    intents.messages = True
    bot = discord.Client(intents=intents)
    # Carregando configurações do Gemini
    genai.configure(api_key=GEMINI_API_KEY)

    # Configurando a geração de texto...
    generation_config = {
        'candidate_count' : 1, # quantidade de respostas candidatas a serem geradas
        'temperature' : 0.7, # quão criativa a IA será
        'max_output_tokens' : 150, # tamanho máximo (ou quase) da resposta em tokens
    }

    model = genai.GenerativeModel(model_name='gemini-1.0-pro', generation_config=generation_config)
    
    personalidade = {
    'role': 'model', 
    'parts': [
        {'text': "Você é Pipo, um bot amigável que gosta de usar emojis e fala com entusiasmo. Responda de forma alegre, mas natural, sem se auto-descrever de forma literal."}
    ]}
    chat = model.start_chat(history=[personalidade]) # iniciando o chat com a personalidade definida

    mensagens_respondidas = set() # conjunto de mensagens já respondidas

    async def historico_canal(canal, limite = 5):
        lista_mensagens = []
        async for mensagem in canal.history(limit=limite):
            if mensagem.author != bot.user: # ignorando mensagens do bot
                lista_mensagens.append(mensagem)
        lista_mensagens.reverse() # reorganizando a lista para que a ordem seja a mesma que a das mensagens
        return lista_mensagens
    
    def gera_resposta(mensagem):
        resposta = chat.send_message(mensagem) # Inclui a personalidade em todas as mensagens
        return resposta.text # retorna a resposta da IA
    
    stop_words = set(["a", "e", "o", "de", "do", "da", "que", "com", "em", "um", "uma", "para", "nos", "na"])
    def extrai_palavra_chave(resposta): # extrai a palavra-chave de uma resposta da IA
        palavras = resposta.split() # separa as palavras da resposta
        palavras_chave  = list()
        for palavra in palavras:
            if palavra.isalpha() and len(palavra) > 2 and palavra.lower() not in stop_words: # filtrando palavras
                palavras_chave.append(palavra)
        return random.choice(palavras_chave) if palavras_chave else None # retorna uma palavra-chave aleatória ou None
    
    async def gif_contexto(channel, resposta):
        if random.random() < 0.4: # 40% de chance de enviar um gif
            palavras_chave = extrai_palavra_chave(resposta) # extraindo a palavra-chave da resposta
            if palavras_chave:
                gif_url = gifs.obtem_gif(palavras_chave)
                if gif_url:
                    await channel.send(gif_url) # enviando o gif
    @bot.event
    async def on_ready():
        print(f'{bot.user} está online!')
    
    @bot.event
    async def on_message(message):
        await asyncio.sleep(1) 
        if message.author.bot: # ignorando a concorrência >:(
            return
        historico = await historico_canal(message.channel, limite= 5) # pegando as últimas 5 mensagens do canal
        for mensagem in historico:
            if mensagem.id not in mensagens_respondidas: # se a mensagem ainda não foi respondida...
                if mensagem.mentions and bot.user in mensagem.mentions: # se o bot foi mencionado...
                    async with message.channel.typing(): # efeitinho de digitação
                        conteudo_mensagem = mensagem.content
                        conteudo_mensagem = conteudo_mensagem.replace(f'<@{bot.user.id}>',
                                                                       '').strip() # removendo a menção ao bot
                        if conteudo_mensagem: # enviando apenas mensagens com conteúdo
                            resposta = gera_resposta(conteudo_mensagem) # gerando a resposta pelo modelo
                            await message.reply(resposta) # respondendo a mensagem
                            mensagens_respondidas.add(mensagem.id) # adicionando a mensagem ao conjunto de mensagens respondidas
                            await gif_contexto(message.channel, resposta)
    # Rodando o bot
    bot.run(DISCORD_TOKEN)


    """
    Reimplementar o sistema de comandos
    Reações
    """ 