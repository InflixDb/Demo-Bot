from pyrogram import Client, filters
from pyrogram.types import Message
from config import Config
from database import add_filter, get_filter
import asyncio

app = Client("temp_filter_bot",
             api_id=Config.API_ID,
             api_hash=Config.API_HASH,
             bot_token=Config.BOT_TOKEN)

@app.on_message(filters.command("start"))
async def start(client, message):
    await message.reply_text("Send a keyword to get a temporary link.")

@app.on_message(filters.command("addfilter") & filters.user(Config.ADMINS))
async def add_filter_cmd(client, message):
    if len(message.command) < 3:
        return await message.reply("Usage: /addfilter <keyword> <message_id>")
    keyword = message.command[1]
    msg_id = int(message.command[2])
    add_filter(keyword, msg_id)
    await message.reply(f"Filter added for keyword: `{keyword}`")

@app.on_message(filters.text & ~filters.command(["start", "addfilter"]))
async def handle_keyword(client, message: Message):
    keyword = message.text.strip().lower()
    msg_id = get_filter(keyword)
    if not msg_id:
        return await message.reply("No result found.")

    # Copy the message to TEMP channel
    temp_msg = await client.copy_message(
        chat_id=Config.TEMP_CHANNEL_ID,
        from_chat_id=Config.FILE_CHANNEL_ID,
        message_id=msg_id
    )

    # Send link to user
    link = f"https://t.me/c/{str(Config.TEMP_CHANNEL_ID)[4:]}/{temp_msg.id}"
    await message.reply(f"Here is your temporary link (expires in 5 min):\n{link}")

    # Wait 5 minutes and delete the message
    await asyncio.sleep(300)
    try:
        await client.delete_messages(Config.TEMP_CHANNEL_ID, temp_msg.id)
    except:
        pass

app.run()
