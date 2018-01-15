if has("python3")
	command! -nargs=1 Py py3 <args>
else
	command! -nargs=1 Py py <args>
endif

Py import sys
Py import vim
Py sys.path.append(vim.eval('expand("<sfile>:h")'))

function! vim_naver_dic#GetNaverDic(word)
Py << endPython

import vim, os
from vim_naver_dic import *

searchword = vim.eval("a:word")
get_naver_dic(searchword)

endPython

endfunction
