import os
import json
import threading
import time
import streamlit as st
from telethon import TelegramClient, events, Button

# ==========================================================================
# 🌐 STREAMLIT UI (RENDER KEEP-ALIVE ENGINE)
# ==========================================================================
st.set_page_config(page_title="MBOT SaaS Engine", page_icon="🔥", layout="centered")
st.title("🔥 MBOT (REACTION + VIEWS) SaaS Engine")
st.markdown("---")
st.success("🤖 Bot Status: Operational 24/7 Live 🟢")
st.info("This web page keeps your Render service active. Do not close if checking logs.")

# ==========================================================================
# ⚙️ CONFIGURATION & DATABASE
# ==========================================================================
BOT_TOKEN = "8933958981:AAGm3jbwzEWCywAyiyAkryfCnvWg4iDkywQ"
API_ID = 37300120               
API_HASH = "aa35ee2b1b569c1adabfdc2adc9e120c"

DB_FILE = "advanced_mbot_db.json"

def load_db():
    if os.path.exists(DB_FILE):
        try:
            with open(DB_FILE, "r") as f: return json.load(f)
        except: pass
    return {"users": {}, "projects": {}}

def save_db(data):
    with open(DB_FILE, "w") as f: json.dump(data, f, indent=4)

# Initialize Telethon Bot Client with a Fresh Active Session
bot = TelegramClient('mbot_render_fresh_final_v3', API_ID, API_HASH)

AVAILABLE_EMOJIS = ["❤️", "👍", "🔥", "🙏", "🎉", "🏆", "😍", "💯", "😭", "⚡"]

# ==========================================================================
# 🏠 MAIN MENU LAYOUT (Bade Buttons - Maximum 2 Per Row)
# ==========================================================================
def get_main_keyboard():
    return bot.build_reply_markup([
        [Button.text("➕ ADD AUTO REACTION PROJECT")],
        [Button.text("📁 MY PROJECTS"), Button.text("🎛️ MORE OPTIONS")],
        [Button.text("🌟 PLAN & BALANCE"), Button.text("💰 RECHARGE NOW")]
    ])

@bot.on(events.NewMessage(pattern='/start'))
async def start_cmd(event):
    uid = str(event.sender_id)
    name = event.sender.first_name or "User"
    
    db = load_db()
    if uid not in db["users"]:
        db["users"][uid] = {
            "name": name, "balance": 55, "spent": 180, 
            "plan": "FREE", "projects_count": 1, "state": ""
        }
        save_db(db)
        
    await event.respond(
        "🤖 **Multi Reactions & Views Bot**\n\n"
        "⚡ _Choose an option from the menu below to configure your automated channels._",
        buttons=get_main_keyboard()
    )

