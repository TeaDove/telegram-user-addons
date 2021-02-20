import logging
import configparser
import os
from pathlib import Path
from pyrogram import Client, filters, types
from pytube import YouTube, exceptions


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
                                  f"by all members of chat\n<b>({self.ping_all_from_non_me})</b>\n\n"
                                  f"<code>!yt_to_video</code> - toggle transforming yt links to videos\n<b>"
                                  f"({self.yt_to_video})</b>\n\n"
                                  f"<code>!video_len [seconds]</code> - change max size of video "
                                  f"to download\n<b>({self.video_len})</b>",
                                  parse_mode="html")
                elif command == "!ping_all_from_non_me":
                    self.ping_all_from_non_me = not self.ping_all_from_non_me
                    message.reply(f"ping_all_from_non_me = <b>{self.ping_all_from_non_me}</b> ", parse_mode="html")
                elif command == "!yt_to_video":
                    self.yt_to_video = not self.yt_to_video
                    message.reply(f"ping_all_from_non_me = <b>{self.yt_to_video}</b> ", parse_mode="html")
                elif command == "!video_len":
                    if len(message_data) == 2:
                        try:
                            video_len = int(message_data[1])
                        except ValueError:
                            message.reply("Wrong args")
                        else:
                            self.video_len = video_len
                            message.reply(f"video_len = <b>{self.video_len}</b> ", parse_mode="html")
                    else:
                        message.reply("Wrong args")
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

                else:
                    if self.my_id == message.from_user.id and self.yt_to_video:
                        try:
                            link = message.text
                            yt = YouTube(link)
                        except exceptions.RegexMatchError:
                            pass
                        else:
                            if yt.length < self.video_len:
                                logging.warning(f"Start downloading video: {link}")
                                try:
                                    yt.streams.first().download(output_path="data/", filename="video")
                                except AttributeError:
                                    logging.warning(f"AttributeError: {link}")
                                else:
                                    logging.warning(f"Download completed {link}")
                                    message.reply_video("data/video.mp4", quote=False, caption=f'<a href="{link}">{yt.title}</a>',
                                                        parse_mode="html")
                                    message.delete()
                                    os.remove("data/video.mp4")
                                    logging.warning(f"Video sent: {link}")

        app.run()
