from pyrogram.enums import ParseMode
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from MusicSp import app
from MusicSp.utils.database import is_on_off
from config import LOG_GROUP_ID


def _chat_username_line(chat) -> str:
    return f"@{chat.username}" if getattr(chat, "username", None) else "ᴘʀɪᴠᴀᴛᴇ"


def _user_username_line(user) -> str:
    return f"@{user.username}" if user and getattr(user, "username", None) else "ɴᴏɴᴇ"


def _user_url(user):
    if not user:
        return None
    if getattr(user, "username", None):
        return f"https://t.me/{user.username}"
    return f"tg://user?id={user.id}"


async def _group_url(chat):
    if getattr(chat, "username", None):
        return f"https://t.me/{chat.username}"
    invite_link = getattr(chat, "invite_link", None)
    if invite_link:
        return invite_link
    try:
        return await app.export_chat_invite_link(chat.id)
    except Exception:
        return None


def _message_link(message):
    try:
        link = message.link
        if link:
            return link
    except Exception:
        pass
    return "-"


async def _log_buttons(chat, user):
    user_url = _user_url(user)
    group_url = await _group_url(chat)
    bot_url = f"https://t.me/{app.username}?start=start" if getattr(app, "username", None) else None

    row = []
    if user_url:
        row.append(InlineKeyboardButton("Uꜱᴇʀ", url=user_url))
    if group_url:
        row.append(InlineKeyboardButton("Gʀᴏᴜᴘ", url=group_url))
    if bot_url:
        row.append(InlineKeyboardButton("Bᴏᴛ", url=bot_url))

    return InlineKeyboardMarkup([row]) if row else None


async def _send_log(text, chat, user):
    if chat and LOG_GROUP_ID and chat.id == LOG_GROUP_ID:
        return
    if not LOG_GROUP_ID:
        return
    try:
        markup = await _log_buttons(chat, user)
        await app.send_message(
            chat_id=LOG_GROUP_ID,
            text=text,
            parse_mode=ParseMode.HTML,
            disable_web_page_preview=True,
            reply_markup=markup,
        )
    except Exception:
        pass


async def play_logs(message, streamtype):
    """Logs a play/vplay command to LOG_GROUP_ID with User/Group/Bot buttons."""
    if not await is_on_off(2):
        return

    chat = message.chat
    user = message.from_user

    try:
        query = message.text.split(None, 1)[1]
    except IndexError:
        query = "-"

    text = (
        f"<b>{app.mention} ᴘʟᴀʏ ʟᴏɢ</b>\n\n"
        f"<b>ᴄʜᴀᴛ ɪᴅ :</b> <code>{chat.id}</code>\n"
        f"<b>ᴄʜᴀᴛ ɴᴀᴍᴇ :</b> {chat.title}\n"
        f"<b>ᴄʜᴀᴛ ᴜsᴇʀɴᴀᴍᴇ :</b> {_chat_username_line(chat)}\n\n"
        f"<b>ᴜsᴇʀ ɪᴅ :</b> <code>{user.id}</code>\n"
        f"<b>ɴᴀᴍᴇ :</b> {user.mention}\n"
        f"<b>ᴜsᴇʀɴᴀᴍᴇ :</b> {_user_username_line(user)}\n\n"
        f"<b>sᴛʀᴇᴀᴍᴛʏᴘᴇ :</b> {streamtype}\n"
        f"<b>ǫᴜᴇʀʏ :</b> {query}\n"
        f"<b>ᴍᴇssᴀɢᴇ ʟɪɴᴋ :</b> {_message_link(message)}"
    )
    await _send_log(text, chat, user)


async def activity_logs(message, activity: str):
    """Logs admin activities (skip/stop/pause/resume/seek/speed/shuffle/loop) to LOG_GROUP_ID."""
    if not await is_on_off(2):
        return

    chat = message.chat
    user = message.from_user
    if not user:
        return

    text = (
        f"<b>{app.mention} ᴀᴄᴛɪᴠɪᴛʏ ʟᴏɢ</b>\n\n"
        f"<b>ᴄʜᴀᴛ ɪᴅ :</b> <code>{chat.id}</code>\n"
        f"<b>ᴄʜᴀᴛ ɴᴀᴍᴇ :</b> {chat.title}\n"
        f"<b>ᴄʜᴀᴛ ᴜsᴇʀɴᴀᴍᴇ :</b> {_chat_username_line(chat)}\n\n"
        f"<b>ᴜsᴇʀ ɪᴅ :</b> <code>{user.id}</code>\n"
        f"<b>ɴᴀᴍᴇ :</b> {user.mention}\n"
        f"<b>ᴜsᴇʀɴᴀᴍᴇ :</b> {_user_username_line(user)}\n\n"
        f"<b>ᴀᴄᴛɪᴠɪᴛʏ :</b> {activity}"
    )
    await _send_log(text, chat, user)
