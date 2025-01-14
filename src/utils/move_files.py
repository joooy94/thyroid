import os
import shutil

def move_files(source_dir, target_dir):
    # 检查源目录是否存在
    if not os.path.exists(source_dir):
        print(f"错误：源目录 '{source_dir}' 不存在")
        return
        
    # 检查目标目录是否存在，如果不存在则创建
    if not os.path.exists(target_dir):
        os.makedirs(target_dir)
        print(f"已创建目标目录: {target_dir}")
    
    # 计数器
    moved_count = 0
    
    # 遍历源目录中的所有文件
    for filename in os.listdir(source_dir):
        # 检查文件是否以B、C、D开头
        if filename.startswith(('B', 'C', 'D', 'b', 'c', 'd')):
            source_path = os.path.join(source_dir, filename)
            target_path = os.path.join(target_dir, filename)
            
            try:
                # 移动文件
                shutil.move(source_path, target_path)
                print(f"已移动: {filename}")
                moved_count += 1
            except Exception as e:
                print(f"移动文件 {filename} 时出错: {str(e)}")
    
    print(f"\n完成! 共移动了 {moved_count} 个文件")

if __name__ == "__main__":
    # 获取用户输入的源目录和目标目录路径
    move_files('/Users/wangzhuoyang/Desktop/projects/thyroid/data/medical_data_output', 
               '/Users/wangzhuoyang/Desktop/projects/thyroid/data/few_shot_data')