#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Flask based webserver 
from flask import Flask, jsonify, render_template
from flask_pymongo import PyMongo
import mongoConnect 


"""
Usage:
    http://127.0.0.1:5000/ --> Main page
    http://127.0.0.1:5000/api/userslist/  --> Lists all boot users
    http://127.0.0.1:5000/api/userconv/Shivakumar --> User Shivakumar's conversation
    http://127.0.0.1:5000/api/freesearch/water --> Lists conversations that has the word 'water' in it.
    http://127.0.0.1:5000/api/allconversations/ --> Lists all the conversations
    http://127.0.0.1:5000/api/bydate/2016-09-29 --> Lists all conversations on a given date
"""

app = Flask(__name__)
dbpasswd =  mongoConnect.dbpasswd 
mongo_uri = 'mongodb://botdbuser:'+dbpasswd+'@ds035026.mlab.com:35026/botdbissh'
app.config['MONGO_DBNAME'] = 'botdbissh'
app.config['MONGO_URI'] = mongo_uri 

mongo = PyMongo(app)

@app.route('/api')
def at_root():
    return 'Welcome !!!'

@app.route('/api/allconversations/',methods=['GET'])
def show_all_convs():
    convs = mongo.db.conversations
    output = get_all_conversations(convs)
    return jsonify({'result':output})

@app.route('/api/freesearch/<search>', methods=['GET'])
def free_text_search(search): 
    convs = mongo.db.conversations
    output = find_convs_by_text(convs, search) 
    return jsonify({'result':output})
    
@app.route('/api/bydate/<search>', methods=['GET'])    
def search_by_date(search):
    print search    
    convs = mongo.db.conversations
    output = get_by_date(convs, search) 
    return jsonify({'result':output})

@app.route('/api/userslist/',methods=['GET'])
def show_all_users():
    convs = mongo.db.conversations
    output = convs.distinct('userFn')
    return jsonify({'result':output})

@app.route('/api/userconv/<userName>', methods=['GET'])
def userconv(userName):
        print userName
        convs = mongo.db.conversations
        if convs.find_one({'userFn':userName}):
            output = get_1user_all_convs(convs,userName)
        else:
            output = "No User - <{0}> found. Check the available users by passing /users in the URL.".format(userName)    
        return jsonify({'result':output})

@app.route('/', methods=['GET'])
def bot_ui():
    convs = mongo.db.conversations
    output = convs.distinct('userFn')
    return render_template("main.html", resdata=output)
            
def get_all_conversations(convs):
    output = []
    for conv in convs.find():
        output.append({'chat_Id':conv['chatId'],
        'messageDate':conv['utcnow'], 'user':conv['userFn']})
        #output.append({'chat_Id':conv['chatId'],'bot_rx':conv['botRxcved']})
    return output

def get_by_date(convs, date):
    output = []
    datestr=str(date)
    for conv in convs.find():
        convstrdate = str(conv['utcnow'].date())
        if convstrdate == datestr:
            output.append(
                {
                'user':conv['userFn'],
                'chatId':conv['chatId'],
                'botSentMsg':conv['botTxed'],
                'userSentMsg':conv['botRxcved'],
                'messageDate':conv['utcnow']
                }
                )
    if not output:
        return "No conversations on %s" % datestr
    else:
        return output

def find_convs_by_text(convs, text):
    output = []
    for conv in convs.find({"$or":[{'botRxcved':{'$regex':text}},{'botTxed':{'$regex':text}}]}):
        output.append(
            {
            'user':conv['userFn'],
            'chatId':conv['chatId'],
            'botSentMsg':conv['botTxed'],
            'userSentMsg':conv['botRxcved'],
            'messageDate':conv['utcnow']
            }
            )
    if not output:
        return "No conversations found having the text - %s" % text
    else:
        return output

def get_all_users(convs):
    alloutput=[]
    for conv in convs.find():
        alloutput.append(conv['userFn'])
    uniqoutput = list(set(alloutput))
    return uniqoutput


def get_1user_all_convs(convs,userName):
    output = []
    for conv in convs.find({'userFn':userName}):
        output.append({ 'chatId':conv['chatId'],
                        'botSentMsg':conv['botTxed'],
                        'userSentMsg':conv['botRxcved'],
                        'messageDate':conv['utcnow']
                        })
    return output
    
if __name__ == '__main__':
    app.run(debug=True)