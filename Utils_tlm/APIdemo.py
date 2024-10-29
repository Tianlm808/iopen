import os
import base64
import requests

# 设置 API 密钥和 API 基础 URL
# api_key = "sk-Ah4NTa5SZxF4f6wU155bA6FeA26f47Ff99A5Fc1bA05a0fAf"  # 替换为实际的 API Key
# api_base = "https://api.apiyi.com/v1"
api_key = "kbPvOnoBoKaCwneSBb58A704BaBd4d33A4E27e88C6Cb5008"  # 替换为实际的 API Key
api_base = "https://api.wumingai.com/v1"
# 文件夹路径和输出文件
image_folder = './test'
output_file = "./out.txt"

# 编码图片为 Base64
def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

# 遍历文件夹中的所有图片并生成描述
with open(output_file, "w", encoding="utf-8") as f:
    for filename in os.listdir(image_folder):
        if filename.endswith((".png", ".jpg", ".jpeg")):
            image_path = os.path.join(image_folder, filename)
            base64_image = encode_image(image_path)

            # 设置请求头和数据
            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {api_key}"
            }

            payload = {
                "model": "gpt-4o",
                "messages": [
                    {
                        "role": "user",
                        "content": [
                            {"type": "text", "text": "用50个字描述图片中的突出目标，比如车，飞机，建筑的颜色，数量，分布情况等特点"},
                            {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"}}
                        ]
                    }
                ],
                "max_tokens": 300
            }

            # 发送请求
            response = requests.post(f"{api_base}/chat/completions", headers=headers, json=payload)
            result = response.json()

            # 获取生成的描述文本
            description = result.get("choices", [{}])[0].get("message", {}).get("content", "").strip()

            # 写入文件，格式：图片名称：描述
            f.write(f"{filename}：{description}\n")

print("图片描述已生成并保存到", output_file)
