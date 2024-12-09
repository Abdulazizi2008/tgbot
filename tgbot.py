from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ConversationHandler, ContextTypes

# Этапы для ConversationHandler
(
    BROKER_NAME, MC, TYPE, LOAD, REFERENCE_NUMBER, PU, PU_TIME, 
    DEL, DEL_TIME, RATE, DEADHEAD, DISTANCE, RESULT
) = range(13)

state_city_abbreviations = {
    "alabama": "AL",
    "alaska": "AK",
    "arizona": "AZ",
    "arkansas": "AR",
    "california": "CA",
    "colorado": "CO",
    "connecticut": "CT",
    "delaware": "DE",
    "florida": "FL",
    "georgia": "GA",
    "hawaii": "HI",
    "idaho": "ID",
    "illinois": "IL",
    "indiana": "IN",
    "iowa": "IA",
    "kansas": "KS",
    "kentucky": "KY",
    "louisiana": "LA",
    "maine": "ME",
    "maryland": "MD",
    "massachusetts": "MA",
    "michigan": "MI",
    "minnesota": "MN",
    "mississippi": "MS",
    "missouri": "MO",
    "montana": "MT",
    "nebraska": "NE",
    "nevada": "NV",
    "new hampshire": "NH",
    "new jersey": "NJ",
    "new mexico": "NM",
    "new york": "NY",
    "north carolina": "NC",
    "north dakota": "ND",
    "ohio": "OH",
    "oklahoma": "OK",
    "oregon": "OR",
    "pennsylvania": "PA",
    "rhode island": "RI",
    "south carolina": "SC",
    "south dakota": "SD",
    "tennessee": "TN",
    "texas": "TX",
    "utah": "UT",
    "vermont": "VT",
    "virginia": "VA",
    "washington": "WA",
    "west virginia": "WV",
    "wisconsin": "WI",
    "wyoming": "WY",
}


def abbreviate_location(location: str) -> str:
    words = location.lower().split()
    abbreviated_words = [
        state_city_abbreviations.get(word, word.capitalize()) for word in words
    ]
    return " ".join(abbreviated_words)

# Начало работы
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user = update.effective_user
    await update.message.reply_text(
        f"Hi, {user.first_name}\nThis bot will make your work easier.😉",
        reply_markup=ReplyKeyboardMarkup([["Convert the text👀"]], resize_keyboard=True, one_time_keyboard=True)
    )
    return BROKER_NAME

