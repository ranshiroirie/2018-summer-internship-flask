# -*- coding: utf-8 -*-
from flask import Flask, request, jsonify
from flask_assistant import Assistant, ask, tell, context_manager
import requests

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
 baseUrl = "http://18-summer-internship-demo.tk/api" 

 apiUrl = baseUrl + "/user/" + familyName + "/" + givenName + "/" + "position"
 result = requests.get(apiUrl)
 if result.status_code != 200:
        return jsonify(res='error'), 400

 json = result.json()
 position = json["beacon"]["position"]
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
