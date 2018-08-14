# -*- coding: UTF-8 -*-
#templates.py

import fileinput,re

field_pat=re.compile(r'\[(.+?)\]')
scope={}
s=0

def replacement(match):
	global s
	s = s + 1
	print(match.group(0),s)
	code=match.group(1)
	print(code)
	try:
		#如果字段可以求值，返回它：
		return str(eval(code,scope))
	except SyntaxError:
		#否则执行相同作用域内的赋值语句
		exec code in scope
		#....返回空字符串：
		return ''
		
#将所有文本以一个字符串的形式获取：
lines=[]
for line in fileinput.input():
	lines.append(line)
text=''.join(lines)
	
#将field模式的所有匹配项都替换掉：
print (field_pat.sub(replacement,text))
