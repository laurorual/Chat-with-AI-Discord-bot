import discord
from discord.ext import commands
import os
import logging # A nova biblioteca de logs
from dotenv import load_dotenv

# 🛠️ CONFIGURAÇÃO DO SISTEMA DE LOGS 🛠️
# Isso define o visual das mensagens no seu terminal do Tmux
logging.basicConfig(
    level=logging.INFO, # Mostra informações normais, avisos e erros
    format='\033[90m%(asctime)s\033[0m | \033[1m%(levelname)-8s\033[0m | \033[36m%(name)s\033[0m : %(message)s',
    datefmt='%d/%m/%Y %H:%M:%S'
)
# Cria o "registrador" principal do bot
logger = logging.getLogger('Dyza')

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

class BotDoMal(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix="!", intents=intents)

    async def setup_hook(self):
        await self.load_extension('cogs.chat')
        await self.load_extension('cogs.engajamento')
        await self.load_extension('cogs.status')
        # Trocamos o print() antigo pelo nosso novo logger
        logger.info("Todos os módulos (Cogs) foram carregados.")

    async def on_ready(self):
        logger.info(f'O mal chegou! Logado com sucesso como {self.user}')

bot = BotDoMal()
bot.run(TOKEN)