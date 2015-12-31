" All system-wide defaults are set in $VIMRUNTIME/debian.vim and sourced by
" the call to :runtime you can find below.  If you wish to change any of those
" settings, you should do it in this file (/etc/vim/vimrc), since debian.vim
" will be overwritten everytime an upgrade of the vim packages is performed.
" It is recommended to make changes after sourcing debian.vim since it alters
" the value of the 'compatible' option.

" This line should not be removed as it ensures that various options are
" properly set to work with the Vim-related packages available in Debian.

if has("syntax")
  syntax on
endif

try
  colorscheme desert
endtry

set nocompatible

" Set utf-8 as the standard encoding
" and en_US as the standard language
set encoding=utf8

" Set Unix as the standard file type
set ffs=unix,dos,mac

" Where split files should go
set splitbelow
set splitright

" Use smart tabbing
set smarttab

" Use 4 spaces for tabs
set expandtab
set tabstop=4
set shiftwidth=4

" How many lines of history to remember
set history=1000

" Linebreak at 500 characters
set lbr
set tw=500

" Disable swap and backup files
set nobackup
set nowb
set noswapfile

" Treat long lines as break lines
map j gj
map k gk

" Move between windows easier
map <C-j> <C-W>j
map <C-k> <C-W>k
map <C-h> <C-W>h
map <C-l> <C-W>l

" Useful mappings for managing tabs
map <leader>tn :tabnew<cr>
map <leader>to :tabonly<cr>
map <leader>tc :tabclose<cr>
map <leader>tm :tabmove<cr>

" Open a new tab with the current buffer's path
map <leader>te :tabedit <c-r>=expand("%:p:h")<cr>/

" Switch the cwd to the directory of the open buffer
map <leader>cd :cd %:p:h<cr>:pwd<cr>

" Set the behavior when switching between buffers
try
  set switchbuf=useopen,usetab,newtab
  set stal=2
catch
endtry

" Enable auto indent and smart indent
set ai
set si

" Have backspace actually go backwards
set backspace=eol,start,indent
set whichwrap+=<,>,h,l

" Allow tab completion in the menu
set wildmenu
set wildignore=*.o,*.d,*~,*.pyc,.git

" Set viminfo
set viminfo=%,\"100,'10,/50,:100,h,f0,n~/.viminfo

" Have vim jump to the last location when opening a file
if has("autocmd")
  au BufReadPost * if line("'\"") > 1 && line("'\"") <= line("$") | exe "normal! g'\"" | endif
endif

" Have vim load indent rules and plugins
if has("autocmd")
  filetype plugin indent on
endif

set timeoutlen=100  " To prevent the lag on 'O'
set scrolloff=9     " Set number of lines to the cursor when moving vertically
set ruler           " Display the bar at the bottom 
set wrap            " Wrap long lines
set hlsearch        " Highlight matches when searching
set showcmd		    " Show (partial) command in status line.
set showmatch       " Show matching brackets.
set mat=2           " How many tenths of a second to blink when matching brackets
set smartcase       " Do smart case matching
set incsearch       " Incremental search
set autowrite       " Automatically save before commands like :next and :make
set hidden          " Hide buffers when they are abandoned
set mouse=a         " Enable mouse usage (all modes)
set lazyredraw      " Don't redraw when running macros
set magic           " Use traditional regular expressions (see wiki)

" Pressing * or # when in visual mode searches for the current selection
vnoremap <silent> * :call VisualSelection('f')<cr>
vnoremap <silent> # :call VisualSelection('b')<cr>

" Delete trailing white space on save
func! DeleteTrailingWS()
  exe "normal mz"
  %s/\s\+$//ge
  exe "normal `z"
endfunc

" And call it on certain files
if has("autocmd")
  autocmd BufWrite *.py :call DeleteTrailingWS()
endif

"" vimgrep settings
"" When you press gv you vimgrep after the selected text
"vnoremap <silent> gv :call VisualSelection('gv')<CR>
"
"" Open vimgrep and put the cursor in the right position
"map <leader>g :vimgrep // **/*.<left><left><left><left><left><left><left>
"
"" Vimgreps in the current file
"map <leader><space> :vimgrep // <C-R>%<C-A><right><right><right><right><right><right><right><right><right>
"
"" When you press <leader>r you can search and replace the selected text
"vnoremap <silent> <leader>r :call VisualSelection('replace')<CR>
"
"" Do :help cope if you are unsure what cope is. It's super useful!
""
"" When you search with vimgrep, display your results in cope by doing:
""   <leader>cc
""
"" To go to the next search result do:
""   <leader>n
""
"" To go to the previous search results do:
""   <leader>p
""
"map <leader>cc :botright cope<cr>
"map <leader>co ggVGy:tabnew<cr>:set syntax=qf<cr>pgg
"map <leader>n :cn<cr>
"map <leader>p :cp<cr>
"
"" Spelling checking
"" Pressing ,ss will toggle and untoggle spell checking
"map <leader>ss :setlocal spell!<cr>
"
"" Shortcuts using <leader>
"map <leader>sn ]s
"map <leader>sp [s
"map <leader>sa zg
"map <leader>s? z=

