import json

from flask import Flask, render_template, request
import requests

app = Flask(__name__)


def send_message_with_button(text, button_text, button_url, bot_token, chat_id):
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    payload = {"chat_id": chat_id, "text": text,
               "reply_markup": {"inline_keyboard": [[{"text": button_text, "callback_data": button_url}]]}}
    response = requests.post(url, json=payload)
    return response.json()


@app.route('/form/')
def get_form():
    id_user = request.args.get('id_user')
    with open(f'static/{id_user}.json', 'r', encoding='utf-8') as file:
        data = json.loads(file.read())

    return render_template("form.html", data=data['tems'], id_user=data['id_user'])


@app.route('/save/', methods=['POST'])
def save_form():
    data = dict(request.form)
    save_data = {}
    id_user = data['id_user']
    time_repeate = data['time']
    with open(f'static/{id_user}.json', 'r', encoding='utf-8') as file:
        old_data = json.loads(file.read())
    del data['id_user']
    del data['time']
    for i in data:
        if 'suboption' not in i:
            save_data[i] = []
        else:
            klass = i.split('-')[0]
            num = i.split('-')[1].replace('suboption', '')
            klass_num = klass.replace('klass_', '')
            save_data[klass].append(old_data['tems'][klass_num][int(num)])

    out_data = {"time": time_repeate, "tems": save_data}
    with open(f'static/{id_user}.json', 'w', encoding='utf-8') as file:
        file.write(json.dumps(out_data))
    bot_token = '7385714840:AAHlyQdM85RjBl7pklB0mAGlU7d6AYy1950'
    chat_id = int(id_user)
    file_path = f"static/{id_user}.json"
    resp = send_message_with_button('Для завершения настройки нажмите кнопку "завершить"', 'завершить', 'end_setting', bot_token, chat_id)
    return resp


@app.route('/', methods=['POST'])
def get_form1():
    data = json.loads(request.get_json())
    with open(f'static/{data["id_user"]}.json', 'w', encoding='utf-8') as file:
        file.write(json.dumps(data))
    return 'ok'


app.run(debug=True)
