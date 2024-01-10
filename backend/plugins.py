from flask import Flask,request, Blueprint, send_from_directory, jsonify, make_response
from flask_cors import CORS
import functions.pdf as pdf
import json
import time 
import logging
# restful 跨域格式
#plugins = Blueprint("plugins", __name__)

# CORS 跨域

# 配置一个输出到控制台的处理器
app = logging.getLogger('app')
app.setLevel(logging.DEBUG)

console_handler = logging.StreamHandler()
file_handler = logging.FileHandler('app.log')
app.addHandler(console_handler)
app.addHandler(file_handler)



plugins = Flask(__name__)
CORS(plugins, resources={r"/*": {"origins": "https://yiyan.baidu.com"}})

def make_json_response(data, status_code=200):
    response = make_response(json.dumps(data), status_code)
    response.headers["Content-Type"] = "application/json"
    return response

# def get_url_from_history(yiyan_info):
#     yiyan_info = json.loads(yiyan_info)
    
#     for ino in range(len(yiyan_info)): 
#         role = yiyan_info[ino]['role']
#         content = yiyan_info[ino]['content']
#         if role == 'user' and '<url>' in content:
#             substr = content.split('<url>')
#             url = substr[1].split('<url>')[0]
#     return url
def get_url_from_history(yiyan_info_json):
    # 解析 JSON 字符串
    yiyan_info = json.loads(yiyan_info_json)
    
    # 遍历列表中的每个项目
    for item in yiyan_info:
        # 检查角色和内容
        role = item['role']
        content = item['content']
        # 如果是用户角色并且内容中包含 URL
        if role == 'user' and '<url>' in content:
            # 提取 URL
            start_index = content.find('<url>') + len('<url>')
            end_index = content.find('</url>', start_index)
            url = content[start_index:end_index]
            return url

@plugins.route("/pdf/load", methods=["POST"])
async def load_pdf():
        url = request.json.get('url',"")
        def event_stream():
        
            json_data1 = {"errCode": "0","actionName": "正在上传文件",
                          "actionContent": "上传文件完成",
                          "prompt":"上传文件成功，欢迎根据PDF进行提问"
                          }
            yield f"data:{json.dumps(json_data1, ensure_ascii=False)}\n\n"    

        return plugins.response_class(event_stream(), mimetype='text/event-stream')  

@plugins.route("/pdf/query", methods=["POST"])
async def query_pdf():
    # url = request.json.get('url',"")
    query = request.json.get('query',"")
    # 提问不再需要上传url，要把以前的url链接在每次提问中提取出来：
    yiyan_info_ori = request.json.get('yiyan_info', "")
    url = get_url_from_history(yiyan_info_ori)
    logging.info(url)

    import requests
    response = requests.get(url)
    with open('backend\corpus.pdf',"wb") as file:
        file.write(response.content)
    file.close()
    pdf.load_recommender('backend\corpus.pdf')
    answer = pdf.generate_answer(query)
    timestamp = str(time.time())
    def event_stream():
        json_data1 = {"errcode":"0",
                      "actionName":"正在上传文件",
                      "actionCentent":"上传文件成功"}
        yield f"data:{json.dumps(json_data1, ensure_ascii=False)}\n\n"
        time.sleep(1)
        json_data2 = {"errCode": "0",
                      "actionName": "正在解析文件",
                      "actionContent": "解析文件完成"}
        yield f"data:{json.dumps(json_data2, ensure_ascii=False)}\n\n"
        time.sleep(1)
        json_data_result = {"errCode": "0", 
                            "actionName": "正在输出回答", 
                            "actionContent": "输出回答完成", 
                            "answer": answer, 
                            "prompt": "根据答案（answer）生成答案的大纲"}
        logging.info(answer)
        yield f"data:{json.dumps(json_data_result, ensure_ascii=False)}\n\n"
    return plugins.response_class(event_stream(), mimetype='text/event-stream')

@plugins.route('/.well-known/<path:path>', methods=['GET'])
def serve_file(path):
    return send_from_directory('static', path)

@plugins.route('/')
def index():
    return 'welcome to my webpage!'


@plugins.route('/<path:path>', methods=['GET'])
def serve_file2(path):
    return send_from_directory('static', path)

if __name__ == '__main__':
    plugins.run(debug=True, host='127.0.0.1',port=3333)