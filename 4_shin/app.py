from flask import Flask, render_template, jsonify, request
from pymongo import MongoClient  # pymongo를 임포트

app = Flask(__name__)

client = MongoClient('localhost', 27017)  # mongoDB는 27017 포트로 돌아감.
db = client.dbhomework  # 'dbhomework'라는 이름의 db를 만듦


## HTML을 주는 부분
@app.route('/')
def homework():
    return render_template('index.html')


## 주문하기(POST) API 역할을 하는 부분
@app.route('/order', methods=['POST'])
def save_order():
    # 1. 클라이언트가 준 이름,수량,주소,전화번호 가져오기
    name_receive = request.form['name_give']
    count_receive = request.form['count_give']
    address_receive = request.form['address_give']
    phone_receive = request.form['phone_give']

    # 2. DB에 정보 삽입하기
    doc = {
        'name': name_receive,
        'count': count_receive,
        'address': address_receive,
        'phone': phone_receive
    }
    db.orders.insert_one(doc)

    # 3. 성공 여부 & 성공 메시지 반환하기
    return jsonify({'result': 'success', 'msg': '주문이 완료되었습니다!'})


@app.route('/order', methods=['GET'])
def view_orders():
    orders = list(db.orders.find({}, {'_id': False}))
    return jsonify({'result': 'success', 'orders': orders})


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
