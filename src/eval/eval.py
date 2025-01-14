# api_call_example.py
from openai import OpenAI
import base64
from pathlib import Path
import json
from tqdm import tqdm
import numpy as np
from sklearn.metrics import confusion_matrix, classification_report

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
7. Heterogeneous or hyperechoic internal echoes
## Rules:
- Focus only on thyroid lymph nodes.
- Be objective and consistent.
- Avoid diagnosing other organs or suggesting treatments.
## Output Format:
```json
{
"classification": "diseased or normal"
}
```"""

def encode_image(image_path):
    """将图片转换为 base64 编码"""
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

def calculate_metrics(all_results):
    """计算混淆矩阵和相关指标"""
    y_true = []
    y_pred = []
    
    for result in all_results:
        if result["success"]:
            try:
                # 解析模型响应中的分类结果
                response = json.loads(result["model_response"])
                predicted_label = response.get("classification", "").lower()
                
                # 添加真实标签和预测标签
                y_true.append(result["true_label"])
                y_pred.append(predicted_label)
            except:
                print(f"Error parsing response for {result['image_path']}")
    
    # 计算混淆矩阵
    labels = ["normal", "diseased"]
    conf_matrix = confusion_matrix(y_true, y_pred, labels=labels)
    
    # 计算详细的分类指标
    report = classification_report(y_true, y_pred, labels=labels, output_dict=True)
    
    # 计算准确率、精确率、召回率和F1分数
    metrics = {
        "confusion_matrix": conf_matrix.tolist(),
        "classification_report": report,
        "total_samples": len(y_true)
    }
    
    return metrics

def evaluate_model(image_dir: str, output_file: str = '/root/medical/evaluation_results.json'):
    """评估模型性能
    Args:
        image_dir: 图片目录路径
        output_file: 评估结果输出文件路径
    """
    client = OpenAI(
        api_key="0",
        base_url="http://0.0.0.0:8000/v1"
    )
    
    image_paths = list(Path(image_dir).glob("*.png"))[:10]
    all_results = []  # 存储所有结果
    
    # 顺序处理每张图片
    for image_path in tqdm(image_paths, desc="Processing images"):
        try:
            true_label = "normal" if "-p0" in str(image_path).lower() else "diseased"
            base64_image = encode_image(str(image_path))
            
            # 构造API请求消息
            messages = [
                {
                    "role": "system",
                    "content": PROMPT
                },
                {
                    "role": "user",
                    "content": "<image>Does the thyroid have any diseases?"
                }
            ]
            
            # 构造完整的请求数据
            request_data = {
                "messages": messages,
                "images": [f"data:image/png;base64,{base64_image}"]
            }
            
            # 发送API请求
            result = client.chat.completions.create(
                model="/root/medical/qwen2_vl/",
                messages=[{
                    "role": "user",
                    "content": json.dumps(request_data)
                }],
                max_tokens=1000
            )
            
            response = result.choices[0].message.content
            print(f"Image: {image_path}")
            print(f"Response: {response}")
            
            all_results.append({
                "image_path": str(image_path),
                "true_label": true_label,
                "model_response": response,
                "success": True
            })
            
        except Exception as e:
            print(f"Error processing {image_path}: {e}")
            all_results.append({
                "image_path": str(image_path),
                "true_label": true_label,
                "model_response": f"Error: {str(e)}",
                "success": False
            })
    
    try:
        # 计算评估指标
        metrics = calculate_metrics(all_results)
        
        # 准备完整的评估结果
        evaluation_results = {
            "predictions": all_results,
            "metrics": metrics
        }
        
        # 写入所有结果到JSON文件
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(evaluation_results, f, indent=2, ensure_ascii=False)
        
        # 打印评估指标
        print("\n=== Evaluation Metrics ===")
        print("\nConfusion Matrix:")
        print("             Predicted Normal  Predicted Diseased")
        print(f"True Normal      {metrics['confusion_matrix'][0][0]}                {metrics['confusion_matrix'][0][1]}")
        print(f"True Diseased    {metrics['confusion_matrix'][1][0]}                {metrics['confusion_matrix'][1][1]}")
        
        print("\nClassification Report:")
        report = metrics['classification_report']
        for label in ['normal', 'diseased']:
            print(f"\n{label.capitalize()}:")
            print(f"Precision: {report[label]['precision']:.3f}")
            print(f"Recall: {report[label]['recall']:.3f}")
            print(f"F1-score: {report[label]['f1-score']:.3f}")
        
        print(f"\nAccuracy: {report['accuracy']:.3f}")
        print(f"Total samples: {metrics['total_samples']}")
        
        # 验证文件是否写入成功
        with open(output_file, 'r', encoding='utf-8') as f:
            json.load(f)
        print(f"\nResults file written and verified successfully: {output_file}")
        
    except Exception as e:
        print(f"Error writing results: {e}")
        raise

if __name__ == "__main__":
    image_dir = "/root/medical/medical_testset"
    output_file = "/root/medical/evaluation_results.json"
    evaluate_model(image_dir, output_file)