"""
pool 和 进程间通信练习
"""

import os
from multiprocessing import Pool,Queue

# 创建消息队列
q = Queue()

# 拷贝函数 拷贝一个文件
def copy_file(file,old_folder,new_folder):
    # 将文件从 old_folder-->new_folder
    fr = open(old_folder+'/'+file,'rb')
    fw = open(new_folder+'/'+file,'wb')
    print("开始拷贝"+(old_folder+file))
    # 循环拷贝内容
    while True:
        data = fr.read(1024*1024)
        if not data:
            break
        fw.write(data)
        q.put(len(data)) # 将拷贝的大小放入消息队列

    fr.close()
    fw.close()

# 控制目录拷贝
def main():
    # 需要拷贝的文件夹
    old_folder_name = "/home/tarena/testDir"
    # 目标文件夹
    new_folder_name = old_folder_name+'-备份'

    # 如果目录存在则删除目录
    if os.path.exists(new_folder_name):
        os.removedirs(new_folder_name)

    # 创建新的文件夹
    os.mkdir(new_folder_name)

    # 获取文件列表
    all_file = os.listdir(old_folder_name)

    # 创建进程池
    pool = Pool()
    for file in all_file:
        pool.apply_async(copy_file,
                         args=(file,
                               old_folder_name,
                               new_folder_name))
    pool.close()

    # 计算所有文件总大小
    sum_size = 0
    for path in all_file:
        sum_size+=os.path.getsize(old_folder_name+'/'+path)
    print("文件总大小：%dM"%(sum_size/1024//1024))

    get_size = 0
    while True:
        get_size += q.get() # 从消息队列中读数值
        copy_process = get_size/sum_size
        print("当前进度：%.1f%%"%(copy_process * 100))
        if copy_process >= 1:
            break

    pool.join()

if __name__ == '__main__':
    main()

