import random
from telegram import Update,InlineKeyboardButton,InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder,CommandHandler,MessageHandler,filters,ContextTypes,CallbackQueryHandler

BOT_TOKEN="8780196442:AAG8Yb5PEZqB2lBcdO71Ux14unk3f8OGs-c"

user_emails={}

def amount_menu():
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton("100",callback_data="100"),
            InlineKeyboardButton("150",callback_data="150"),
            InlineKeyboardButton("220",callback_data="220")
        ]
    ])

def again_menu():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("Generate Again",callback_data="again")]
    ])

def generate(email,amount):

    results=set()

    while len(results)<amount:

        temp=""

        for ch in email:   # পুরো email change হবে

            if ch.isalpha():

                if random.choice([True,False]):
                    temp+=ch.upper()
                else:
                    temp+=ch.lower()

            else:
                temp+=ch   # dot, number, @ same থাকবে

        results.add(temp)

    return list(results)

async def start(update:Update,context:ContextTypes.DEFAULT_TYPE):

    await update.message.reply_text(
        "Send Gmail\nExample:\nexample@gmail.com"
    )

async def owner(update:Update,context:ContextTypes.DEFAULT_TYPE):

    keyboard=[
        [InlineKeyboardButton("Bot Owner",url="https://t.me/mdzubayed")]
    ]

    await update.message.reply_text(
        "Bot Owner: @mdzubayed",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

async def team(update:Update,context:ContextTypes.DEFAULT_TYPE):

    keyboard=[
        [InlineKeyboardButton("Join RabbiBD Team",url="https://t.me/RabbiBD1212")]
    ]

    await update.message.reply_text(
        "RabbiBD Work Team",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

async def handle_email(update:Update,context:ContextTypes.DEFAULT_TYPE):

    email=update.message.text

    if "@" not in email:

        await update.message.reply_text("Send valid Gmail")

        return

    user_emails[update.message.chat_id]=email

    await update.message.reply_text(
        "Select amount:",
        reply_markup=amount_menu()
    )

async def buttons(update:Update,context:ContextTypes.DEFAULT_TYPE):

    query=update.callback_query

    await query.answer()

    user_id=query.message.chat_id

    if query.data=="again":

        await query.message.reply_text(
            "Select amount:",
            reply_markup=amount_menu()
        )

        return

    amount=int(query.data)

    email=user_emails.get(user_id)

    results=generate(email,amount)

    text="Generated Emails:\n\n"

    for i,g in enumerate(results,1):

        text+=f"{i} → {g}\n"

    await query.message.reply_text(
        text,
        reply_markup=again_menu()
    )

app=ApplicationBuilder().token(BOT_TOKEN).build()

app.add_handler(CommandHandler("start",start))
app.add_handler(CommandHandler("owner",owner))
app.add_handler(CommandHandler("team",team))

app.add_handler(MessageHandler(filters.TEXT,handle_email))

app.add_handler(CallbackQueryHandler(buttons))

app.run_polling()
