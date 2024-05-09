from flask import Flask, request, jsonify, send_file, render_template, redirect
import datetime
import json
import os
from flask_limiter import Limiter
import pandas as pd

import fr24爬虫test as frpc
import pickle  # 保存字典
import streamlit as st  # 绘图
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
#机型筛选依据
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

    return jsonify({'redirect': f'/{airport_code}/flights'})

#获取航班数据并返回文件路径
'''def get_flights(apcode,output_filename):#请求excel文件的函数
    
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
'''

def get_flights(apcode):#调用爬虫请求json文件
    
    ip_address = request.remote_addr
    #接受HTTP请求
    # airport_code = request.args.get('airport_code', default='', type=str)
    # data = request.args.getlist('mode')
    
    data_mode = ['departures', 'arrivals']
    # 调用你的get_flight_data函数
    final_a_path,final_d_path = frpc.run(apcode, data_mode, jet_type,ip_address)
    
    # if isinstance(final_a_path, tuple) and final_a_path[1] == 500:  # 检查到达数据路径是否返回了错误信息
    #     return jsonify({"message": final_a_path[0]}), 500  # 返回错误信息
    # elif isinstance(final_d_path, tuple) and final_d_path[1] == 500:  # 检查出发数据路径是否返回了错误信息
    #     return jsonify({"message": final_d_path[0]}), 500  # 返回错误信息
    # if final_a_path and final_d_path:
    
    print(f'{final_a_path},{final_d_path}')
    return final_a_path,final_d_path#输出2个json文件的路径

@app.route('/<apcode>/flights')
def flights(apcode):#与html交互
    arrivals_data_path, departures_data_path = get_flights(apcode)
    if arrivals_data_path is None or departures_data_path is None:
        return "Error: No flight data available for the given airport code", 400
    
    a_i_table_html,a_n_table_html = to_DataFrame(arrivals_data_path)
    
    d_i_table_html,d_n_table_html = to_DataFrame(departures_data_path)
    
    return render_template('flights.html', a_i_table=a_i_table_html, a_n_table=a_n_table_html,airport_code=apcode, d_i_table=d_i_table_html, d_n_table=d_n_table_html)

def process_flights_data(flight_data_path):#数据筛选
    if flight_data_path[-21:-13] != 'arrivals':#判断json数据是or到达
        word = 'destination'
        status = 'departure'
    else:
        word = 'origin'
        status = 'arrival'
    interested_aircraft = []
    normal_aircraft = []
    with open(str(flight_data_path), 'r') as f:
        all_flights = json.load(f)
    for flight in all_flights:#遍历获取的航班信息
        model_code = flight['flight']['aircraft']['model']['code']
        arrivals_time = flight['flight']['time']['scheduled'][f'{status}']
    # 转化为北京时间
        arrivals_time = datetime.datetime.fromtimestamp(arrivals_time).strftime('%Y-%m-%d %H:%M:%S')
        
        if any( model_code is None or substring in model_code for substring in jet_type):#分类航班
                flight_number = flight['flight']['identification']['number']['default']
                arrival_time = datetime.datetime.fromtimestamp(flight['flight']['time']['scheduled'][f'{status}']).strftime('%Y-%m-%d %H:%M:%S')
                origin_airport = flight['flight']['airport'][f'{word}']['code']['iata']
                registration = flight['flight']['aircraft']['registration']
                code = flight['flight']['aircraft']['model']['code']
                interested_aircraft.append([flight_number, arrival_time, origin_airport, registration if registration else 'None', code if code else None])
        else:
                flight_number = flight['flight']['identification']['number']['default']
                arrival_time = datetime.datetime.fromtimestamp(flight['flight']['time']['scheduled'][f'{status}']).strftime('%Y-%m-%d %H:%M:%S')
                origin_airport = flight['flight']['airport'][f'{word}']['code']['iata']
                registration = flight['flight']['aircraft']['registration']
                code = flight['flight']['aircraft']['model']['code']
                normal_aircraft.append([flight_number, arrival_time, origin_airport, registration if registration else 'None', code if code else None])
    return interested_aircraft, normal_aircraft

def to_DataFrame(data_path):#绘制表格
    if data_path[-21:-13] != 'arrivals':#判断json数据是or到达
        word1 = '起飞'
        word2 = '到达'
    else:
        word1 = '到达'
        word2 = '起飞'

    a_interested_aircraft, a_normal_aircraft = process_flights_data(data_path)
    # 将航班信息转换为DataFrame
    idf = pd.DataFrame(a_interested_aircraft, columns=["航班号", f'计划{word1}时间', f"{word2}地机场", "注册号", "机型"])
    ndf = pd.DataFrame(a_normal_aircraft, columns=["航班号", f'计划{word1}时间', f"{word2}地机场", "注册号", "机型"])
    # 使用Flask绘制表格
    a_i_table_html = idf.to_html(index=False)
    a_n_table_html = ndf.to_html(index=False)
    return a_i_table_html,a_n_table_html

if __name__ == '__main__':
    app.run(host='0.0.0.0',port=1145, debug=True)