import discord
from discord.ext import commands, tasks
import random

class Status(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
        # A lista de frases que ela vai ficar alternando
        self.frases_status = [
            "Bolando um plano maligno...",
            "Streamando Resident Evil",
            "Jogando com a sua paciência",
            "Assistindo o caos se instaurar",
            "Planejando a dominação do servidor",
            "Ignorando vocês propositalmente",
            "Hackeando a dona original (mentira... ou não)"
        ]
        
        # Dá o play na rotina de mudar o status
        self.mudar_status.start()

    # ⏱️ Configurado para rodar a cada 8 HORAS
    @tasks.loop(hours=8)
    async def mudar_status(self):
        # Essa linha é uma segurança: faz a rotina esperar o bot conectar no Discord 
        # antes de tentar mudar o status pela primeira vez ao ligar.
        await self.bot.wait_until_ready()
        
        # Sorteia uma frase da lista
        frase_escolhida = random.choice(self.frases_status)
        
        # Cria a atividade (Aparecerá como "Jogando...")
        atividade = discord.Game(name=frase_escolhida)
        
        # Também poderíamos usar: 
        # discord.Activity(type=discord.ActivityType.watching, name="o caos") -> "Assistindo o caos"
        # discord.Activity(type=discord.ActivityType.listening, name="seus choros") -> "Ouvindo seus choros"
        
        # Aplica o status no bot
        await self.bot.change_presence(status=discord.Status.online, activity=atividade)

    def cog_unload(self):
        self.mudar_status.cancel()

async def setup(bot):
    await bot.add_cog(Status(bot))