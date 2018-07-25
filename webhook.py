from flask import Flask
from flask_assistant import Assistant, ask, tell
import logging

logging.getLogger('flask_assistant').setLevel(logging.DEBUG)

app = Flask(__name__)
assist = Assistant(app, route='/')

@assist.action('give-emplyee')
def retrieve_position():
# if request.headers['Content-Type'] != 'application/json':
#         print(request.headers['Content-Type'])
#         return flask.jsonify(res='error'), 400
#
#     name = request.json["request"]["parameters"]
    # ここにAPIを呼ぶ処理
    name = "ゆきえ"
    speech = name + "さんはカフェにいます。"
    # speech = name　"さんは" time "ごろ"　position "にいました。"


    return ask(speech)

if __name__ == '__main__':
    app.run(debug=True)
