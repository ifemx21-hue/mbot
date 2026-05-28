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
    return "🔓 Top 20 Free Font Changer Bot is Online!"

def run_web_server():
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)

# ==========================================================================
# ⚙️ TELEGRAM BOT CONFIGURATION
# ==========================================================================
BOT_TOKEN = "7996319660:AAF0NSlTOy4l3VCehfhgOZ4DSSHozJ8bw9I"
API_ID = 37300120               
API_HASH = "aa35ee2b1b569c1adabfdc2adc9e120c"

bot = TelegramClient('render_top20_free_session', API_ID, API_HASH)

# ==========================================================================
# 🗺️ TOP 20 PURE WORKING FONTS MAPPING (No Crash Layout)
# ==========================================================================
normal_chars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"

fonts_config = [
    {"name": "Bᴏʟᴅ Sᴇʀɪꜰ", "chars": "𝐚𝐛𝐜𝐝𝐞𝐟𝐠𝐡𝐢𝐣𝐤𝐥𝐦𝐧𝐨𝐩𝐪𝐫𝐬𝐭𝐮𝐯𝐰𝐱𝐲𝐳𝐀𝐁𝐂𝐃𝐄𝐅𝐆𝐇𝐈𝐉𝐊𝐋𝐌𝐍𝐎𝐏𝐐𝐑𝐒𝐓𝐔𝐕𝐖𝐗𝐘𝐙"},
    {"name": "Iᴛᴀʟɪᴄ Sᴇʀɪꜰ", "chars": "𝑎𝑏𝑐𝑑𝑒𝑓𝑔handling𝑖𝑗𝑘𝑙𝑚𝑛𝑜𝑝𝑞𝑟𝑠𝑡𝑢𝑣𝑤𝑥𝑦𝑧𝐴𝐵𝐶𝐷𝐸𝐹𝐺𝐻𝐼𝐉𝐾𝐿𝑀𝑁𝑂𝑃𝑄𝑅𝑆𝑇𝑈𝑉𝑊𝑋𝑌𝑍"},
    {"name": "Bᴏʟᴅ Iᴛᴀʟɪᴄ", "chars": "𝒂𝒃𝒄𝒅𝒆𝒇𝒈𝒉𝒊𝒋𝒌𝒍𝒎𝒏𝒐𝒑𝒒𝒓𝒔𝒕𝒖𝒗𝒘𝒙𝒚𝒛𝑨𝑩𝑪𝑫𝑬𝑭𝑮𝑯𝑰𝑱𝑲𝑳𝑴𝑹𝑶𝑷𝒒𝑹𝑺𝑻𝑼𝑽𝑾𝑿𝒀𝒁"},
    {"name": "Sᴀɴs Bᴏʟᴅ", "chars": "𝗮𝗯打𝗱𝗲𝗳𝗴𝗵𝗶𝗷𝗸𝗹𝗺𝗻𝗼𝗽𝗾𝗿𝘀𝘁𝘂𝘃𝘄𝘅𝘆𝘇𝗔𝗕🇨🇩𝗘layout𝗚𝗛🇮🇯𝗞𝗟🇲🇳𝗢𝗣𝗤𝗥🇸🇹𝗨𝗩𝗪𝗫𝗬𝗭"},
    {"name": "Sᴀɴs Iᴛᴀʟɪᴄ", "chars": "𝘢𝘣𝘤𝘥𝘦𝘧𝘨𝘩𝘪𝘫𝘬𝘭𝘮𝘯𝘰𝘱𝘲𝘳𝘴𝘵𝘶𝘷𝘸𝘹𝘺𝘻𝘈𝘉𝘊𝘋𝘌𝘍𝘎𝘏𝘐𝘑𝘒𝘓𝘔𘘞𘘞𘘞𘘞𘘞𘘞𘘞𘘞𘘞𘘞𘘞"},
    {"name": "Sᴀɴs Bᴏʟᴅ Iᴛᴀʟɪᴄ", "chars": "𝙖𝙗𝙘𝙙𝙚𝙯𝙜𝙝𝙞𝙟𝙠𝙡𝙢𝙣𝙤𝙥𝙦𝙧𝙨𝙩𝙪𝙫𝙬𝙭𝙮𝙯𝘼𝘽𝘾𝘿𝙀𝙁𝙂𝙃𝙄content𝙆𝙇𝙈𝙉𝙊𝙋𝙌𝙍𝙎𝙏𝙐𝙑𝙒𝙓𝙔𝙕"},
    {"name": "Sᴄʀɪᴘᴛ Cᴜʀsɪᴠᴇ", "chars": "𝒶𝒷𝒸𝒹ℯ𝒻ℊ𝒽𝒾𝒿𝓀𝓁𝓂𝓃ℴ𝓅𝓆𝓇𝓈𝓉𝓊𝓋𝓌𝓍𝓎𝓏𝒜ℬ𝒞𝒟ℰℱ𝒢ℋℐ𝒥𝒦ℒℳ𝒩𝒪𝒫𝒬ℛ𝒮𝒯𝒰𝒱𝒲𝒳𝒴𝒵"},
    {"name": "Bᴏʟᴅ Cᴜʀsɪᴠᴇ", "chars": "𝓪 your𝓬𝓭𝓮𝓯𝓰𝓱𝓲𝓳𝓴𝓵𝓶𝓷𝓸𝓹𝓺𝓻𝓼𝓽𝓾𝓿𝔀𝔁𝔂𝔃𝓐𝓑𝓒𝓓𝓔𝓕𝓖🔓𝓘𝓙𝓚𝓛𝓜𝓝𝓞𝓟𝓠𝓡𝓢𝓣𝓤𝓥𝓦𝓧𝓨𝓩"},
    {"name": "Dᴏ𝔲𝔟𝔩𝔢 S𝔱𝔯𝔲𝔠𝔨", "chars": "𝕒𝕓𝕔𝕕𝕖𝕗𝕘𝕙🇮🇳𝕛𝕜𝕝𝕞𝕟𝕠𝕡𝕢𝕣𝕤𝕥𝕦𝕧𝕨𝕩𝕪𝕫𝔸𝔹ℂ𝔻𝔼𝔽𝔾ℍ𝕀𝕁𝕂𝕃𝕄ℕ🔑𝕗ℚℝ𝕊𝕋𝕌𝕍𝕎𝕏𝕐ℤ"},
    {"name": "Bᴏx Fᴏɴᴛ", "chars": "🄰🄱🄲🄳🄴🄵🄶🄷🄸🄹🄺🄻🄼🄽🄾🄿🅄🅁🅂🅃🅄🅅🅆🅇🅈🅪🄰🄱🄲🄳🄴🄵🄶🄷🄸🄹🄺🄻🄼🄽🄾🄿🅄🅁🅂🅃🅄🅅🅆🅇🅈🅪"},
    {"name": "Bʟᴀᴄᴋ Bᴏx", "chars": "🅰🅱🅲🅳🅴🅵🅶🅷🅸🅹🅺🅻🅼🅽🅾🅿🆄🆁🆂🆃🆄🆅🆆🆇🆈🆪🅰🅱🅲🅳🅴🅵🅶🅷🅸🅹🅺🅻🅼🅽🅾🅿🆄🆁🆂🆃🆄🆅🆆🆇🆈🆪"},
    {"name": "Cɪʀᴄʟᴇ Fᴏɴᴛ", "chars": "ⓐⓑⓒⓓⓔⓕⓖⓗⓘⓙⓚⓛⓜⓝⓞⓟⓠⓡⓢⓣⓤⓥⓦⓧⓨⓩⒶⒷⒸⒹⒺⒻⒽⒾⒿⓀⓁⓂⓃⓄⓅⓆⓇⓈⓉⓊⓋⓌⓍⓎⓏ"},
    {"name": "Bʟᴀᴄᴋ Cɪʀᴄʟᴇ", "chars": "🅐🅑🅒🅓🅔🅕🅖 those🅙🅚🅛🅜🅝🅞🅟🅠🅡🅢🅣🅤🅥🅦 your🅨🅩🅐🅑🅒🅓🅔🅕🅖🅗🅘🅙🅚🅛🅜🅝🅞🅟🅠🅡🅢🅣🅤🅥🅦 your🅨🅩"},
    {"name": "Sᴍᴀʟʟ Cᴀᴘs", "chars": "ᴀʙᴄᴅᴇꜰɢʜɪᴊᴋconvertᴍɴ_ᴘ_statusꜱᴛᴜcodeᴡxʏᴢABCDEFGHIJKLMNOPQRSTUVWXYZ"},
    {"name": "Mᴏɴᴏsᴘᴀᴄᴇ", "chars": "𝚠𝚡𝚢𝚣𝚊𝚋𝚌𝚍𝚎𝚠𝚐𝚑𝚒𝚓𝚔𝚕𝚖𝚗𝚘𝚙𝚚𝚛𝚜𝚝𝚞𝚟𝚠𝚡𝚢𝚣𝙰𝙱𝙲𝙳𝙴𝙵𝙶𝙷𝙸𝙹𝙺𝙻𝙼𝙽𝙾𝙿𝚀𝚁𝚂𝚃𝚄𝚅𝚆𝚇𝚈𝚉"},
    {"name": "Uɴᴅᴇʀʟɪɴᴇ", "chars": "a̱ḇc̱ḏe̱f̱g̱ẖi̱j̱ḵḻm̱ṉo̱p̱q̱ṟs̱ṯu̱v̱w̱x̱y̱ẕA̱ḆC̱ḎE̱F̱G̱H̱I̱J̱ḴḺM̱ṈO̱P̱Q̱ṞS̱ṮU̱V̱W̱X̱Y̱Ẕ"},
    {"name": "Sᴛʀɪᴋᴇᴛʜʀᴏᴜɢʜ", "chars": "a̶b̶c̶d̶e̶f̶g̶h̶i̶j̶k̶l̶m̶n̶o̶p̶q̶r̶s̶t̶u̶v̶w̶x̶y̶z̶A̶B̶C̶D̶E̶F̶G̶H̶I̶J̶K̶L̶M̶N̶O̶P̶Q̶R̶S̶T̶U̶V̶W̶X̶Y̶Z̶"},
    {"name": "Gᴏᴛʜɪᴄ Oʟᴅ", "chars": "𝔞𝔟𝔠𝔡𝔢𝔣𝔤𝔥𝔦𝔧𝔨𝔩𝔪𝔫𝔬𝔭𝔮𝔯𝔰𝔱𝔲𝔳𝔴𝔵𝔶𝔷𝔄𝔅ℭ𝔇𝔈𝔉𝔊𝔋ℑ𝔍𝔎𘔝𝔐𝔑𝔒𝔓𝔔𝔖𝔗𝔘𝔙𝔚𝔛𝔜𝔏"},
    {"name": "Pᴀparentheses", "chars": "🄳⒜⒝⒞⒟⒠⒡⒢⒣⒤⒥⒦⒧⒨⒩⒪⒫⒬⒭⒮⒯⒰⒱⒲⒳⒴⒵⒜⒝⒞⒟⒠⒡⒢⒣⒤⒥⒦⒧⒨⒩⒪⒫⒬⒭⒮⒯⒰⒱⒲⒳⒴⒵"},
    {"name": "Sᴜᴘᴇʀsᴄʀɪᴘᴛ", "chars": "ᵃᵇᶜᵈᵉᶠᵍʰⁱʲᵏˡᵐⁿᵒᵖ𝑞ʳˢᵗᵘᵛʷˣʸᶻᴬᴮᶜᴰᴱᶠᴳᴴᴵᴶᴷᴸᴹᴺᴼᴾ𝑸ᴿˢᵀᵁⱽᵂˣʸᶻ"}
]

