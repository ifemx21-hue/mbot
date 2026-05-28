import os
import time
from threading import Thread
from flask import Flask
from telethon import TelegramClient, events, Button

# ==========================================================================
# 🌐 WEB SERVER FOR RENDER (KEEP-ALIVE NODE)
# ==========================================================================
app = Flask(__name__)

@app.route('/')
def home():
    return "🔓 100% Free Font Changer Bot is Alive!"

def run_web_server():
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)

# ==========================================================================
# ⚙️ TELEGRAM BOT CONFIGURATION
# ==========================================================================
BOT_TOKEN = "7996319660:AAF0NSlTOy4l3VCehfhgOZ4DSSHozJ8bw9I"
API_ID = 37300120               
API_HASH = "aa35ee2b1b569c1adabfdc2adc9e120c"

bot = TelegramClient('render_font_free_animated_v1', API_ID, API_HASH)

# ==========================================================================
# 🗺️ ALIGNED FONTS DATABASE
# ==========================================================================
normal_chars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"

fonts_config = [
    {"name": "Bᴏʟᴅ", "chars": "𝒂𝒃𝒄𝒅𝒆𝒇𝒈𝒉𝒊𝒋𝒌𝒍𝒎𝒏𝒐𝒑𝒒𝒓𝒔𝒕𝒖𝒗𘘞𝒙𝒚𝒛𝑨\u200b𝑩𝑪𝑫𝑬𝑭𝑮𝑯𝑰𝑱𝑲𝑳𝑴𝑾𝑶𝑷𝑸𝑹𝑺𝑻𝑼𝑽𝑾𝑿𝒀𝒁"},
    {"name": "Iᴛᴀʟɪᴄ", "chars": "𝘢𝘣𝘤𝘥\u200b𝘦𝘿𝘨𝘩𝘪𝘫𝘹𝘭𝘮𝘯𝘰𝘱𝘲𝘳𝘴𝘵𝘶𝘷𝘸𝘹𝘺𝘻𝘈𘘞𘘞𘘞𘘞𘘞𘘞𘘞𘘞𘘞𘘞𘘞𘘞𘘞𘘞𘘞𘘞𘘞𘘞𘘞𘘞𘘞𘘞𘘞𘘞𘘞𘘞"},
    {"name": "Sᴀɴs Bᴏʟᴅ", "chars": "𝗮𝗯𝗰𝗱𝗲打𝗴𝗵𝗶𝗷𝗸𝗹𝗺𝗻𝗼𝗽𝗾𝗿𝘀𝒕𝘂▼𝘄𝗅𝘆𝘇𝗔𝗕🇨🇩𝗘𝗙𝗚𝗛𝗜𝗝𝗞𝗟𝗠🇳🇵𝗤𝗥🇸🇹𝗨▼𝗪𝗫𝗬𝗭"},
    {"name": "Gᴏᴛʜɪᴄ", "chars": "𝔞𝔟𝔠𝔡𝔢𝔣𝔤𝔥𝔦𝔧𝔨𝔩𝔪𝔫𝔬𝔭𝔮𝔯𝔰𝔱𝔲𝔳𝔴𝔵𝔶𝔷𝔄𝔅ℭ𝔇𝔈𝔉𝔊𝔋ℑ𝔍𝔎𘔝𝔐𝔑𝔒𝔓𝔔𝔖𝔗𝔘𝔙𝔚𝔛𝔜𝔏"},
    {"name": "Dᴏ𝔲𝔟𝔩𝔢 S𝔱𝔯𝔲𝔠𝔨", "chars": "𝕒𝕓𝕔𝕕𝕖𝕗𝕘𝕙𝕚𝕛𝕜𝕝𝕞𝕟𝕠𝕡𝕢𝕣𝕤𝕥𝕦𝕧𝕨𝕩𝕪𝕫𝔸𝔹ℂ𝔻𝔼𝔽𝔾ℍ𝕀𝕁𝕂𝕃𝕄ℕ🔑𝕗ℚℝ𝕊𝕋𝕌𝕍𝕎𝕏𝕐ℤ"},
    {"name": "Bᴏx Fᴏɴᴛ", "chars": "🄰🄱🄲🄳🄴🄵🄶🄷🄸🄹🄺🄻🄼🄽🄾🄿🅄🅁🅂🅃🅄🅅🅆🅇🅈🅪🄰🄱🄲🄳🄴🄵🄶🄷🄸🄹🄺🄻🄼🄽🄾🄿🅄🅁🅂🅃🅄🅅🅆🅇🅈🅪"}
]

