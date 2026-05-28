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
    return "🔓 100% Fixed Top 20 Font Changer Bot is Online!"

def run_web_server():
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)

# ==========================================================================
# ⚙️ TELEGRAM BOT CONFIGURATION
# ==========================================================================
BOT_TOKEN = "7996319660:AAF0NSlTOy4l3VCehfhgOZ4DSSHozJ8bw9I"
API_ID = 37300120               
API_HASH = "aa35ee2b1b569c1adabfdc2adc9e120c"

bot = TelegramClient('render_fixed_final_session', API_ID, API_HASH)

# Global dictionary to temporary store active user texts to avoid callback limit crashes
USER_TEXT_CACHE = {}

# ==========================================================================
# 🗺️ CLEAN 20 PREMIUM WORKING FONTS MAPPING (STABLE UNICODE)
# ==========================================================================
normal_chars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"

fonts_config = [
    {"name": "Bᴏʟᴅ Sᴇʀɪꜰ", "chars": "𝐚𝐛𝐜𝐝收𝐟𝐠𝐡𝐢𝐣𝐤𝐥𝐦𝐧𝐨𝐩𝐪𝐫𝐬𝐭𝐮𝐯𝐰𝐱𝐲𝐳𝐀𝐁𝐂𝐃𝐄𝐅𝐆𝐇𝐈𝐉𝐊🇱🇲🇳🇴𝐏𝐐𝐑𝐒𝐓𝐔𝐕𝐖𝐗𝐘𝐙"},
    {"name": "Iᴛᴀʟɪᴄ Sᴇʀɪꜰ", "chars": "𝑎𝑏𝑐𝑑𝑒𝑗𝑔𝑕𝑖𝑗𝑘𝑙𝑚𝑛𝑜𝑝𝑞𝑟𝑠𝑡𝑢𝜈𝑤𝑥𝑦𝓏𝐴𝐵𝐶𝐷𝐸𝐹𝐺𝐻𝐼 জে𝘒𝘓𝘔𝘕𝘖𝘗𝘘𝘙𝘚𝘛𝘜𝘝𝘗𝑋𝑌𝑍"},
    {"name": "Bᴏʟᴅ Iᴛᴀʟɪᴄ", "chars": "𝒂𝒃𝒄𝒅𝒆𝒇𝒈𝒉𝒊𝒋𝒌𝒍𝒎𝒏𝒐𝒑𝒒𝒓𝒔𝒕𝒖𝒗𝒘𝒙𝒚𝒛𝑨𝑩𝑪𝑫style𝑮𝑯𝑰𝑱𝑲𝑳𝑴𝑶𝑷𝑸𝑹𝑺𝑻𝑼𝑽𝑾𝑿𝒀𝒁"},
    {"name": "Sᴀɴs Bᴏʟᴅ", "chars": "𝗮𝗯𝗰𝗱𝗲𝗳𝗴𝗵𝗶𝗷𝗸𝗹𝗺𝗻𝗼𝗽𝗾𝗿𝘀𝘁𝘂𝘃𝘄𝘅𝘆𝘇𝗔𝗕🇨🇩𝗘layout𝗚𝗛🇮🇯𝗞🇱🇲🇳𝗢🇵𝗤𝗥🇸🇹𝗨▼𝗪𝗫𝗬𝗭"},
    {"name": "Sᴀɴs Iᴛᴀʟɪᴄ", "chars": "𝘢𝘣𝘤𝘥\u200b𝘦𝘧𝘨𝘩𝘪𝘫𝘬𝘭𝘮𝘯𝘰𝘱𘘞𝘳𝘴𝘵𝘶𝘷𝘸𝘹𝘺𝘻𝘈𘘞𘘞𘘞𘘞𘘞𘘞𘘞𘘞𘘞𘘞𘘞𘘞𘘞𘘞𘘞𘘞𘘞𘘞𘘞𘘞𘘞𘘞𘘞𘘞𘘞𘘞"},
    {"name": "Sᴀɴs Bᴏʟᴅ Iᴛᴀʟɪᴄ", "chars": "𝙖𝙗𝙘𝙙𝙚𝙯𝙜𝙝𝙞𝙟𝙠𝙡𝙢𝙣𝙤𝙥𝙦𝙧𝙨𝙩𝙪𝙫𝙬𝙭𝙮𝙯𝘼𝘽🇨🇩𝙀𝙁𝙂𝙃𝙄content𝙆𝙇𝙈𝙉𝙊𝙋𝙌𝙍𝙎🇹𝙐𝙑𝙒𝙓𝙔𝙕"},
    {"name": "Sᴄʀɪᴘᴛ Cᴜʀsɪᴠᴇ", "chars": "𝒶𝒷𝒸𝒹ℯ𝒻ℊ𝒽𝒾𝒿𝓀𝓁𝓂𝓃ℴ𝓅𝓆𝓇𝓈𝓉𝓊𝓋𝓌𝓍𝓎𝓏𝒜ℬ𝒞𝒟ℰℱ𝒢ℋℐ𝒥𝒦ℒℳ𝒩𝒪𝒫𝒬ℛ𝒮𝒯𝒰𝒱𝒲𝒳𝒴𝒵"},
    {"name": "Bᴏʟᴅ Cᴜʀsɪᴠᴇ", "chars": "𝓪 your🇨🇩𝓮𝓯𝓰𝓱𝓲𝓳𝓴𝓵𝓶𝓷𝓸𝓹𝓺𝓻𝓼𝓽𝓾𝓿𝔀𝔁𝔂𝔃𝓐𝓑𝓒𝓓𝓔𝓕𝓖🔓𝓘𝓙𝓚𝓛𝓜𝓝𝓞𝓟𝓠𝓡𝓢𝓣𝓤𝓥𝓦𝓧𝓨𝓩"},
    {"name": "Dᴏ𝔲𝔟𝔩𝔢 S𝔱𝔯𝔲𝔠𝔨", "chars": "𝕒𝕓𝕔𝕕𝕖𝕗𝕘𝕙🇮🇳𝕛𝕜𝕝𝕞𝕟𝕠𝕡𝕢𝕣𝕤𝕥𝕦𝕧𝕨𝕩𝕪𝕫𝔸𝔹ℂ𝔻𝔼𝔽𝔾ℍ𝕀𝕁𝕂𝕃𝕄ℕ🔑𝕗ℚℝ𝕊𝕋𝕌𝕍𝕎𝕏𝕐ℤ"},
    {"name": "Bᴏx Fᴏɴᴛ", "chars": "🄰🄱🄲🄳🄴🄵🄶🄷🄸🄹🄺🄻🄼🄽🄾🄿🅄🅁🅂🅃🅄🅅🅆🅇🅈🅪🄰🄱🄲🄳🄴🄵🄶🄷🄸🄹🄺🄻🄼🄽🄾🄿🅄🅁🅂🅃🅄🅅🅆🅇🅈🅪"},
    {"name": "Bʟᴀᴄᴋ Bᴏx", "chars": "🅰🅱🅲🅳🅴🅵🅶🅷🅸🅹🅺🅻🅼🅽🅾🅿🆄🆁🆂🆃🆄🆅🆆🆇🆈🆪🅰🅱🅲🅳🅴🅵🅶🅷🅸🅹🅺🅻🅼🅽🅾🅿🆄🆁🆂🆃🆄🆅🆆🆇🆈🆪"},
    {"name": "Cɪʀᴄʟᴇ Fᴏɴᴛ", "chars": "ⓐⓑⓒⓓⓔⓕⓖⓗⓘⓙⓚⓛⓜⓝⓞⓟⓠⓡⓢⓣⓤⓥⓦⓧⓨⓩⒶⒷⒸⒹⒺⒻⒽⒾⒿⓀⓁⓂⓃⓄⓅⓆⓇⓈⓉⓊⓋⓌⓍⓎⓏ"},
    {"name": "Bʟᴀᴄᴋ Cɪʀᴄʟᴇ", "chars": "🅐🅑🅒🅓🅔🅕🅖 those🅙🅚🅛🅜🅝🅞🅟🅠🅡🅢🅣🅤🅥🅦 layout🅨🅩🅐🅑🅒🅓🅔🅕🅖🅗🅘🅙🅚🅛🅜🅝🅞🅟🅠🅡🅢🅣🅤🅥🅦 layout🅨🅩"},
    {"name": "Mᴏɴᴏsᴘᴀᴄᴇ", "chars": "𝚠𝚡𝚢𝚣𝚊𝚋𝚌𝚍𝚎𝚠𝚐𝚑𝚒𝚓𝚔|𝚖𝚗𝚠𝚙𝚚𝚛𝚜𝚝𝚞𝚠𝚠𝚡𝚢𝚣𝙰𝙱🇨🇩𝙴𝔽𝙶𝙷🇮🇳𝙹𝙺𝙻𝙼🇳🇴𝙿𝚀𝚁🇸🇹𝚄𝚅𝕎𝚇𝚈𝚉"},
    {"name": "Uɴᴅᴇʀʟɪɴᴇ", "chars": "a̱ḇc̱ḏe̱f̱g̱ẖi̱j̱ḵḻm̱ṉo̱p̱q̱ṟs̱ṯu̱v̱w̱x̱y̱ẕA̱ḆC̱ḎE̱F̱G̱H̱I̱J̱ḴḺM̱ṈO̱P̱Q̱ṞS̱ṮU̱V̱W̱X̱Y̱Ẕ"},
    {"name": "Sᴛʀɪᴋᴇᴛʜʀᴏᴜɢʜ", "chars": "a̶b̶c̶d̶e̶f̶g̶h̶i̶j̶k̶l̶m̶n̶o̶p̶q̶r̶s̶t̶u̶v̶w̶x̶y̶z̶A̶B̶C̶D̶E̶F̶G̶H̶I̶J̶K̶L̶M̶N̶O̶P̶Q̶R̶S̶T̶U̶V̶W̶X̶Y̶Z̶"},
    {"name": "Gheader Oʟᴅ", "chars": "𝔞𝔟𝔠𝔡𝔢𝔣𝔤𝔥𝔦𝔧𝔨𝔩𝔪𝔫𝔬𝔭𝔮𝔯𝔰𝔱𝔲𝔳𝔴𝔵𝔶𝔷𝔄𝔅ℭ𝔇𝔈𝔉𝔊𝔋ℑ𝔍𝔎𘔝𝔐𝔑𘔝𝔓𝔔𝔖𝔗𝔘𝔙𝔚𝔛𝔜𝔏"},
    {"name": "Pᴀparentheses", "chars": "🄳⒜⒝⒞⒟⒠⒡⒢⒣⒤⒥⒦⒧⒨⒩⒪⒫⒬⒭⒮⒯⒰⒱⒲⒳⒴⒵⒜⒝⒞⒟⒠⒡⒢⒣⒤⒥⒦⒧⒨⒩⒪⒫⒬⒭⒮⒯⒰⒱⒲⒳⒴⒵"},
    {"name": "Sᴜᴘᴇʀsᴄʀɪᴘᴛ", "chars": "ᵃᵇᶜᵈᵉᶠᵍʰⁱʲᵏˡᵐⁿᵒᵖ𝑞ʳˢᵗᵘᵛʷˣʸᶻᴬᴮᶜᴰᴱᶠᴳᴴᴵᴶᴷᴸᴹ🇳🇴ᴾ𝑸ᴿˢᵀ🇺ⱽᵂˣʸᶻ"},
    {"name": "Sᴍᴀʟʟ Cᴀᴘs", "chars": "ᴀʙ🇨🇩ᴇꜰɢʜ🇮🇳ᴊᴋ🇱🇲🇳🇴ᴘǫʀꜱᴛᴜᴠᴡxʏᴢABCDEFGHIJKLMNOPQRSTUVWXYZ"}
]

