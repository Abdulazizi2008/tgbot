from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ConversationHandler, ContextTypes

# Этапы для ConversationHandler
(
    BROKER_NAME, MC, TYPE, LOAD, PU, PU_ADDRESS, PU_TIME, 
    DEL, DEL_ADDRESS, DEL_TIME, RATE, DEADHEAD, DISTANCE, TOTAL_DISTANCE, RESULT
) = range(15) 

# Начало работы
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user = update.effective_user
    await update.message.reply_text(
        f"Hi, {user.first_name}\nThis bot will make your work easier.😉",
        reply_markup=ReplyKeyboardMarkup([["Convert the text👀"]], resize_keyboard=True, one_time_keyboard=True)
    )
    return BROKER_NAME

# Запрос на ввод данных
async def ask_broker_name(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text("Enter broker name:")
    return MC

async def ask_mc(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    context.user_data['broker_name'] = update.message.text.upper()
    await update.message.reply_text("Enter the MC:")
    return TYPE

async def ask_type(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    context.user_data['mc'] = update.message.text.upper()
    await update.message.reply_text("Enter the TYPE:")
    return LOAD

async def ask_load(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    context.user_data['type'] = update.message.text.upper()
    await update.message.reply_text("Enter the LOAD:")
    return PU

async def ask_pu(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    context.user_data['load'] = update.message.text.upper()
    await update.message.reply_text("Enter the PU:")
    return PU_ADDRESS

async def ask_pu_address(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    context.user_data['pu'] = update.message.text.upper()
    await update.message.reply_text("Enter the PU address:")
    return PU_TIME

async def ask_pu_time(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    context.user_data['pu_address'] = update.message.text.upper()
    await update.message.reply_text("Enter a PU time:")
    return DEL

async def ask_del(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    context.user_data['pu_time'] = update.message.text.upper()
    await update.message.reply_text("Enter DEL:")
    return DEL_ADDRESS

async def ask_del_address(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    context.user_data['del'] = update.message.text.upper()
    await update.message.reply_text("Enter DEL address:")
    return DEL_TIME

async def ask_del_time(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    context.user_data['del_address'] = update.message.text.upper()
    await update.message.reply_text("Enter DEL time:")
    return RATE

async def ask_rate(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    context.user_data['del_time'] = update.message.text.upper()
    await update.message.reply_text("Enter the RATE:")
    return DEADHEAD

async def ask_deadhead(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    context.user_data['rate'] = update.message.text.upper()
    await update.message.reply_text("Enter the DEADHEAD:")
    return DISTANCE

async def ask_distance(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    context.user_data['deadhead'] = update.message.text.upper()
    await update.message.reply_text("Enter the DISTANCE:")
    return TOTAL_DISTANCE

async def ask_total_distance(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    context.user_data['distance'] = update.message.text.upper()
    await update.message.reply_text("Enter Total Distance:")
    return RESULT  # Используем новое состояние RESULT

async def result_text(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    context.user_data['total_distance'] = update.message.text.upper()  # Сохраняем Total Distance
    await update.message.reply_text("Working on it...")
    return await display_result(update, context)  # Переход к отображению результатов

async def display_result(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    data = context.user_data
    template = f"""
📦{data['broker_name']}📦 {data['mc']}
TYPE: {data['type']}

🗂LOAD# {data['load']}
___________________________________

↗️PU: {data['pu']}
{data['pu_address']}
🕰 {data['pu_time']}

➡️DEL: {data['del']}
{data['del_address']}
🕰 {data['del_time']}
___________________________________

RATE: ${data['rate']}

DEADHEAD: {data['deadhead']} mi
DISTANCE: {data['distance']} mi
TOTAL DISTANCE: {data['total_distance']} mi
____________________________________

CHARGES:
❗️Late charge (no reason) — 150$
❗️No communication — 50$
❗️Restricted road — 750$
❗️Stationary no update — 100$
❗️No trailer pictures or BOL — 100$
❗️Rejection (uninformed) — 300$
❗️Not using app - 100$
❗️No pictures of sticker- 100$
    """
    await update.message.reply_text(template.upper())
    return ConversationHandler.END  # Завершаем разговор после отображения результата


async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text("Operation cancelled.", reply_markup=None)
    return ConversationHandler.END

def main() -> None:
    application = Application.builder().token("7610522422:AAH-kUpcst8MilD3cVmcpknwaaV-mdwP0FQ").build()

    conv_handler = ConversationHandler(
    entry_points=[CommandHandler("start", start)],  
    states={
        BROKER_NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, ask_broker_name)],
        MC: [MessageHandler(filters.TEXT & ~filters.COMMAND, ask_mc)],
        TYPE: [MessageHandler(filters.TEXT & ~filters.COMMAND, ask_type)],
        LOAD: [MessageHandler(filters.TEXT & ~filters.COMMAND, ask_load)],
        PU: [MessageHandler(filters.TEXT & ~filters.COMMAND, ask_pu)],
        PU_ADDRESS: [MessageHandler(filters.TEXT & ~filters.COMMAND, ask_pu_address)],
        PU_TIME: [MessageHandler(filters.TEXT & ~filters.COMMAND, ask_pu_time)],
        DEL: [MessageHandler(filters.TEXT & ~filters.COMMAND, ask_del)],
        DEL_ADDRESS: [MessageHandler(filters.TEXT & ~filters.COMMAND, ask_del_address)],
        DEL_TIME: [MessageHandler(filters.TEXT & ~filters.COMMAND, ask_del_time)],
        RATE: [MessageHandler(filters.TEXT & ~filters.COMMAND, ask_rate)],
        DEADHEAD: [MessageHandler(filters.TEXT & ~filters.COMMAND, ask_deadhead)],
        DISTANCE: [MessageHandler(filters.TEXT & ~filters.COMMAND, ask_distance)],
        TOTAL_DISTANCE: [MessageHandler(filters.TEXT & ~filters.COMMAND, ask_total_distance)],
        RESULT: [MessageHandler(filters.TEXT & ~filters.COMMAND, result_text)], 
    },
    fallbacks=[CommandHandler("cancel", cancel)],
)

    application.add_handler(conv_handler)


    application.run_polling()

if __name__ == "__main__":
    main() 