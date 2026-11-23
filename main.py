import telebot
from telebot.types import (
    InlineKeyboardMarkup,
    InlineKeyboardButton,
)
import requests
import re
import time
import string
import random
import os
from datetime import datetime
from typing import Tuple, List, Optional
import pytz

# ================= CONFIG =================
BOT_TOKEN = "9096964141:AAHBz4o5CaPFVbp_5l7F2gjH_VqMAxCvQA8"
OWNER_NAME = "TH TAJ OWNER"
OWNER_ID   = 8884231104

API_BASE = "https://charlie-revenue-joshua-alone.trycloudflare.com"
API_KEY  = ""  # This API does not require an API key

IST      = pytz.timezone("Asia/Kolkata")
DHAKA_TZ = IST

VALID_REGIONS   = ["BD"]
DEFAULT_REGION  = "BD"

if not BOT_TOKEN:
    raise SystemExit("BOT_TOKEN missing!")

bot = telebot.TeleBot(BOT_TOKEN, parse_mode="HTML")
# =========================================


# ================= FONT =================
def sc(text: str) -> str:
    """Small-caps font (a–z / A–Z / 0–9 only; emojis preserved)."""
    if not text:
        return text
    normal = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
    small  = (
        "ᴀʙᴄᴅᴇғɢʜɪᴊᴋʟᴍɴᴏᴘǫʀsᴛᴜᴠᴡxʏᴢ"
        "ᴀʙᴄᴅᴇғɢʜɪᴊᴋʟᴍɴᴏᴘǫʀsᴛᴜᴠᴡxʏᴢ"
        "0123456789"
    )
    return text.translate(str.maketrans(normal, small))


def footer() -> str:
    return f"\n\n━━━━━━━━━━━━━━\n👑 Owner: {OWNER_NAME}"


# ================= PREMIUM EMOJI =================
PREMIUM_EMOJI_IDS = {
    "🔥": "6118433577488093576",
    "👤": "6264538349034281099",
    "⚠️": "6221914376329237010",
    "❌": "6285138648568437249",
    "🎉": "6158973086600273462",
    "🎮": "5375338737028841420",
    "💎": "5380111356227770863",
    "📊": "6221939111045895344",
    "🛍️": "6129550284290006595",
    "🛍": "6129479035077531636",
    "💰": "6129732880529628243",
    "🏆": "6129444065453808638",
    "👑": "6158882647473920838",
    "🛡": "6073269883246749014",
    "🛡️": "6073269883246749014",
    "🔙": "6129828611055689014",
    "🚀": "6158992706010880884",
    "🆓": "5316902932417885675",
    "🔑": "5316858509571144216",
    "📝": "6129932613688764241",
    "📂": "5818797194127346654",
    "🎟": "6129959208126258284",
    "⏱": "6129705667616841573",
    "✅": "6077936244954764334",
    "🎁": "6129950489342647259",
    "🔗": "6129433877791382400",
    "🎰": "6073269883246749014",
    "📢": "6129705083501293112",
    "🔹": "5116575178012235794",
    "🔄": "6156744720128154345",
    "🗑": "6131660826924292492",
    "🎯": "6129727043669072880",
    "🔢": "5188375125552033525",
    "🚫": "6129415619885407680",
    "📡": "6129909635613726974",
    "🛒": "6129627894349045589",
    "💾": "6129870783339567154",
    "📥": "6129779562529168023",
    "➕": "4956507094124594921",
    "❤️": "6237579651066107302",
    "📋": "5319160079465857105",
    "📌": "6129772480128097710",
    "🤖": "6237579651066107302",
    "💡": "6224008512188452721",
    "⚡": "6118531988073747281",
    "🪪": "5447311106030726740",
    "📅": "6129939837823753679",
    "🆕": "6129694470637100146",
    "👇": "6129434968713076807",
    "🔐": "6100425986501777047",
    "🧠": "6224008512188452721",
    "❓": "6181356978678275248",
    "📦": "6129570565125577536",
    "⏰": "6129782440157256336",
    "⏳": "6267229004311303657",
    "🏅": "6265004494719816749",
    "🌐": "5375177250553487549",
    "⚔️": "6129731974291527294",
    "🐺": "6129532314146838421",
    "📭": "6129805465476929485",
    "👆": "6129650399977675538",
    "🟢": "6129828611055689014",
    "🟡": "6129801569941592173",
    "🔍": "6129769198773083022",
    "⏸": "6129708236007283169",
    "🔴": "5400315084251625106",
    "⚪": "6129443429798648428",
    "📈": "4958506272551863292",
    "💠": "6129553312241949602",
    "🕒": "5346181118884331907",
    "📤": "6129494286506401122",
    "🌠": "5375349255403740823",
    "🍀": "6129778965528713511",
    "💺": "6129433877791382400",
}

