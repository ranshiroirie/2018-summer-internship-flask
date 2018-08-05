# -*- coding: utf-8 -*-
from flask import Flask, request, jsonify
from flask_assistant import Assistant, ask, tell
import logging
import requests

logging.getLogger('flask_assistant').setLevel(logging.DEBUG)

app = Flask(__name__)
assist = Assistant(app, route='/')

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
 #baseUrl = "http://18-summer-internship-demo.tk/api" 
 baseUrl = "http://127.0.0.1:8000/api" 

 apiUrl = baseUrl + "/user/" + familyName + "/" + givenName + "/" + "position"
 result = requests.get(apiUrl)
 if result.status_code != 200:
        return jsonify(res='error'), 400

 json = result.json()
 print(json)
 position = json["beacon"]["position"]
 speech = familyName + "さんは" + position + "にいます。"

 return tell(speech)

@assist.action('give-date')
def get_schedule():
 if request.headers['Content-Type'] != "application/json; charset=UTF-8":
        print(request.headers['Content-Type'])
        return jsonify(res='error'), 400
 # 日付のタイムゾーンをISO8601の日本時間に変換
 time = request.json["result"]["parameters"]["date-time"][0]
 if time[-1:] == 'Z':
        time = time[:-1]

 apiUrl = 'http://18-summer-internship-demo.tk/api/schedule'
 payload = {'datetime': time} 
 result = requests.get(apiUrl, params=payload)
 json = result.json()
 
 if result.status_code == 404:
        return tell(json["message"])
 elif result.status_code != 200:
        return jsonify(res='error'), 400
 
 print(json)
 summary = json["summary"]
 start = json["event_start"]
 end = json["event_end"]
 speech = "直近の予定は" + summary + "開始時間" + start + "終了時間" + end + "です"
 print(speech)
 return ask(speech)

if __name__ == '__main__':
    app.run()
