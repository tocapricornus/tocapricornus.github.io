#-*-coding:utf-8
import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from datetime import datetime
from setting import config as CF

def isDirPath():
	if not os.path.isdir(svr_page_cat_path):
		os.makedirs(svr_page_cat_path)

tp_name = 'content.html'

action_checkout_path = 'static_site_repo' #action에서 체크아웃위치

file_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) #D:\project_2023\html_template\py
file_dir_one =os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))#D:\project_2023\html_template
file_dir_two = os.path.dirname(os.path.realpath(file_dir_one)) #D:\project_2023

if CF.IS_REAL:
	file_dir_one = f'{file_dir_two}/{action_checkout_path}' 
#템플릿 위치
svr_tp_path = file_dir_one+"/tp/example/" #D:\project_2023\html_template/tp/example/
svr_tp_file_path = f'{svr_tp_path}{tp_name}' #D:\project_2023\html_template/tp/example/content.html

#페이지 위치
svr_page_path = f'{file_dir_one}/page/' #D:\project_2023\html_template\page\
svr_page_cat_path= f'{svr_page_path}{datetime.today().year}{datetime.today().month}' #D:\project_2023\html_template\page\202310


print("################ py.dirUtil.py 시작")
print("CF.IS_REAL : ",CF.IS_REAL)
print("today : ", datetime.today() )
print("tp_name : ", tp_name) 
print("file_dir : ", file_dir) 
print("file_dir_one : ", file_dir_one) 
print("file_dir_two : ", file_dir_two) 
print("svr_tp_path : ", svr_tp_path) 
print("svr_tp_file_path : ", svr_tp_file_path) 
print("svr_page_path : ", svr_page_path) 
print("svr_page_cat_path : ", svr_page_cat_path)

print("################ py.dirUtil.py 끝")
