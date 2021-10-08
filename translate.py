
import os
import shutil
import functools    
utf_8_file = functools.partial(open, encoding='utf-8')


# sometimes translator wasn't able to handle comments such as //comment,
# so put a space after // (// comment)
def NormalizeComment(text):
	i = 0

	buff = text

	# gambiarra monstruosa(pt-br)
	# melhor modo de se fazer, ahhh provavelmente não
	while i + 2 < len(text):
		if text[i + 1] == "/" and text[i + 2] != "/" and text[i + 2] != " " and text[i + 2] != "\t":
			buff = f"{text[:i+2]} {text[i+2:]}"
			text = buff

		i = i + 1

	return buff

# backup the base code file
def Backup(fileName):
	directory = os.path.dirname("./Bak/")

	if not os.path.exists(directory):
		os.makedirs(directory)

	# have to change, if the file exists it will fail 
	shutil.move(fileName, directory)


# Extract code comments into new files (code, comment) 
def Extract(fileName):
	with open(fileName, "r+", encoding="euc-kr") as f:
		lines = f.readlines()

	Backup(fileName)

	comments = utf_8_file("comment.txt", "w+")
	code = utf_8_file("code.txt", "w+")

	for l in lines:
		if "//" in l:
			comments.write(NormalizeComment(l))
			code.write("\n")
		else:
			code.write(l)
			comments.write("\n")

	comments.close()
	code.close()


# Join code and comments together in one file.
def Join(fileName):
	with utf_8_file("comment.txt", "r") as f:
		commentLines = f.readlines()

	with utf_8_file("code.txt", "r") as f:
		codeLines = f.readlines()

	with utf_8_file(fileName, "w+") as code:
		i = 0

		for l in commentLines:
			if "//" in l:
				code.write(l)
			else:
				code.write(codeLines[i])

			i = i + 1


#from googletrans import Translator

# Tried to translate the file using googletrans API
# but it failed miserably(translator timeout, wrong translations, part of remaining code being corrupted)
# method NormalizeComment lost purpose, but keep it for better comment style
'''def TranslateFile(fileName):
	translator = Translator(service_urls=[
		'translate.google.com',
		'translate.google.co.kr',
		])

	with utf_8_file(fileName, "r") as f:
		lines = f.readlines()
	
	with utf_8_file(fileName, "w+") as f:
		for line in lines:
			if not line.startswith('\n'):
				result = translator.translate(line, dest='en', src='ko')
				f.write(result.text)
				print(f"From: {line}, To: {result.text}\n")
			else:
				f.write(line)
'''

'''
import sys

if len(sys.argv) < 2:
	exit()

file = sys.argv[1]

Extract(file)
TranslateFile("comment.txt")	 
Join(file)
'''


