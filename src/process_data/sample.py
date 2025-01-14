import json
import random

def downsample_dataset(json_file, output_file):
    # 读取原始数据
    with open(json_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # 分离 normal 和 diseased 样本
    normal_samples = []
    diseased_samples = []
    
    for item in data:
        output_dict = json.loads(item['output'])
        if output_dict['classification'] == 'normal':
            normal_samples.append(item)
        else:
            diseased_samples.append(item)
    
    print(f"Original dataset:")
    print(f"Normal: {len(normal_samples)}")
    print(f"Diseased: {len(diseased_samples)}")
    
    # 降采样 diseased 到与 normal 相同数量
    balanced_diseased = random.sample(diseased_samples, len(normal_samples))
    
    # 合并数据集
    balanced_dataset = normal_samples + balanced_diseased
    random.shuffle(balanced_dataset)  # 随机打乱顺序
    
    # 保存新的平衡数据集
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(balanced_dataset, f, ensure_ascii=False, indent=2)
    
    print(f"\nBalanced dataset:")
    print(f"Normal: {len(normal_samples)}")
    print(f"Diseased: {len(balanced_diseased)}")
    print(f"Total samples: {len(balanced_dataset)}")
    
    return balanced_dataset

# 使用示例
balanced_data = downsample_dataset(
    'LLaMA-Factory/data/thyroid.json',
    'LLaMA-Factory/data/thyroid_balanced.json'
)