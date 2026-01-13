from config import api_id, api_hash
import asyncio
import os

from telethon import TelegramClient
from telethon.tl.functions.channels import CreateChannelRequest, EditPhotoRequest
from telethon.tl.functions.channels import TogglePreHistoryHiddenRequest
from telethon.tl.functions.messages import ExportChatInviteRequest
from telethon.tl.types import InputChatUploadedPhoto
from telethon.errors import ChatNotModifiedError

from webinar import WEBINARS

# ================= CONFIG =================

api_id = api_id
api_hash = api_hash
SESSION_NAME = "antonio"

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
LOG_FILE = "log.txt"

# ================= LOG =================

def save_log(webinar, invite_link):
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write("=" * 40 + "\n")
        f.write(f"Webinar: {webinar.topic}\n")
        f.write(f"Data: {webinar.date}\n")
        f.write(f"Hora: {webinar.time}\n")
        f.write(f"Link: {invite_link}\n")
        f.write("=" * 40 + "\n\n")

# ================= MENSAGENS =================

def build_messages(webinar):
    return [
        (
            "1.jpg",
            f"""
👋 Olá, candidatos a tutores!

Bem-vindos ao Pré-Teste da Kodland!
Sou Antonio Carlos, seu treinador e avaliador nessa etapa. 🚀

{webinar.datetime_text}
📍 Via Zoom

Vou apresentar todos os detalhes do Pré-Teste.

⚠️ Se não puder assistir ao vivo, a gravação será enviada.
Mas assistir é obrigatório para seguir no processo.
❓ Dúvidas só serão respondidas durante ou após o Webinar.
"""
        ),
        (
            "2.jpg",
            """
📱 Telegram:
Se ainda não tem um nome de usuário (@exemplo), crie agora.
Vamos usar somente o Telegram a partir de agora.

📋 Formulário de Dados:
https://forms.gle/maxcs8SqWbUU3Hq56

"Apellido" = sobrenome.

🔗 Instale o Zoom:
https://zoom.us/pt/download
"""
        ),
        (
            "3.jpg",
            """
🎓 Minicurso de Preparação:
https://learn.kodland.org/my-courses/1659/at-class

Credenciais:
dtutor2129 / tCGP6C7lsC
"""
        ),
        (
            "4.jpg",
            """
🔑 Acesso às Plataformas:

Tutor:
https://backoffice.kodland.org
👤 btutor17352 | 🔒 yLrF4DDfon

Aluno:
https://learn.kodland.org/
👤 bcandidate | 🔒 s3ctgTenz6

💡 Use abas anônimas para evitar erro de login.

📦 Após o Webinar, enviarei materiais por mensagem direta.
"""
        ),
    ]

# ================= CORE =================

async def create_group(client, webinar):
    print(f"📦 Criando grupo: {webinar.title}")

    result = await client(
        CreateChannelRequest(
            title=webinar.title,
            about="Grupo oficial do Webinar Kodland",
            megagroup=True,
        )
    )

    group = result.chats[0]
    entity = await client.get_entity(group)

    await asyncio.sleep(2)

    # Histórico visível
    try:
        await client(
            TogglePreHistoryHiddenRequest(
                channel=entity,
                enabled=False,
            )
        )
    except ChatNotModifiedError:
        pass

    # Capa do grupo
    group_image = os.path.join(BASE_DIR, "group.jpg")
    await client(
        EditPhotoRequest(
            channel=entity,
            photo=InputChatUploadedPhoto(
                await client.upload_file(group_image)
            ),
        )
    )

    await asyncio.sleep(1)

    # Mensagens
    for img, text in build_messages(webinar):
        path = os.path.join(BASE_DIR, img)
        await client.send_file(entity, path, caption=text)
        await asyncio.sleep(1)

    # Link de convite
    invite = await client(
        ExportChatInviteRequest(
            peer=entity,
            legacy_revoke_permanent=False,
        )
    )

    save_log(webinar, invite.link)

    print("✅ Grupo criado")
    print(f"🔗 {invite.link}\n")

# ================= RUN =================

async def main():
    async with TelegramClient(SESSION_NAME, api_id, api_hash) as client:
        for webinar in WEBINARS:
            await create_group(client, webinar)
            await asyncio.sleep(10)  # pausa segura

asyncio.run(main())
