import os
import time, datetime

def dirfilename(ignorelist = ['node_modules', '.git', 'list.txt']):
	dirlist = []
	filelist = []

	for dirname, dirnames, filenames in os.walk('.'):
		# Advanced usage:
		# editing the 'dirnames' list will stop os.walk() from recursing into there.
		for ignorename in ignorelist:
			if ignorename in dirnames:
				# don't go into any .git directories.
				dirnames.remove(ignorename)
			if ignorename in filenames:
				# don't go into any .git directories.
				filenames.remove(ignorename)
			# if 'node_modules' in dirnames:
			# 	# don't go into any .git directories.
			# 	dirnames.remove('node_modules')

		# print path to all subdirectories first.
		for subdirname in dirnames:
			dirlist.append(os.path.join(dirname, subdirname))

		for filename in filenames:
			filelist.append(os.path.join(dirname, filename))

	return (dirlist, filelist)

# generated by hello_def_python in hello.python.nightfog.snippets
def makealias(dirlist, filelist, prefix='sample_redux', description='run'):
	aliasname = 'hello.' + prefix.replace('_', '.')
	mkcommand = 'alias ' + aliasname + "='function __" + aliasname + '() { '
	for dirname in dirlist:
		mkcommand += 'mkdir -p ' + dirname + '; '

	# mkcommand += '\n\n'

	for filename in filelist:
		mkcommand += 'echo "' + prefix + '_' + os.path.basename(os.path.dirname(filename)).replace('.', '_') + '_' + os.path.basename(filename).replace('.', '_') + '" >> ' + filename + ';'
		# mkcommand += '\n'

	# edit with vi
	mkcommand += 'vi '
	for filename in filelist:
		mkcommand += filename + ' '
	mkcommand += ';'

	# add description
	mkcommand += 'echo "' + description + '";'
	mkcommand += '}; __' + aliasname + "'"
	return mkcommand

def makesnippet(dirlist, filelist, prefix='sample_redux'):
	dateTime = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')
	snipstring = ''
	filelist.sort(key=lambda f: os.path.splitext(f)[1])
	for filename in filelist:
		snipname = prefix + '_' + os.path.basename(os.path.dirname(filename)).replace('.', '_') + '_' + os.path.basename(filename).replace('.', '_') 
		snipstring += 'snippet *' + snipname + ' "sample ' + snipname + ' template" b\n'
		snipstring += '// generated by ' + snipname + ' in ' + prefix.replace('_', '.') + '.nightfog.snippets\n'
		snipstring += '// last edited : ' + dateTime + '\n'

		f = open(filename, 'r')
		data = f.read()
		f.close()
		snipstring += data

		snipstring += '\n'
		snipstring += 'endsnippet\n\n'
	return snipstring