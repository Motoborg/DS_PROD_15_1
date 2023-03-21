# pip install flask

# Теперь импортируем его и создадим объект Flask-приложения.
from flask import Flask, request, jsonify
import datetime
import pickle
import numpy as np

app = Flask(__name__)

# Теперь мы можем написать функцию, которая будет обрабатывать запросы, и прикрепить её к какому-то пути (URI). 
# Это делается с помощью специального декоратора route.
@app.route('/hello')
def hello_func():
    name = request.args.get('name')
    return f'hello {name}!'

@app.route('/')
def index():
    return 'Test message. The server is running'

@app.route('/time')
def current_time():
    now = datetime.datetime.now()
    dic = {"time": now}
    return dic

# Укажем, что функция обрабатывает метод POST:
@app.route('/add', methods=['POST'])
# Напишем саму функцию:
def add():
    num = request.json.get('num')
    if num > 10:
        return 'too much', 400
    return jsonify({
        'result': num + 1
    })

with open('./model_for_web.pkl', 'rb') as pkl_file: 
    model_web = pickle.load(pkl_file)
    
@app.route('/predict', methods=['POST'])
# Напишем саму функцию:
def predict():
    features = np.array(request.json)
    features = features.reshape(1, 4)
    prediction = model_web.predict(features)
    return  jsonify({'prediction': prediction[0]})

# Нам осталось запустить приложение. 
# Для этого выполним метод run, не забыв занести его в стандартный main.

# Примечание. В блоке if __name__ == '__main__' прописывается код, 
# который не должен выполняться при импорте модуля. Переменная __name__ — это специальная переменная, 
# которая будет равна "__main__", только если файл запускается как основная программа, 
# и выставляется равной имени модуля при импорте модуля.

# Например, если мы захотим импортировать файл server.py как внешний модуль,
# то код, указанный в блоке if __name__ == '__main__', 
# соответствующий запуску сервера, не будет выполнен.

# from server import *

# Напишите новую функцию index(), которая будет возвращать строку "Test message. The server is running". 
# Оберните эту функцию в декоратор app.route(), указав в качестве эндпоинта '/'.
# см. выше строку 18

# Параметры запроса во Flask находятся в специальном объекте request, который нужно импортировать. 
# Параметры адресной строки можно найти в поле args этого объекта, где args — это словарь.



if __name__ == '__main__':

    app.run('localhost', 5000)