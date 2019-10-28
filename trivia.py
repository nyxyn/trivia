import hexchat
import threading
import requests
import time
import html
import random

CHANNEL_EVENT = 'Channel Message'
SELF_EVENT = 'Your Message'
KEYWORD = '.trivia'
CHANNEL_KEY = 'channel'
QUESTION_URL = 'https://opentdb.com/api.php?amount=1'

__module_name__ = 'trivia'
__module_version__ = '1.0'
__module_description__ = 'Play trivia game'


def get_choices(result):
    correct_answer = result['correct_answer']
    incorrect_answers = result['incorrect_answers']

    choices = [ correct_answer ]
    choices.extend(incorrect_answers)

    for i, choice in enumerate(choices):
        choices[i] = html.unescape(choice)

    random.shuffle(choices)
    return choices


def get_question():
    response = requests.get(QUESTION_URL).json()
    results = response['results']

    question = html.unescape(results[0]['question'])
    choices = get_choices(results[0])
    answer = html.unescape(results[0]['correct_answer'])
    return { 'question': question, 'choices': choices, 'answer': answer }


def say(channel):
    channel_context = hexchat.find_context(channel=channel)

    question = get_question()
    query = question['question']
    choices = question['choices']

    question_command = 'msg {} <Trivia Bot>: {} Choices: {}'.format(channel, query, choices)
    channel_context.command(question_command)
    time.sleep(20)

    answer = question['answer']
    answer_command = 'msg {} <Trivia Bot>: Answer: {}'.format(channel, answer)
    channel_context.command(answer_command)


def print_callback(words, eol, userdata):
    message = words[1].lower()
    channel = hexchat.get_info(CHANNEL_KEY)

    if KEYWORD in message:
        thread = threading.Thread(target=say, args=(channel,))
        thread.start()

    return hexchat.EAT_NONE


hexchat.prnt('Setting hook for trivia...')
hexchat.hook_print(CHANNEL_EVENT, print_callback)
hexchat.hook_print(SELF_EVENT, print_callback)
hexchat.prnt('Hook set')

