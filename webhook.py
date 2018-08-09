# -*- coding: utf-8 -*-
from flask import Flask, request, jsonify
from flask_assistant import Assistant, ask, tell, context_manager
import requests

app = Flask(__name__)
assist = Assistant(app, route='/')

@app.route('/')
def index():
    return "Hello, World!"

@assist.action('trash')
def search():
    name = request.json["result"]["parameters"]["cities"]
    return ask('確かに' + name)

@assist.action('give-employee')
def retrieve_position():
 if request.headers['Content-Type'] != "application/json; charset=UTF-8":
        print(request.headers['Content-Type'])
        return jsonify(res='error'), 400

 name = request.json["result"]["parameters"]["employee"]
 splitName = name.split(",")
 familyName = splitName[0]
 givenName =  splitName[1]

  # ここにAPIを呼ぶ処理
 baseUrl = "https://www.team1-internship-asia-quest.net:80" 

 apiUrl = baseUrl + "/employee?family_name=" + familyName + "&given_name=" + givenName
 result = requests.get(apiUrl)
 if result.status_code != 200:
        return jsonify(res='error'), 400

 json = result.json()
 position = str(json[0]["position"]).decode('unicode-escape')
 speech = familyName + "さんは" + position + "にいます。"

 return ask(speech)

@assist.action('give-date')
def get_schedule():
 if request.headers['Content-Type'] != "application/json; charset=UTF-8":
        print(request.headers['Content-Type'])
        return jsonify(res='error'), 400
 # 日付のタイムゾーンをISO8601の日本時間に変換
 time = request.json["result"]["parameters"]["date-time"]
 if time[-1:] == 'Z':
        time = time[:-1]

 apiUrl = 'http://18-summer-internship-demo.tk/api/schedule'
 payload = {'datetime': time} 
 result = requests.get(apiUrl, params=payload)
 json = result.json()
 
 if result.status_code == 404:
        return ask(json["message"])
 elif result.status_code != 200:
        return jsonify(res='error'), 400
 
 summary = json["summary"]
 start = json["event_start"]
 end = json["event_end"]
 speech = start + "から" + end + "に" +  summary + "の予定があります"
 return ask(speech)

if __name__ == '__main__':
    app.run()
