"""
First, a few callback functions are defined. Then, those functions are passed to
the Dispatcher and registered at their respective places.
Then, the bot is started and runs until we press Ctrl-C on the command line.
"""

import logging,external

from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, Update
from telegram.ext import (
    Updater,
    CommandHandler,
    MessageHandler,
    Filters,
    ConversationHandler,
    CallbackContext,
)

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)

FINDFUNCTION, BORED = range(2)


def start(update: Update, _: CallbackContext) -> int:
    """Starts the conversation and asks the user about their gender."""
    reply_keyboard = [['I\'m bored', 'Show me random NSFW anime pic', 'Show me a random safe anime image']]

    update.message.reply_text(
        'Hi! I\'m a bot, as random as universe'
        'Send /cancel to stop talking to me.\n\n'
        'Select something from below',
        reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True),
    )

    return FINDFUNCTION

def callbored(update: Update,):
    retjson = external.areyoubored()
    if retjson is not None:
        update.message.reply_text(retjson["activity"])
    else:
        update.message.reply_text(' Error in getting what you asked. Report this')

def NSFW(update: Update,):
    retjson = external.showRandomImages("nsfw")
    if retjson is not None:
        update.message.reply_text(retjson["url"])
    else:
        update.message.reply_photo(' Error in getting what you asked. Report this')

def SFW(update: Update,):
    retjson = external.showRandomImages("sfw")
    if retjson is not None:
        update.message.reply_photo(retjson["url"])
    else:
        update.message.reply_text(' Error in getting what you asked. Report this')

def findFunction(update: Update, _: CallbackContext) -> int:
    """Stores the selected gender and asks for a photo."""
    user = update.message.from_user
    logger.info("User %s requested %s.", user.first_name, update.message.text)

    function_needed = update.message.text
    if 'bored' in function_needed:
        callbored(update)
        update.message.reply_text(' Wanna /start again?',)
    elif 'NSFW' in function_needed:
        NSFW(update)
        update.message.reply_text(' Wanna /start again?',)
    elif 'image' in function_needed:
        SFW(update)
        update.message.reply_text(' Wanna /start again?',)
    else:
        update.message.reply_text(function_needed+
            ' not implemented, please /start again..',)
        return None

def cancel(update: Update, _: CallbackContext) -> int:
    """Cancels and ends the conversation."""
    user = update.message.from_user
    logger.info("User %s canceled the conversation.", user.first_name)
    update.message.reply_text(
        'Bye! I hope we can talk again some day.', reply_markup=ReplyKeyboardRemove()
    )

    return ConversationHandler.END

def unknown(update, context)-> int:
    context.bot.send_message(chat_id=update.effective_chat.id, text="Sorry, I didn't understand that command.")


def main() -> None:
    """Run the bot."""
    # Create the Updater and pass it your bot's token.
    updater = Updater("TOKEN")

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher


    dispatcher.add_handler(ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            FINDFUNCTION: [MessageHandler((Filters.regex('bored') ^ Filters.regex('NSFW') ^ Filters.regex('safe')), findFunction), CommandHandler('start', start)],
        },
        fallbacks=[CommandHandler('cancel', cancel)],
    ))
    dispatcher.add_handler(MessageHandler(Filters.command, unknown))

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
