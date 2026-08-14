import math
import random
from pyrogram.enums import ButtonStyle
from pyrogram.types import InlineKeyboardButton

from MusicSp.utils.formatters import time_to_seconds

_STYLES = [ButtonStyle.PRIMARY, ButtonStyle.SUCCESS, ButtonStyle.DANGER]


def _rand_style():
    return random.choice(_STYLES)


def autoplay_menu_markup(_, chat_id, current: bool):
    on_text = "✅ On" if current else "On"
    off_text = "✅ Off" if not current else "Off"
    buttons = [
        [
            InlineKeyboardButton(text=on_text, callback_data=f"ADMIN AutoplayOn|{chat_id}", style=ButtonStyle.SUCCESS),
            InlineKeyboardButton(text=off_text, callback_data=f"ADMIN AutoplayOff|{chat_id}", style=ButtonStyle.DANGER),
        ],
        [InlineKeyboardButton(text=_["CLOSE_BUTTON"], callback_data=f"ADMIN AutoplayClose|{chat_id}", style=ButtonStyle.PRIMARY)],
    ]
    return buttons


def track_markup(_, videoid, user_id, channel, fplay):
    buttons = [
        [
            InlineKeyboardButton(
                text=_["P_B_1"],
                callback_data=f"MusicStream {videoid}|{user_id}|a|{channel}|{fplay}",
                 style=ButtonStyle.PRIMARY,
            ),
            InlineKeyboardButton(
                text=_["P_B_2"],
                callback_data=f"MusicStream {videoid}|{user_id}|v|{channel}|{fplay}",
                 style=ButtonStyle.SUCCESS,
            ),
        ],
        [
            InlineKeyboardButton(
                text=_["CLOSE_BUTTON"],
                callback_data=f"forceclose {videoid}|{user_id}",
                style=ButtonStyle.DANGER,
            )
        ],
    ]
    return buttons


def stream_markup_timer(_, chat_id, played, dur):
    played_sec = time_to_seconds(played)
    duration_sec = time_to_seconds(dur)
    percentage = (played_sec / duration_sec) * 100
    umm = math.floor(percentage)
    if 0 < umm <= 10:
        bar = "◉—————————"
    elif 10 < umm < 20:
        bar = "—◉————————"
    elif 20 <= umm < 30:
        bar = "——◉———————"
    elif 30 <= umm < 40:
        bar = "———◉——————"
    elif 40 <= umm < 50:
        bar = "————◉—————"
    elif 50 <= umm < 60:
        bar = "—————◉————"
    elif 60 <= umm < 70:
        bar = "——————◉———"
    elif 70 <= umm < 80:
        bar = "———————◉——"
    elif 80 <= umm < 95:
        bar = "————————◉—"
    else:
        bar = "—————————◉"
    buttons = [
        [
            InlineKeyboardButton(text="▷", callback_data=f"ADMIN Resume|{chat_id}", style=_rand_style()),
            InlineKeyboardButton(text="II", callback_data=f"ADMIN Pause|{chat_id}", style=_rand_style()),
            InlineKeyboardButton(text="↻", callback_data=f"ADMIN Replay|{chat_id}", style=_rand_style()),
            InlineKeyboardButton(text="‣‣I", callback_data=f"ADMIN Skip|{chat_id}", style=_rand_style()),
            InlineKeyboardButton(text="▢", callback_data=f"ADMIN Stop|{chat_id}", style=_rand_style()),
        ],
        [
            InlineKeyboardButton(
                text=f"{played} {bar} {dur}",
                callback_data="GetTimer",
                 style=ButtonStyle.PRIMARY,
            )
        ],
        [
            InlineKeyboardButton(text="-15ˢ", callback_data=f"ADMIN SeekBack15|{chat_id}", style=_rand_style()),
            InlineKeyboardButton(text="15ˢ+", callback_data=f"ADMIN SeekFwd15|{chat_id}", style=_rand_style()),
        ],
        [
            InlineKeyboardButton(text="🎵 Autoplay", callback_data=f"ADMIN AutoplayMenu|{chat_id}", style=_rand_style()),
        ],
        [
            InlineKeyboardButton(text="❀彡 𝓓𝓮𝓿𝓮𝓵𝓸𝓹𝓮𝓻 彡❀", url="https://t.me/Oye_babyy", style=_rand_style()),
        ],
        [InlineKeyboardButton(text=_["CLOSE_BUTTON"], callback_data="close",
                              style=ButtonStyle.DANGER,
                             )
        ],
    ]
    return buttons


