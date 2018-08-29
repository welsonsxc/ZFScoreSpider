# -*- coding:utf-8 -*-
import pymysql

# 数据库: qjjw
# 学生账号密码表:stu_pw {学号:stu_xh;密码:stu_pw}
# 学生信息表:stu_info {学号:stu_xh;密码:stu_name}
# 学生成绩表:stu_score {学号:stu_xh;学年:study_year;
#						学期:study_term;课程名:class_name;
#						学分:study_credit;绩点:study_gpa;
#						成绩:study_score;开科学院:study_from}

host1='localhost'
user1='root'
password1='Scsql2018!'
db1='qjjw'

# 查询表
def SqlSelect(dbtable_name):
	db= pymysql.connect(host=host1,user=user1,
		password=password1,db=db1,port=3306)
	cur=db.cursor()
	sql="select * from %s" % dbtable_name
	try:
		cur.execute(sql)
		results=cur.fetchall()
		return (results)
	except Exception as e:
		raise e
	finally:
		cur.close()
		db.close()

# 输出表
def Sqlprint(dbtable_name):
	results=SqlSelect(dbtable_name)
	if (dbtable_name=='stu_pw'):
		print('===============账号密码表===============')
		print('学号\t\t 密码')
		for row in results:
			stu_xh=row[0]
			stu_pw=row[1]
			print(stu_xh,'\t',stu_pw)
	elif (dbtable_name=='stu_info'):
		print('===============学号姓名表===============')
		print('学号\t\t 姓名')
		for row in results:
			stu_xh=row[0]
			stu_name=row[1]
			print(stu_xh,'\t',stu_name)
	elif (dbtable_name=='stu_score'):
		print('===============学生成绩表===============')
		#print('学号\t\t 姓名')
		for row in results:
			print(str(row))

# 查询成绩
def SqlSearchscore(userxh,year_now,term_now):
	db= pymysql.connect(host=host1,user=user1,
		password=password1,db=db1,port=3306)
	cur=db.cursor()
	sum=0
	i=0;
	sql="select * from stu_score where stu_xh=%s"%userxh 
	try:
		print ('执行sql语句:'+sql)
		cur.execute(sql)
		results=cur.fetchall()
		print('===============')
		print('学号:'+userxh+' 学年:'+year_now+' 学期:'+term_now)
		for row in results:
			id=row[0]
			year=row[2]
			term=row[3]
			name=row[4]
			credit=row[5]
			gpa=row[6]
			score=row[7]
			if (year==year_now):
				if(term==term_now):
					print(name+'  成绩:'+str(score)+'  绩点:'+str(gpa)+'  学分:'+str(score))
					i=i+1
					sum=sum+gpa
		avg=sum/i
		print('为您查询到本学期共'+str(i)+'门课,平均绩点:'+str(avg))
	except Exception as e:
		raise e
	finally:
		cur.close()
		db.close()
		
# 查询该学生是否存在信息		
def SqlSearchinfo(dbtable_name,userxh):
	db= pymysql.connect(host=host1,user=user1,
	password=password1,db=db1,port=3306)
	cur=db.cursor()
	sql="select count(*) from %s where stu_xh=%s"%(dbtable_name,userxh)
	try:
		cur.execute(sql)
		results=cur.fetchall()
		if str(results) !='((0,),)':
			return True
		else:
			return False
	except Exception as e:
		raise e
	finally:
		cur.close()
		db.close()

# 保存学号和密码
def Insertpw(userxh,password):
	# 创建数据库游标连接
	db= pymysql.connect(host=host1,user=user1,
		password=password1,db=db1,port=3306)
	cur=db.cursor()
	#格式化传递数据
	fh=r"'"
	userxh=fh+userxh+fh
	password=fh+password+fh
	# 如果该学生存在则更新密码
	if (SqlSearchinfo('stu_pw',userxh)==True):
		sql="update stu_pw set stu_pw=%s where stu_xh=%s"%(password,userxh)
	else:
		sql="INSERT INTO stu_pw (stu_xh,stu_pw) VALUES (%s,%s)"%(userxh,password)
	print('执行sql语句:'+sql)
	#插入数据
	try:
		cur.execute(sql)
		db.commit()
	except Exception as e:
		db.rollback()
		print('插入失败')
	finally:
		cur.close()
		db.close()

