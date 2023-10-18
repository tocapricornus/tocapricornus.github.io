#-*- coding: utf-8 -*-
import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import urllib.request
import json
from setting import config as CF

class NaverApi:
	def __init__(self) -> None:
		pass
		
	#네이버 책검색
	def bookSearch(self, isbn):
		try:
			encText = urllib.parse.quote("검색할 단어")
			url = "https://openapi.naver.com/v1/search/book_adv?d_isbn=" + isbn # json 결과		
			request = urllib.request.Request(url)
			request.add_header("X-Naver-Client-Id",CF.NV_API_CID)
			request.add_header("X-Naver-Client-Secret",CF.NV_API_SID)
			response = urllib.request.urlopen(request)
			rescode = response.getcode()
			#print("rescode ",rescode)
			if(rescode==200):
				response_body = response.read()
				response_text = response_body.decode('utf-8')
				jsonData = json.loads(response_text)
				return jsonData['items'][0]		    
			else:
				print("Error Code:" + rescode)

		except Exception as e:
			raise e
