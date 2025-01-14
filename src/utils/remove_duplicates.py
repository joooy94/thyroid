import os

def remove_duplicates(folder_a, folder_b):
    # 检查两个文件夹是否存在
    if not os.path.exists(folder_a):
        print(f"错误：文件夹A '{folder_a}' 不存在")
        return
    if not os.path.exists(folder_b):
        print(f"错误：文件夹B '{folder_b}' 不存在")
        return
    
    # 获取文件夹A中的所有文件名
    files_in_a = set(os.listdir(folder_a))
    
    # 计数器
    removed_count = 0
    
    # 遍历文件夹B中的文件
    for filename in os.listdir(folder_b):
        # 如果文件在A中存在
        if filename in files_in_a:
            file_path = os.path.join(folder_b, filename)
            try:
                # 删除文件
                os.remove(file_path)
                print(f"已删除: {filename}")
                removed_count += 1
            except Exception as e:
                print(f"删除文件 {filename} 时出错: {str(e)}")
    
    print(f"\n完成! 共删除了 {removed_count} 个重复文件")

if __name__ == "__main__":
    # 文件夹A和B的路径
    remove_duplicates('/Users/wangzhuoyang/Desktop/projects/thyroid/data/100_testset_png', 
                      '/Users/wangzhuoyang/Desktop/projects/thyroid/data/few_shot_data') 