from flask import Flask, jsonify, request

# Tạo đối tượng Flask
app = Flask(__name__)

# Định nghĩa route home, hỗ trợ cả GET và POST
@app.route('/', methods=['GET', 'POST'])
def home():
    return "Hello, World!"

# Route API trả về dữ liệu JSON
@app.route('/api/predict', methods=['GET', 'POST'])
def predict():
    # Mô hình dự đoán giả lập
    prediction = {
        'customer_id': 123,
        'purchase_probability': 0.85
    }
    return jsonify(prediction)

# Chạy server trên localhost
if __name__ == '__main__':
    app.run(debug=True)
