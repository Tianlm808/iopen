import os
import json

# 定义类别字典，将标签名称转换为 YOLO 的 class_id
class_dict = {
    "car": 0,
    "airplane": 1,
    "powerline": 2,
    "pylon": 3,
    "bulldozers": 4,
    "trucks": 5,
    "cranes": 6
}


def convert_polygon_to_bbox(points, img_width, img_height):
    """
    将多边形的点转换为矩形包围盒，并归一化 YOLO 格式 (x_center, y_center, width, height)
    """
    x_coordinates = [p[0] for p in points]
    y_coordinates = [p[1] for p in points]

    x_min = min(x_coordinates)
    y_min = min(y_coordinates)
    x_max = max(x_coordinates)
    y_max = max(y_coordinates)

    # 计算中心坐标、宽度和高度，并归一化
    x_center = (x_min + x_max) / 2.0 / img_width
    y_center = (y_min + y_max) / 2.0 / img_height
    width = (x_max - x_min) / img_width
    height = (y_max - y_min) / img_height

    return x_center, y_center, width, height


def convert_json_to_txt(json_folder, txt_folder):
    """
    将指定文件夹中的所有 JSON 文件转换为 YOLO 格式的 .txt 文件
    """
    # 如果标签保存的文件夹不存在，创建它
    if not os.path.exists(txt_folder):
        os.makedirs(txt_folder)

    # 遍历 JSON 文件夹中的所有文件
    for json_file_name in os.listdir(json_folder):
        if json_file_name.endswith(".json"):
            json_file_path = os.path.join(json_folder, json_file_name)

            # 打开并读取 JSON 文件
            with open(json_file_path, 'r') as f:
                data = json.load(f)

            # 获取图像的宽度和高度 (你可以从数据中获取或预先指定)
            img_width = 1024  # 这里是假设的图像宽度，根据实际情况调整
            img_height = 1024  # 这里是假设的图像高度，根据实际情况调整

            # 构造对应的 .txt 文件路径
            txt_file_name = json_file_name.replace(".json", ".txt")
            txt_file_path = os.path.join(txt_folder, txt_file_name)

            # 打开 .txt 文件以写入 YOLO 格式标签
            with open(txt_file_path, 'w') as txt_file:
                for shape in data['shapes']:
                    class_label = shape['label']
                    points = shape['points']

                    # 获取类别的 ID
                    if class_label in class_dict:
                        class_id = class_dict[class_label]
                    else:
                        print(f"警告: 未知的类别 {class_label} 在文件 {json_file_name}")
                        continue

                    # 转换多边形为包围盒（bounding box）
                    x_center, y_center, width, height = convert_polygon_to_bbox(points, img_width, img_height)

                    # 写入到 .txt 文件中
                    txt_file.write(f"{class_id} {x_center:.6f} {y_center:.6f} {width:.6f} {height:.6f}\n")

            print(f"转换完成: {json_file_name} -> {txt_file_name}")


# 文件夹路径
json_folder_path = './car'  # JSON 文件夹路径
txt_folder_path = './labels/val'  # 保存生成的 .txt 文件的路径

# 开始转换
convert_json_to_txt(json_folder_path, txt_folder_path)
