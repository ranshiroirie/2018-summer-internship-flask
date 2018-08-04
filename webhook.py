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
 baseUrl = "http://18-summer-internship-demo.tk/api" 
 apiUrl = baseUrl + "/user/" + familyName + "/" + givenName + "/" + "position"
 result = requests.get(apiUrl)
 if result.status_code != 200:
        return jsonify(res='error'), 400

 json = result.json()
 print(json)
 position = json["beacon"]["position"]
 speech = familyName + "さんは" + position + "にいます。"

 return ask(speech)

@assist.action('give-date')
def get_schedule():
 if request.headers['Content-Type'] != "application/json; charset=UTF-8":
        print(request.headers['Content-Type'])
        return jsonify(res='error'), 400
 # 日付のタイムゾーンを変換
 time = request.json["result"]["parameters"]["date-time"]
 if time[-1:] == 'Z':
        time = time[:-1]

 print(time)
 print(time)
 print(time)
 baseUrl = 'http://18-summer-internship-demo.tk/api'
 apiUrl = baseUrl + "/schedule?" + time
 result = requests.get(apiUrl)
 if result.status_code != 200:
        return jsonify(res='error'), 400

 json = result.json()
 print(json)


if __name__ == '__main__':
    app.run()
