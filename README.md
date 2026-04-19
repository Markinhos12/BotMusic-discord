# 🎵 Discord Music Bot (Python)

Um bot de música para Discord escrito em Python que toca músicas do YouTube usando discord.py e yt-dlp.

## 📋 Pré-requisitos

- Python 3.8+
- pip (gerenciador de pacotes Python)
- FFmpeg instalado
- Uma conta Discord
- Um servidor Discord (ou crie um)

## 🚀 Instalação

### 1. Clone ou baixe o repositório
```bash
git clone https://github.com/SEU_USUARIO/discord-music-bot-python.git
cd discord-music-bot-python
```

### 2. Crie um ambiente virtual
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Instale as dependências
```bash
pip install -r requirements.txt
```

### 4. Instale o FFmpeg

**Windows:**
- Baixe em [ffmpeg.org](https://ffmpeg.org/download.html)
- Ou use chocolatey: `choco install ffmpeg`
- Ou use winget: `winget install ffmpeg`

**macOS:**
```bash
brew install ffmpeg
```

**Linux (Ubuntu/Debian):**
```bash
sudo apt-get install ffmpeg
```

### 5. Configure o token do bot

#### Passo 5.1: Crie um bot no Discord Developer Portal
1. Acesse [Discord Developer Portal](https://discord.com/developers/applications)
2. Clique em "New Application"
3. Dê um nome ao seu bot
4. Vá até a aba "Bot" e clique em "Add Bot"
5. Copie o token clicando em "Copy"

#### Passo 5.2: Defina as permissões
1. Vá até "OAuth2" > "URL Generator"
2. Selecione os escopos: `bot`
3. Selecione as permissões:
   - `Send Messages`
   - `Read Message History`
   - `Connect` (para canais de voz)
   - `Speak` (para canais de voz)
4. Copie a URL gerada e abra em seu navegador para adicionar o bot ao servidor

#### Passo 5.3: Configure as variáveis de ambiente
1. Renomeie `.env.example` para `.env`
2. Cole seu token do bot:
```env
TOKEN=seu_token_do_bot_aqui
PREFIX=!
```

### 6. Execute o bot
```bash
python main.py
```

## 📝 Comandos

| Comando | Descrição | Exemplo |
|---------|-----------|---------|
| `!play <música>` | Toca uma música do YouTube | `!play despacito` |
| `!stop` | Para a música e sai do canal | `!stop` |
| `!skip` | Pula para a próxima música | `!skip` |
| `!queue` | Mostra a fila de reprodução | `!queue` |
| `!help` | Mostra o menu de ajuda | `!help` |

## 💡 Como usar

1. Entre em um canal de voz do Discord
2. No chat, digite: `!play [nome da música]`
3. O bot vai procurar no YouTube e começar a tocar
4. Use `!skip` para pular, `!stop` para parar

## 📂 Estrutura do Projeto

```
discord-music-bot-python/
├── main.py             # Arquivo principal do bot
├── requirements.txt    # Dependências do projeto
├── .env.example        # Exemplo de variáveis de ambiente
├── .gitignore          # Arquivos ignorados pelo git
└── README.md          # Este arquivo
```

## 🛠️ Desenvolvimento

Para modificar ou estender o bot:

1. O bot está estruturado em um `Cog` chamado `MusicCog`
2. Todos os comandos estão nessa classe
3. As filas de músicas são armazenadas em um dicionário `queues`

### Adicionando um novo comando

```python
@commands.command(name='seu_comando')
async def seu_comando(self, ctx):
    """Descrição do comando"""
    await ctx.reply("Resposta aqui")
```

## ⚠️ Limitações

- Funciona apenas com YouTube (por enquanto)
- O bot suporta apenas um servidor por instância
- Pause/Resume podem ser adicionados no futuro
- Requer FFmpeg instalado no sistema

## 🐛 Problemas comuns

### "Bot não aparece online"
- Verifique se o token está correto no arquivo `.env`
- Certifique-se de que o bot foi adicionado ao servidor

### "Bot não toca música"
- Instale o FFmpeg (verificar com `ffmpeg -version`)
- Verifique se o bot tem permissão de conectar ao canal de voz
- Certifique-se de que está digitando o comando correto: `!play [música]`

### "ModuleNotFoundError: No module named..."
- Certifique-se de que o ambiente virtual está ativado
- Rode `pip install -r requirements.txt` novamente

### "Erro de token inválido"
- Verifique se copie o token correto do Developer Portal
- Não compartilhe seu token com ninguém!

## 📦 Dependências

- **discord.py**: Biblioteca para interagir com a API do Discord
- **yt-dlp**: Biblioteca para buscar e fazer download de vídeos do YouTube
- **python-dotenv**: Para carregar variáveis de ambiente

## 📄 Licença

Este projeto está sob a licença MIT.

## 👤 Autor

Criado por [Seu Nome]

## 🤝 Contribuições

Contribuições são bem-vindas! Sinta-se à vontade para abrir issues ou pull requests.

---

**Aproveite a música! 🎶**
