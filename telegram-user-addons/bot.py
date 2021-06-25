import logging
import configparser

from pathlib import Path
from pyrogram import Client, filters, types

logging.basicConfig(level=logging.WARNING)


class BotAddon:
    def __init__(self, folder_name=Path("secret_data")):
        self.folder_name = folder_name
        self.config = configparser.ConfigParser()
        self.config.read(folder_name / "config.ini")
        self.ping_all_from_non_me = True
        self.yt_to_video = True
        self.video_len = 500
        self.my_id = 0

    def start(self):
        app = Client(session_name=str(self.folder_name / "my_account"), api_id=self.config['credentials']['pyrogram_api_id'],
                    api_hash=self.config['credentials']['pyrogram_api_hash'])

        app.start()
        self.my_id = app.get_users('me').id
        app.stop()

        @app.on_message(filters.text)
        def my_handler(client, message: types.Message):
            message_data = message.text.split(' ')
            command = message_data[0]
            if message.chat.id == self.my_id:
                if command == "!help":
                    message.reply("In chat with yourself you can change settings of your addon:\n\n"
                                  "<code>!ping_all_from_non_me</code> - toggle using !ping_all command "
                                  f"by all members of chat\n<b>({self.ping_all_from_non_me})</b>\n\n", parse_mode="html")
                elif command == "!ping_all_from_non_me":
                    self.ping_all_from_non_me = not self.ping_all_from_non_me
                    message.reply(f"ping_all_from_non_me = <b>{self.ping_all_from_non_me}</b> ", parse_mode="html")
            else:
                if command == '!ping_all':
                    if self.ping_all_from_non_me or (self.my_id == message.from_user.id):
                        logging.warning(f"Pinging all in {message.chat.title}")
                        list_mentions = []
                        for member in message.chat.iter_members():
                            if not member.user.is_bot:
                                try:
                                    list_mentions.append(member.user.mention)
                                except AttributeError:
                                    pass
                        conclusion = ''
                        if self.my_id != message.from_user.id:
                            conclusion = '\n\n<b>Requested by:</b>\n'
                            try:
                                conclusion += message.from_user.mention
                            except AttributeError:
                                pass
                        message.reply('\n'.join(list_mentions) + conclusion)
                        logging.warning(f"Done pinging all in {message.chat.title}")
                elif command == "!get_all":
                    message.delete()
                    list_mentions = []
                    for member in message.chat.iter_members():
                        if not member.user.is_bot:
                            try:
                                list_mentions.append(member.user.mention)
                            except AttributeError:
                                pass
                    app.send_message("me", "\n".join(list_mentions) + f"\n\nfrom {message.chat.title}")

        app.run()
