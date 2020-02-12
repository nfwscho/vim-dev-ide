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
from vim_dev_common import *

searchword = vim.eval("a:word")
dicstring = get_naver_dic(searchword)
create_new_buffer(dicstring)

endPython

endfunction


function! vim_naver_dic#GetNaverPapago(sentence)
Py << endPython

import vim, os
from vim_naver_dic import *
from vim_dev_common import *

searchsentence = vim.eval("a:sentence")
papagostring = get_naver_papago(searchsendence)
create_new_buffer(papagostring)

endPython

endfunction

