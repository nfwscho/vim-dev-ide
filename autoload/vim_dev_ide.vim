" This script is based on vim_shell_executor.vim
" https://github.com/JarrodCTaylor/vim-shell-executor
" --------------------------------
" Add our plugin to the path
" --------------------------------
 if has("python3")
     command! -nargs=1 Py py <args>
 else
     command! -nargs=1 Py py <args>
 endif
Py import sys
Py import vim
Py sys.path.append(vim.eval('expand("<sfile>:h")'))

" --------------------------------
"  Function(s)
" --------------------------------
function! LeftPad(s,amt,...)
    if a:0 > 0
        let char = a:1
    else
        let char = ' '
    endif
    return repeat(char,a:amt - len(a:s)) . a:s
endfunction

function! DisplayTimeDifference(time1,time2)
    let l:t1List = split( a:time1, ":" )
    let l:t2List = split( a:time2, ":" )
    let l:difference = abs((l:t1List[1] * 60 + l:t1List[2]) - (l:t2List[1] * 60 + l:t2List[2]))
    let l:minutesDifference = LeftPad(float2nr(floor(difference/60)), 2, "0")
    let l:secondsDifference = LeftPad(l:difference - (l:minutesDifference * 60), 2, "0")
    set cmdheight=2
    echo "Execution started at: " . a:time1 . " Successfully finished at: " . a:time2 . " Duration: 00:" . l:minutesDifference . ":" . l:secondsDifference
    set cmdheight=1
endfunction

function! vim_dev_ide#Test(selection_or_buffer)
let startExecutionTime = strftime("%T")
echo "Execution started at: " . startExecutionTime
Py << endPython
from vim_dev_common import *
from vim_dev_ide import *
from vim_samplesnip_maker import *

def execute():
    buf_type = get_correct_buffer(vim.eval("a:selection_or_buffer"))
    shell_program_output = get_program_output_from_buffer_contents(buf_type)
    create_new_buffer(shell_program_output)

execute()

endPython

let endExecutionTime = strftime("%T")
call DisplayTimeDifference(startExecutionTime, endExecutionTime)
endfunction


function! vim_dev_ide#MoveNextSymbol(forword)
	if a:forword != "forword"
		echo search('[\{\}\,;\(\)"`\x27]', 'b')
	else
		echo search('[\{\}\,;\(\)"`\x27]')
	endif
endfunction

function! vim_dev_ide#DevExec(comval)
	let comval = a:comval
	if comval == "ascii"
		echo 'Command Found' . comval
		execute "terminal('ascii')"
	else
		echo 'Command Not Found' . comval
		execute "terminal(" . comval . ")"
	endif
endfunction
