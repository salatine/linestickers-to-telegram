# LINE Stickers to Telegram
![image](https://user-images.githubusercontent.com/95940523/160180035-b3eb62c8-3732-468f-ba27-18910bfde38f.png)

A simple program which uploads stickers originally from LINE to Telegram.

## Setup
First of all, clone your project or download it to a folder. Now you will need to create a `stickers.json` file on your project folder with all the sticker pack info. To do that, you can easily use <a href="https://github.com/line-stickers/LineStickersEditor/releases/tag/latest/">Line Sticker Editor</a>, there is a quick simple <a href="https://line-stickers.github.io/">tutorial</a> on how to use this tool.

We use Poetry to manage dependencies. To install it, open a terminal on your project and execute:

`(Invoke-WebRequest -Uri https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py -UseBasicParsing).Content | python -`

Also, we need to create a venv for this project, and finally, install our dependencies.
```
poetry shell
poetry install
```

When you first open the project, import_telegram_stickers/variables.py should look like this:
```
# your bot's username, like 'mybotisverycool'
TELEGRAM_BOT_USERNAME = None 

# your bot's token, like '110201543:AAHdqTcvCH1vGWJxfSeofSAs0K5PALDsaw'
TELEGRAM_BOT_TOKEN = None 

# your User ID, like 3840182041
USER_ID = None 

# a name for your sticker pack, like 'mycoolstickerpack'
STICKER_NAME = None 

# a title for your sticker pack, like 'My Cool Sticker Pack'
STICKER_TITLE = None 
```
You will need to set all these four variables. Starting with `TELEGRAM_BOT_USERNAME`, `TELEGRAM_BOT_TOKEN`: you can get a bot's username and token by creating one with @botfather on Telegram. We need a Telegram Bot because the app's requests only work with a bot's token, even if it doesn't do anything.

You can get your `USER_ID` talking to @userinfobot on Telegram.

`STICKER_NAME` is your Sticker Pack's name, appeared normally in "t.me/addstickers/<STICKER_NAME>", for example. `STICKER_NAME` needs to be a string.
Note that if this name is already being used by another sticker pack, it will cause an error.

`STICKER_TITLE` is your Sticker Pack's title, appeared at the top of the stickers on Telegram. `STICKER_TITLE` needs to be a string.

## Running
To run it, simply execute:

`python -m import_telegram_stickers.main`
And it's done! To use your new sticker pack, access "t.me/addstickers/<STICKER_NAME>_by_<TELEGRAM_BOT_USERNAME>".
