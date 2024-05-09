from flask import Flask, render_template,request
import requests 
import fr24爬虫test as frpc
app = Flask(__name__, template_folder='C:\\Users\\EddieChen\\Documents\\works\\clear workspace\\FR24\\template')

@app.route('/')
def home():
    return render_template('FR24_flight_data.html')

@app.route('/submit', methods=['POST'])
def submit():
    message = request.form['message']
    
    return '消息已收到'
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=1145, debug=True)

