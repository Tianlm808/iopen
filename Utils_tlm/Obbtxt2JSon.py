import json
import os

def obb_txt_to_labelme_json(txt_file, json_file, image_width=1024, image_height=1024):
    shapes = []
    with open(txt_file, 'r') as f:
        for line in f:
            parts = line.strip().split()
            if len(parts) == 9:
                # 解析类别和四个归一化顶点坐标
                cls = parts[0]  # 类别
                # 反归一化坐标
                points = [(float(parts[i]) * image_width, float(parts[i + 1]) * image_height) for i in range(1, 9, 2)]

                # 创建 LabelMe 形状字典
                shape = {
                    "label": cls,
                    "points": points,
                    "group_id": None,
                    "shape_type": "polygon",
                    "flags": {}
                }
                shapes.append(shape)

    # 创建 LabelMe 格式的 JSON 数据
    labelme_data = {
        "version": "5.0.1",
        "flags": {},
        "shapes": shapes,
        "imagePath": os.path.basename(txt_file).replace('.txt', '.jpg'),
        "imageData": None,  # 不存储图像数据
        "imageHeight": image_height,
        "imageWidth": image_width
    }

    # 保存 JSON 文件
    with open(json_file, 'w') as f:
        json.dump(labelme_data, f, indent=4)
    print(f"Converted {txt_file} to {json_file}.")

# 设定要转换的文件路径
input_folder = '../predictions/'  # 你的 .txt 文件夹
output_folder = '../labelme_json/'  # 输出 .json 的文件夹

# 确保输出文件夹存在
os.makedirs(output_folder, exist_ok=True)

# 批量转换 .txt 文件到 .json 文件
for filename in os.listdir(input_folder):
    if filename.endswith('.txt'):
        txt_file = os.path.join(input_folder, filename)
        json_file = os.path.join(output_folder, filename.replace('.txt', '.json'))
        obb_txt_to_labelme_json(txt_file, json_file, image_width=1024, image_height=1024)