def stream_markup(_, chat_id):
    buttons = [
        [
            InlineKeyboardButton(text="▷", callback_data=f"ADMIN Resume|{chat_id}", style=_rand_style()),
            InlineKeyboardButton(text="II", callback_data=f"ADMIN Pause|{chat_id}", style=_rand_style()),
            InlineKeyboardButton(text="↻", callback_data=f"ADMIN Replay|{chat_id}", style=_rand_style()),
            InlineKeyboardButton(text="‣‣I", callback_data=f"ADMIN Skip|{chat_id}", style=_rand_style()),
            InlineKeyboardButton(text="▢", callback_data=f"ADMIN Stop|{chat_id}", style=_rand_style()),
        ],
        [
            InlineKeyboardButton(text="-15ˢ", callback_data=f"ADMIN SeekBack15|{chat_id}", style=_rand_style()),
            InlineKeyboardButton(text="15ˢ+", callback_data=f"ADMIN SeekFwd15|{chat_id}", style=_rand_style()),
        ],
        [
            InlineKeyboardButton(text="🎵 Autoplay", callback_data=f"ADMIN AutoplayMenu|{chat_id}", style=_rand_style()),
        ],
        [
            InlineKeyboardButton(text="❀彡 𝓓𝓮𝓿𝓮𝓵𝓸𝓹𝓮𝓻 彡❀", url="https://t.me/Oye_babyy", style=_rand_style()),
        ],
        [InlineKeyboardButton(text=_["CLOSE_BUTTON"], callback_data="close",
                              style=ButtonStyle.DANGER,
                             )
                    ],
    ]
    return buttons


def playlist_markup(_, videoid, user_id, ptype, channel, fplay):
    buttons = [
        [
            InlineKeyboardButton(
                text=_["P_B_1"],
                callback_data=f"DevSpPlaylists {videoid}|{user_id}|{ptype}|a|{channel}|{fplay}",
                 style=ButtonStyle.PRIMARY,
            ),
            InlineKeyboardButton(
                text=_["P_B_2"],
                callback_data=f"DevSpPlaylists {videoid}|{user_id}|{ptype}|v|{channel}|{fplay}",
                 style=ButtonStyle.SUCCESS,
            ),
        ],
        [
            InlineKeyboardButton(
                text=_["CLOSE_BUTTON"],
                callback_data=f"forceclose {videoid}|{user_id}",
                style=ButtonStyle.DANGER,
            ),
        ],
    ]
    return buttons


def livestream_markup(_, videoid, user_id, mode, channel, fplay):
    buttons = [
        [
            InlineKeyboardButton(
                text=_["P_B_3"],
                callback_data=f"LiveStream {videoid}|{user_id}|{mode}|{channel}|{fplay}",
                 style=ButtonStyle.PRIMARY,
            ),
        ],
        [
            InlineKeyboardButton(
                text=_["CLOSE_BUTTON"],
                callback_data=f"forceclose {videoid}|{user_id}",
                style=ButtonStyle.DANGER,
            ),
        ],
    ]
    return buttons


def slider_markup(_, videoid, user_id, query, query_type, channel, fplay):
    query = f"{query[:20]}"
    buttons = [
        [
            InlineKeyboardButton(
                text=_["P_B_1"],
                callback_data=f"MusicStream {videoid}|{user_id}|a|{channel}|{fplay}",
                 style=ButtonStyle.PRIMARY,
            ),
            InlineKeyboardButton(
                text=_["P_B_2"],
                callback_data=f"MusicStream {videoid}|{user_id}|v|{channel}|{fplay}",
                 style=ButtonStyle.SUCCESS,
            ),
        ],
        [
            InlineKeyboardButton(
                text="◁",
                callback_data=f"slider B|{query_type}|{query}|{user_id}|{channel}|{fplay}",
                 style=ButtonStyle.PRIMARY,
            ),
            InlineKeyboardButton(
                text=_["CLOSE_BUTTON"],
                callback_data=f"forceclose {query}|{user_id}",
                style=ButtonStyle.DANGER,
            ),
            InlineKeyboardButton(
                text="▷",
                callback_data=f"slider F|{query_type}|{query}|{user_id}|{channel}|{fplay}",
                 style=ButtonStyle.PRIMARY,
            ),
        ],
    ]
    return buttons