_EMOJI_PATTERN = re.compile(
    r'('
    r'[\U0001F600-\U0001F64F]|'
    r'[\U0001F300-\U0001F5FF]|'
    r'[\U0001F680-\U0001F6FF]|'
    r'[\U0001F700-\U0001F77F]|'
    r'[\U0001F780-\U0001F7FF]|'
    r'[\U0001F800-\U0001F8FF]|'
    r'[\U0001F900-\U0001F9FF]|'
    r'[\U0001FA00-\U0001FA6F]|'
    r'[\U0001FA70-\U0001FAFF]|'
    r'[\u2600-\u26FF]|'
    r'[\u2700-\u27BF]|'
    r'[\u2300-\u23FF]|'
    r'[\uFE0F]|'
    r'[\u200D]'
    r')+',
    flags=re.UNICODE,
)


def PE(text: str) -> str:
    """Wrap every known emoji in a <tg-emoji> tag for premium rendering."""
    if not text:
        return text

    def rep(m):
        e = m.group(0)
        if e in PREMIUM_EMOJI_IDS:
            return f'<tg-emoji emoji-id="{PREMIUM_EMOJI_IDS[e]}">{e}</tg-emoji>'
        base = e.replace("\ufe0f", "")
        if base in PREMIUM_EMOJI_IDS:
            return f'<tg-emoji emoji-id="{PREMIUM_EMOJI_IDS[base]}">{e}</tg-emoji>'
        for key, eid in PREMIUM_EMOJI_IDS.items():
            if key in e:
                return f'<tg-emoji emoji-id="{eid}">{e}</tg-emoji>'
        return e

    return _EMOJI_PATTERN.sub(rep, text)


# ================= ESCAPE / FORMATTERS =================
def esc(s) -> str:
    """HTML escape user data using NUMERIC entities.
    Named entities (like &lt;) contain letters that sc() would translate
    (lt → ʟᴛ), breaking them. Numeric entities (&#60;) have no letters,
    so sc() leaves them intact."""
    if s is None:
        return ""
    s = str(s)
    return (s.replace("&", "&#38;")
             .replace("<", "&#60;")
             .replace(">", "&#62;"))


def _sanitize_lt_gt(text: str) -> str:
    """Escape raw < > in template text BEFORE PE() adds <tg-emoji> tags.
    Called AFTER sc() so any template `<uid>` that got translated to
    `<ᴜɪᴅ>` also becomes &#60;ᴜɪᴅ&#62;."""
    if not text:
        return text
    return text.replace("<", "&#60;").replace(">", "&#62;")


def fmt_num(n) -> str:
    try:
        return f"{int(n):,}"
    except Exception:
        return str(n)


def ago_str(ts) -> str:
    if not ts:
        return "N/A"
    try:
        d = int(time.time() - float(ts))
        if d < 5:     return "Just Now"
        if d < 60:    return f"{d}s Ago"
        if d < 3600:  return f"{d // 60}m Ago"
        if d < 86400: return f"{d // 3600}h Ago"
        return f"{d // 86400}d Ago"
    except Exception:
        return "N/A"


