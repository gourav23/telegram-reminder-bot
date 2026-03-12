{\rtf1\ansi\ansicpg1252\cocoartf2867
\cocoatextscaling0\cocoaplatform0{\fonttbl\f0\fswiss\fcharset0 Helvetica;}
{\colortbl;\red255\green255\blue255;}
{\*\expandedcolortbl;;}
\paperw11900\paperh16840\margl1440\margr1440\vieww11520\viewh8400\viewkind0
\pard\tx720\tx1440\tx2160\tx2880\tx3600\tx4320\tx5040\tx5760\tx6480\tx7200\tx7920\tx8640\pardirnatural\partightenfactor0

\f0\fs24 \cf0 import datetime\
from apscheduler.schedulers.asyncio import AsyncIOScheduler\
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup\
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes\
\
TOKEN = "8638028990:AAHYWwHar66bXiuv_zwLvvzob__JssfbIW8"\
\
scheduler = AsyncIOScheduler()\
scheduler.start()\
\
reminders = \{\}\
\
async def remind(update: Update, context: ContextTypes.DEFAULT_TYPE):\
\
    chat_id = update.effective_chat.id\
\
    if len(context.args) < 3:\
        await update.message.reply_text(\
            "Usage:\\n/remind YYYY-MM-DD HH:MM message"\
        )\
        return\
\
    date = context.args[0]\
    time = context.args[1]\
    message = " ".join(context.args[2:])\
\
    run_time = datetime.datetime.strptime(f"\{date\} \{time\}", "%Y-%m-%d %H:%M")\
\
    job = scheduler.add_job(send_reminder, "date", run_date=run_time, args=[chat_id, message])\
    reminders[job.id] = job\
\
    await update.message.reply_text("\uc0\u9989  Reminder Scheduled")\
\
\
async def send_reminder(chat_id, message):\
\
    keyboard = [[InlineKeyboardButton("\uc0\u9989  Confirm", callback_data="confirm")]]\
\
    await app.bot.send_message(\
        chat_id,\
        f"\uc0\u9200  Reminder:\\n\{message\}",\
        reply_markup=InlineKeyboardMarkup(keyboard)\
    )\
\
\
async def confirm(update: Update, context: ContextTypes.DEFAULT_TYPE):\
\
    query = update.callback_query\
    await query.answer()\
\
    for job_id in list(reminders):\
        scheduler.remove_job(job_id)\
        reminders.pop(job_id)\
\
    await query.edit_message_text("\uc0\u9989  Reminder confirmed and stopped")\
\
\
app = ApplicationBuilder().token(TOKEN).build()\
\
app.add_handler(CommandHandler("remind", remind))\
app.add_handler(CallbackQueryHandler(confirm))\
\
app.run_polling()}