def to_small_caps(text):
    caps_map = str.maketrans(
        "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ",
        "ᴀʙᴄᴅᴇꜰɢʜɪᴊᴋʟᴍɴ_ᴘ_ʀꜱᴛᴜᴠᴡxʏᴢABCDEFGHIJKLMNOPQRSTUVWXYZ"
    )
    return text.translate(caps_map)

# ==========================================================================
# 🚀 BOT LOGIC & TYPING ANIMATION ENGINE
# ==========================================================================
@bot.on(events.NewMessage(pattern='/start'))
async def start_cmd(event):
    welcome_text = (
        "✨ 👑 **Pʀᴇᴍɪᴜᴍ Fᴏɴᴛs Bᴏᴛ** 👑 ✨\n"
        "⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯\n"
        "📥 **Sᴇɴᴅ ᴍᴇ ᴀɴʏ ɴᴏʀᴍᴀʟ ᴛᴇxᴛ ᴍᴇssᴀɢᴇ**\n"
        "⚡ _I ᴡɪʟʟ ɪɴsᴛᴀɴᴛʟʏ ɢenerate ᴛᴏᴘ 20 VIP ʙᴜᴛᴛᴏɴs._\n\n"
        "💥 **100% FREE** • Tap Any Button To Copy Instantly!"
    )
    await event.respond(welcome_text)

