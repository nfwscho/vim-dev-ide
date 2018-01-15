command! DevTest call vim_dev_ide#Test("buffer")
command! DevCreateSnippet call vim_samplesnip_maker#CreateAliasAndSnippets(expand('<cword>'))
command! DevNaverDic call vim_naver_dic#GetNaverDic(expand('<cword>'))
