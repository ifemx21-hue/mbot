import os
from threading import Thread
from flask import Flask
from telethon import TelegramClient, events, Button

# ==========================================================================
# 🌐 WEB SERVER FOR RENDER (KEEP-ALIVE NODE)
# ==========================================================================
app = Flask(__name__)

@app.route('/')
def home():
    return "👑 Premium Font Changer Bot is Active!"

def run_web_server():
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)

# ==========================================================================
# ⚙️ TELEGRAM BOT CONFIGURATION
# ==========================================================================
BOT_TOKEN = "7996319660:AAF0NSlTOy4l3VCehfhgOZ4DSSHozJ8bw9I"
API_ID = 37300120               
API_HASH = "aa35ee2b1b569c1adabfdc2adc9e120c"

bot = TelegramClient('render_font_premium_v1', API_ID, API_HASH)

# ==========================================================================
# 🗺️ ALIGNED FONTS DATABASE (Premium Selection)
# ==========================================================================
normal_chars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"

fonts_config = [
    {"name": "Bᴏʟᴅ", "chars": "𝒂𝒃𝒄𝒅𝒆𝒇𝒈𝒉𝒊𝒋𝒌𝒍𝒎𝒏𝒐𝒑𝒒𝒓𝒔𝒕𝒖𝒗𝒘𝒙𝒚𝒛𝑨𝑩𝑪𝑫𝑬𝑭𝑮𝑯𝑰𝑱𝑲𝑳𝑴𝑵𝑶𝑷𝑸𝑹𝑺𝑻𝑼𝑽𝑾𝑿𝒀𝒁"},
    {"name": "Iᴛᴀʟɪᴄ", "chars": "𝘢𝘣𝘤𝘥\u200b𝘦𝘧𝘨𝘩𝘪𝘫𝘬𝘭𝘮𝘯𝘰𝘱𝘲𝘳𝘴𝘵𝘶𝘷𝘸𝘹𝘺𝘻𝘈𝘉𝘊𝘋\u200b𘘞𝘎𝘏𝘐𝘑𝘒𝘓𝘔𝘕𝘖𘘞𝘘𘘞𘘞𘘞𘘞𘘞𘘞𘘞"},
    {"name": "Sᴀɴs Bᴏʟᴅ", "chars": "𝗮𝗯𝗰𝗱𝗲打𝗴𝗵𝗶𝗷𝗸𝗹𝗺𝗻𝗼𝗽𝗾𝗿𝘀𝘁𝘂𝘃𝘄𝗅𝘆𝘇𝗔𝗕𝗖𝗗𝗘𝗙𝗚𝗛𝗜𝗝𝗞𝗟𝗠𝗡𝗢𝗣𝗤𝗥𝗦𝗧𝗨▼𝗪𝗫𝗬𝗭"},
    {"name": "Gᴏᴛʜɪᴄ", "chars": "𝔞𝔟𝔠𝔡𝔢𝔣𝔤𝔥𝔦𝔧𝔨𝔩𝔪𝔫𝔬𝔭𝔮𝔯𝔰𝔱𝔲𝔳𝔴𝔵𝔶𝔷𝔄𝔅ℭ𝔇𝔈𝔉𝔊𝔋ℑ𝔍𝔎𘔝𝔐𝔑𝔒𝔓𝔔𝔖𝔗𝔘𝔙𝔚𝔛𝔜𝔏"},
    {"name": "Dᴏ𝔲𝔟𝔩𝔢 S𝔱𝔯𝔲𝔠𝔨", "chars": "𝕒𝕓𝕔𝕕𝕖𝕗𝕘𝕙𝕚𝕛𝕜𝕝𝕞𝕟𝕠𝕡𝕢𝕣𝕤𝕥𝕦𝕧𝕨𝕩𝕪𝕫𝔸𝔹ℂ𝔻𝔼𝔽𝔾ℍ𝕀𝕁𝕂𝕃𝕄ℕ🔑𝕗ℚℝ𝕊𝕋𝕌𝕍𝕎𝕏𝕐ℤ"},
    {"name": "Bᴏx Fᴏɴᴛ", "chars": "🄰🄱🄲🄳🄴🄵🄶🄷🄸🄹🄺🄻🄼🄽🄾🄿🅄🅁🅂🅃🅄🅅🅆🅇🅈🅪🄰🄱🄲🄳🄴🄵🄶🄷🄸🄹🄺🄻🄼🄽🄾🄿🅄🅁🅂🅃🅄🅅🅆🅇🅈🅪"}
]