def to_small_caps(text):
    caps_map = str.maketrans(
        "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ",
        "ᴀʙᴄᴅᴇꜰɢʜɪᴊᴋʟᴍɴ_ᴘ_ʀꜱᴛᴜᴠᴡxʏᴢABCDEFGHIJKLMNOPQRSTUVWXYZ"
    )
    return text.translate(caps_map)

# ==========================================================================
# 🚀 BOT LOGIC & ANIMATION ACTIONS
# ==========================================================================
@bot.on(events.NewMessage(pattern='/start'))
async def start_cmd(event):
    welcome_text = (
        "✨ 💫 **PʀEMiUM FᴏNTs BᴏT (FʀEE)** 💫 ✨\n"
        "⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯\n"
        "📥 **Sᴇɴᴅ ᴍᴇ ᴀɴʏ ɴᴏʀᴍᴀʟ ᴛᴇxᴛ ᴍᴇssᴀɢᴇ**\n"
        "⚡ _I ᴡɪʟʟ ɪɴsᴛᴀɴᴛʟʏ ᴄᴏɴᴠᴇʀᴛ ɪᴛ ɪɴᴛᴏ sᴛstyle ʙᴜᴛᴛᴏɴs ɢʀɪᴅ._\n\n"
        "🔥 **100% FREE** • No Limits • No Ads!"
    )
    await event.respond(welcome_text)

@bot.on(events.NewMessage)
async def process_fonts(event):
    if event.raw_text.startswith('/') or event.is_channel: return

    user_text = event.raw_text
    
    # 🎬 STEP 1: ANIMATION EFFECT - Show custom dynamic system typing delay
    async with bot.action(event.chat_id, 'typing'):
        time.sleep(0.8) # 0.8 seconds realistic simulation pause
        
    buttons_grid = []
    small_caps_user_text = to_small_caps(user_text)
    
    for font in fonts_config:
        try:
            trans_rule = str.maketrans(normal_chars, font["chars"])
            converted_text = user_text.translate(trans_rule)
            
            # Format requested by user: ( Exᴀᴍᴘʟᴇ ) · FontName
            btn_label = f"( {converted_text} ) · {font['name']}"
            buttons_grid.append([Button.inline(btn_label, data=f"cp_{converted_text[:40]}")])
        except Exception:
            continue

    if buttons_grid:
        # Fully un-locked free visual control panel buttons
        buttons_grid.append([
            Button.inline("🌟 ALL FONTS UNLOCKED", data="free_alert")
        ])
        buttons_grid.append([
            Button.inline("🔄 REFRESH LOOP", data="refresh_anim"), 
            Button.inline("✨ CLEAN TEXT", data="clean_anim")
        ])
        
        await event.respond(
            f"⚡ 💎 **Aʟʟ ғᴏɴᴛs - « ( {small_caps_user_text} ) »**\n👑 _Cʜᴏᴏsᴇ ʏᴏᴜʀ sᴛʏʟᴇ ʙᴇbᴏᴡ (Tap to Copy):_ ",
            buttons=buttons_grid
        )

# ==========================================================================
# ⚡ FREE DISPATCHER & BUTTON INTERACTION PROMPTS
# ==========================================================================
@bot.on(events.CallbackQuery)
async def handle_clicks(event):
    data = event.data.decode('utf-8')
    
    if data.startswith("cp_"):
        copied_text = data.split("_")[1]
        # Direct clean copy popup acknowledgment
        await event.answer(f"✅ Auto-Copied To Clipboard!\n\n📝 {copied_text}", alert=True)
        
    elif data == "free_alert":
        await event.answer("🎉 This bot is 100% Free Forever for Farru Bhai!", alert=True)
        
    elif data == "refresh_anim":
        # 🔄 Text replacement animation visual loop trick
        await event.answer("♻️ Reloading fonts layout map...", alert=False)
        await event.edit("⚙️ _Updating Engine Nodes..._")
        time.sleep(0.4)
        await event.edit("✨ _Generating Premium Layout..._")
        time.sleep(0.3)
        # Brings back original state
        await event.edit(buttons=event.reply_markup)
        
    elif data == "clean_anim":
        await event.answer("🧹 Layout buffer cleared!", alert=False)

# ==========================================================================
# 🏁 ENGINE RUN
# ==========================================================================
if __name__ == '__main__':
    print("🌐 Starting Keep-Alive Web Server...")
    Thread(target=run_web_server, daemon=True).start()

    print("🟢 100% Free Animated Fonts Bot Connected!")
    bot.start(bot_token=BOT_TOKEN)
    bot.run_until_disconnected()
    