# Запросы на ввод данных
async def ask_broker_name(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text("Enter broker name:")
    return MC

async def ask_mc(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    context.user_data['broker_name'] = update.message.text.strip().upper()
    await update.message.reply_text("Enter the MC:")
    return TYPE

async def ask_type(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    context.user_data['mc'] = update.message.text.strip().upper()
    await update.message.reply_text("Enter the TYPE:")
    return LOAD

async def ask_load(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    context.user_data['type'] = update.message.text.strip().upper()
    await update.message.reply_text("Enter the LOAD:")
    return REFERENCE_NUMBER

async def ask_reference_number(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    context.user_data['load'] = update.message.text.strip().upper()
    await update.message.reply_text(
        "Enter the reference number or press 'Skip entering reference number':",
        reply_markup=ReplyKeyboardMarkup([["Skip entering reference number"]], resize_keyboard=True, one_time_keyboard=True)
    )
    return PU

async def ask_pu(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    if update.message.text.strip().lower() == "skip entering reference number":
        context.user_data['reference_number'] = "N/G"
    else:
        context.user_data['reference_number'] = update.message.text.strip().upper()

    await update.message.reply_text("Enter the PU location:")
    return PU_TIME

async def ask_pu_time(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    # Сохраняем и сокращаем PU
    user_input = update.message.text.strip()
    context.user_data['pu'] = abbreviate_location(user_input)  # Сокращаем название
    
    await update.message.reply_text("Enter PU time:")
    return DEL

async def ask_del(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    context.user_data['pu_time'] = update.message.text.strip().upper()
    
    await update.message.reply_text("Enter the DEL location:")
    return DEL_TIME

async def ask_del_time(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    # Сокращаем название DEL
    user_input = update.message.text.strip()
    context.user_data['del'] = abbreviate_location(user_input)  # Сокращаем название
    
    await update.message.reply_text("Enter DEL time:")
    return RATE

async def ask_rate(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    context.user_data['del_time'] = update.message.text.strip().upper()
    await update.message.reply_text("Enter RATE:")
    return DEADHEAD

async def ask_deadhead(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    context.user_data['rate'] = update.message.text.strip().upper()
    await update.message.reply_text("Enter the DEADHEAD:")
    return DISTANCE

async def ask_distance(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    context.user_data['deadhead'] = int(update.message.text.strip())  # Преобразуем в число
    await update.message.reply_text("Enter the DISTANCE:")
    return RESULT

# Отображение результатов
async def display_result(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    context.user_data['distance'] = int(update.message.text.strip())  # Преобразуем в число
    context.user_data['total_distance'] = context.user_data['deadhead'] + context.user_data['distance']

    data = context.user_data
    template = f"""
📦 {data['broker_name']} 📦 {data['mc']}
TYPE: {data['type']}

🗂 LOAD# {data['load']}

REFERENCE NUMBER: {data['reference_number']}
___________________________________

↗️ PU: {data['pu']}
🕰 {data['pu_time']}

➡️ DEL: {data['del']}
🕰 {data['del_time']}
___________________________________

RATE: ${data['rate']}

DEADHEAD: {data['deadhead']} mi
DISTANCE: {data['distance']} mi
TOTAL DISTANCE: {data['total_distance']} mi
____________________________________

CHARGES:
❗️ Late charge (no reason) — 150$
❗️ No communication — 50$
❗️ Restricted road — 750$
❗️ Stationary no update — 100$
❗️ No trailer pictures or BOL — 100$
❗️ Rejection (uninformed) — 300$
❗️ Not using app — 100$
❗️ No pictures of sticker — 100$
    """
    await update.message.reply_text(template)
    return ConversationHandler.END

# Отмена
async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text("Operation cancelled.", reply_markup=None)
    return ConversationHandler.END

# Основной метод
def main() -> None:
    application = Application.builder().token("7610522422:AAH-kUpcst8MilD3cVmcpknwaaV-mdwP0FQ").build()

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            BROKER_NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, ask_broker_name)],
            MC: [MessageHandler(filters.TEXT & ~filters.COMMAND, ask_mc)],
            TYPE: [MessageHandler(filters.TEXT & ~filters.COMMAND, ask_type)],
            LOAD: [MessageHandler(filters.TEXT & ~filters.COMMAND, ask_load)],
            REFERENCE_NUMBER: [MessageHandler(filters.TEXT & ~filters.COMMAND, ask_reference_number)],
            PU: [MessageHandler(filters.TEXT & ~filters.COMMAND, ask_pu)],
            PU_TIME: [MessageHandler(filters.TEXT & ~filters.COMMAND, ask_pu_time)],
            DEL: [MessageHandler(filters.TEXT & ~filters.COMMAND, ask_del)],
            DEL_TIME: [MessageHandler(filters.TEXT & ~filters.COMMAND, ask_del_time)],
            RATE: [MessageHandler(filters.TEXT & ~filters.COMMAND, ask_rate)],
            DEADHEAD: [MessageHandler(filters.TEXT & ~filters.COMMAND, ask_deadhead)],
            DISTANCE: [MessageHandler(filters.TEXT & ~filters.COMMAND, ask_distance)],
            RESULT: [MessageHandler(filters.TEXT & ~filters.COMMAND, display_result)],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )

    application.add_handler(conv_handler)
    application.run_polling()

if __name__ == "__main__":
    main()