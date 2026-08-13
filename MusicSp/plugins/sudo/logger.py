from datetime import datetime

from pyrogram import filters
from pyrogram.enums import ParseMode
from pyrogram.types import ChatMemberUpdated

from MusicSp import app
from MusicSp.misc import SUDOERS
from MusicSp.utils.database import add_off, add_on
from MusicSp.utils.decorators.language import language

# ⚠️ Apna LOG group / channel ki ID yahan daalo (config.py se import bhi kar sakte ho)
LOG_GROUP_ID = -1001234567890  # <-- ISKO APNI LOG GROUP ID SE REPLACE KARO


@app.on_message(filters.command(["logger"]) & SUDOERS)
@language
async def logger(client, message, _):
    usage = _["log_1"]
    if len(message.command) != 2:
        return await message.reply_text(usage)
    state = message.text.split(None, 1)[1].strip().lower()
    if state == "enable":
        await add_on(2)
        await message.reply_text(_["log_2"])
    elif state == "disable":
        await add_off(2)
        await message.reply_text(_["log_3"])
    else:
        await message.reply_text(usage)


@app.on_message(filters.command(["cookies"]) & SUDOERS)
@language
async def cookies(client, message, _):
    await message.reply_document("cookies/logs.csv")
    await message.reply_text("Please check given file to cookies file choosing logs...")


# ----------------------------------------------------------------------
# Bot jab kisi group me add hota hai to logger group me info bhejo
# Ab quote (blockquote) style + spoiler (blur) formatting ke sath
# ----------------------------------------------------------------------
@app.on_chat_member_updated()
async def bot_added_to_group(client, chat_member_updated: ChatMemberUpdated):
    chat = chat_member_updated.chat
    new_member = chat_member_updated.new_chat_member
    old_member = chat_member_updated.old_chat_member
    added_by = chat_member_updated.from_user

    # Sirf tab trigger ho jab bot khud group me add/invite hua ho
    if not new_member or new_member.user.id != client.me.id:
        return

    # Agar bot pehle se member tha aur sirf status change hua (promote/demote) to skip
    if old_member and old_member.user.id == client.me.id:
        return

    try:
        try:
            invite_link = await client.export_chat_invite_link(chat.id)
        except Exception:
            invite_link = (
                f"https://t.me/{chat.username}" if chat.username else "Not available (private / no perm)"
            )

        adder_name = added_by.first_name if added_by else "Unknown"
        adder_username = f"@{added_by.username}" if added_by and added_by.username else "No username"
        adder_id = added_by.id if added_by else "Unknown"

        members_count = await client.get_chat_members_count(chat.id)

        text = (
            "<b>🆕 #NewGroup</b>\n\n"
            "<blockquote>"
            f"<b>Group Name:</b> {chat.title}\n"
            f"<b>Group ID:</b> <tg-spoiler><code>{chat.id}</code></tg-spoiler>\n"
            f"<b>Group Link:</b> <tg-spoiler>{invite_link}</tg-spoiler>\n"
            f"<b>Members Count:</b> {members_count}"
            "</blockquote>\n\n"
            "<blockquote>"
            f"<b>Added By:</b> {adder_name}\n"
            f"<b>Username:</b> {adder_username}\n"
            f"<b>User ID:</b> <tg-spoiler><code>{adder_id}</code></tg-spoiler>"
            "</blockquote>\n\n"
            f"<b>Time:</b> {datetime.now().strftime('%d-%m-%Y %H:%M:%S')}"
        )

        await client.send_message(LOG_GROUP_ID, text, parse_mode=ParseMode.HTML)

    except Exception as e:
        try:
            await client.send_message(LOG_GROUP_ID, f"⚠️ Error logging new group: {e}")
        except Exception:
            pass


# ----------------------------------------------------------------------
# Song play logger — quote (blockquote) + spoiler (blur) style
# Isko apne play.py / stream handler me call karna hai
# ----------------------------------------------------------------------
async def song_play_logger(client, chat, user, song_name: str, duration: str = None, source: str = "YouTube"):
    """
    client    -> pyrogram Client (app)
    chat      -> group chat object (message.chat)
    user      -> user object jisne gaana play kiya (message.from_user)
    song_name -> gaane ka naam / title
    duration  -> optional, gaane ki duration (string, jaise "3:45")
    source    -> optional, gaana kaha se aaya (YouTube / Spotify / File / etc.)
    """
    try:
        user_name = user.first_name if user else "Unknown"
        user_username = f"@{user.username}" if user and user.username else "No username"
        user_id = user.id if user else "Unknown"

        group_name = chat.title if chat else "Unknown Group"
        group_id = chat.id if chat else "Unknown"

        try:
            group_link = await client.export_chat_invite_link(chat.id)
        except Exception:
            group_link = f"https://t.me/{chat.username}" if chat.username else "Private Group"

        duration_line = f"\n<b>Duration:</b> {duration}" if duration else ""

        text = (
            "<b>🎵 #NewSongPlayed</b>\n\n"
            "<blockquote>"
            f"<b>Song Name:</b> {song_name}\n"
            f"<b>Source:</b> {source}"
            f"{duration_line}"
            "</blockquote>\n\n"
            "<blockquote>"
            f"<b>Group Name:</b> {group_name}\n"
            f"<b>Group ID:</b> <tg-spoiler><code>{group_id}</code></tg-spoiler>\n"
            f"<b>Group Link:</b> <tg-spoiler>{group_link}</tg-spoiler>"
            "</blockquote>\n\n"
            "<blockquote>"
            f"<b>Played By:</b> {user_name}\n"
            f"<b>Username:</b> {user_username}\n"
            f"<b>User ID:</b> <tg-spoiler><code>{user_id}</code></tg-spoiler>"
            "</blockquote>\n\n"
            f"<b>Time:</b> {datetime.now().strftime('%d-%m-%Y %H:%M:%S')}"
        )

        await client.send_message(LOG_GROUP_ID, text, parse_mode=ParseMode.HTML)

    except Exception as e:
        try:
            await client.send_message(LOG_GROUP_ID, f"⚠️ Error logging song play: {e}")
        except Exception:
            pass