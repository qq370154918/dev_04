# -*- coding: utf-8 -*-

# 创建一个生成器，获取文件流，每次获取的是文件字节数据
def get_file_content(filename, chunk_size=1024):
    with open(filename, encoding='utf-8') as file:
        while True:
            content = file.read(chunk_size)
            # 如果文件结尾，那么content为None
            if not content:
                break
            yield content
