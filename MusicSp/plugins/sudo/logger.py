from datetime import datetime

from pyrogram import filters
from pyrogram.types import ChatMemberUpdated

from MusicSp import app
from MusicSp.misc import SUDOERS
from MusicSp.utils.database import add_off, add_on
from MusicSp.utils.decorators.language import language

# ⚠️ Apna LOG group / channel ki ID yahan daalo (config.py se import bhi kar sakte ho)
LOG_GROUP_ID = -1003716296507  # <-- ISKO APNI LOG GROUP ID SE REPLACE KARO


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
# NEW: Bot jab kisi group me add hota hai to logger group me info bhejo
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
        # Group ka invite link nikaalne ki koshish (agar bot ke paas permission hai)
        try:
            invite_link = await client.export_chat_invite_link(chat.id)
        except Exception:
            invite_link = chat.username and f"https://t.me/{chat.username}" or "Link not available (private group / no permission)"

        adder_name = added_by.first_name if added_by else "Unknown"
        adder_username = f"@{added_by.username}" if added_by and added_by.username else "No username"
        adder_id = added_by.id if added_by else "Unknown"

        members_count = await client.get_chat_members_count(chat.id)

        text = (
            "**#NewGroup**\n\n"
            f"**Group Name:** {chat.title}\n"
            f"**Group ID:** `{chat.id}`\n"
            f"**Group Link:** {invite_link}\n"
            f"**Members Count:** {members_count}\n\n"
            f"**Added By:** {adder_name}\n"
            f"**Username:** {adder_username}\n"
            f"**User ID:** `{adder_id}`\n\n"
            f"**Time:** {datetime.now().strftime('%d-%m-%Y %H:%M:%S')}"
        )

        await client.send_message(LOG_GROUP_ID, text)

    except Exception as e:
        try:
            await client.send_message(LOG_GROUP_ID, f"⚠️ Error logging new group: {e}")
        except Exception:
            pass
