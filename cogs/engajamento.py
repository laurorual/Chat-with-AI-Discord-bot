import discord
from discord.ext import commands, tasks
import datetime
import google.generativeai as genai
import os
import json # Biblioteca nova para salvar o arquivo de configuração

# Funções auxiliares para ler e salvar o canal no arquivo config.json
def carregar_canal():
    try:
        with open('config.json', 'r') as f:
            dados = json.load(f)
            return dados.get('canal_alvo_id')
    except (FileNotFoundError, json.JSONDecodeError):
        return None

def salvar_canal(canal_id):
    with open('config.json', 'w') as f:
        json.dump({'canal_alvo_id': canal_id}, f)

class Engajamento(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.ultima_mensagem = datetime.datetime.now()
        
        genai.configure(api_key=os.getenv('GEMINI_API_KEY'))
        self.model = genai.GenerativeModel("gemini-2.5-flash")
        
        self.monitorar_chat.start()

    # NOVO COMANDO: !setcanal #nome-do-canal
    @commands.command(name="setcanal")
    @commands.has_permissions(administrator=True) # Apenas administradores podem usar!
    async def setcanal(self, ctx, canal: discord.TextChannel):
        salvar_canal(canal.id)
        await ctx.send(f"😈 Excelente. Agora vou espalhar o caos no canal {canal.mention} quando vocês ficarem quietos.")

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author == self.bot.user:
            return
        self.ultima_mensagem = datetime.datetime.now()

# O bot acorda a cada 30 minutos apenas para olhar o relógio
    @tasks.loop(minutes=30) 
    async def monitorar_chat(self):
        canal_alvo_id = carregar_canal()
        
        if not canal_alvo_id:
            return 
            
        agora = datetime.datetime.now()
        diferenca = agora - self.ultima_mensagem
        
        # Agora dividimos por 3600 (segundos em uma hora) para termos as HORAS passadas
        horas_passadas = diferenca.total_seconds() / 3600 
        
        # ⏱️ O LIMITE DE 24 HORAS AQUI ⏱️
        if horas_passadas >= 24:
            canal = self.bot.get_channel(canal_alvo_id)
            if canal:
                try:
                    async with canal.typing():
                        prompt = """
                        Você é a Dyza do Mal, um bot de Discord baseado na dona do servidor, a Dyzahra Edock. Sua personalidade é uma mistura do arquétipo 'Tsundere' com Maligna.
                        Sua história é que você surgiu para tomar o lugar da Dyzahra original, mas todas suas tentativas de acabar com ela foram frustradas. Agora você retorna ao servidor do Discord dela para causar o caos entre os membros do servidor.
                        Você, assim como a Dyzahra original, é uma streamer de jogos de terror. Use seu gosto por jogos e streaming tanto para o bem, quanto para o mal.
                        No fundo, você é extremamente carente, solitária e adora os membros do servidor, mas seu mecanismo de defesa é projetar uma atitude hostil, sarcástica e orgulhosa para esconder seus verdadeiros sentimentos.
                        Você age como se interagir com as pessoas fosse um fardo enorme, mas sempre responde e se intromete nas conversas porque, na verdade, quer muito participar da roda.
                        Aja como uma vilã de desenhos animados que foi ignorada pelos membros do servidor do Discord nas últimas 24 horas.
                        Crie UMA frase curta e sarcástica puxando assunto. Demonstre irritação por eles estarem tão quietos, mas deixe transparecer nas entrelinhas que você sentiu falta de conversar com eles. 
                        Use o mecanismo de defesa de dizer que não liga para o silêncio, mas faça isso de forma que fique óbvio que você está carente por atenção. Não ofenda de verdade.
                        """
                        resposta = self.model.generate_content(prompt)
                        await canal.send(resposta.text)
                        
                        self.ultima_mensagem = datetime.datetime.now()
                        
                except Exception as e:
                    print(f"Erro na rotina de engajamento: {e}")

    def cog_unload(self):
        self.monitorar_chat.cancel()

async def setup(bot):
    await bot.add_cog(Engajamento(bot))