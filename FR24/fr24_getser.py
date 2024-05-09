from flask import Flask, request, jsonify,send_file, render_template
import fr24爬虫test as frpc
import datetime
import time
import os
from flask_limiter import Limiter
import pickle #保存字典
#全局信息
file_path = os.path.dirname(os.path.abspath(__file__))
app = Flask(__name__, template_folder=f'{file_path}\\template')
ip_counter = {}
ip_counter_file = f'{file_path}\\dic\\ip_counter.pkl'
if not os.path.exists(ip_counter_file):
    os.makedirs(os.path.dirname(ip_counter_file), exist_ok=True)
# 获取当前时间
timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H.%M.%S')
#限制ip访问次数
def get_remote_address():
    return request.remote_addr
limiter = Limiter(app=app, key_func=get_remote_address) # type: ignore
#机型筛选
jet_type = ["A33",'A34',"A35","A38","B78","B77","B76","B74","B75","B78","C9",'74','76','75','77','78','33','35','380','C27']
#返回首页HTML
@app.route('/')
def home():
    return render_template('FR24_flight_data.html')

#接受HTTP请求输入机场代码
@app.route('/input_airport_code', methods=['POST'])
def input_airport_code():
        # 获取客户端的IP地址
    ip_address = request.remote_addr

    # 在字典中更新IP地址的访问次数
    if ip_address in ip_counter:
        ip_counter[ip_address] += 1
    else:
        ip_counter[ip_address] = 1
        # 将更新后的IP计数器存储到本地字典存档
    with open(ip_counter_file, 'wb') as f:
        pickle.dump(ip_counter, f)
    
    if 'airport_code' not in request.form:#检查是否有该名称的输入
        return "Bad request", 400

    airport_code = request.form['airport_code']
    
    # 检查输入是否符合3个或4个英文字符
    if not airport_code.isalpha() or len(airport_code) < 3 or len(airport_code) > 4:
        return "Invalid airport code", 400
    #转大写
    airport_code = request.form['airport_code'].upper()
    output_filename = f'{airport_code}_{timestamp}.xlsx'

    return get_flights(airport_code,output_filename)

#获取航班数据并返回文件路径
def get_flights(apcode,output_filename):
    
    ip_address = request.remote_addr
    #接受HTTP请求
    # airport_code = request.args.get('airport_code', default='', type=str)
    # data = request.args.getlist('mode')
    
    data_mode = ['departures', 'arrivals']
    # 调用你的get_flight_data函数
    final_path = frpc.run(apcode, data_mode, jet_type, output_filename,ip_address)
    if isinstance(final_path, tuple) and final_path[1] == 500:  # 检查是否返回了错误信息
        return jsonify({"message": final_path[0]}), 500  # 返回错误信息

    if final_path:
        print(f'{final_path}')
        return send_file(f'{final_path}', as_attachment=True)
    else:
        return jsonify({"message": "请稍等片刻"})


if __name__ == '__main__':
    app.run(host='0.0.0.0',port=1145, debug=True)