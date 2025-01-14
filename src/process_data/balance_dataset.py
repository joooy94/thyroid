import json
import random
import os
from pathlib import Path
from collections import defaultdict

# 定义问题列表
chinese_questions = [
    "甲状腺是否有疾病？",
    "甲状腺是否存在病变？",
    "甲状腺是否有病？",
    "甲状腺功能是否正常？"
]

english_questions = [
    "Does the thyroid have any diseases?",
    "Are there any abnormalities in the thyroid?",
    "Is there a problem with the thyroid?",
    "Is the thyroid function normal?"
]

# 定义答案
chinese_answers = {
    True: "有病",
    False: "没病"
}

english_answers = {
    True: "sick",
    False: "not sick"
}

def create_json_entry(image_path):
    # 检查图片是否包含 "-P0_"
    is_sick = "-P0_" not in image_path
    
    # 随机决定使用中文还是英文
    use_chinese = random.choice([True, False])
    
    # 选择问题和答案
    question = random.choice(chinese_questions if use_chinese else english_questions)
    answer = chinese_answers[is_sick] if use_chinese else english_answers[is_sick]
    
    return {
        "messages": [
            {
                "content": f"<image>{question}",
                "role": "user"
            },
            {
                "content": answer,
                "role": "assistant"
            }
        ],
        "images": [
            image_path
        ]
    }

def generate_balanced_dataset(image_dir):
    # 用于存储不同类别的图片路径
    categorized_images = {
        'sick': [],
        'healthy': []
    }
    
    # 遍历并分类图片
    for image_path in Path(image_dir).glob("*.png"):
        if "-P0_" in str(image_path):
            categorized_images['healthy'].append(str(image_path))
        else:
            categorized_images['sick'].append(str(image_path))
    
    # 找出较少的类别的数量
    min_count = min(len(categorized_images['sick']), len(categorized_images['healthy']))
    
    # 从每个类别中随机选择相同数量的样本
    selected_healthy = random.sample(categorized_images['healthy'], min_count)
    selected_sick = random.sample(categorized_images['sick'], min_count)
    
    # 生成平衡后的数据集
    balanced_dataset = []
    
    # 合并并打乱所有选中的图片
    all_selected_images = selected_healthy + selected_sick
    random.shuffle(all_selected_images)
    
    # 为每张图片创建JSON条目
    for image_path in all_selected_images:
        entry = create_json_entry(image_path)
        balanced_dataset.append(entry)
    
    return balanced_dataset, min_count

def main():
    image_dir = "medical_data_output"  # 替换为你的图片目录路径
    
    # 生成平衡数据集
    dataset, samples_per_class = generate_balanced_dataset(image_dir)
    
    # 保存为 JSON 文件
    output_file = "balanced_thyroid_dataset.json"
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(dataset, f, ensure_ascii=False, indent=2)
    
    print(f"平衡数据集已保存到 {output_file}")
    print(f"每个类别的样本数量: {samples_per_class}")
    print(f"总样本数量: {len(dataset)}")
    
    # 统计最终数据集中的类别分布
    sick_count = sum(1 for item in dataset if "-P0_" not in item["images"][0])
    healthy_count = sum(1 for item in dataset if "-P0_" in item["images"][0])
    print(f"\n最终数据集统计:")
    print(f"有病样本数量: {sick_count}")
    print(f"正常样本数量: {healthy_count}")

if __name__ == "__main__":
    main() 