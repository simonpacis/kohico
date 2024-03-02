let SessionLoad = 1
if &cp | set nocp | endif
let s:cpo_save=&cpo
set cpo&vim
imap <C-G>S <Plug>ISurround
imap <C-G>s <Plug>Isurround
imap <C-S> <Plug>Isurround
inoremap <Plug>(emmet-merge-lines) =emmet#util#closePopup()<NL>=emmet#mergeLines()<NL>inoremap <Plug>(emmet-anchorize-summary) =emmet#util#closePopup()<NL>=emmet#anchorizeURL(1)<NL>inoremap <Plug>(emmet-anchorize-url) =emmet#util#closePopup()<NL>=emmet#anchorizeURL(0)<NL>inoremap <Plug>(emmet-remove-tag) =emmet#util#closePopup()<NL>=emmet#removeTag()<NL>inoremap <Plug>(emmet-split-join-tag) :call emmet#splitJoinTag()<NL>inoremap <Plug>(emmet-toggle-comment) =emmet#util#closePopup()<NL>=emmet#toggleComment()<NL>inoremap <Plug>(emmet-image-encode) =emmet#util#closePopup()<NL>=emmet#imageEncode()<NL>inoremap <Plug>(emmet-image-size) =emmet#util#closePopup()<NL>=emmet#imageSize()<NL>inoremap <Plug>(emmet-move-prev-item) :call emmet#moveNextPrevItem(1)<NL>inoremap <Plug>(emmet-move-next-item) :call emmet#moveNextPrevItem(0)<NL>inoremap <Plug>(emmet-move-prev) =emmet#util#closePopup()<NL>=emmet#moveNextPrev(1)<NL>inoremap <Plug>(emmet-move-next) =emmet#util#closePopup()<NL>=emmet#moveNextPrev(0)<NL>inoremap <Plug>(emmet-balance-tag-outword) :call emmet#balanceTag(-1)<NL>inoremap <Plug>(emmet-balance-tag-inward) :call emmet#balanceTag(1)<NL>inoremap <Plug>(emmet-update-tag) =emmet#util#closePopup()<NL>=emmet#updateTag()<NL>inoremap <Plug>(emmet-expand-word) =emmet#util#closePopup()<NL>=emmet#expandAbbr(1,"")<NL>inoremap <Plug>(emmet-expand-abbr) =emmet#util#closePopup()<NL>=emmet#expandAbbr(0,"")<NL>imap <M-Down> <Plug>(copilot-accept-line)
inoremap <Plug>(emmet-anchorize-summary) =emmet#util#closePopup()<NL>=emmet#anchorizeURL(1)<NL>inoremap <Plug>(emmet-anchorize-url) =emmet#util#closePopup()<NL>=emmet#anchorizeURL(0)<NL>inoremap <Plug>(emmet-remove-tag) =emmet#util#closePopup()<NL>=emmet#removeTag()<NL>inoremap <Plug>(emmet-split-join-tag) :call emmet#splitJoinTag()<NL>inoremap <Plug>(emmet-toggle-comment) =emmet#util#closePopup()<NL>=emmet#toggleComment()<NL>inoremap <Plug>(emmet-image-encode) =emmet#util#closePopup()<NL>=emmet#imageEncode()<NL>inoremap <Plug>(emmet-image-size) =emmet#util#closePopup()<NL>=emmet#imageSize()<NL>inoremap <Plug>(emmet-move-prev-item) :call emmet#moveNextPrevItem(1)<NL>inoremap <Plug>(emmet-move-next-item) :call emmet#moveNextPrevItem(0)<NL>inoremap <Plug>(emmet-move-prev) =emmet#util#closePopup()<NL>=emmet#moveNextPrev(1)<NL>inoremap <Plug>(emmet-move-next) =emmet#util#closePopup()<NL>=emmet#moveNextPrev(0)<NL>inoremap <Plug>(emmet-balance-tag-outword) :call emmet#balanceTag(-1)<NL>inoremap <Plug>(emmet-balance-tag-inward) :call emmet#balanceTag(1)<NL>inoremap <Plug>(emmet-update-tag) =emmet#util#closePopup()<NL>=emmet#updateTag()<NL>inoremap <Plug>(emmet-expand-word) =emmet#util#closePopup()<NL>=emmet#expandAbbr(1,"")<NL>inoremap <Plug>(emmet-expand-abbr) =emmet#util#closePopup()<NL>=emmet#expandAbbr(0,"")<NL>imap <M-Down> <Plug>(copilot-accept-line)
inoremap <Plug>(emmet-anchorize-url) =emmet#util#closePopup()
=emmet#anchorizeURL(0)
inoremap <Plug>(emmet-remove-tag) =emmet#util#closePopup()
=emmet#removeTag()
inoremap <Plug>(emmet-split-join-tag) :call emmet#splitJoinTag()
inoremap <Plug>(emmet-toggle-comment) =emmet#util#closePopup()
=emmet#toggleComment()
inoremap <Plug>(emmet-image-encode) =emmet#util#closePopup()
=emmet#imageEncode()
inoremap <Plug>(emmet-image-size) =emmet#util#closePopup()
=emmet#imageSize()
inoremap <Plug>(emmet-move-prev-item) :call emmet#moveNextPrevItem(1)
inoremap <Plug>(emmet-move-next-item) :call emmet#moveNextPrevItem(0)
inoremap <Plug>(emmet-move-prev) =emmet#util#closePopup()
=emmet#moveNextPrev(1)
inoremap <Plug>(emmet-move-next) =emmet#util#closePopup()
=emmet#moveNextPrev(0)
inoremap <Plug>(emmet-balance-tag-outword) :call emmet#balanceTag(-1)
inoremap <Plug>(emmet-balance-tag-inward) :call emmet#balanceTag(1)
inoremap <Plug>(emmet-update-tag) =emmet#util#closePopup()
=emmet#updateTag()
inoremap <Plug>(emmet-expand-word) =emmet#util#closePopup()
=emmet#expandAbbr(1,"")
inoremap <Plug>(emmet-expand-abbr) =emmet#util#closePopup()
=emmet#expandAbbr(0,"")
imap <M-Down> <Plug>(copilot-accept-line)
imap <M-Right> <Plug>(copilot-accept-word)
imap <M-Bslash> <Plug>(copilot-suggest)
imap <M-[> <Plug>(copilot-previous)
imap <M-]> <Plug>(copilot-next)
imap <Plug>(copilot-suggest) <Cmd>call copilot#Suggest()<NL>imap <Plug>(copilot-previous) <Cmd>call copilot#Previous()<NL>imap <Plug>(copilot-next) <Cmd>call copilot#Next()<NL>imap <Plug>(copilot-dismiss) <Cmd>call copilot#Dismiss()<NL>map! <D-v> *
imap <Plug>(copilot-previous) <Cmd>call copilot#Previous()<NL>imap <Plug>(copilot-next) <Cmd>call copilot#Next()<NL>imap <Plug>(copilot-dismiss) <Cmd>call copilot#Dismiss()<NL>map! <D-v> *
imap <Plug>(copilot-next) <Cmd>call copilot#Next()
imap <Plug>(copilot-dismiss) <Cmd>call copilot#Dismiss()
map! <D-v> *
nnoremap  h
nnoremap <NL> j
nnoremap  k
nnoremap  l
nnoremap <silent>  :CtrlP<NL>vnoremap -d ""d
vnoremap -d ""d
nnoremap -D ""D
nnoremap -d ""d
nnoremap -ø :Mdto docx<NL>nnoremap -æ :Mdto pdf<NL>nnoremap -p :call WlTable()<NL>nnoremap -bl :ls<NL>nnoremap -bq :bp | bd #<NL>nnoremap -h :bprevious<NL>nnoremap -l :bnext<NL>nnoremap <silent> -m :call OneSentencePerLine(1, line('$'))<NL>nnoremap -t :call NewBufferWithoutNerdTree()<NL>nnoremap -9 :blast<NL>nnoremap -8 <Plug>AirlineSelectTab8
nnoremap -æ :Mdto pdf<NL>nnoremap -p :call WlTable()<NL>nnoremap -bl :ls<NL>nnoremap -bq :bp | bd #<NL>nnoremap -h :bprevious<NL>nnoremap -l :bnext<NL>nnoremap <silent> -m :call OneSentencePerLine(1, line('$'))<NL>nnoremap -t :call NewBufferWithoutNerdTree()<NL>nnoremap -9 :blast<NL>nnoremap -8 <Plug>AirlineSelectTab8
nnoremap -p :call WlTable()
nnoremap -bl :ls
nnoremap -bq :bp | bd #
nnoremap -h :bprevious
nnoremap -l :bnext
nnoremap <silent> -m :call OneSentencePerLine(1, line('$'))
nnoremap -t :call NewBufferWithoutNerdTree()
nnoremap -9 :blast
nnoremap -8 <Plug>AirlineSelectTab8
nnoremap -7 <Plug>AirlineSelectTab7
nnoremap -6 <Plug>AirlineSelectTab6
nnoremap -5 <Plug>AirlineSelectTab5
nnoremap -4 <Plug>AirlineSelectTab4
nnoremap -3 <Plug>AirlineSelectTab3
nnoremap -2 <Plug>AirlineSelectTab2
nnoremap -1 <Plug>AirlineSelectTab1
nnoremap -q :Bonly<NL>nnoremap -w :bp|sp|bn|bd<NL>nnoremap -n :call ToggleNERDTree()<NL>nmap -r :NERDTreeFocus<NL>R
nnoremap -w :bp|sp|bn|bd<NL>nnoremap -n :call ToggleNERDTree()<NL>nmap -r :NERDTreeFocus<NL>R
nnoremap -n :call ToggleNERDTree()
nmap -r :NERDTreeFocus
R
nnoremap -å :Combine<NL>nnoremap <silent> -z :call GoyoOpenWithoutNerdTree()<NL>imap ¨m <Plug>(emmet-merge-lines)
nnoremap <silent> -z :call GoyoOpenWithoutNerdTree()<NL>imap ¨m <Plug>(emmet-merge-lines)
imap ¨m <Plug>(emmet-merge-lines)
imap ¨A <Plug>(emmet-anchorize-summary)
imap ¨a <Plug>(emmet-anchorize-url)
imap ¨k <Plug>(emmet-remove-tag)
imap ¨j <Plug>(emmet-split-join-tag)
imap ¨/ <Plug>(emmet-toggle-comment)
imap ¨I <Plug>(emmet-image-encode)
imap ¨i <Plug>(emmet-image-size)
imap ¨N <Plug>(emmet-move-prev)
imap ¨n <Plug>(emmet-move-next)
imap ¨D <Plug>(emmet-balance-tag-outword)
imap ¨d <Plug>(emmet-balance-tag-inward)
imap ¨u <Plug>(emmet-update-tag)
imap ¨; <Plug>(emmet-expand-word)
imap ¨, <Plug>(emmet-expand-abbr)
imap Ý <Plug>(copilot-next)
imap Û <Plug>(copilot-previous)
imap Ü <Plug>(copilot-suggest)
nnoremap D "_D
xmap S <Plug>VSurround
nnoremap <silent> [unite]cx :exec "Unite  -default-action=start citation/key:" . escape(input('Search Key : '),' ') <NL>nnoremap <silent> [unite]c :Unite -buffer-name=citation-start-insert -default-action=append      citation/key<NL>nnoremap [unite] <Nop>
nnoremap <silent> [unite]c :Unite -buffer-name=citation-start-insert -default-action=append      citation/key<NL>nnoremap [unite] <Nop>
nnoremap [unite] <Nop>
nmap cS <Plug>CSurround
nmap cs <Plug>Csurround
nmap ds <Plug>Dsurround
vnoremap d "_d
nnoremap d "_d
xmap gx <Plug>NetrwBrowseXVis
nmap gx <Plug>NetrwBrowseX
xmap gS <Plug>VgSurround
nnoremap x "_x
nmap ySS <Plug>YSsurround
nmap ySs <Plug>YSsurround
nmap yss <Plug>Yssurround
nmap yS <Plug>YSurround
nmap ys <Plug>Ysurround
xnoremap <silent> <Plug>NetrwBrowseXVis :call netrw#BrowseXVis()<NL>nnoremap <silent> <Plug>NetrwBrowseX :call netrw#BrowseX(netrw#GX(),netrw#CheckIfRemote(netrw#GX()))<NL>nnoremap <silent> <Plug>SurroundRepeat .
nnoremap <silent> <Plug>NetrwBrowseX :call netrw#BrowseX(netrw#GX(),netrw#CheckIfRemote(netrw#GX()))<NL>nnoremap <silent> <Plug>SurroundRepeat .
nnoremap <silent> <Plug>SurroundRepeat .
vnoremap <Plug>(emmet-code-pretty) :call emmet#codePretty()<NL>nnoremap <Plug>(emmet-merge-lines) :call emmet#mergeLines()<NL>nnoremap <Plug>(emmet-anchorize-summary) :call emmet#anchorizeURL(1)<NL>nnoremap <Plug>(emmet-anchorize-url) :call emmet#anchorizeURL(0)<NL>nnoremap <Plug>(emmet-remove-tag) :call emmet#removeTag()<NL>nnoremap <Plug>(emmet-split-join-tag) :call emmet#splitJoinTag()<NL>nnoremap <Plug>(emmet-toggle-comment) :call emmet#toggleComment()<NL>nnoremap <Plug>(emmet-image-encode) :call emmet#imageEncode()<NL>nnoremap <Plug>(emmet-image-size) :call emmet#imageSize()<NL>nnoremap <Plug>(emmet-move-prev-item) :call emmet#moveNextPrevItem(1)<NL>nnoremap <Plug>(emmet-move-next-item) :call emmet#moveNextPrevItem(0)<NL>nnoremap <Plug>(emmet-move-prev) :call emmet#moveNextPrev(1)<NL>nnoremap <Plug>(emmet-move-next) :call emmet#moveNextPrev(0)<NL>vnoremap <Plug>(emmet-balance-tag-outword) :call emmet#balanceTag(-1)<NL>nnoremap <Plug>(emmet-balance-tag-outword) :call emmet#balanceTag(-1)<NL>vnoremap <Plug>(emmet-balance-tag-inward) :call emmet#balanceTag(1)<NL>nnoremap <Plug>(emmet-balance-tag-inward) :call emmet#balanceTag(1)<NL>nnoremap <Plug>(emmet-update-tag) :call emmet#updateTag()<NL>nnoremap <Plug>(emmet-expand-word) :call emmet#expandAbbr(1,"")<NL>vnoremap <Plug>(emmet-expand-abbr) :call emmet#expandAbbr(2,"")<NL>nnoremap <Plug>(emmet-expand-abbr) :call emmet#expandAbbr(3,"")<NL>nnoremap <silent>  :CtrlP<NL>noremap <Right> <Nop>
nnoremap <Plug>(emmet-merge-lines) :call emmet#mergeLines()<NL>nnoremap <Plug>(emmet-anchorize-summary) :call emmet#anchorizeURL(1)<NL>nnoremap <Plug>(emmet-anchorize-url) :call emmet#anchorizeURL(0)<NL>nnoremap <Plug>(emmet-remove-tag) :call emmet#removeTag()<NL>nnoremap <Plug>(emmet-split-join-tag) :call emmet#splitJoinTag()<NL>nnoremap <Plug>(emmet-toggle-comment) :call emmet#toggleComment()<NL>nnoremap <Plug>(emmet-image-encode) :call emmet#imageEncode()<NL>nnoremap <Plug>(emmet-image-size) :call emmet#imageSize()<NL>nnoremap <Plug>(emmet-move-prev-item) :call emmet#moveNextPrevItem(1)<NL>nnoremap <Plug>(emmet-move-next-item) :call emmet#moveNextPrevItem(0)<NL>nnoremap <Plug>(emmet-move-prev) :call emmet#moveNextPrev(1)<NL>nnoremap <Plug>(emmet-move-next) :call emmet#moveNextPrev(0)<NL>vnoremap <Plug>(emmet-balance-tag-outword) :call emmet#balanceTag(-1)<NL>nnoremap <Plug>(emmet-balance-tag-outword) :call emmet#balanceTag(-1)<NL>vnoremap <Plug>(emmet-balance-tag-inward) :call emmet#balanceTag(1)<NL>nnoremap <Plug>(emmet-balance-tag-inward) :call emmet#balanceTag(1)<NL>nnoremap <Plug>(emmet-update-tag) :call emmet#updateTag()<NL>nnoremap <Plug>(emmet-expand-word) :call emmet#expandAbbr(1,"")<NL>vnoremap <Plug>(emmet-expand-abbr) :call emmet#expandAbbr(2,"")<NL>nnoremap <Plug>(emmet-expand-abbr) :call emmet#expandAbbr(3,"")<NL>nnoremap <silent>  :CtrlP<NL>noremap <Right> <Nop>
nnoremap <Plug>(emmet-anchorize-summary) :call emmet#anchorizeURL(1)
nnoremap <Plug>(emmet-anchorize-url) :call emmet#anchorizeURL(0)
nnoremap <Plug>(emmet-remove-tag) :call emmet#removeTag()
nnoremap <Plug>(emmet-split-join-tag) :call emmet#splitJoinTag()
nnoremap <Plug>(emmet-toggle-comment) :call emmet#toggleComment()
nnoremap <Plug>(emmet-image-encode) :call emmet#imageEncode()
nnoremap <Plug>(emmet-image-size) :call emmet#imageSize()
nnoremap <Plug>(emmet-move-prev-item) :call emmet#moveNextPrevItem(1)
nnoremap <Plug>(emmet-move-next-item) :call emmet#moveNextPrevItem(0)
nnoremap <Plug>(emmet-move-prev) :call emmet#moveNextPrev(1)
nnoremap <Plug>(emmet-move-next) :call emmet#moveNextPrev(0)
vnoremap <Plug>(emmet-balance-tag-outword) :call emmet#balanceTag(-1)
nnoremap <Plug>(emmet-balance-tag-outword) :call emmet#balanceTag(-1)
vnoremap <Plug>(emmet-balance-tag-inward) :call emmet#balanceTag(1)
nnoremap <Plug>(emmet-balance-tag-inward) :call emmet#balanceTag(1)
nnoremap <Plug>(emmet-update-tag) :call emmet#updateTag()
nnoremap <Plug>(emmet-expand-word) :call emmet#expandAbbr(1,"")
vnoremap <Plug>(emmet-expand-abbr) :call emmet#expandAbbr(2,"")
nnoremap <Plug>(emmet-expand-abbr) :call emmet#expandAbbr(3,"")
nnoremap <silent> <C-P> :CtrlP
noremap <Right> <Nop>
noremap <Left> <Nop>
noremap <Down> <Nop>
noremap <Up> <Nop>
nnoremap <C-H> h
nnoremap <C-L> l
nnoremap <C-K> k
nnoremap <C-J> j
vmap <BS> "-d
vmap <D-x> "*d
vmap <D-c> "*y
vmap <D-v> "-d"*P
nmap <D-v> "*P
imap S <Plug>ISurround
imap s <Plug>Isurround
imap  <Plug>Isurround
vmap ¨c <Plug>(emmet-code-pretty)
nmap ¨m <Plug>(emmet-merge-lines)
nmap ¨A <Plug>(emmet-anchorize-summary)
nmap ¨a <Plug>(emmet-anchorize-url)
nmap ¨k <Plug>(emmet-remove-tag)
nmap ¨j <Plug>(emmet-split-join-tag)
nmap ¨/ <Plug>(emmet-toggle-comment)
nmap ¨I <Plug>(emmet-image-encode)
nmap ¨i <Plug>(emmet-image-size)
nmap ¨N <Plug>(emmet-move-prev)
nmap ¨n <Plug>(emmet-move-next)
vmap ¨D <Plug>(emmet-balance-tag-outword)
nmap ¨D <Plug>(emmet-balance-tag-outword)
vmap ¨d <Plug>(emmet-balance-tag-inward)
nmap ¨d <Plug>(emmet-balance-tag-inward)
nmap ¨u <Plug>(emmet-update-tag)
nmap ¨; <Plug>(emmet-expand-word)
vmap ¨, <Plug>(emmet-expand-abbr)
nmap ¨, <Plug>(emmet-expand-abbr)
let &cpo=s:cpo_save
unlet s:cpo_save
set background=dark
set backspace=indent,eol,start
set clipboard=unnamed
set fileencodings=ucs-bom,utf-8,default,latin1
set helplang=en
set hidden
set laststatus=2
set listchars=tab:|\ 
set modelines=0
set mouse=n
set regexpengine=2
set runtimepath=
set runtimepath+=~/.vim
set runtimepath+=~/.vim/pack/vendor/start/nerdtree
set runtimepath+=~/.vim/pack/thirdparty/start/vimoutliner
set runtimepath+=~/.vim/pack/themes/start/dracula
set runtimepath+=~/.vim/pack/dist/start/vim-airline
set runtimepath+=~/.vim/bundle/ack.vim
set runtimepath+=~/.vim/bundle/citation.vim
set runtimepath+=~/.vim/bundle/codi.vim
set runtimepath+=~/.vim/bundle/copilot.vim
set runtimepath+=~/.vim/bundle/ctrlp.vim
set runtimepath+=~/.vim/bundle/emmet-vim
set runtimepath+=~/.vim/bundle/goyo.vim
set runtimepath+=~/.vim/bundle/gruvbox
set runtimepath+=~/.vim/bundle/loremipsum
set runtimepath+=~/.vim/bundle/nerdtree
set runtimepath+=~/.vim/bundle/PHP-Indenting-for-VIm
set runtimepath+=~/.vim/bundle/send.vim
set runtimepath+=~/.vim/bundle/sparkup
set runtimepath+=~/.vim/bundle/surround
set runtimepath+=~/.vim/bundle/unite.vim
set runtimepath+=~/.vim/bundle/vim-colors-pencil
set runtimepath+=~/.vim/bundle/vim-javascript
set runtimepath+=~/.vim/bundle/vim-svelte
set runtimepath+=~/.vim/bundle/Vundle.vim
set runtimepath+=/usr/share/vim/vimfiles
set runtimepath+=/usr/share/vim/vim90
set runtimepath+=~/.vim/pack/themes/start/dracula/after
set runtimepath+=/usr/share/vim/vimfiles/after
set runtimepath+=~/.vim/bundle/vim-javascript/after
set runtimepath+=~/.vim/after
set shiftwidth=2
set showtabline=2
set smartindent
set tabline=%!airline#extensions#tabline#get()
set tabstop=2
set viminfo='100,<50,s10,h,!
set wildignore=*.pyc
set window=0
let s:so_save = &g:so | let s:siso_save = &g:siso | setg so=0 siso=0 | setl so=-1 siso=-1
let v:this_session=expand("<sfile>:p")
silent only
silent tabonly
cd ~/Documents/Dev/ko2hyp
if expand('%') == '' && !&modified && line('$') <= 1 && getline(1) == ''
  let s:wipebuf = bufnr('%')
