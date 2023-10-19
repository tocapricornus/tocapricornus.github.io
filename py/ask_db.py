#-*-coding:utf-8
import pymysql
from setting import config as CF

class AskDb:		
	def __init__(self, ip=None, user=None, pw=None, db=None):
		self.conn = pymysql.connect(host=CF.DB_HOST, user=CF.DB_USER, password=CF.DB_PW, db=CF.DB_SID,charset="utf8")

	def getConnection(self):
		return  self.conn
		
	#단축URL이 없는 상품 조회
	def selectAll(self, sqlId):	
		self.cur = self.conn.cursor()
		self.cur.execute(sqlId)
		rows = self.cur.fetchall()
		return rows

	def selectOne(self,sqlId):				
		self.cur = self.conn.cursor()
		self.cur.execute(sqlId)	
		row = self.cur.fetchone()	
		#print(row)		
		return row	
	
	def update(self,sqlId):
		try:
			self.cur = self.conn.cursor()
			self.cur.execute(sqlId)		
			self.conn.commit()	
		except Exception as e:
			print(e)

	def insert(self,sqlId):
		try:
			self.cur = self.conn.cursor()
			self.cur.execute(sqlId)
			self.conn.commit()		
		except Exception as e:
			print(e)

	def delete(self,sqlId):
		try:
			self.cur = self.conn.cursor()
			self.cur.execute(sqlId)
			self.conn.commit()		
		except Exception as e:
			print(e)
	
	def closeConn(self):	
		self.conn.close()


	def df_orderInsert(self, isbn, yn):
		sqlId = f" INSERT INTO {CF.DB_SID}.T_ORDER VALUES('{isbn}','{CF.SITE_KIND}','{yn}',NOW())"
		#print(sqlId)
		self.insert(sqlId)

	def df_isOrder(self, isbn):
		return self.selectOne(f" SELECT COUNT(*) FROM {CF.DB_SID}.VW_ORDER WHERE ORDER_KEY ='{isbn}' AND ORDER_TYPE='{CF.SITE_KIND}' ")[0]
		