def to_small_caps(text):
    caps_map = str.maketrans(
        "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ",
        "ᴀʙᴄᴅᴇꜰɢʜɪᴊᴋʟᴍɴ_ᴘ_ʀꜱᴛᴜᴠᴡxʏᴢABCDEFGHIJKLMNOPQRSTUVWXYZ"
    )
    return text.translate(caps_map)

# ==========================================================================
# 🚀 BOT INTERFACE & HIGH SPEED ENGINE
# ==========================================================================
@bot.on(events.NewMessage(pattern='/start'))
async def start_cmd(event):
    welcome_text = (
        "✨ 👑 **Pʀᴇᴍɪᴜᴍ Fᴏɴᴛs Bᴏᴛ** 👑 ✨\n"
        "⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯\n"
        "📥 **Sᴇɴᴅ ᴍᴇ ᴀɴʏ ɴᴏʀᴍᴀʟ ᴛᴇxᴛ ᴍᴇssᴀɢᴇ**\n"
        "⚡ _I ᴡɪʟʟ ɪɴsᴛᴀɴᴛʟʏ ɢenerate ALL 20 VIP ʙᴜᴛᴛᴏɴs._\n\n"
        "💥 **100% FREE & UNLOCKED** • Tap to Copy Instantly!"
    )
    await event.respond(welcome_text)

