import os
import tkinter as tk
from tkinter import filedialog

def create_files_with_extension(extension,name_files, num_files, folder_path):

    for i in range(num_files):
        file_name = f"{name_files}_{i+1}.{extension}"
        file_path = os.path.join(folder_path, file_name)
        with open(file_path, 'w') as file:
            file.write("")
        print(f"已创建文件: {file_path}")

def main():
    
    root = tk.Tk()
    root.withdraw()

    folder_path = filedialog.askdirectory()
    if not folder_path:
        print("未选择文件夹，程序退出。")
        return

    extension = input("请输入文件后缀（例如 'txt'）：")
    num_files = int(input("请输入要创建的文件数量："))
    name_files = input("请输入文件名：")
    print(f"正在在文件夹{folder_path}中创建{num_files}个文件，文件名为{name_files}，后缀为{extension}。")
    print("请稍等...")

    create_files_with_extension(extension, name_files, num_files, folder_path)
    print(f"{num_files}个文件已创建完成,请查看指定文件夹{folder_path}。")
    input("按任意键退出程序...")
    root.destroy()

if __name__ == "__main__":
    main()