from flask import Flask, request, jsonify
import re
import threading

app = Flask(__name__)

latest_sms = None
lock = threading.Lock()

def reset_otp():
    global latest_sms
    with lock: 
        latest_sms = None
        print("OTP value reset to None")

@app.route('/')
def home():
    return "This app developed by Tanvir Mahamud Shariful"

@app.route('/forward_sms', methods=['POST'])
def forward_sms():
    global latest_sms
    data = request.get_json()
    message = data.get('message', '')
    otp = re.search(r'\b\d{6}\b', message)

    if otp:
        with lock: 
            latest_sms = otp.group()
        print(f"OTP: {latest_sms}")
        
      
        timer = threading.Timer(120, reset_otp)
        timer.start()
    else:
        print("OTP not found")
    
    return jsonify({'status': 'success', 'message': 'SMS forwarded successfully!'}), 200

@app.route('/otp', methods=['GET'])
def get_sms():
    with lock:  
        if latest_sms:
            return jsonify({"otp": latest_sms}), 200
        else:
            return jsonify({"error": "No SMS received yet"}), 404

if __name__ == '__main__':
    app.run(debug=True)
