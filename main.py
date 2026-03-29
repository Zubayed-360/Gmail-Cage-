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

    name,domain=email.split("@")

    results=set()

    while len(results)<amount:

        temp=list(name)

        # random uppercase
        for i in range(len(temp)):
            if random.choice([True,False]):
                temp[i]=temp[i].upper()

        new="".join(temp)

        # random dot
        if len(new)>3:
            pos=random.randint(1,len(new)-1)
            new=new[:pos]+"."+new[pos:]

        results.add(new+"@"+domain)

    return list(results)

async def start(update:Update,context:ContextTypes.DEFAULT_TYPE):

    await update.message.reply_text(
        "Send Gmail\nExample:\nexample@gmail.com"
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

app.add_handler(MessageHandler(filters.TEXT,handle_email))

app.add_handler(CallbackQueryHandler(buttons))

app.run_polling()
