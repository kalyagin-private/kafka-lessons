import faust
import logging
from os import path
from message import Message

logging.getLogger().setLevel(logging.INFO)

# Конфигурация Faust-приложения
app = faust.App(
    "cen-app",
    broker="localhost:19092,localhost:29092,localhost:39092",
    value_serializer="json",
)

# Определение топика для входных входящих сообщений
input_topic = app.topic("messages", key_type=str, value_type=Message)
# Определение топика для сообщений после цензурирования
censor_topic = app.topic("censor_messages", key_type=str, value_type=Message)
# Определение топика для выходных данных
output_topic = app.topic("filtered_messages", key_type=str, value_type=Message)


def is_can_send(from_user_id, to_user_id):
    user_path = f"blocked_users/{to_user_id}.txt"
    try:
        if not (path.exists(user_path)):
            return True
        with open(user_path, "r") as f:
            blocked_users = f.read()
            if str(from_user_id) in blocked_users:
                return False
            else:
                return True
    except Exception as e:
        logging.error(e)


# Функция, реализующая потоковую обработку данных
@app.agent(input_topic)
async def censor(messages):
    async for msg in messages:

        message = msg.message
        try:
            with open("bad_words.txt", "r", encoding="utf-8") as f:
                bad_words_list = f.read().split("\n")
            for word in bad_words_list:
                if word in message:
                    message = message.replace(word, "***")
            msg.message = message
            await censor_topic.send(value=msg)
        except Exception as e:
            logging.error(e)


@app.agent(censor_topic)
async def process(messages):
    async for message in messages:
        # Обработка данных
        if is_can_send(message.from_user_id, message.to_user_id):
            await output_topic.send(value=message)
