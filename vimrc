set nocompatible                " disable compatibility with vi (enables some vim features)
set background=dark             " set color scheme (for light or dark backgrounds)
set backspace=indent,eol,start  " allow backspacing over everything in insert mode
set nobackup                    " do not keep a backup file
set history=50                  " keep 50 lines of command line history
set ruler                       " show the cursor position all the time
set showcmd                     " display incomplete commands
set incsearch                   " do incremental searching
set number                      " line numbers
set tabstop=4                   " how many columns a tab counts for
set shiftwidth=4                " how many columns is idented with reindent operations
set expandtab                   " use spaces instead of tabs
set textwidth=0                 " number of columns before automatic line break (0=disable)
set nowrap                      " dont wrap lines
set modeline                    " execute modeline (vim configuration at the end of files)

" Highlight ugly whitespaces.
highlight WhitespaceEOL ctermbg=red guibg=red
match WhitespaceEOL /\s\+$/

" Highlight text over 80 columns.
augroup vimrc_autocmds
    autocmd BufEnter * highlight OverLength ctermbg=darkgrey guibg=#592929
    autocmd BufEnter * match OverLength /\%79v.*/
augroup END

" Enable mouse, if available.
if has('mouse')
    set mouse=a
endif

" Switch syntax highlighting on, when the terminal has colors.
" Also switch on highlighting the last used search pattern.
if &t_Co > 2 || has("gui_running")
    syntax on
    set hlsearch
endif

if has("autocmd")
    " enable file type detection.
    " use the default filetype settings, so that mail gets 'tw' set to 72,
    " 'cindent' is on in c files, etc.
    " also load indent files, to automatically do language-dependent indenting.
    filetype plugin indent on

    " put these in an autocmd group, so that we can delete them easily.
    augroup vimrcex
        au!

        " for all text files set 'textwidth' to 78 characters.
        autocmd filetype text setlocal textwidth=78

        " when editing a file, always jump to the last known cursor position.
        " don't do it when the position is invalid or when inside an event handler
        " (happens when dropping a file on gvim).
        " also don't do it when the mark is in the first line, that is the default
        " position when opening a file.
        autocmd bufreadpost *
                    \ if line("'\"") > 1 && line("'\"") <= line("$") |
                    \   exe "normal! g`\"" |
                    \ endif

    augroup end
else
    set autoindent
endif

" Convenient command to see the difference between the current buffer and the
" file it was loaded from, thus the changes you made.
" Only define it when not defined already.
if !exists(":DiffOrig")
    command DiffOrig vert new | set bt=nofile | r ++edit # | 0d_ | diffthis
		  \ | wincmd p | diffthis
endif