def now_bst() -> datetime:
    return datetime.now(DHAKA_TZ)


def fmt_duration(sec) -> str:
    try:
        sec = int(sec)
        if sec <= 0:
            return "Expired"
        d, rem = divmod(sec, 86400)
        h, rem = divmod(rem, 3600)
        m, s = divmod(rem, 60)
        parts = []
        if d: parts.append(f"{d}d")
        if h: parts.append(f"{h}h")
        if m: parts.append(f"{m}m")
        if not parts: parts.append(f"{s}s")
        return " ".join(parts)
    except Exception:
        return "N/A"


def is_owner(uid) -> bool:
    try:
        return OWNER_ID != 0 and int(uid) == int(OWNER_ID)
    except Exception:
        return False


# ================= BUSINESS HELPERS =================
def generate_code(length: int = 10) -> str:
    chars = string.ascii_uppercase + string.digits
    return ''.join(random.choices(chars, k=length))


# ================= API HELPERS =================
def call_like_api(uid: str, region: str = DEFAULT_REGION) -> Tuple[Optional[dict], Optional[str]]:
    try:
        url = f"{API_BASE}/like"
        params = {"uid": str(uid), "server_name": region.upper()}
        r = requests.get(url, params=params, timeout=40)
        r.raise_for_status()

        try:
            data = r.json()
        except Exception:
            return None, f"⚠️ API returned non-JSON (HTTP {r.status_code})"

        if "LikesbeforeCommand" not in data:
            return None, data.get("error") or data.get("message") or "API error"

        if int(data.get("remaining", 1)) <= 0:
            return None, "❌ Daily limit over — try again after reset (4 AM IST)"

        return data, None
    except requests.exceptions.Timeout:
        return None, "⏳ API timeout — try again"
    except requests.exceptions.ConnectionError:
        return None, "🔌 Cannot reach API server"
    except Exception as e:
        return None, f"⚠️ {type(e).__name__}: {e}"


def call_remain_api() -> Optional[dict]:
    try:
        r = requests.get(f"{API_BASE}/remain", timeout=15)
        return r.json()
    except Exception:
        return None


def api_ping() -> Tuple[bool, int]:
    start = time.time()
    try:
        r = requests.get(f"{API_BASE}/health", timeout=8)
        latency = int((time.time() - start) * 1000)
        return (r.status_code == 200), latency
    except Exception:
        return False, 0


# ================= TELEGRAM SEND HELPER =================
def send_premium(chat_id, text: str, reply_to=None, kb=None) -> Optional[object]:
    """sc() → sanitize < > → PE() → HTML send. Fallback to plain text on parse error."""
    body = PE(_sanitize_lt_gt(sc(text)))
    kwargs = {"chat_id": chat_id, "text": body, "parse_mode": "HTML"}
    if reply_to is not None:
        kwargs["reply_to_message_id"] = reply_to
    if kb is not None:
        kwargs["reply_markup"] = kb
    try:
        return bot.send_message(**kwargs)
    except Exception as e:
        err_str = str(e).lower()
        if "can't parse entities" in err_str or "unsupported start tag" in err_str:
            plain = re.sub(r"<[^>]+>", "", body)
            kwargs["text"] = plain
            del kwargs["parse_mode"]
            try:
                return bot.send_message(**kwargs)
            except Exception as e2:
                print(f"[send_premium fallback] {type(e2).__name__}: {e2}")
                return None
        print(f"[send_premium error] {type(e).__name__}: {e}")
        return None