# ==========================================================================
# 🔄 HANDLING INTERFACE CLICKS
# ==========================================================================
@bot.on(events.NewMessage)
async def handle_menu_clicks(event):
    if event.is_channel: return
    uid = str(event.sender_id)
    text = event.raw_text
    db = load_db()
    
    if text == "➕ ADD AUTO REACTION PROJECT":
        user_projects = [p for p, d in db["projects"].items() if d.get("owner") == uid]
        if len(user_projects) >= db["users"].get(uid, {}).get("projects_count", 1):
            limit_txt = (
                "🚫 **Project Creation Limit Reached**\n\n"
                "Your current plan allows a maximum of 1 projects, and you have reached this limit.\n\n"
                "To create more projects:\n• Upgrade your plan for higher limits\n• Contact admin to increase your project quota"
            )
            await event.respond(limit_txt)
            return
            
        db["users"][uid]["state"] = "waiting_for_channel"
        save_db(db)
        await event.respond("📢 **Send your Telegram Channel Username or ID:**\n\n_Example: @FarruLootersOfficial_")

    elif text == "📁 MY PROJECTS":
        user_projects = [p for p, d in db["projects"].items() if d.get("owner") == uid]
        if not user_projects:
            await event.respond("❌ **Aapka koi active project nahi hai!**")
        else:
            txt = "📁 **YOUR ACTIVE PROJECTS**\n⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯\n"
            for i, p in enumerate(user_projects, 1):
                pd = db["projects"][p]
                txt += f"♦️ {i}. **{pd['title']}** (`{p}`)\n❤️ Rxn: {pd['rxn_count']} | {', '.join(pd['emojis'])}\n\n"
            
            inline_buttons = [[Button.inline(f"📁 {db['projects'][p]['title']}", data=f"manage_{p}")] for p in user_projects]
            await event.respond(txt + "⚡ _Tap a project name to view details._", buttons=inline_buttons)

    elif text == "🌟 PLAN & BALANCE":
        ud = db["users"].get(uid, {"plan": "FREE", "balance": 0, "spent": 0})
        dash_txt = (
            "🌟 **PLAN & BALANCE**\n"
            "⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯\n"
            f"🆓 **{ud['plan']}**\n_Valid till: ∞_\n\n"
            "❤️ **Reactions:** 30/post\n"
            "👁️ **Views:** 30/post\n\n"
            f"💎 **Credits:** {ud['balance']}\n"
            f"📊 **Spent:** {ud['spent']}\n"
            f"📁 **Projects:** {len([p for p, d in db['projects'].items() if d.get('owner') == uid])}"
        )
        await event.respond(dash_txt)

    elif text == "🎛️ MORE OPTIONS":
        more_buttons = [
            [Button.inline("❤️ REFER & EARN", data="refer"), Button.inline("🎁 DAILY GIFT", data="gift")],
            [Button.inline("🚀 INSTANT REACT", data="inst_react"), Button.inline("🤖 COOL BOTS", data="cool_bots")],
            [Button.inline("🔙 Back to Menu", data="main_menu")]
        ]
        await event.respond("⚙️ **Advanced Bot Controls & Options:**", buttons=more_buttons)

    elif db["users"].get(uid, {}).get("state") == "waiting_for_channel":
        ch_identifier = text.strip()
        db["users"][uid]["state"] = ""
        db["users"][uid]["temp_project_target"] = ch_identifier
        save_db(db)
        
        if "creation_flow" not in db["users"][uid]:
            db["users"][uid]["creation_flow"] = {"emojis": [], "rxn_count": 30, "dist": "Random", "speed": "Fast", "views": 30}
        save_db(db)
        
        await send_step_1_emojis(event, uid)

# ==========================================================================
# 📊 MULTI-STEP WIZARD ENGINE
# ==========================================================================

async def send_step_1_emojis(event, uid):
    db = load_db()
    selected = db["users"][uid]["creation_flow"]["emojis"]
    
    txt = f"📝 **Step 1 • Select Emojis**\n⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯\nChoose reactions for your posts.\n\n**Selected ({len(selected)}):** {', '.join(selected) if selected else 'None'}\n\n⭐ _Tap emojis to add/remove. Tap ✅ Done when finished._"
    
    grid = []
    row = []
    for em in AVAILABLE_EMOJIS:
        marker = "🟢 " if em in selected else "➕ "
        row.append(Button.inline(f"{marker}{em}", data=f"toggle_{em}"))
        if len(row) == 5:
            grid.append(row)
            row = []
    if row: grid.append(row)
    
    grid.append([Button.inline("✅ Done & Continue", data="step1_done")])
    
    if hasattr(event, 'click'):
        await event.edit(txt, buttons=grid)
    else:
        await event.respond(txt, buttons=grid)

