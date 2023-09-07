#!/bin/bash
set -e

# vim-pathogen
rm -rf $HOME/.vim $HOME/.cache/jedi
mkdir -p $HOME/.vim/autoload $HOME/.vim/bundle
wget -O $HOME/.vim/autoload/pathogen.vim https://tpo.pe/pathogen.vim

# COC
git clone --depth 1 https://github.com/neoclide/coc.nvim $HOME/.vim/bundle/coc.nvim
cd $HOME/.vim/bundle/coc.nvim/
yarn install

# vimrc
VIMRC=$HOME/.vimrc

# general stuff
echo "set background=dark" > $VIMRC
echo "set encoding=utf-8" >> $VIMRC
echo "set nu" >> $VIMRC
echo "syntax on" >> $VIMRC
echo "" >> $VIMRC
# load plugins with pathogen
echo "execute pathogen#infect()" >> $VIMRC
echo "" >> $VIMRC
# python
echo "au BufNewFile,BufRead *.py set tabstop=4" >> $VIMRC
echo "au BufNewFile,BufRead *.py set softtabstop=4" >> $VIMRC
echo "au BufNewFile,BufRead *.py set shiftwidth=4" >> $VIMRC
echo "au BufNewFile,BufRead *.py set textwidth=88" >> $VIMRC
echo "au BufNewFile,BufRead *.py set expandtab" >> $VIMRC
echo "au BufNewFile,BufRead *.py set autoindent" >> $VIMRC
echo "au BufNewFile,BufRead *.py set fileformat=unix" >> $VIMRC
echo "" >> $VIMRC
echo "highlight BadWhitespace ctermbg=red guibg=darkred" >> $VIMRC
echo "au BufRead,BufNewFile *.py,*.pyw,*.c,*.h match BadWhitespace /\s\+$/" >> $VIMRC
echo "" >> $VIMRC
echo "set backspace=indent,eol,start" >> $VIMRC

vim +'CocInstall -sync coc-pyright' +qall

COC=$HOME/.vim/coc-settings.json
echo "{" > $COC
echo "  \"coc.preferences.formatOnSaveFiletypes\": [\"python\"]," >> $COC
echo "  \"python.linting.ruffEnabled\": true," >> $COC
echo "  \"python.linting.enabled\": true," >> $COC
echo "  \"python.formatting.provider\": \"black\"" >> $COC
echo "}" >> $COC