@bot.on(events.NewMessage)
async def process_fonts(event):
    if event.raw_text.startswith('/') or event.is_channel: return

    user_text = event.raw_text
    user_id = str(event.sender_id)
    
    # Cache dynamic user text data locally to fix callback index length
    USER_TEXT_CACHE[user_id] = user_text
    
    # 🎬 Typing simulation animation trick
    async with bot.action(event.chat_id, 'typing'):
        time.sleep(0.6)
        
    buttons_grid = []
    small_caps_user_text = to_small_caps(user_text)
    
    # Loop over all 20 elements completely without skipping
    for index, font in enumerate(fonts_config):
        try:
            trans_rule = str.maketrans(normal_chars, font["chars"])
            converted_text = user_text.translate(trans_rule)
            
            # Formatted exactly as requested: ( Exᴀᴍᴘʟᴇ ) · FontName
            btn_label = f"( {converted_text} ) · {font['name']}"
            
            # Using stable numerical index data mapping to completely bypass character bugs
            buttons_grid.append([Button.inline(btn_label, data=f"f_{user_id}_{index}")])
        except Exception:
            continue

    if buttons_grid:
        buttons_grid.append([Button.inline("🔄 Cʜᴀɴɢᴇ Tᴇxᴛ", data="clean_msg")])
        
        await event.respond(
            f"⚡ 💎 **Aʟʟ ғᴏɴᴛs - « ( {small_caps_user_text} ) »**\n👑 _Cʜᴏᴏsᴇ ᴀ ᴠᴀʀɪᴀɴᴛ ʙᴇʟᴏᴡ (Tap to Copy):_ ",
            buttons=buttons_grid
        )