endif
if &shortmess =~ 'A'
  set shortmess=aoOA
else
  set shortmess=aoO
endif
badd +34 README.md
badd +353 kohico.py
argglobal
%argdel
edit README.md
argglobal
balt kohico.py
let s:cpo_save=&cpo
set cpo&vim
imap <buffer> <C-N> <Plug>SparkupNext
imap <buffer> <C-E> <Plug>SparkupExecute
xnoremap <buffer> <silent> [[ :exe "normal! gv"|call search('\%(^#\{1,5\}\s\+\S\|^\S.*\n^[=-]\+$\)', "bsW")
nnoremap <buffer> <silent> [[ :call search('\%(^#\{1,5\}\s\+\S\|^\S.*\n^[=-]\+$\)', "bsW")
xnoremap <buffer> <silent> ]] :exe "normal! gv"|call search('\%(^#\{1,5\}\s\+\S\|^\S.*\n^[=-]\+$\)', "sW")
nnoremap <buffer> <silent> ]] :call search('\%(^#\{1,5\}\s\+\S\|^\S.*\n^[=-]\+$\)', "sW")
imap <buffer>  <Plug>SparkupExecute
imap <buffer>  <Plug>SparkupNext
let &cpo=s:cpo_save
unlet s:cpo_save
setlocal noautoindent
setlocal backupcopy=
setlocal nobinary
setlocal nobreakindent
setlocal breakindentopt=
setlocal bufhidden=
setlocal buflisted
setlocal buftype=
setlocal nocindent
setlocal cinkeys=0{,0},0),0],:,0#,!^F,o,O,e
setlocal cinoptions=
setlocal cinscopedecls=public,protected,private
setlocal cinwords=if,else,while,do,for,switch
setlocal colorcolumn=
setlocal comments=fb:*,fb:-,fb:+,n:>
setlocal commentstring=<!--%s-->
setlocal complete=.,w,b,u,t,i
setlocal concealcursor=
setlocal conceallevel=0
setlocal completefunc=
setlocal nocopyindent
setlocal cryptmethod=
setlocal nocursorbind
setlocal nocursorcolumn
setlocal nocursorline
setlocal cursorlineopt=both
setlocal define=
setlocal dictionary=
setlocal nodiff
setlocal equalprg=
setlocal errorformat=
setlocal expandtab
if &filetype != 'markdown'
setlocal filetype=markdown
endif
setlocal fillchars=
setlocal fixendofline
setlocal foldcolumn=0
setlocal foldenable
setlocal foldexpr=0
setlocal foldignore=#
setlocal foldlevel=0
setlocal foldmarker={{{,}}}
setlocal foldmethod=manual
setlocal foldminlines=1
setlocal foldnestmax=20
setlocal foldtext=foldtext()
setlocal formatexpr=
setlocal formatoptions=tcqln
setlocal formatlistpat=^\\s*\\d\\+\\.\\s\\+\\|^\\s*[-*+]\\s\\+\\|^\\[^\\ze[^\\]]\\+\\]:\\&^.\\{4\\}
setlocal formatprg=
setlocal grepprg=
setlocal iminsert=0
setlocal imsearch=-1
setlocal include=
setlocal includeexpr=
setlocal indentexpr=
setlocal indentkeys=0{,0},0),0],:,0#,!^F,o,O,e
setlocal noinfercase
setlocal iskeyword=@,48-57,_,192-255
setlocal keywordprg=
setlocal nolinebreak
setlocal nolisp
setlocal lispoptions=
setlocal lispwords=
set list
setlocal list
setlocal listchars=
setlocal makeencoding=
setlocal makeprg=
setlocal matchpairs=(:),{:},[:],<:>
setlocal modeline
setlocal modifiable
setlocal nrformats=bin,octal,hex
set number
setlocal number
setlocal numberwidth=4
setlocal omnifunc=htmlcomplete#CompleteTags
setlocal path=
setlocal nopreserveindent
setlocal nopreviewwindow
setlocal quoteescape=\\
setlocal noreadonly
setlocal norelativenumber
setlocal noscrollbind
setlocal scrolloff=-1
setlocal shiftwidth=4
setlocal noshortname
setlocal showbreak=
setlocal sidescrolloff=-1
setlocal signcolumn=auto
setlocal smartindent
setlocal nosmoothscroll
setlocal softtabstop=4
setlocal spell
setlocal spellcapcheck=[.?!]\\_[\\])'\"\	\ ]\\+
setlocal spellfile=
setlocal spelllang=en
setlocal spelloptions=
setlocal statusline=%!airline#statusline(1)
setlocal suffixesadd=
setlocal swapfile
setlocal synmaxcol=3000
if &syntax != 'markdown'
setlocal syntax=markdown
endif
setlocal tabstop=4
setlocal tagcase=
setlocal tagfunc=
setlocal tags=
setlocal termwinkey=
setlocal termwinscroll=10000
setlocal termwinsize=
setlocal textwidth=0
setlocal thesaurus=
setlocal thesaurusfunc=
setlocal noundofile
setlocal undolevels=-123456
setlocal virtualedit=
setlocal wincolor=
setlocal nowinfixheight
setlocal nowinfixwidth
setlocal wrap
setlocal wrapmargin=0
silent! normal! zE
let &fdl = &fdl
let s:l = 45 - ((38 * winheight(0) + 28) / 56)
if s:l < 1 | let s:l = 1 | endif
keepjumps exe s:l
normal! zt
keepjumps 45
normal! 0176|
tabnext 1
if exists('s:wipebuf') && len(win_findbuf(s:wipebuf)) == 0
  silent exe 'bwipe ' . s:wipebuf
endif
unlet! s:wipebuf
set winheight=1 winwidth=20
set shortmess=filnxtToOS
let s:sx = expand("<sfile>:p:r")."x.vim"
if filereadable(s:sx)
  exe "source " . fnameescape(s:sx)
endif
let &g:so = s:so_save | let &g:siso = s:siso_save
doautoall SessionLoadPost
unlet SessionLoad
" vim: set ft=vim :
let g:Pyvar=1