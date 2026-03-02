# Chat with AI Discord bot

A simple bot to add to your Discord server, so it can chat and interact with everyone and make it more fun!

## FEATURES

-  You can chat with it by @ them or by replying to it's message!
-  It can randomly reply to someone's message from time to time!
-  It can decide by itself if it will reply with a text or with a reaction, if it will reply with short or long text and even decide the tone for its text!
-  You can customize its personality by editing the chat.py file!
-  It can send a message automatically if the server has no new messages that day!
-  And probably other features i just can't remember right now.

Basically, i've made it to behave like any other member from discord servers, with the ability to decide by itself the best approach to do it!

## FAQ

- Q: How do i setup this bot? I want it on my server!
- A: You must clone this repo, create an .env file with a `DISCORD_TOKEN` and `GEMINI_API_KEY` in it, run `pip install -r requirements.txt` and start the bot via `python main.py`. Yes, you must host this bot somewhere, i recommend you hosting it in your computer.

- Q: Isn't Gemini API like a paid subscription?
- A: Yes! BUT you can use it for free too. If you put your credit card information in it (even with no intention on paying for using it) you have even MORE usage for free!

- Q: I don't know how to get a `DISCORD_TOKEN` and `GEMINI_API_KEY` please help
- A: You can get this info easly by using Youtube or Google!

- Q: Your bot is written in Portuguese, but i speak in another language! How do i change that?
- A: Inside the file `chat.py`, look for `self.instrucao_persona` and edit its personality with the language you want! I REALLY recommend you doing it, since the one written in there right now only makes sense for me and my friends LOL.