# Small caps conversion tool for global UI text styling
def to_small_caps(text):
    caps_map = str.maketrans(
        "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ",
        "ᴀʙᴄᴅᴇꜰɢʜɪᴊᴋʟᴍɴ_ᴘ_ʀꜱᴛᴜᴠᴡxʏᴢABCDEFGHIJKLMNOPQRSTUVWXYZ"
    )
    return text.translate(caps_map)

# ==========================================================================
# 🚀 BOT INTERFACE & LOGIC
# ==========================================================================
@bot.on(events.NewMessage(pattern='/start'))
async def start_cmd(event):
    welcome_text = (
        "👑 ⚜️ **Pʀᴇᴍɪᴜᴍ Fᴏɴᴛs Bᴏᴛ** ⚜️ 👑\n"
        "⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯\n"
        "📥 **Sᴇɴᴅ ᴍᴇ ᴀɴʏ ɴᴏʀᴍᴀʟ ᴛᴇxᴛ ᴍᴇssᴀɢᴇ**\n"
        "⚡ _I ᴡɪʟʟ ɪɴsᴛᴀɴᴛʟʏ ᴄᴏɴᴠᴇʀᴛ ɪᴛ ɪɴᴛᴏ ᴠɪᴘ sᴛʏʟɪsʜ ʙᴜᴛᴛᴏɴs ɢʀɪᴅ._\n\n"
        "💎 ✨ _Dʀᴏᴘ ʏᴏᴜʀ ᴛᴇxᴛ ʙᴇʟᴏᴡ ᴛᴏ ᴛᴇsᴛ_ ✨ 💎"
    )
    await event.respond(welcome_text)

@bot.on(events.NewMessage)
async def process_fonts(event):
    if event.raw_text.startswith('/') or event.is_channel: return

    user_text = event.raw_text
    buttons_grid = []
    
    # Converting the user's text to premium style preview for the grid
    small_caps_user_text = to_small_caps(user_text)
    
    for font in fonts_config:
        try:
            trans_rule = str.maketrans(normal_chars, font["chars"])
            converted_text = user_text.translate(trans_rule)
            
            # Format: ( Tᴇxᴛ ) · FontName
            btn_label = f"( {converted_text} ) · {font['name']}"
            
            # Storing the exact style to provide an immediate clean layout
            buttons_grid.append([Button.inline(btn_label, data=f"cp_{converted_text[:40]}")])
        except Exception:
            continue

    if buttons_grid:
        # High tier premium styling utility buttons
        buttons_grid.append([
            Button.inline("📋 Aʟʟ Fᴏɴᴛs", data="msg_all"), 
            Button.inline("🔄 Cʜᴀɴɢᴇ Fᴏɴᴛ", data="msg_change")
        ])
        buttons_grid.append([
            Button.inline("⚜️ 1 / 8", data="page"), 
            Button.inline("Nᴇxᴛ ➡️", data="page")
        ])
        
        await event.respond(
            f"⚜️ 💎 **Aʟʟ ғᴏɴᴛs - « ( {small_caps_user_text} ) »**\n👑 _Cʜᴏᴏsᴇ ᴀ ᴠᴀʀɪᴀɴᴛ ʙᴇʟᴏᴡ:_ ",
            buttons=buttons_grid
        )

# ==========================================================================
# ⚡ PREMIUM CLICK DISPATCHER (AUTO-COPY ALERT SYSTEM)
# ==========================================================================
@bot.on(events.CallbackQuery)
async def handle_clicks(event):
    data = event.data.decode('utf-8')
    
    if data.startswith("cp_"):
        copied_text = data.split("_")[1]
        await event.answer(f"👑 Cᴏ𝔭𝔶 s𝔲𝔡𝔡𝔢𝔫𝔩𝔶!!\n\n📝 {copied_text}", alert=True)
    elif data == "msg_all":
        await event.answer("💎 V Makes Premium Font Engine Loaded!", alert=False)
    elif data == "msg_change":
        await event.answer("👑 Sᴇɴᴅ ᴀ ɴᴇᴡ ᴛext message ᴛᴏ ᴄʜᴀɴɢᴇ ɪɴsᴛᴀɴᴛʟʏ!", alert=True)
    elif data == "page":
        await event.answer("💎 Uᴘɢʀᴀᴅᴇ ᴛᴏ VIP Pʟᴀɴ ᴛᴏ ᴜɴʟᴏᴄᴋ ᴀʟʟ ᴘᴀɢᴇs!", alert=True)

# ==========================================================================
# 🏁 ENGINE RUN
# ==========================================================================
if __name__ == '__main__':
    print("🌐 Starting Keep-Alive Web Server...")
    Thread(target=run_web_server, daemon=True).start()

    print("👑 VIP Premium Fonts Layout Engine Connected!")
    bot.start(bot_token=BOT_TOKEN)
    bot.run_until_disconnected()
    
