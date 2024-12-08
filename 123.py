import requests
import json

data = json.dumps({'id_user':731866035, "tems":{'7':['a','b','c']}})
res = requests.post('http://127.0.0.1:5000/', json=data)




#def send_json_file(bot_token, chat_id, file_path):
#    url = "https://api.telegram.org/bot{}/sendDocument".format(bot_token)
#    files = {'document': open(file_path, 'rb')}
#    data = {'chat_id': chat_id}
#    response = requests.post(url, files=files, data=data)
#    return response.json()

