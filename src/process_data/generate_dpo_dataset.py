# python generate_dpo_dataset.py \
# --image_dir /root/thyroid/data/data/trainset \
# --output_dir /root/thyroid/LLaMA-Factory/LLaMA-Factory-main/data \
# --output_name thyroid_dpo.json
import json
import random
import os
from pathlib import Path
import argparse

# 系统提示
PROMPT = """# Role: Thyroid Imaging Diagnostic Assistant
## Task:
Analyze thyroid lymph node ultrasound images to classify them as **"diseased"** or **"normal"**.
## Key Features to Analyze:
1. Shape: Round or oval
2. Aspect ratio < 2
3. Irregular morphology or confluence
4. Vascular flow signals
5. Poorly defined or absent hilum
6. Calcifications, cystic degeneration, or necrosis
7. Heterogeneous or hyperechoic internal echoes"""

# 定义问题和答案模板
TEMPLATES = {
    'zh': {
        'questions': [
            "甲状腺是否有疾病？",
            "甲状腺是否存在病变？",
            "甲状腺是否有病？",
            "甲状腺功能是否正常？"
        ],
        'answers': {
            'positive': ["有病"],
            'negative': ["没病"]
        }
    },
    'en': {
        'questions': [
            "Does the thyroid have any diseases?",
            "Are there any abnormalities in the thyroid?",
            "Is there a problem with the thyroid?",
            "Is the thyroid function normal?"
        ],
        'answers': {
            'positive': ["sick"],
            'negative': ["not sick"]
        }
    }
}

def create_dpo_entry(image_path):
    # 确定是否为病例
    is_sick = "-P0" not in image_path
    
    # 随机选择语言
    lang = random.choice(['zh', 'en'])
    
    # 随机选择问题和答案
    question = random.choice(TEMPLATES[lang]['questions'])
    
    # 根据是否为病例选择正确和错误的答案
    if is_sick:
        chosen = random.choice(TEMPLATES[lang]['answers']['positive'])
        rejected = random.choice(TEMPLATES[lang]['answers']['negative'])
    else:
        chosen = random.choice(TEMPLATES[lang]['answers']['negative'])
        rejected = random.choice(TEMPLATES[lang]['answers']['positive'])
    
    return {
        "conversations": [
            {
                "from": "system",
                "value": PROMPT
            },
            {
                "from": "human",
                "value": f"<image>{question}"
            }
        ],
        "chosen": {
            "from": "gpt",
            "value": chosen
        },
        "rejected": {
            "from": "gpt",
            "value": rejected
        },
        "images": [image_path]
    }

def generate_balanced_dataset(image_dir):
    # 分类存储图片路径
    categorized_images = {
        'sick': [],
        'healthy': []
    }
    
    # 遍历并分类图片
    for image_path in Path(image_dir).glob("*.png"):
        category = 'healthy' if "-P0" in str(image_path) else 'sick'
        categorized_images[category].append(str(image_path))
    
    # 获取最小类别数量
    min_count = min(len(categorized_images['sick']), 
                   len(categorized_images['healthy']))
    
    # 随机采样平衡数据集
    selected_healthy = random.sample(categorized_images['healthy'], min_count)
    selected_sick = random.sample(categorized_images['sick'], min_count)
    
    # 合并并打乱数据
    all_images = selected_healthy + selected_sick
    random.shuffle(all_images)
    
    # 生成数据集
    dataset = [create_dpo_entry(img_path) for img_path in all_images]
    
    return dataset, min_count

def parse_args():
    parser = argparse.ArgumentParser(description='Generate DPO dataset for thyroid image classification')
    parser.add_argument('--image_dir', type=str, required=True,
                      help='Directory containing the thyroid images')
    parser.add_argument('--output_dir', type=str, required=True,
                      help='Directory to save the output JSON file')
    parser.add_argument('--output_name', type=str, default='thyroid_dpo.json',
                      help='Name of the output JSON file')
    return parser.parse_args()

def main():
    args = parse_args()
    
    # 创建输出目录
    os.makedirs(args.output_dir, exist_ok=True)
    
    # 生成数据集
    dataset, samples_per_class = generate_balanced_dataset(args.image_dir)
    
    # 保存数据集
    output_file = os.path.join(args.output_dir, args.output_name)
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(dataset, f, ensure_ascii=False, indent=2)
    
    # 打印统计信息
    print(f"数据集已保存至: {output_file}")
    print(f"每类样本数量: {samples_per_class}")
    print(f"总样本数量: {len(dataset)}")

if __name__ == "__main__":
    main() 