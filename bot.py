from telegram.ext.updater import Updater
from telegram.update import Update
from telegram.ext.callbackcontext import CallbackContext
from telegram.ext.commandhandler import CommandHandler
from telegram.ext.messagehandler import MessageHandler
from telegram.ext.filters import Filters
# Lab3 service to send logs
from fluent import sender
from fluent import event
# Lab4 service to send metrix to prometheus with built in tornado
from prometheus_client import start_http_server, Counter


# Fluentd service to send and edit logs
sender.setup('fluentd.tgbot', host='localhost', port=24224)

# Create metric to count number of function calls
MESSAGES_COUNER = Counter('tgbot_calls', 'Number of times users send messages')
ERORRS_COUNER = Counter('tgbot_errors', 'Number of errors')

# Start up the server to expose the metrics.
start_http_server(9091, "127.0.0.1")

updater = Updater("5339490694:AAFx8UeC5_uPFI1O2mPJRMk7yJi_ejhdOf8",
                  use_context=True)

@ERORRS_COUNER.count_exceptions()
def start(update: Update, context: CallbackContext):
    update.message.reply_text(
        "Hello sir, Welcome to the Bot. Please write \
        /help to see the commands available.")
    MESSAGES_COUNER.inc()


@ERORRS_COUNER.count_exceptions()
def help(update: Update, context: CallbackContext):
    update.message.reply_text("""Available Commands :-
    /youtube - To get the youtube URL
    /linkedin - To get the LinkedIn profile URL
    /gmail - To get gmail URL
    /geeks - To get the GeeksforGeeks URL""")
    MESSAGES_COUNER.inc()

@ERORRS_COUNER.count_exceptions()
def gmail_url(update: Update, context: CallbackContext):
    update.message.reply_text("My gmail link here")
    print(context.user_data)
    MESSAGES_COUNER.inc()

@ERORRS_COUNER.count_exceptions()
def youtube_url(update: Update, context: CallbackContext):
    update.message.reply_text("Youtube Link => \
    https://www.youtube.com/")
    MESSAGES_COUNER.inc()

@ERORRS_COUNER.count_exceptions()
def linkedIn_url(update: Update, context: CallbackContext):
    update.message.reply_text(
        "LinkedIn URL => \
        https://www.linkedin.com/")
    MESSAGES_COUNER.inc()

@ERORRS_COUNER.count_exceptions()
def geeks_url(update: Update, context: CallbackContext):
    update.message.reply_text(
        "GeeksforGeeks URL => https://www.geeksforgeeks.org/")
    MESSAGES_COUNER.inc()

@ERORRS_COUNER.count_exceptions()
def unknown(update: Update, context: CallbackContext):
    update.message.reply_text(
        "Sorry '%s' is not a valid command" % update.message.text)
    
    event.Event('UserData', {
        'UserId':   update.message.from_user.id,
        'UserName': update.message.from_user.name,
        'MessageText': update.message.text,
    })
    MESSAGES_COUNER.inc()

@ERORRS_COUNER.count_exceptions()
def unknown_text(update: Update, context: CallbackContext):
    update.message.reply_text(
        "Sorry I can't recognize you , you said '%s'" % update.message.text)
    
    event.Event('UserData', {
        'UserId':   update.message.from_user.id,
        'UserName': update.message.from_user.name,
        'MessageText': update.message.text,
    })
    MESSAGES_COUNER.inc()


updater.dispatcher.add_handler(CommandHandler('start', start))
updater.dispatcher.add_handler(CommandHandler('youtube', youtube_url))
updater.dispatcher.add_handler(CommandHandler('help', help))
updater.dispatcher.add_handler(CommandHandler('linkedin', linkedIn_url))
updater.dispatcher.add_handler(CommandHandler('gmail', gmail_url))
updater.dispatcher.add_handler(CommandHandler('geeks', geeks_url))
updater.dispatcher.add_handler(MessageHandler(Filters.command, unknown))
updater.dispatcher.add_handler(MessageHandler(Filters.text, unknown_text))

updater.start_polling()