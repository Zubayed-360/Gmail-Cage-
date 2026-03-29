import asyncio
from telegram import Update,InlineKeyboardButton,InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder,CommandHandler,MessageHandler,filters,ContextTypes,CallbackQueryHandler

BOT_TOKEN="8780196442:AAG8Yb5PEZqB2lBcdO71Ux14unk3f8OGs-c"

def menu():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("Generate Again",callback_data="again")]
    ])

def generate(email):

    try:

        name,domain=email.split("@")

        results=[]

        for i in range(len(name)):

            new=name[:i]+name[i].upper()+name[i+1:]

            results.append(new+"@"+domain)

        return results[:100]

    except:

        return []

async def start(update:Update,context:ContextTypes.DEFAULT_TYPE):

    await update.message.reply_text(

        "Send Gmail\nExample:\nexample@gmail.com"

    )

async def email_handler(update:Update,context:ContextTypes.DEFAULT_TYPE):

    email=update.message.text.lower()

    data=generate(email)

    if len(data)==0:

        await update.message.reply_text("Invalid Email")

        return

    text="Generated Emails:\n\n"

    for i in data:

        text+=i+"\n"

    await update.message.reply_text(

        text,

        reply_markup=menu()

    )

async def button(update:Update,context:ContextTypes.DEFAULT_TYPE):

    q=update.callback_query

    await q.answer()

    await q.message.reply_text(

        "Send new Gmail"

    )

app=ApplicationBuilder().token(BOT_TOKEN).build()

app.add_handler(CommandHandler("start",start))

app.add_handler(MessageHandler(filters.TEXT,email_handler))

app.add_handler(CallbackQueryHandler(button))

print("Bot Running")

app.run_polling()
