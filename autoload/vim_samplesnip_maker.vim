if has("python3")
	command! -nargs=1 Py py3 <args>
else
	command! -nargs=1 Py py <args>
endif

Py import sys
Py import vim
Py sys.path.append(vim.eval('expand("<sfile>:h")'))

function! vim_samplesnip_maker#CreateAliasAndSnippets()
Py << endPython

import vim, os
import time, datetime
from vim_samplesnip_maker import *
from vim_dev_common import *
from vim_dev_ide import *

ignorelist = ['.git', 'node_modules', 'package-lock.json', 'README.md']
dirlist, filelist = dirfilename(ignorelist)

# print(dirlist)
# print("filelist")
# print(filelist)
print("**dirlist")

for dirname in dirlist:
	print(dirname)

print("**filelist")
for filename in filelist:
	print(filename)

aliasresult = (makealias(dirlist, filelist))
snippetresult = makesnippet(dirlist, filelist)

# buf_type = get_correct_buffer("buffer")
# shell_program_output = get_program_output_from_buffer_contents(buf_type)
create_new_buffer(aliasresult + snippetresult)

endPython

endfunction