def edit_premium(chat_id, message_id, text: str, kb=None):
    """sc() → sanitize < > → PE() → HTML edit. Fallback to plain text on parse error."""
    body = PE(_sanitize_lt_gt(sc(text)))
    kwargs = {
        "chat_id": chat_id,
        "message_id": message_id,
        "text": body,
        "parse_mode": "HTML",
    }
    if kb is not None:
        kwargs["reply_markup"] = kb
    try:
        bot.edit_message_text(**kwargs)
    except Exception as e:
        err_str = str(e).lower()
        if "can't parse entities" in err_str or "unsupported start tag" in err_str:
            plain = re.sub(r"<[^>]+>", "", body)
            kwargs["text"] = plain
            del kwargs["parse_mode"]
            try:
                bot.edit_message_text(**kwargs)
            except Exception:
                pass
        # message not modified vs other errors — silent


# ================= KEYBOARD HELPERS =================
def build_inline(rows):
    buttons = []
    for row in rows:
        btn_row = []
        for item in row:
            try:
                text, data = item[0], item[1]
                if isinstance(data, str) and (data.startswith("http://") or data.startswith("https://")):
                    btn_row.append(InlineKeyboardButton(text, url=data))
                else:
                    btn_row.append(InlineKeyboardButton(text, callback_data=str(data)))
            except Exception:
                continue
        if btn_row:
            buttons.append(btn_row)
    return InlineKeyboardMarkup(buttons) if buttons else None


# ================= START =================
@bot.message_handler(commands=["start"])
def start(msg):
    text = (
        "🔥 VIP MANUAL LIKE BOT\n\n"
        "📌 AVAILABLE COMMANDS\n\n"
        "⚡ /like uid [region]\n"
        "📊 /remain\n"
        "🩺 /ping\n"
        "🌐 /regions\n\n"
        "📝 EXAMPLES\n"
        "/like 123456789\n"
        "/like 123456789 ind\n\n"
        "ℹ️ NOTES\n"
        "• Default region: BD\n"
        "• Wrong input → error shown\n"
        "• Daily API limit applied\n"
        "• Reset time: 4 AM IST"
    )
    send_premium(msg.chat.id, text + footer(), reply_to=msg.message_id)


# ================= REGIONS =================
@bot.message_handler(commands=["regions"])
def cmd_regions(msg):
    lines = ["🌐 SUPPORTED REGIONS", ""]
    for r in VALID_REGIONS:
        mark = "🟢" if r == DEFAULT_REGION else "⚪"
        lines.append(f"{mark} {r}")
    lines.append("")
    lines.append(f"📌 default: {DEFAULT_REGION}")
    lines.append("")
    lines.append("💡 usage: /like uid region")
    send_premium(msg.chat.id, "\n".join(lines) + footer(), reply_to=msg.message_id)


# ================= PING =================
@bot.message_handler(commands=["ping"])
def cmd_ping(msg):
    ok, latency = api_ping()
    if ok:
        text = (
            "🩺 API STATUS\n\n"
            f"🟢 online\n"
            f"⚡ latency: {latency} ms\n"
            f"🌐 host: {API_BASE}"
        )
    else:
        text = (
            "🩺 API STATUS\n\n"
            "🔴 offline\n"
            f"🌐 host: {API_BASE}"
        )
    send_premium(msg.chat.id, text + footer(), reply_to=msg.message_id)


# ================= REMAIN =================
@bot.message_handler(commands=["remain"])
def cmd_remain(msg):
    data = call_remain_api()
    if not data:
        send_premium(
            msg.chat.id,
            "❌ cannot reach /remain endpoint" + footer(),
            reply_to=msg.message_id,
        )
        return

    text = (
        "📊 DAILY LIKE LIMIT\n\n"
        f"🎯 total limit : {fmt_num(data.get('daily_limit', 0))}\n"
        f"✅ used        : {fmt_num(data.get('used', 0))}\n"
        f"📈 remaining   : {fmt_num(data.get('remaining', 0))}\n\n"
        f"🕒 reset at    : {data.get('reset_info', '4 AM IST')}"
    )
    send_premium(msg.chat.id, text + footer(), reply_to=msg.message_id)


