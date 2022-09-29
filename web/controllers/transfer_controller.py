from flask import Flask, request, jsonify

from services import transfer_service

app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/settle', methods=['POST'])
def initiate_transfer():
    data = request.json
    from_iban, to_iban, amount = data['from_iban'], data['to_iban'], data['amount']
    amount = amount if isinstance(amount, int) else int(amount)

    transfer_service.initiate_transfer(from_iban, to_iban, amount)

    return jsonify(dict(result=f'Transfer initiated from IBAN {from_iban} to IBAN {to_iban} for amount: {amount}'))


if __name__ == '__main__':
    app.run()
