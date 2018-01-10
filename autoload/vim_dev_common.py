import vim, os
import time, datetime

def create_new_buffer(contents):
    vim.command('normal! Hmx``')
    delete_old_output_if_exists()
    if int(vim.eval('exists("g:executor_output_win_height")')):
        vim.command('aboveleft {}split executor_output'.format(vim.eval("g:executor_output_win_height")))
    else:
        vim.command('aboveleft split executor_output')
    vim.command('normal! ggdG')
    vim.command('setlocal filetype=text')
    vim.command('setlocal buftype=nowrite')

    contentslist = contents
    if isinstance(contents, str):
        contentslist = contents.split('\n')
    # try:
    #     vim.command('call append(0, "{0}")'.format(contentslist))
    for index, line in enumerate(contentslist):
        vim.current.buffer.append(line)
    vim.command('execute \'wincmd j\'')
    vim.command('normal! `xzt``')

def delete_old_output_if_exists():
    if int(vim.eval('buflisted("executor_output")')):
        capture_buffer_height_if_visible()
        vim.command('bdelete executor_output')

def capture_buffer_height_if_visible():
    executor_output_winnr = int(vim.eval('bufwinnr(bufname("executor_output"))'))
    if executor_output_winnr > 0:
        executor_output_winheight = vim.eval('winheight("{}")'.format(executor_output_winnr))
        vim.command("let g:executor_output_win_height = {}".format(executor_output_winheight))

def get_visual_selection():
    buf = vim.current.buffer
    starting_line_num, col1 = buf.mark('<')
    ending_line_num, col2 = buf.mark('>')
    return vim.eval('getline({}, {})'.format(starting_line_num, ending_line_num))

def get_correct_buffer(buffer_type):
    if buffer_type == "buffer":
        return vim.current.buffer
    elif buffer_type == "selection":
        return get_visual_selection()