# ================= MANUAL LIKE =================
@bot.message_handler(commands=["like"])
def manual_like(msg):
    parts = msg.text.split()

    if len(parts) < 2 or len(parts) > 3:
        send_premium(
            msg.chat.id,
            "❌ WRONG USAGE\n\n"
            "✅ correct format:\n"
            "/like uid\n"
            "/like uid region\n\n"
            "📝 example:\n"
            "/like 123456789\n"
            "/like 123456789 ind"
            + footer(),
            reply_to=msg.message_id,
        )
        return

    uid = parts[1].strip()
    region = parts[2].strip().upper() if len(parts) == 3 else DEFAULT_REGION

    if not uid.isdigit() or not (6 <= len(uid) <= 15):
        send_premium(
            msg.chat.id,
            "❌ invalid uid\n\n"
            "📌 uid must be 6–15 digits only"
            + footer(),
            reply_to=msg.message_id,
        )
        return

    if region not in VALID_REGIONS:
        send_premium(
            msg.chat.id,
            f"❌ invalid region: {esc(region)}\n\n"
            f"🌐 supported: {', '.join(VALID_REGIONS)}\n\n"
            f"💡 use /regions to see the list"
            + footer(),
            reply_to=msg.message_id,
        )
        return

    m = send_premium(
        msg.chat.id,
        f"🔥 sending likes...\n\n"
        f"⚡ uid : {uid}\n"
        f"🌐 region : {region}\n"
        f"⏳ please wait",
        reply_to=msg.message_id,
    )
    if m is None:
        return

    started = time.time()
    data, err = call_like_api(uid, region)
    elapsed = int((time.time() - started) * 1000)

    if err:
        edit_premium(
            msg.chat.id,
            m.message_id,
            f"❌ LIKE FAILED\n\n{err}" + footer(),
        )
        return

    likes_before = int(data.get("LikesbeforeCommand", 0))
    likes_after  = int(data.get("LikesafterCommand", 0))
    given        = int(data.get("LikesGivenByAPI", likes_after - likes_before))
    remaining    = data.get("remaining", "-")

    text = (
        "✅ LIKE SUCCESSFUL\n\n"
        f"👤 nickname : {esc(data.get('PlayerNickname', '-'))}\n"
        f"🪪 uid      : {esc(data.get('UID', uid))}\n"
        f"⚔️ level    : {esc(data.get('Level', '-'))}\n\n"
        f"👍 likes before : {fmt_num(likes_before)}\n"
        f"🔥 likes after  : {fmt_num(likes_after)}\n"
        f"🎯 likes given  : {fmt_num(given)}\n\n"
        f"📈 remaining    : {esc(remaining)}\n"
        f"🌍 region       : {region}\n"
        f"⚡ latency      : {elapsed} ms\n"
        f"🟢 status       : success"
    )
    edit_premium(msg.chat.id, m.message_id, text + footer())


# ================= UNKNOWN COMMAND =================
@bot.message_handler(func=lambda m: m.text and m.text.startswith("/"))
def unknown(msg):
    send_premium(
        msg.chat.id,
        "❌ unknown command\n\n"
        "ℹ️ use /start to see available commands"
        + footer(),
        reply_to=msg.message_id,
    )


# ================= RUN =================
if __name__ == "__main__":
    print("🔥 VIP manual like bot starting...")
    print(f"🤖 bot: {BOT_TOKEN.split(':')[0]}")
    print(f"👑 owner: {OWNER_ID}")
    print(f"🌐 API: {API_BASE}")
    print(f"🌍 default region: {DEFAULT_REGION}")
    while True:
        try:
            bot.infinity_polling(timeout=60, long_polling_timeout=60)
        except Exception as e:
            print(f"[polling crash] {type(e).__name__}: {e}")
            time.sleep(5)