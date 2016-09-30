Dependencies:
- PyMongo
- python-telegram-bot
- python-flask

Setup:
- Setup a account in Telegram messenger.
- After unzipping, cd to the folder and then start the bot server in a terminal by
    python bot1.py
- Start the webserver in a terminal by
    python botrest.py

Usage:
- In the Telegram client (on the phone or web), search and find a bot named 'botissh'
    - Enter /start, or /joke or anything then that gets echoed.
- Test the REST APIs, in the browser

    http://127.0.0.1:5000/ --> Main page
    http://127.0.0.1:5000/api/userslist/  --> Lists all boot users
    http://127.0.0.1:5000/api/userconv/Shivakumar --> User Shivakumar's conversation
    http://127.0.0.1:5000/api/freesearch/water --> Lists conversations that has the word 'water' in it.
    http://127.0.0.1:5000/api/allconversations/ --> Lists all the conversations

