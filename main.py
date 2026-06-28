import telebot
from telebot import types

# ⚠️ သင့်ရဲ့ Bot Token ကို ဒီမှာ ထည့်ပါ
API_TOKEN = '8993842721:AAGxapD-bEP22dll8-nLy_0ThMUj1mTPmwc' 

# ⚠️ သင့်ရဲ့ ကိုယ်ပိုင် Account Chat ID ကို ဒီမှာ ပြောင်းထည့်ပေးပါ
ADMIN_CHAT_ID = 8902469958  

bot = telebot.TeleBot(API_TOKEN)

# User တစ်ယောက်ချင်းစီရဲ့ Order data ကို ယာယီသိမ်းထားဖို့ storage
user_orders = {}

# ငွေပေးချေမှုဆိုင်ရာ အချက်အလက် စာသား
PAYMENT_TEXT = (
    "💳 Payment Methods (ငွေပေးချေရန်)\n"
    "KPay\n"
    "• Account: 09 755 750 390\n"
    "• Name: Zin Myo Win\n\n"
    "WaveMoney\n"
    "• Account: 09 755 750 390\n"
    "• Name: Hay Man Saung\n\n"
    "⚠️ ငွေလွှဲပြီးလျှင် Screenshot (ပြေစာ) လေး ပြန်ပို့ပေးပါခင်ဗျာ။"
)

# 1. User က /start နှိပ်ရင် ပြသမယ့် စျေးနှုန်း List စာသား
@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    chat_id = message.chat.id
    user_orders[chat_id] = {"item": None, "game_id": None, "user_name": message.from_user.first_name}
    
    welcome_text = (
        "Mingalarpar khin Byar! 🙏✨ GameShop မှ ကြိုဆိုပါတယ်။\n\n"
        "PUBG UC နဲ့ MLBB Diamonds တွေကို ဈေးနှုန်းအသက်သာဆုံးနဲ့ အမြန်ဆုံး အကောင့်ထဲထည့်ပေးနေပါပြီ။\n\n"
        "🔥 PUBG Mobile: UC Top-up\n"
        "💎 Mobile Legends: Diamonds\n"
        "👉 Order တင်ဖို့အတွက်:\n\n"
        "Game ID (MLBB ဆိုရင် Zone ID ပါပြပေးပါ)\n"
        "ဝယ်ယူလိုတဲ့ နံပါတ်လေးကို Chat မှာ စာရေးပြီး ပို့ပေးပါနော်။\n\n"
        "[GameShop] - Gaming Top-up Price List 🇲🇲✨\n"
        "1. UC 60 = [ ] ks\n"
        "2. UC 325 = [ ] ks\n"
        "3. UC 660 = [ ] ks\n"
        "4. UC 1800 = [ ] ks\n"
        "5. UC 3850 = [ ] ks\n\n"
        "6. 86 Diamonds = [ ] ks\n"
        "7. 172 Diamonds = [ ] ks\n"
        "8. 257 Diamonds = [ ] ks\n"
        "9. 344 Diamonds = [ ] ks\n"
        "10. 706 Diamonds = [ ] ks\n"
        "11. Weekly Diamond Pass = [ ] ks\n\n"
        "💸 Payment: KPay / WaveMoney\n"
        "Order တင်ရန်အတွက် Game ID (MLBB အတွက် Zone ID အပါ) ကို Chat Box တွင် ပို့ပေးပါခင်ဗျာ။ 🙏"
    )
    
    msg = bot.send_message(chat_id, welcome_text)
    bot.register_next_step_handler(msg, process_item_step)

# 2. ဝယ်ယူမယ့် Item နံပါတ်ကို စစ်ဆေးတဲ့အဆင့်
def process_item_step(message):
    chat_id = message.chat.id
    user_choice = message.text.strip() if message.text else ""
    
    valid_items = [str(i) for i in range(1, 12)]
    if user_choice not in valid_items:
        msg = bot.send_message(chat_id, "⚠️ မမှန်ကန်သော နံပါတ်ဖြစ်နေပါသည်။ ကျေးဇူးပြု၍ စျေးနှုန်း List ထဲရှိ နံပါတ် (၁ မှ ၁၁) ထဲက တစ်ခုခုကို ပြန်ရိုက်ပေးပါဗျာ။")
        bot.register_next_step_handler(msg, process_item_step)
        return

    if chat_id not in user_orders:
        user_orders[chat_id] = {"item": None, "game_id": None, "user_name": message.from_user.first_name}
        
    user_orders[chat_id]["item"] = user_choice
    
    msg = bot.send_message(chat_id, "Order တင်ရန်အတွက် Game ID လေး ပို့ပေးပါခင်ဗျာ။")
    bot.register_next_step_handler(msg, process_game_id_step)

# 3. Game ID ဖတ်ပြီး MLBB ဟုတ်မဟုတ် စစ်ဆေးတဲ့အဆင့်
def process_game_id_step(message):
    chat_id = message.chat.id
    
    if chat_id not in user_orders:
        bot.send_message(chat_id, "⚠️ စက်ရှင်သက်တမ်းကုန်ဆုံးသွားပါပြီ။ /start ကိုနှိပ်ပြီး ပြန်စပေးပါဗျာ။")
        return
        
    game_id = message.text.strip() if message.text else ""
    user_orders[chat_id]["game_id"] = game_id
    selected_item = user_orders[chat_id]["item"]
    
    mlbb_items = ["6", "7", "8", "9", "10", "11"]
    
    if selected_item in mlbb_items:
        msg = bot.send_message(chat_id, "Zone ID လေးပါ ပို့ပေးပါနော်။")
        bot.register_next_step_handler(msg, process_zone_id_step)
    else:
        msg = bot.send_message(chat_id, PAYMENT_TEXT)
        bot.register_next_step_handler(msg, process_screenshot_step)

