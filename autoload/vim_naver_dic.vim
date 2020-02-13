if has("python3")
	command! -nargs=1 Py py3 <args>
else
	command! -nargs=1 Py py <args>
endif

Py import sys
Py import vim
Py sys.path.append(vim.eval('expand("<sfile>:h")'))

function! s:get_visual_selection()
    " Why is this not a built-in Vim script function?!
    let [line_start, column_start] = getpos("'<")[1:2]
    let [line_end, column_end] = getpos("'>")[1:2]
    let lines = getline(line_start, line_end)
    if len(lines) == 0
        return ''
    endif
    let lines[-1] = lines[-1][: column_end - (&selection == 'inclusive' ? 1 : 2)]
    let lines[0] = lines[0][column_start - 1:]
    return join(lines, "\n")
endfunction

function! vim_naver_dic#GetNaverDic()
let a:sentence = s:get_visual_selection()

Py << endPython

import vim, os
from vim_naver_dic import *
from vim_dev_common import *

searchword = vim.eval("a:sentence")
dicstring = get_naver_dic(searchword)
create_new_buffer(dicstring)

endPython

endfunction


function! vim_naver_dic#GetNaverPapago() abort
echom "test!!!"
let sentence = s:get_visual_selection()

" Py << endPython

" import vim, os
" from vim_naver_dic import *
" from vim_dev_common import *

" searchsentence = vim.eval("sentence")
" papagostring = get_naver_papago(searchsentence)
" create_new_buffer(papagostring)

" endPython

endfunction

