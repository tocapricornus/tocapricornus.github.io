#-*- coding: utf-8 -*-
import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import util.askUtil as askUtil
from bs4 import BeautifulSoup
from setting import config as CF
import time
import requests


class kyobo():
	def __init__(self, ad, naverApi):
		self.ad = ad
		self.nvApi = naverApi
		self.book_list = []



	def kbDetailInfoGet(self, url):	
		res  = requests.get(url, timeout=25)	
		if res.status_code == 200:		
			return BeautifulSoup(res.text, 'html.parser')
		
			
	def getBookList(self):
		v_page = askUtil.getRandom(1,5)
		# v_page = 4
		print("v_page : ",v_page)
		url = f'https://product.kyobobook.co.kr/api/gw/pub/pdt/best-seller/online?page={v_page}&per=100&period=001&dsplDvsnCode=000&dsplTrgtDvsnCode=001'
		
		
		try:	
			bookData = requests.get(url,headers={'User-Agent': 'Mozilla/5.0'}, timeout=25).json()	
			cnt = 0
			for i in bookData['data']['bestSeller']:
				# print("i ",i)		
				isbn 				= askUtil.custUtil(i, 'cmdtCode') 
				if self.ad.df_isOrder(isbn) > 0:
					continue
				cnt+=1
				saleCmdtid 			= askUtil.custUtil(i, 'saleCmdtid') #"saleCmdtid": "S000061863239",
				saleCmdtClstName	= askUtil.custUtil(i, 'saleCmdtClstName') #"saleCmdtClstName": "경제전망",
				book_nm 			= askUtil.custUtil(i, 'cmdtName') #"cmdtName": "트렌드 코리아 2023",
				desc 				= askUtil.custUtil(i, 'inbukCntt') 
				author 				= askUtil.custUtil(i, 'chrcName') #"chrcName": "김난도 외",	
				publisher 			= askUtil.custUtil(i, 'pbcmName')
				pubDate 			= askUtil.custUtil(i, 'rlseDate')					

				rwcnt 		 		= askUtil.custUtil(i, 'buyRevwRvgr') #평점			
				coverLargeUrl 		= None
							
				try:
					naver_api_book_result 			= self.nvApi.bookSearch(isbn)
					# print("naver_api_book_result : ",naver_api_book_result)
					# description			=  askUtil.custUtil(naver_api_book_result,'description')
					# if not description:
					description = desc
					coverLargeUrl 		= naver_api_book_result['image']
					coverSmallUrl 		= naver_api_book_result['image']
				except Exception as e:
					description = desc			
					print("################## nv e ##########: ",e)
					# print(" nv API err  : ",i)
				
				link_c 				= ''
				book_cd 			= saleCmdtClstName

				# print("description : ",description)
				# print("author : ",author)
				# print("isbn : ",isbn)
				# print("coverLargeUrl : ",coverLargeUrl)
				if description and author and isbn and coverLargeUrl:
					book_nm = askUtil.getSqlReplace(book_nm)				
					description = askUtil.repl_excp(askUtil.getSqlReplace(description))		

					description2 =''
					description3 =''
					try:
						soup = self.kbDetailInfoGet(f'https://product.kyobobook.co.kr/detail/{saleCmdtid}')
						for item in soup.select('div.prod_detail_contents_inner'):					
							description2 = item.select_one('div.book_publish_review p').text
							description3 = item.select_one('div.book_inside p').text
							# print("description2 : ",description2)
							# print("description3 : ",description3)
							# print("==============")
							break
						description2 = askUtil.repl_excp(askUtil.getSqlReplace(description2))
						description3 = askUtil.repl_excp(askUtil.getSqlReplace(description3))
					except Exception as e:
						description2 = askUtil.repl_excp(askUtil.getSqlReplace(description2))
						description3 = askUtil.repl_excp(askUtil.getSqlReplace(description3))
						print("kbDetailInfoGet e ",e)
						self.ad.df_orderInsert(isbn, 'N')


					reviewList=[]
					try:					
						reviewInfo = requests.get(f'https://product.kyobobook.co.kr/api/review/list?page=1&pageLimit=30&reviewSort=001&revwPatrCode=000&saleCmdtid={saleCmdtid}',headers={'User-Agent': 'Mozilla/5.0'}, timeout=25).json()	
						for info in reviewInfo['data']['reviewList']:
							try:
								reviewList.append(askUtil.repl_excp(askUtil.getSqlReplace(info['revwCntt'])))
							except Exception as e:
								print("for e: ",e)
					except Exception as e:
						print("review list ",e)
						self.ad.df_orderInsert(isbn, 'N')
						print("cnt : ", str(cnt)," ISBN_NO : ",isbn)
					
					if len(reviewList) > 5:
						self.book_list.append( {"BOOK_NM":book_nm,"BOOK_IMG_L_URL":coverLargeUrl,
											"BOOK_IMG_S_URL":coverSmallUrl,"AUTHOR":author,"ISBN_NO":isbn,"PUB_SR":publisher,"PUB_DT":pubDate,"BOOK_CD":book_cd,
											"REVIEW_LIST":reviewList,"BOOK_DESC":description,"BOOK_DESC2":description2,"BOOK_DESC3":description3
											})
					else:
						self.ad.df_orderInsert(isbn, 'N')
				
				if len(self.book_list) >= 1:
					break
				
				time.sleep(1)
			print("kyobobook.py end")
		except Exception as e:
			print("kyobobook.py e99 : ",e)
		print("self.book_list size: ", len(self.book_list))
		return self.book_list

		#https://crontab.guru/
# if __name__ == '__main__':		
# 		print("kyobobook")