# 4. MLBB သမားတွေအတွက် Zone ID သိမ်းဆည်းပြီး Payment ပြသမယ့်အဆင့်
def process_zone_id_step(message):
    chat_id = message.chat.id
    
    if chat_id not in user_orders:
        bot.send_message(chat_id, "⚠️ စက်ရှင်သက်တမ်းကုန်ဆုံးသွားပါပြီ။ /start ကိုနှိပ်ပြီး ပြန်စပေးပါဗျာ။")
        return
        
    zone_id = message.text.strip() if message.text else ""
    user_orders[chat_id]["zone_id"] = zone_id
    
    msg = bot.send_message(chat_id, PAYMENT_TEXT)
    bot.register_next_step_handler(msg, process_screenshot_step)

# 5. Screenshot လက်ခံပြီး Admin ဆီ ပို့ပေးမယ့်အဆင့်
def process_screenshot_step(message):
    chat_id = message.chat.id
    
    if chat_id not in user_orders:
        bot.send_message(chat_id, "⚠️ စက်ရှင်သက်တမ်းကုန်ဆုံးသွားပါပြီ။ /start ကိုနှိပ်ပြီး ပြန်စပေးပါဗျာ။")
        return

    if message.content_type != 'photo':
        msg = bot.send_message(chat_id, "⚠️ ကျေးဇူးပြု၍ Screenshot ပို့ပေးပါခင်ဗျာ။")
        bot.register_next_step_handler(msg, process_screenshot_step)
        return

    order = user_orders[chat_id]
    
    bot.send_message(chat_id, "🎉 လူကြီးမင်းရဲ့ Order နှင့် Screenshot ကို လက်ခံရရှိပါပြီ။ Admin မှ မကြာမီ ဆောင်ရွက်ပေးပါလိမ့်မယ်။ ကျေးဇူးတင်ပါတယ်ခင်ဗျာ။ 🙏")

    # 💡 စာသားပုံစံကို Safe ဖြစ်အောင် HTML format ပြောင်းလဲလိုက်ပါတယ်
    admin_msg = f"<b>🔔 Order အသစ် ရောက်ရှိလာပါပြီ!</b>\n\n"
    admin_msg += f"👤 User Name: {order['user_name']}\n"
    admin_msg += f"📦 Item (နံပါတ်): {order['item']}\n"
    admin_msg += f"🆔 Game ID: {order['game_id']}\n"
    
    if "zone_id" in order:
        admin_msg += f"🌐 Zone ID: {order['zone_id']}\n"
        
    admin_msg += f"\n⚙️ <i>User_ID: {chat_id}</i>"  # Markdown အမှားကို ကာကွယ်ရန် HTML စာလုံးစောင်း <i> သုံးထားပါတယ်

    photo_id = message.photo[-1].file_id 
    bot.send_photo(ADMIN_CHAT_ID, photo_id, caption=admin_msg, parse_mode="HTML")

    if chat_id in user_orders:
        del user_orders[chat_id]


# 6. Admin က /yes လို့ Reply ပြန်ရင် အလုပ်လုပ်မယ့်အပိုင်း
@bot.message_handler(func=lambda message: message.chat.id == ADMIN_CHAT_ID and message.text == "/yes")
def admin_approve_order(message):
    if message.reply_to_message and (message.reply_to_message.caption or message.reply_to_message.text):
        caption = message.reply_to_message.caption if message.reply_to_message.caption else message.reply_to_message.text
        
        if "User_ID:" in caption:
            try:
                user_id = int(caption.split("User_ID:")[1].strip())
                
                user_notif = "🎉 <b>လူကြီးမင်း ဝယ်ယူထားသော Game Item ကို အကောင့်ထဲသို့ ထည့်သွင်းပေးပြီးပါပြီခင်ဗျာ!</b>\n\nGame ထဲသို့ဝင်၍ စစ်ဆေးနိုင်ပါပြီ။ GameShop ကို အားပေးမှုအတွက် အထူးပင် ကျေးဇူးတင်ရှိပါတယ်ဗျာ။ 🙏✨"
                bot.send_message(user_id, user_notif, parse_mode="HTML")
                
                bot.reply_to(message, "✅ User ဆီသို့ Order အောင်မြင်ကြောင်း စာလှမ်းပို့ပေးလိုက်ပါပြီ။")
            except Exception as e:
                bot.reply_to(message, "⚠️ Error: User ID ကို ဖတ်မရပါ။")
        else:
            bot.reply_to(message, "⚠️ ဤမက်ဆေ့ခ်ျသည် Order မက်ဆေ့ခ်ျ မဟုတ်ပါ သို့မဟုတ် User ID မပါရှိပါ။")
    else:
        bot.reply_to(message, "💡 ကျေးဇူးပြု၍ User ရဲ့ Order ပြေစာ မက်ဆေ့ခ်ျကို **Reply** ထောက်ပြီးမှ `/yes` လို့ ရိုက်ပို့ပေးပါဗျာ။")

bot.infinity_polling()