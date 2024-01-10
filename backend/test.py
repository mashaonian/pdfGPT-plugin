import json

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

# 测试函数
request_body = {
    "yiyan_info": "[{\"role\":\"user\",\"content\":\"<file>papermage.pdf</file><url>https://dwz.cn/1rTiz9in</url>\"},{\"role\":\"assistant\",\"content\":\"上传文件成功，欢迎根据PDF进行提问。\"}]",
    "query": "这篇文章的作者是谁？"
}

url = get_url_from_history(request_body["yiyan_info"])
print(url)