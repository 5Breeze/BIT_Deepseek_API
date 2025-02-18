import requests
import json
import yaml

# 从config.yaml加载badge值
def load_config():
    try:
        with open('config.yaml', 'r', encoding='utf-8') as file:
            config = yaml.safe_load(file)
            return config.get('badge')
    except FileNotFoundError:
        print("配置文件 config.yaml 未找到！")
        return None
    except yaml.YAMLError as e:
        print(f"YAML解析错误：{e}")
        return None

url = "https://ibit.yanhekt.cn/proxy/v1/chat/stream/private/kb"

# 加载badge值
badge_value = load_config()
if not badge_value:
    print("没有找到有效的badge值，无法继续执行。")
    exit()

# 更新cookie中的badge_2
cookie_value = badge_value.rstrip('=') + '%3D'

headers = {
    "Host": "ibit.yanhekt.cn",
    "Connection": "keep-alive",
    "sec-ch-ua-platform": "\"Windows\"",
    "Authorization": "Bearer undefined",
    "Xdomain-Client": "web_user",
    "sec-ch-ua": "\"Not(A:Brand\";v=\"99\", \"Microsoft Edge\";v=\"133\", \"Chromium\";v=\"133\"",
    "sec-ch-ua-mobile": "?0",
    "badge": badge_value,  # 使用从config.yaml加载的badge值
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36 Edg/133.0.0.0",
    "DNT": "1",
    "Content-Type": "application/json",
    "x-assistant-id": "43",
    "Accept": "*/*",
    "Origin": "https://ibit.yanhekt.cn",
    "Sec-Fetch-Site": "same-origin",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Dest": "empty",
    "Cookie": f"badge_2={cookie_value}"  # 使用修改后的cookie值
}

payload = {
    "query": "今天天气怎么样呢？",
    "dialogue_id": 73224,
    "stream": True,
    "history": [
        {"role": "user", "content": "你好"},
        {"role": "assistant", "content": "<think>\n好，用户发来了..."}
    ],
    "temperature": 0.7,
    "top_k": 3,
    "score_threshold": 0.5,
    "prompt_name": "default",
    "knowledge_base_name": "cuc"
}

try:
    with requests.post(url, headers=headers, json=payload, stream=True) as response:
        response.encoding = 'utf-8'
        
        if response.status_code != 200:
            print(f"请求失败，状态码：{response.status_code}")
            print(response.text)
            exit()

        # 处理流式响应
        for line in response.iter_lines():
            if line:
                decoded_line = line.decode('utf-8')
                if decoded_line.startswith('data: '):
                    json_str = decoded_line[6:]  # 去掉 data: 前缀
                    try:
                        data = json.loads(json_str)
                        if 'answer' in data:
                            print(data['answer'], end='', flush=True)
                    except json.JSONDecodeError:
                        print(f"\nJSON 解析错误：{json_str}")

except requests.exceptions.RequestException as e:
    print(f"请求异常：{e}")
except KeyboardInterrupt:
    print("\n用户中断")