async def send_step_2_quantity(event, uid):
    db = load_db()
    current = db["users"][uid]["creation_flow"]["rxn_count"]
    txt = f"🎈 **Step 2 • Total Reactions**\n⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯\nHow many reactions per post?\n\n👉 **Current Selection:** `{current} reactions`"
    
    buttons = [
        [Button.inline("🔹 10", data="q_10"), Button.inline("🔹 20", data="q_20"), Button.inline(f"🟢 {current}" if current==30 else "🔹 30", data="q_30")],
        [Button.inline("🔒 50", data="locked"), Button.inline("🔒 70", data="locked"), Button.inline("🔒 100", data="locked")],
        [Button.inline("⛩️ Custom Quantity ⛩️", data="custom_val")],
        [Button.inline("🔙 Back", data="back_to_step1"), Button.inline("🟢 Continue", data="step2_done")]
    ]
    await event.edit(txt, buttons=buttons)

async def send_step_3_distribution(event, uid):
    db = load_db()
    current = db["users"][uid]["creation_flow"]["dist"]
    txt = f"⚙️ **Step 3 • Distribution Type**\n⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯\nWhat pattern should the reactions follow?\n\n🎲 **Random** - Each emoji gets 7-8 reactions\n⚖️ **All Equally** - Each emoji gets exactly 7 reactions"
    
    buttons = [
        [Button.inline(f"🟢 🎲 Random" if current=="Random" else "🎲 Random", data="dist_Random")],
        [Button.inline(f"🟢 ⚖️ All Equally" if current=="Equally" else "⚖️ All Equally", data="dist_Equally")],
        [Button.inline("🔒 Advanced Customization", data="locked")],
        [Button.inline("🔙 Back", data="back_to_step2"), Button.inline("🟢 Continue", data="step3_done")]
    ]
    await event.edit(txt, buttons=buttons)

async def send_step_4_speed(event, uid):
    db = load_db()
    current = db["users"][uid]["creation_flow"]["speed"]
    txt = f"⚡ **STEP 4 • Choose Speed**\n⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯\nChoose delivery speed:\n\n👉 **Selected:** ⚡ {current} Delivery"
    
    buttons = [
        [Button.inline("🟢 Fast ⚡" if current=="Fast" else "Fast ⚡", data="spd_Fast"), Button.inline("Medium ⏱️", data="locked"), Button.inline("Slow 🐢", data="locked")],
        [Button.inline("🔙 Back", data="back_to_step3"), Button.inline("🟢 Continue", data="step4_done")]
    ]
    await event.edit(txt, buttons=buttons)

async def send_step_5_views(event, uid):
    db = load_db()
    current = db["users"][uid]["creation_flow"]["views"]
    txt = f"👁️ **STEP 5 • Views Configuration**\n⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯\nHow many views per post?\n\n👉 **Selected:** `{current} views (instant)`"
    
    buttons = [
        [Button.inline("0 Views", data="v_0"), Button.inline("10 Views", data="v_10"), Button.inline(f"🟢 30 Views" if current==30 else "30 Views", data="v_30")],
        [Button.inline("🔒 50", data="locked"), Button.inline("🔒 100", data="locked"), Button.inline("⚙️ CUSTOM", data="locked")],
        [Button.inline("🔙 Back", data="back_to_step4"), Button.inline("🟢 Continue", data="step5_done")]
    ]
    await event.edit(txt, buttons=buttons)

async def send_final_review(event, uid):
    db = load_db()
    flow = db["users"][uid]["creation_flow"]
    target = db["users"][uid]["temp_project_target"]
    
    txt = (
        "✨ **FINAL REVIEW** ✨\n"
        "⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯\n"
        f"📺 **Channel:** `Shubh Earning 💸` ({target})\n\n"
        "╭⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯\n"
        f" 😊 Emojis: {', '.join(flow['emojis']) if flow['emojis'] else '❤️, 🔥, 😁'}\n"
        f" 🎯 Mode: ALL\n"
        f" 🔴 Reactions: {flow['rxn_count']}\n"
        f" 👁️ Views: 👁️ {flow['views']} (⚡ instant)\n"
        f" Reaction Delivery: ⚡ Instant\n"
        f" ⚙️ Distribution: {flow['dist']}\n"
        " 🔀 Randomize: OFF\n"
        "╰⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯"
    )
    
    buttons = [
        [Button.inline("🟢 Save Changes & Start", data="save_project_final")],
        [Button.inline("🛠️ EDIT", data="back_to_step5"), Button.inline("❌ Cancel", data="main_menu")]
    ]
    await event.edit(txt, buttons=buttons)

