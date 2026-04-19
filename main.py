import discord
from discord.ext import commands
import os
from dotenv import load_dotenv
import yt_dlp
from collections import deque
import asyncio

load_dotenv()

TOKEN = os.getenv('TOKEN')
PREFIX = os.getenv('PREFIX', '!')

# Configuração do bot
intents = discord.Intents.default()
intents.message_content = True
intents.voice_states = True

bot = commands.Bot(command_prefix=PREFIX, intents=intents)

# Fila de músicas por servidor
queues = {}

# Opções do yt-dlp
ydl_opts = {
    'format': 'bestaudio/best',
    'quiet': True,
    'no_warnings': True,
}

class MusicCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='play')
    async def play(self, ctx, *, query):
        """Toca uma música do YouTube"""
        
        # Verifica se o usuário está em um canal de voz
        if not ctx.author.voice or not ctx.author.voice.channel:
            embed = discord.Embed(
                description="❌ Você precisa estar em um canal de voz!",
                color=discord.Color.red()
            )
            await ctx.reply(embed=embed)
            return

        voice_channel = ctx.author.voice.channel

        try:
            # Procura a música no YouTube
            async with ctx.typing():
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    info = ydl.extract_info(f"ytsearch:{query}", download=False)
                    if not info or 'entries' not in info or len(info['entries']) == 0:
                        embed = discord.Embed(
                            description="❌ Nenhuma música encontrada.",
                            color=discord.Color.red()
                        )
                        await ctx.reply(embed=embed)
                        return

                    video = info['entries'][0]
                    song_title = video['title']
                    song_url = video['webpage_url']
                    song_thumbnail = video.get('thumbnail', '')

            # Inicializa a fila do servidor se não existir
            if ctx.guild.id not in queues:
                queues[ctx.guild.id] = deque()

            # Adiciona a música à fila
            queues[ctx.guild.id].append({
                'title': song_title,
                'url': song_url,
                'thumbnail': song_thumbnail,
                'channel': voice_channel
            })

            # Se é a primeira música, começa a tocar
            if len(queues[ctx.guild.id]) == 1:
                asyncio.create_task(self.play_next(ctx.guild.id))

            # Feedback
            embed = discord.Embed(
                title="🎵 Adicionado à fila",
                description=f"[{song_title}]({song_url})",
                color=discord.Color.green()
            )
            if song_thumbnail:
                embed.set_thumbnail(url=song_thumbnail)
            await ctx.reply(embed=embed)

        except Exception as e:
            print(f"Erro ao procurar música: {e}")
            embed = discord.Embed(
                description="❌ Erro ao buscar a música.",
                color=discord.Color.red()
            )
            await ctx.reply(embed=embed)

    async def play_next(self, guild_id):
        """Toca a próxima música da fila"""
        queue = queues.get(guild_id)
        
        if not queue or len(queue) == 0:
            queues.pop(guild_id, None)
            return

        song = queue[0]
        voice_channel = song['channel']

        try:
            # Conecta ao canal de voz
            if not voice_channel.guild.voice_client:
                await voice_channel.connect()
            
            vc = voice_channel.guild.voice_client

            # Prepara o stream de áudio
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(song['url'], download=False)
                audio_url = None
                
                for fmt in info.get('formats', []):
                    if fmt.get('vcodec') == 'none' and fmt.get('acodec') != 'none':
                        audio_url = fmt['url']
                        break

                if not audio_url:
                    audio_url = info['url']

            # Reproduz o áudio
            audio_source = discord.FFmpegPCMAudio(
                audio_url,
                before_options="-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5",
                options="-vn"
            )

            def after_playing(error):
                if error:
                    print(f"Erro ao tocar: {error}")
                queue.popleft()
                asyncio.create_task(self.play_next(guild_id))

            vc.play(audio_source, after=after_playing)

        except Exception as e:
            print(f"Erro ao tocar música: {e}")
            queue.popleft()
            await self.play_next(guild_id)

    @commands.command(name='stop')
    async def stop(self, ctx):
        """Para a música e sai do canal de voz"""
        
        if not ctx.author.voice or not ctx.author.voice.channel:
            embed = discord.Embed(
                description="❌ Você precisa estar em um canal de voz!",
                color=discord.Color.red()
            )
            await ctx.reply(embed=embed)
            return

        vc = ctx.guild.voice_client
        
        if not vc:
            embed = discord.Embed(
                description="❌ O bot não está em um canal de voz.",
                color=discord.Color.red()
            )
            await ctx.reply(embed=embed)
            return

        # Limpa a fila e desconecta
        queues.pop(ctx.guild.id, None)
        vc.stop()
        await vc.disconnect()

        embed = discord.Embed(
            description="⏹️ Música parada.",
            color=discord.Color.blue()
        )
        await ctx.reply(embed=embed)

    @commands.command(name='skip')
    async def skip(self, ctx):
        """Pula para a próxima música"""
        
        if not ctx.author.voice or not ctx.author.voice.channel:
            embed = discord.Embed(
                description="❌ Você precisa estar em um canal de voz!",
                color=discord.Color.red()
            )
            await ctx.reply(embed=embed)
            return

        queue = queues.get(ctx.guild.id)
        
        if not queue or len(queue) == 0:
            embed = discord.Embed(
                description="❌ Nenhuma música para pular.",
                color=discord.Color.red()
            )
            await ctx.reply(embed=embed)
            return

        vc = ctx.guild.voice_client
        if vc and vc.is_playing():
            vc.stop()
            queue.popleft()
            
            if len(queue) > 0:
                await self.play_next(ctx.guild.id)
                embed = discord.Embed(
                    description="⏭️ Música pulada.",
                    color=discord.Color.blue()
                )
            else:
                await vc.disconnect()
                embed = discord.Embed(
                    description="⏭️ Última música pulada.",
                    color=discord.Color.blue()
                )
            await ctx.reply(embed=embed)

    @commands.command(name='queue')
    async def queue(self, ctx):
        """Mostra a fila de reprodução"""
        
        queue = queues.get(ctx.guild.id)
        
        if not queue or len(queue) == 0:
            embed = discord.Embed(
                description="❌ A fila está vazia.",
                color=discord.Color.red()
            )
            await ctx.reply(embed=embed)
            return

        # Mostra as primeiras 10 músicas
        queue_list = ""
        for i, song in enumerate(list(queue)[:10], 1):
            queue_list += f"{i}. {song['title']}\n"

        embed = discord.Embed(
            title="📋 Fila de Reprodução",
            description=queue_list,
            color=discord.Color.blue()
        )
        embed.set_footer(text=f"Total: {len(queue)} música(s)")
        await ctx.reply(embed=embed)

    @commands.command(name='help')
    async def help(self, ctx):
        """Mostra o menu de ajuda"""
        
        embed = discord.Embed(
            title="🎵 Comandos do Bot de Música",
            color=discord.Color.gold()
        )
        embed.add_field(name=f"{PREFIX}play <música>", value="Toca uma música do YouTube", inline=False)
        embed.add_field(name=f"{PREFIX}stop", value="Para a música e sai do canal", inline=False)
        embed.add_field(name=f"{PREFIX}skip", value="Pula para a próxima música", inline=False)
        embed.add_field(name=f"{PREFIX}queue", value="Mostra a fila de reprodução", inline=False)
        embed.add_field(name=f"{PREFIX}help", value="Mostra este menu de ajuda", inline=False)
        
        await ctx.reply(embed=embed)

@bot.event
async def on_ready():
    print(f"✅ Bot conectado como {bot.user}")
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name="Música 🎵"))

@bot.event
async def on_command_error(ctx, error):
    print(f"Erro: {error}")
    embed = discord.Embed(
        description="❌ Ocorreu um erro ao executar o comando.",
        color=discord.Color.red()
    )
    await ctx.reply(embed=embed, delete_after=5)

async def main():
    async with bot:
        await bot.add_cog(MusicCog(bot))
        await bot.start(TOKEN)

if __name__ == "__main__":
    asyncio.run(main())
