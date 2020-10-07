import random
import logging
import datetime

from settings import *

from telegram import ParseMode, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, PollAnswerHandler, CallbackQueryHandler
from telegram.utils.helpers import mention_html

from services.webhooks.webhooks import check_voice_connected, tea_party_next_gaming_night

from cogs.games.model import GamingNight

from .model import Poll, PollAnswer


# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger("telegram")


class TelegramBot():
    updater = None

    commands = [
        {
            'cmd': 'help',
            'description': "Zeigt Hilfe an",
            'func': "printHelp"
        },
        {
            'cmd': 'status',
            'description': "Developer only",
            'func': "cmdStatus"
        },
        {
            'cmd': 'roll',
            'description': "Eine Zufallszahl zwischen 0 und 100",
            'func': "cmdRoll"
        },
        {
            'cmd': 'online',
            'description': "Zeigt Anzahl Personen im Voice",
            'func': "cmdCheckVoiceOnline"
        },
        {
            'cmd': 'vote',
            'description': "Startet Voting ODER zeigt geplanten Spieleabend an",
            'func': "cmdPollNext"
        },
        # {
        #     'cmd': 'games',
        #     'description': "Zeigt welche Spiele zur Zeit gespielt werden",
        #     'func': "cmdGames"
        # },
    ]

    def error(self, update, context):
        """
        Log Errors caused by Updates.
        :param update:
        :param context:
        :return:
        """
        logger.warning('Update {} caused error'.format(update))
        logger.warning('Error: {}'.format(context.error))

    def __init__(self):
        """
        Setup Telegram Bot instance
        Register command handler
        """
        self.updater = Updater(TELEGRAM_SECRET_TOKEN, use_context=True)

        # Get the dispatcher to register handlers
        dp = self.updater.dispatcher

        # log all errors
        dp.add_error_handler(self.error)

        for c in self.commands:
            dp.add_handler(CommandHandler(c['cmd'], getattr(self, c['func'])))

        # handle poll answers
        dp.add_handler(PollAnswerHandler(self.receive_poll_answer))

        # Button Handler
        # self.updater.dispatcher.add_handler(CallbackQueryHandler(self.button))

        # Start the Bot
        self.updater.start_polling()

        # Run the bot until you press Ctrl-C or the process receives SIGINT,
        # SIGTERM or SIGABRT. This should be used most of the time, since
        # start_polling() is non-blocking and will stop the bot gracefully.
        # self.updater.idle()

    def printHelp(self, update, context):
        """
        Prints out the help
        Based on self.commands!
        :param update:
        :param context:
        :return:
        """
        final_help = "I can do the following: \n"
        for help_item in self.commands:
            command = "/%s : %s" % (help_item['cmd'], help_item['description'])
            final_help += command + "\n"

        update.message.reply_text(final_help, parse_mode=ParseMode.MARKDOWN_V2)

    def cmdRoll(self, update, context):
        """
        Answer with a random number between 1 and 100
        :param update:
        :param context:
        :return:
        """
        r = random.randint(1, 101)
        update.message.reply_text(r)

    def cmdStatus(self, update, context):
        update.message.reply_text(update.message.chat.id)

    def cmdCheckVoiceOnline(self, update, context):
        check_voice_connected()

    def _get_german_weekday(self, plus):
        """
        Get the german name and the corresponding date
        """
        chosen_date = datetime.datetime.today() + datetime.timedelta(days=plus)
        cd_id = chosen_date.weekday()
        if cd_id == 0:
            return "Montag {}".format(chosen_date.strftime("%d.%m"))
        elif cd_id == 1:
            return "Dienstag {}".format(chosen_date.strftime("%d.%m"))
        elif cd_id == 2:
            return "Mittwoch {}".format(chosen_date.strftime("%d.%m"))
        elif cd_id == 3:
            return "Donnerstag {}".format(chosen_date.strftime("%d.%m"))
        elif cd_id == 4:
            return "Freitag {}".format(chosen_date.strftime("%d.%m"))
        elif cd_id == 5:
            return "Samstag {}".format(chosen_date.strftime("%d.%m"))
        elif cd_id == 6:
            return "Sonntag {}".format(chosen_date.strftime("%d.%m"))

    def _next_gaming_night_result(self):
        """
        Find out the winner when the next gaming night is 
        """
        latest_poll = Poll.objects.order_by('-id').first()
        user_answers = PollAnswer.objects(poll_id=latest_poll.poll_id)

        results = {
            0: 0,
            1: 0,
            2: 0,
            3: 0,
            4: 0,
            5: 0,
            6: 0
        }
        for ua in user_answers:
            for selected_item in ua.answer:
                results.update({
                    selected_item: results[selected_item] + 1
                })

        sorted_results = sorted(
            results.items(), key=lambda x: x[1], reverse=True)
        logger.info("Sorted Results {}".format(sorted_results))

        winner_date = latest_poll.questions[sorted_results[0][0]]
        logger.info("Winner Date: {}".format(winner_date))

        selected_date = latest_poll.updated_at + \
            datetime.timedelta(days=sorted_results[0][0])
        logger.info("Selected Date: {}".format(selected_date))

        selected_date = selected_date.replace(hour=20, minute=0)

        logger.info("Next date for gaming night: {}".format(selected_date))
        return winner_date, selected_date

    def cmdPollNext(self, update, context):
        """
        Create a poll to see vote for the next meeting date
        """

        # check if what day is today and if there is a poll within the last 7 days, with an outstanding meetup night
        current_gaming_night = None
        try:
            current_gaming_night = GamingNight.objects().order_by("-id").first()
            if current_gaming_night is not None:
                logger.info("Found gaming night setup!")
                logger.info(current_gaming_night)
                if current_gaming_night.selected_date >= datetime.datetime.today():
                    logger.info(
                        "Selected Gaming night is in the future of today")
                    if current_gaming_night.selected_date > (datetime.datetime.today() - datetime.timedelta(days=6)):
                        logger.info(
                            "Gaming night is bigger than the last 6 days")
                        self.sendMessage("Es ist bereits ein Spieleabend geplant innerhalb der naechsten 7 Tagen: {}".format(
                            current_gaming_night.selected_date.strftime("%d.%m")))
                        return
        except:
            pass

        today = "Heute ({})".format(self._get_german_weekday(0))
        tomorrow = "Morgen ({})".format(self._get_german_weekday(1))
        day3 = "{}".format(self._get_german_weekday(2))
        day4 = "{}".format(self._get_german_weekday(3))
        day5 = "{}".format(self._get_german_weekday(4))
        day6 = "{}".format(self._get_german_weekday(5))
        day7 = "{}".format(self._get_german_weekday(6))

        questions = [today, tomorrow, day3, day4,
                     day5, day6, day7, "Nicht verfuegbar!"]
        message = self.updater.bot.send_poll(update.message.chat.id, "Naechster Termin fuer einen Spieleabend? (ab 20 Uhr)",
                                             questions, is_anonymous=False, allows_multiple_answers=True, disable_notification=True)

        # save a poll refernce in the database
        p = Poll()
        p.poll_id = message.poll.id
        p.questions = questions
        p.message_id = message.message_id
        p.chat_id = update.effective_chat.id
        p.answers = 0
        p.save()

    def receive_poll_answer(self, update, context):
        """Summarize a users poll vote"""
        answer = update.poll_answer
        poll_id = answer.poll_id
        selected_poll = None
        try:
            selected_poll = Poll.objects(poll_id=poll_id).first()
        except:
            logger.error("Had keyerror, unknown poll_id {}".format(poll_id))
            return

        # go over the answers from user
        questions = selected_poll.questions
        selected_options = answer.option_ids
        answer_string = ""

        logger.debug("Got answers from user mention...%s" %
                     update.effective_user.full_name)

        # perpare string to output in chat
        for question_id in selected_options:
            if question_id != selected_options[-1]:
                answer_string += questions[question_id] + " und "
            else:
                answer_string += questions[question_id]

        # save user answers as object in the db
        poll_answer = PollAnswer()
        poll_answer.poll_id = selected_poll.poll_id
        poll_answer.username = update.effective_user.full_name
        poll_answer.user_id = update.effective_user.id
        poll_answer.answer = selected_options
        poll_answer.save()

        # create a mention for the chat output
        user_mention = mention_html(
            update.effective_user.id, update.effective_user.full_name)
        context.bot.send_message(selected_poll.chat_id,
                                 "{}: {}!".format(
                                     user_mention, answer_string),
                                 parse_mode=ParseMode.HTML)
        selected_poll.answers += 1
        logger.info("Poll answer count: {}".format(selected_poll.answers))
        # Close poll after three participants voted
        if selected_poll.answers == 3:
            selected_poll.closed = True
            context.bot.stop_poll(selected_poll.chat_id,
                                  selected_poll.message_id)
            logger.info("we are in the answer closing stage")
            result_str, selected_date = self._next_gaming_night_result()

            final_message = "Voting ist nun beendet. Es ist: {} ab um 20 Uhr".format(
                result_str)

            context.bot.send_message(selected_poll.chat_id, final_message)

            # create a gaming night document
            new_gaming_night = GamingNight()
            new_gaming_night.poll_id = selected_poll.poll_id
            new_gaming_night.selected_date = selected_date
            new_gaming_night.save()

            # send message to Tea Party Discord Chat
            tea_party_next_gaming_night(
                "Der naechste Spieleabend ist: {} ab um 20:00 Uhr".format(result_str))

        selected_poll.save()

    # def button(self, update, context):
    #     query = update.callback_query

    #     # CallbackQueries need to be answered, even if no notification to the user is needed
    #     # Some clients may have trouble otherwise. See https://core.telegram.org/bots/api#callbackquery
    #     query.answer()

    #     query.edit_message_text(text="Selected option: {}".format(query.data))

    # def chooseReminder(self, update, context):
    #     keyboard = [[InlineKeyboardButton("Ja", callback_data='1'),
    #                  InlineKeyboardButton("Nein", callback_data='0')]]

    #     reply_markup = InlineKeyboardMarkup(keyboard)

    #     update.message.reply_text(
    #         'Moechtest du erinnert werden?', reply_markup=reply_markup)

    def sendMessage(self, message):
        """
        Sends a message to a specific channel in Telegram
        this is configured via TELEGRAM_CHANNEL_ID in the environment
        Used by pipeline in other bots
        :param message:
        :return:
        """
        logger.debug("Channel: %s" % TELEGRAM_CHANNEL_ID)
        self.updater.bot.send_message(
            chat_id=TELEGRAM_CHANNEL_ID, text=message)
