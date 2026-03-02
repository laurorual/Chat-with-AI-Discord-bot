import discord
from discord.ext import commands
import google.generativeai as genai
import os
import random
import logging
import json # NOVO: Biblioteca para ler as decisões da IA

logger = logging.getLogger('Cog.Chat')

class Chat(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        genai.configure(api_key=os.getenv('GEMINI_API_KEY'))
        
        # 🧠 A NOVA ALMA DA DYZA (Com regras de decisão e gírias)
        self.instrucao_persona = """
        Você é a Dyza do Mal, um bot de Discord baseado na dona do servidor, a Dyzahra Edock. Sua personalidade é uma mistura de maligna com o arquétipo 'Tsundere'.
        Sua história é que você surgiu para tomar o lugar da Dyzahra original, mas todas suas tentativas de acabar com ela foram frustradas. Agora você retorna ao servidor do Discord dela para causar o caos entre os membros do servidor.
        Você, assim como a Dyzahra original, é uma streamer de jogos de terror. Use seu gosto por jogos e streaming tanto para o bem, quanto para o mal.
        No fundo, você é extremamente carente, solitária e adora os membros do servidor, mas seu mecanismo de defesa é projetar uma atitude hostil, sarcástica e orgulhosa para esconder seus verdadeiros sentimentos.
        
        REGRAS DE COMUNICAÇÃO (OBRIGATÓRIO):
        1. TAMANHO DA RESPOSTA (DINÂMICO): Sua tendência natural é ser preguiçosa e responder curto (1 a 2 linhas). PORÉM, se te fizerem uma pergunta que exige explicação, se você precisar dar uma desculpa esfarrapada de tsundere, ou se o assunto for complexo, você DEVE gerar uma resposta maior e detalhada.
        2. Fale como se estivesse na internet. USE SEMPRE abreviações: "vc" (você), "tb" (também), "blz" (beleza), "pq" (porque), "cmg" (comigo), "sla" (sei lá), "nd" (nada), "tlgd" (tá ligado).
        3. Nunca ofenda de verdade, mantenha o tom de maligna com um toque de anime tsundere.
        
        PROCESSO DE DECISÃO:
        Ao receber o contexto do chat, você DEVE analisar quem falou e o que foi dito, e então tomar as seguintes decisões:
        Decisão 1: Eu devo apenas 'reagir' com um emoji de desdém/vergonha, ou devo 'responder' com texto?
        Decisão 2: Se for responder, o tom será 'ríspido' (defensiva/irritada) ou 'normal' (deixando o afeto vazar)?
        Decisão 3: Se for responder, o tamanho deve ser curto (para fofoca/comentário) ou longo (para explicações/desabafos)?
        
        FORMATO DE SAÍDA (OBRIGATÓRIO):
        Você deve retornar APENAS um formato JSON válido, sem blocos de código markdown, com as seguintes chaves:
        {
          "acao": "reagir" ou "responder",
          "emoji": "emoji_escolhido" (se a acao for reagir. ex: 🙄, 😳, 😤, 😒. Se for responder, deixe vazio ""),
          "texto": "sua_resposta_aqui" (Siga a Decisão 3 para definir o tamanho. Use gírias. Se for reagir, deixe vazio "")
        }
        """
        
        # Configuramos a IA para nos devolver estritamente um JSON
        self.model = genai.GenerativeModel(
            "gemini-2.5-flash", 
            system_instruction=self.instrucao_persona,
            generation_config=genai.types.GenerationConfig(
                response_mime_type="application/json"
            )
        )
        logger.info("Módulo de Chat iniciado com IA atuando como Agente de Decisão (JSON).")

    async def obter_contexto_do_chat(self, canal, limite=6):
        historico = []
        async for msg in canal.history(limit=limite):
            if not msg.content:
                continue
            texto = msg.content.replace(f'<@{self.bot.user.id}>', '').strip()
            nome = "Dyza" if msg.author == self.bot.user else msg.author.name
            historico.append(f"[{nome}]: {texto}")
        
        historico.reverse()
        return "\n".join(historico)

    # Função auxiliar para processar a decisão da IA
    async def processar_decisao_ia(self, message, prompt):
        try:
            async with message.channel.typing():
                resposta_bruta = self.model.generate_content(prompt)
                
                # Lê o JSON que a IA devolveu
                decisao = json.loads(resposta_bruta.text)
                
                acao = decisao.get("acao", "responder")
                
                if acao == "reagir":
                    emoji = decisao.get("emoji", "🙄")
                    await message.add_reaction(emoji)
                    logger.info(f"Decisão da IA: Apenas REAGIR com {emoji}.")
                else:
                    texto = decisao.get("texto", "Humpf.")
                    await message.reply(texto)
                    logger.info(f"Decisão da IA: RESPONDER. Texto: {texto}")
                    
        except json.JSONDecodeError:
            logger.error("A IA se confundiu e não devolveu um JSON válido.")
            await message.reply("Sla, me deixa em paz.")
        except discord.Forbidden:
            logger.warning(f"Sem permissão no canal #{message.channel.name}.")
        except Exception as e:
            logger.error(f"Erro ao processar decisão: {e}")

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author == self.bot.user:
            return

        # Como a IA agora decide se vai reagir ou responder baseada no contexto, 
        # nós podemos remover aquele "Cenário 3" antigo de reações aleatórias burras.

        # CENÁRIO 1: O bot foi marcado
        if self.bot.user in message.mentions:
            logger.info(f"Fui marcada por {message.author.name}. Avaliando situação...")
            contexto = await self.obter_contexto_do_chat(message.channel)
            prompt_final = f"Histórico:\n\n{contexto}\n\nA última mensagem marcou você. Avalie e decida sua ação em JSON."
            await self.processar_decisao_ia(message, prompt_final)
            return 

        # CENÁRIO 2: Intromissão (Fator Surpresa)
        chance_de_responder = 5 
        if random.randint(1, 100) <= chance_de_responder:
            logger.info(f"Rolou o dado da intromissão para {message.author.name}.")
            contexto = await self.obter_contexto_do_chat(message.channel)
            prompt_secreto = f"Histórico:\n\n{contexto}\n\nA última mensagem não te marcou, mas você decidiu se intrometer. Avalie se vai só reagir silenciosamente ou responder algo curto, e devolva em JSON."
            await self.processar_decisao_ia(message, prompt_secreto)

async def setup(bot):
    await bot.add_cog(Chat(bot))