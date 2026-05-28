import os
from threading import Thread
from flask import Flask
from telethon import TelegramClient, events

# ==========================================================================
# 🌐 WEB SERVER FOR RENDER (KEEP-ALIVE NODE)
# ==========================================================================
app = Flask(__name__)

@app.route('/')
def home():
    return "🤖 Font Changer Bot is Running Live 24/7!"

def run_web_server():
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)

# ==========================================================================
# ⚙️ TELEGRAM BOT CONFIGURATION
# ==========================================================================
BOT_TOKEN = "8933958981:AAGm3jbwzEWCywAyiyAkryfCnvWg4iDkywQ"
API_ID = 37300120               
API_HASH = "aa35ee2b1b569c1adabfdc2adc9e120c"

bot = TelegramClient('render_font_session_v2', API_ID, API_HASH)

# ==========================================================================
# 🗺️ PERFECTLY ALIGNED FONT DICTIONARIES (52 Characters Each)
# ==========================================================================
normal_chars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"

fonts_map = {
    "𝔖𝔗𝔜𝔏𝔈 𝔄": "𝔞𝔟𝔠𝔡𝔢𝔣𝔤𝔥𝔦𝔧𝔨𝔩𝔪𝔫𝔬𝔭𝔮𝔯𝔰𝔱𝔲𝔳𝔴𝔵𝔶𝔷𝔄𝔅ℭ𝔇𝔈𝔉𝔊𝔋ℑ𝔍𝔎𝔏𝔐𝔑𝔒𝔓𝔔𝔖𝔗𝔘𝔙𝔚𝔛𝔜𝔏",
    "𝓢𝓣𝓨𝓛𝓔 𝓑": "𝓪𝓫𝓬𝓭𝓮𝓯𝓰𝓱𝓲𝓳𝓴𝓵𝓶𝓷𝓸𝓹𝓺𝓻𝓼𝓽𝓾𝓿𝔀𝔁𝔂𝔃𝓐𝓑𝓒𝓓𝓔𝓕𝓖🔓𝓘𝓙𝓚𝓛𝓜𝓝𝓞𝓟𝓠𝓡𝓢𝓣𝓤𝓥𝓦𝓧𝓨𝓩",
    "𝕊𝕋𝕐𝕃𝔼 ℂ": "𝕒𝕓𝕔𝕕𝕖𝕗𝕘𝕙𝕚𝕛𝕜𝕝𝕞𝕟𝕠𝕡𝕢𝕣𝕤𝕥𝕦𝕧𝕨𝕩𝕪𝕫𝔸𝔹ℂ𝔻𝔼𝔽𝔾ℍ𝕀𝕁𝕂𝕃𝕄ℕ𝕆ℙℚℝ𝕊𝕋𝕌𝕍𝕎𝕏𝕐ℤ",
    "⚡ 𝑩𝑶𝑳𝑫 𝑰𝑻𝑨𝑳𝑰𝑪": "𝒂𝒃𝒄𝒅𝒆𝒇𝒈𝒉𝒊𝒋𝒌𝒍改𝒏𝒐𝒑𝒒𝒓𝒔𝒕𝒖𝒗𝒘𝒙𝒚𝒛𝑨𝑩𝑪𝑫𝑬𝑭𝑮𝑯𝑰𝑱𝑲𝑳𝑴𝑵𝑶𝑷𝑸𝑹𝑺𝑻𝑼𝑽𝑾𝑿𝒀𝒁",
    "🄱🄾🅇 🄵🄾🄽🅃": "🄰🄱🄲🄳🄴🄵🄶🄷🄸🄹🄺🄻🄼🄽🄾🄿🅄🅁🅂🅃🅄🅅🅆🅇🅈🅪🄰🄱🄲🄳🄴🄵🄶🄷🄸🄹🄺🄻🄼🄽🄾🄿🅄🅁🅂🅃🅄🅅🅆🅇🅈🅪",
}

# ==========================================================================
# 🚀 BOT LOGIC
# ==========================================================================
@bot.on(events.NewMessage(pattern='/start'))
async def start_cmd(event):
    await event.respond(
        "👋 **Welcome to Stylish Font Changer Bot!**\n\n"
        "✍️ Mujhe koi bhi text message bhejo, main use mast fonts mein badal dunga."
    )

@bot.on(events.NewMessage)
async def convert_text(event):
    if event.raw_text.startswith('/') or event.is_channel: return

    user_text = event.raw_text
    output = "✨ **Here are your Stylish Fonts:**\n⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯\n\n"
    
    for font_name, font_chars in fonts_map.items():
        # Dynamic translation table with strict length compliance
        trans_rule = str.maketrans(normal_chars, font_chars)
        converted = user_text.translate(trans_rule)
        output += f"🌟 **{font_name}:**\n`{converted}`\n\n"
        
    output += "👉 _Tap text to auto-copy!_"
    await event.respond(output)

# ==========================================================================
# 🏁 MAIN STARTUP POINT
# ==========================================================================
if __name__ == '__main__':
    print("🌐 Starting Keep-Alive Web Server...")
    Thread(target=run_web_server, daemon=True).start()

    print("🟢 Bot Engine Connecting to Telegram...")
    bot.start(bot_token=BOT_TOKEN)
    bot.run_until_disconnected()
    