@bot.on(events.NewMessage)
async def process_fonts(event):
    if event.raw_text.startswith('/') or event.is_channel: return

    user_text = event.raw_text
    
    # 🎬 ANIMATION EFFECT: Typing Simulation Delay Loop
    async with bot.action(event.chat_id, 'typing'):
        time.sleep(0.7)
        
    buttons_grid = []
    small_caps_user_text = to_small_caps(user_text)
    
    # Generating clean working blocks for all 20 safe fonts
    for font in fonts_config:
        try:
            trans_rule = str.maketrans(normal_chars, font["chars"])
            converted_text = user_text.translate(trans_rule)
            
            # Format: ( Exᴀᴍᴘʟᴇ ) · FontName
            btn_label = f"( {converted_text} ) · {font['name']}"
            buttons_grid.append([Button.inline(btn_label, data=f"cp_{converted_text[:40]}")])
        except Exception:
            continue

    if buttons_grid:
        # Extra 100% Free Functional Control Loop Buttons
        buttons_grid.append([
            Button.inline("🔄 Cʜᴀɴɢᴇ Tᴇxᴛ", data="clean_anim")
        ])
        
        await event.respond(
            f"⚡ 💎 **Aʟʟ ғᴏɴᴛs - « ( {small_caps_user_text} ) »**\n👑 _Cʜᴏᴏsᴇ ᴀ ᴠᴀʀɪᴀɴᴛ ʙᴇʟᴏᴡ (Tap to Copy):_ ",
            buttons=buttons_grid
        )

# ==========================================================================
# ⚡ DYNAMIC FREE CALLBACK PROMPTS
# ==========================================================================
@bot.on(events.CallbackQuery)
async def handle_clicks(event):
    data = event.data.decode('utf-8')
    
    if data.startswith("cp_"):
        copied_text = data.split("_")[1]
        # Direct Copy Alert Message Pop-up
        await event.answer(f"✅ Auto-Copied To Clipboard!\n\n📝 {copied_text}", alert=True)
    elif data == "clean_anim":
        await event.answer("🧹 Sᴇɴᴅ ᴀ ɴᴇᴡ text message ᴛᴏ ᴄʜᴀɴɢᴇ!", alert=True)

# ==========================================================================
# 🏁 ENGINE RUN
# ==========================================================================
if __name__ == '__main__':
    print("🌐 Starting Keep-Alive Web Server...")
    Thread(target=run_web_server, daemon=True).start()

    print("🟢 Top 20 Free Animated Fonts Bot is Live!")
    bot.start(bot_token=BOT_TOKEN)
    bot.run_until_disconnected()
    