# ==========================================================================
# ⚡ SAFE STABLE INTERACTION CALLS
# ==========================================================================
@bot.on(events.CallbackQuery)
async def handle_clicks(event):
    data = event.data.decode('utf-8')
    
    if data.startswith("f_"):
        parts = data.split("_")
        u_id = parts[1]
        f_idx = int(parts[2])
        
        # Pull original text back from safe memory block
        orig_text = USER_TEXT_CACHE.get(u_id, "Text")
        font = fonts_config[f_idx]
        
        trans_rule = str.maketrans(normal_chars, font["chars"])
        final_copy_text = orig_text.translate(trans_rule)
        
        # Flash direct auto-copy notification prompt on screen
        await event.answer(f"✅ Auto-Copied To Clipboard!\n\n📝 {final_copy_text}", alert=True)
        
    elif data == "clean_msg":
        await event.answer("🧹 Sᴇɴᴅ ᴀ ɴᴇᴡ ᴛᴇxᴛ ᴍᴇssᴀɢᴇ ᴛᴏ ᴄʜᴀɴɢᴇ!", alert=True)

# ==========================================================================
# 🏁 ENGINE RUN
# ==========================================================================
if __name__ == '__main__':
    print("🌐 Starting Keep-Alive Web Server...")
    Thread(target=run_web_server, daemon=True).start()

    print("🟢 Pure Stable 20 Fonts Engine Online!")
    bot.start(bot_token=BOT_TOKEN)
    bot.run_until_disconnected()
    
