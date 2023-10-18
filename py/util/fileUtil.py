#-*-coding:utf-8
import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from bs4 import BeautifulSoup as bfs

def read_file(path):
    file = open(path, 'rt', encoding='UTF8')
    data = None
    
    try:
        data = file.read()
    except Exception as e:
        print(e)
    finally:
        file.close()

    soup = bfs(data, 'html.parser')
    # print(soup.contents[0])
    return soup

def save_file(path, content):
    f_output = open(f'{path}','w', encoding='UTF8')
    try:
        print("save_file path ",path)
        f_output.write(str(content))
    except Exception as e:
        print(e)
    finally:
        f_output.close()


def file_open_text(path):
    f_input  = open(path, 'rt', encoding='UTF8')
    cnt = 0
    result = ''
    try:
        for fi in f_input.readlines():
            result += fi
    except Exception as e:
        print('file_open_text error', e)
    finally:
        f_input.close()
    return result
