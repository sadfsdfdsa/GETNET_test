from flask import Flask, request, render_template
import json
from utils.utils import email_sender
import random

# Передача персональных данных проверяется секретным кодом пользователя (заглушка для JWT)
# Передача данных идет с помощью axios - post запросами (ajax аналог, легко меняется)
# Формат передачи: json
# Frontend реализован с помощью подключаемого ядра Vue, но не сделан Router.
# Запросы к API реализованы согласно REST: GET, POST, PUT, не реализованы: PATCH, DELETE.
# Базовый пользователь: sh@mail.ru 123; После регистрации сбрасывается!
# Не реализована эмуляция кнопки "назад" на фронте, не реализована эмуляция смены url адресов для удобства использования.


# custom flask app without basic templates (error with {{vue variables}}
class CustomFlask(Flask):
    jinja_options = Flask.jinja_options.copy()
    jinja_options.update(dict(
        variable_start_string='%%',
        variable_end_string='%%',
    ))


app = CustomFlask(__name__)

# user data and array with users (one element)
user_balance = {'balance': 1050, 'history': [{'date': '15.06.2019', 'action': '+', 'value': 500},
                                             {'date': '08.06.2019', 'action': '-', 'value': 740}]}
user_history = [{'date': '08.06.2019', 'service': 'оплата услуги "интернет"', 'value': 740, 'company': 'getnet'},
                {'date': '08.05.2019', 'service': 'оплата услуги "интернет"', 'value': 740, 'company': 'getnet'}]
user = {'id': 0, 'name': 'artem', 'email': 'sh@mail.ru', 'password': '123', 'scode': 'secret_code'}
users = [user]

# new user model
new_user = {'id': 0, 'email': None, 'code': None, 'password': None, 'name': 'name', 'scode': 'secret_code'}

# API


@app.route('/api/v1/registration', methods=['POST'])
def reg():
    global new_user
    data = request.json
    user_email = data['email']
    user_password = data['password']
    code = random.randint(101, 999)
    print('code', code)
    email_sender(str(code), user_email)
    new_user['email'] = user_email
    new_user['code'] = str(code)
    new_user['password'] = user_password
    return json.dumps({'data': 'data'})


@app.route('/api/v1/code_approve', methods=['POST'])
def approve():
    global user, new_user
    data = request.json
    if data['code'] == new_user['code']:
        print('post user', new_user)
        user = new_user
        return json.dumps(new_user)
    else:
        return json.dumps({'error': 'error'})


@app.route('/api/v1/auth', methods=['POST'])
def auth():
    global user
    data = request.json
    if data['email'] == user['email'] and data['password'] == user['password']:
        print('auth user', data)
        return json.dumps(user)
    else:
        return json.dumps({'error': 'error'})


@app.route('/api/v1/user', methods=['PUT'])
def put_user():
    global user
    data = request.json
    if data['scode'] == user['scode']:
        print('put user', data)
        user = data
    return json.dumps({'success': 'success'})


@app.route('/api/v1/user/<int:user_id>/<string:action>', methods=['GET'])
def get_data(user_id, action):
    code_header = request.headers['scode']
    if users[user_id]['scode'] == code_header:
        if action == 'balance':
            return json.dumps(user_balance)
        elif action == 'history':
            return json.dumps(user_history)
        else:
            return json.dumps({'error': 'error'})
    else:
        return json.dumps({'error': 'error'})


# INDEX HTML WITH VUE APP
@app.route('/')
def index():
    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)