# 保存学生信息
def Insertinfo(userxh,name):
	# 创建数据库游标连接
	db= pymysql.connect(host=host1,user=user1,
		password=password1,db=db1,port=3306)
	cur=db.cursor()
	#格式化传递数据
	fh=r"'"
	userxh=fh+userxh+fh
	name=fh+name+fh
	# 如果该学生存在则更新信息
	if (SqlSearchinfo('stu_info',userxh)==True):
		sql="update stu_info set stu_name=%s where stu_xh=%s"%(name,userxh)
	else:
		sql="INSERT INTO stu_info (stu_xh,stu_name) VALUES (%s,%s)"%(userxh,name)
	print('执行sql语句:'+sql)
	#插入数据
	try:
		cur.execute(sql)
		db.commit()
	except Exception as e:
		db.rollback()
		print('插入失败')
	finally:
		cur.close()
		db.close()

# 保存成绩
def Insertscore(filename,userxh):
	# 创建数据库游标连接
	db= pymysql.connect(host=host1,user=user1,
		password=password1,db=db1,port=3306)
	cur=db.cursor()
	fh=r"'"
	if SqlSearchinfo('stu_score',userxh)==True:
		SqlDelete('stu_score',userxh)
	f=open(filename,'r')
	for each_line in f:
		temp=each_line.split(',',14)
		for i in range(14):
			temp[i-1].replace('\'',' ')
		#学年
			if i==1:
				year=temp[i-1][2:11]
				year=fh+year+fh
		#学期
			if i==2:	
				term=temp[i-1][2]
				term=fh+term+fh
		#课程代码
			#if i==3:	
				#print ('课程代码:'+temp[i-1])
		#课程名称
			if i==4:	
				name=temp[i-1][2:len(temp[i-1])-1]
				name=fh+name+fh
		#课程性质
			#if i==5:	
				#print ('课程性质:'+temp[i-1])
		#课程归属
			#if i==6:	
				#print ('课程归属:'+temp[i-1])
		#学分
			if i==7:	
				credit=temp[i-1][2:len(temp[i-1])-1]
				credit=float(credit)
		#绩点
			if i==8:	
				gpa=temp[i-1][5:len(temp[i-1])-1]
				gpa=float(gpa)
		#成绩
			if i==9:	
				score=temp[i-1][2:len(temp[i-1])-1]
				score=fh+score+fh
		#辅修标记
			#if i==10:	
				#print ('辅修标记:'+temp[i-1])
		#补考成绩
			#if i==11:	
				#print ('补考成绩:'+temp[i-1])
		#重修成绩
			#if i==12:	
				#print ('重修成绩:'+temp[i-1])
		#开课学院
			if i==13:	
				studyfrom=temp[i-1][2:len(temp[i-1])-1]
				studyfrom=fh+studyfrom+fh
		#备注
			#if i==14:	
				#print ('备注:'+temp[i-1])
		#重修标记
			#if i==15:	
				#print ('重修标记:'+temp[i-1])
		sql="INSERT INTO stu_score (stu_xh,study_year,study_term,class_name,study_credit,study_gpa,study_score,study_from) VALUES (%s,%s,%s,%s,%d,%f,%s,%s)"%(userxh,year,term,name,credit,gpa,score,studyfrom)
		try:
			print('执行sql语句:'+sql)
			cur.execute(sql)
			db.commit()
		except Exception as e:
			db.rollback()
			print('插入失败')
	f.close()
	cur.close()
	db.close()	

# 删除
def SqlDelete(dbtable_name,userxh):
	db= pymysql.connect(host=host1,user=user1,
		password=password1,db=db1,port=3306)
	cur = db.cursor()
	fh=r"'"
	userxh=fh+userxh+fh
	sql="delete from %s where stu_xh = %s" % (dbtable_name,userxh)
	try:
		print('执行sql语句：'+sql)
		cur.execute(sql)  #像sql语句传递参数
		db.commit()
	except Exception as e:
		db.rollback() 
		print('删除失败')
	finally:
		cur.close()
		db.close()

if __name__=="__main__":
	#SqlDelete('stu_score','2017830402024')
	#Insertpw('2017830402024','SCjiaowu287486.')
	#Insertinfo('2017830402024','盛超')
	#Insertscore('table.txt','2017830402024')
	#SqlSearchscore('2017830402024','2017-2018','2')
	#print(SqlSelect('stu_info'))
	Sqlprint('stu_pw')
	Sqlprint('stu_info')
	Sqlprint('stu_score')
	