# ==========================================================================
# 🛑 CALLBACK DISPATCHER
# ==========================================================================
@bot.on(events.CallbackQuery)
async def callback_handler(event):
    uid = str(event.sender_id)
    data = event.data.decode('utf-8')
    db = load_db()
    
    if data.startswith("toggle_"):
        emoji = data.split("_")[1]
        if emoji in db["users"][uid]["creation_flow"]["emojis"]:
            db["users"][uid]["creation_flow"]["emojis"].remove(emoji)
        else:
            db["users"][uid]["creation_flow"]["emojis"].append(emoji)
        save_db(db)
        await send_step_1_emojis(event, uid)
        
    elif data == "step1_done": await send_step_2_quantity(event, uid)
    elif data.startswith("q_"):
        db["users"][uid]["creation_flow"]["rxn_count"] = int(data.split("_")[1])
        save_db(db)
        await send_step_2_quantity(event, uid)
        
    elif data == "step2_done": await send_step_3_distribution(event, uid)
    elif data.startswith("dist_"):
        db["users"][uid]["creation_flow"]["dist"] = data.split("_")[1]
        save_db(db)
        await send_step_3_distribution(event, uid)
        
    elif data == "step3_done": await send_step_4_speed(event, uid)
    elif data.startswith("spd_"):
        db["users"][uid]["creation_flow"]["speed"] = data.split("_")[1]
        save_db(db)
        await send_step_4_speed(event, uid)
        
    elif data == "step4_done": await send_step_5_views(event, uid)
    elif data.startswith("v_"):
        db["users"][uid]["creation_flow"]["views"] = int(data.split("_")[1])
        save_db(db)
        await send_step_5_views(event, uid)
        
    elif data == "step5_done": await send_final_review(event, uid)
    
    elif data == "save_project_final":
        target = db["users"][uid]["temp_project_target"]
        flow = db["users"][uid]["creation_flow"]
        
        db["projects"][target] = {
            "owner": uid,
            "title": "Shubh Earning 💸",
            "emojis": flow["emojis"] if flow["emojis"] else ["❤️", "🔥"],
            "rxn_count": flow["rxn_count"],
            "views": flow["views"]
        }
        save_db(db)
        await event.edit("✅ **Project successfully saved and auto-system is live!**")
        
    elif data == "main_menu":
        await event.edit("🏠 **Main Menu Loaded.** Use keyboard buttons below to navigate.", buttons=None)
        
    elif data == "back_to_step1": await send_step_1_emojis(event, uid)
    elif data == "back_to_step2": await send_step_2_quantity(event, uid)
    elif data.startswith("back_to_step3"): await send_step_3_distribution(event, uid)
    elif data == "back_to_step4": await send_step_4_speed(event, uid)
    elif data.startswith("back_to_step5") or data == "back_to_step5": await send_step_5_views(event, uid)
    elif data == "locked": await event.answer("⚠️ Feature locked in free layout!", alert=True)

# ==========================================================================
# 🏁 AUTOMATIC THREAD EXECUTION FOR SERVER HOOKS (FIXED TYPO HERE)
# ==========================================================================
def start_telegram_bot():
    print("🚀 Starting Telethon Bot Engine with new Token...")
    try:
        bot.start(bot_token=BOT_TOKEN)
        bot.run_until_disconnected()
    except Exception as e:
        print(f"❌ Error starting bot: {e}")

if "bot_thread_started" not in st.session_state:
    st.session_state.bot_thread_started = True
    t = threading.Thread(target=start_telegram_bot, daemon=True)
    t.start()
    
