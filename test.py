from os import name
from socket import MSG_OOB
from pywebio import start_server
from pywebio.input import *
from pywebio.output import *
from pywebio.session import data, run_async, run_js

import asyncio

from tornado.web import MAX_SUPPORTED_SIGNED_VALUE_VERSION

chat_msgs = []
online_users = set()

MAX_MESSAGES_COUNT = 100

async def main():
    global chat_msgs

    put_markdown("дарова это онлайн чат окда")

    msg_box = output()
    put_scrollable(msg_box, height=300, keep_bottom=True)

    nickname = await input("вход в какой-то хз там чат крч да", required=True, placeholder="ваше имя окда", validate=lambda n: "уже такой ник есть окда"if n in online_users or n == 'какой-то' else None)
    online_users.add(nickname)

    chat_msgs.append(("какой-то", f"{nickname} зашёл"))
    msg_box.append(put_markdown(f"{nickname} зашёл"))


    refresh_task = run_async(refresh_msg(nickname, msg_box))

    while True:
        data = await input_group("какой-то там чат хз реал ну крч да чатик так чатик короче", [
            input(placeholder="введите текст", name="msg"),
            actions(name="cmd", buttons=["отправить сообщение на марс", {'label':"выебаться с чата", 'type':'cancel'}])
    ], validate=lambda m: ('msg', "введите текст") if m["cmd"] == "отправить сообщение на марс" and not m['msg'] else None)

    


        if data is None:
            break


        msg_box.append(put_markdown(f"`{nickname}`: {data['msg']}"))
        chat_msgs.append((nickname, data['msg']))


    refresh_task.close()

    online_users.remove(nickname)
    toast("вы выебались из чата.")
    msg_box.append(f"какой-то {nickname} выебался из чата")
    chat_msgs.append(f"какой-то {nickname} выебался из чата")

async def refresh_msg(nickname, msg_box):
    global chat_msgs
    last_idx = len(chat_msgs)

    while True:
        await asyncio.sleep(1)

        for m in chat_msgs[last_idx]:
            if m[0] != nickname:
                msg_box.append(put_markdown(f"`{m[0]}`: {m[1]}"))

        if len(chat_msgs) > MAX_MESSAGES_COUNT:
            chat_msgs = chat_msgs[len(chat_msgs) // 2:]

        last_idx = len(chat_msgs)   

if __name__ == "__main__":
    start_server(main, debug=True, port=1823, cdn=False)                      