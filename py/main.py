#-*-coding:utf-8
import os, sys
from setting import config as CF
from pathlib import Path
from page import pageUtil
import util.dirUtil as dirUtil
from datetime import datetime

from crawling import kyobobook
import ask_db
from API import naverApi

#현재년월
today=datetime.today()
print("UTC TIME : ",datetime.utcnow())
#디렉토리 확인 및 없으면 생성
dirUtil.isDirPath()

#첫 시작으로 초기화
def project_origin(origin=False):
    pu =  pageUtil(CF.SITE_NAME, dirUtil.svr_tp_file_path, f'{dirUtil.file_dir_one}/index.html')
    pu.init_page(f'{dirUtil.svr_tp_path}aside_menu.html', f'{dirUtil.svr_page_path}aside_menu.html')
    pu.init_page(f'{dirUtil.svr_tp_path}index.html', f'{dirUtil.file_dir_one}/index.html')
    import shutil
    shutil.rmtree(dirUtil.svr_page_cat_path)
    pu.change_sitemap(origin=True)
    quit()

if __name__=="__main__":        
    print("#############################\n#############################\nDEV PC ? ",CF.IS_REAL,"\n#############################\n#############################")
  
    #############################
    #주의 : 모든페이지 삭제시 사용
    # project_origin(origin=True)
    ##############################
    
    #############################
    #크롤링
    ad = ask_db.AskDb()
    kbb = kyobobook.kyobo(ad,naverApi.NaverApi())
    bookList = kbb.getBookList()
    print("kyboo book list size : ", len(bookList))

    # print("============ bookList", bookList)
    try:
        if bookList:
            title_nm    = bookList[0]['BOOK_NM']
            img_url     = bookList[0]['BOOK_IMG_L_URL']
            content_list= bookList[0]['REVIEW_LIST']
    except Exception as e:
        print(e)
    
    #############################
    #페이지 만들기
    try:
        pu = pageUtil(CF.SITE_NAME, dirUtil.svr_tp_file_path, f'{dirUtil.file_dir_one}/index.html')
        pu.set_adsense(CF.ADSENSE_CLIENT, CF.ADSENSE_SEARCH, CF.ANALYTICS_GTAG, CF.IS_REAL)
        if CF.SITE_KIND == 'BOOK':
            isbn    = bookList[0]['ISBN_NO']
            pub_nm  = bookList[0]['PUB_SR']
            pub_dt  = bookList[0]['PUB_DT']
            author  = bookList[0]['AUTHOR']
            pu.set_book_info(isbn, pub_nm, pub_dt, author)
            pu.set_page_nm(isbn, 'html')
            print(" isbn : ", isbn)
            
        else:
            pu.set_page_nm('1') # file name

        pu.change_content(f'{dirUtil.svr_page_cat_path}/{pu.page_file_nm}.{pu.ext}', title_nm, img_url, content_list)
        ad.df_orderInsert(isbn, 'Y')
    except Exception as e:
        print("main.py make page e ", e)
        ad.df_orderInsert(isbn, 'N')
    finally:
        ad.closeConn()
