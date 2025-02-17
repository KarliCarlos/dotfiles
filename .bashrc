#
# ~/.bashrc
#

export PATH="$HOME/bin:$PATH"

# If not running interactively, don't do anything
[[ $- != *i* ]] && return

alias ls='ls --color=auto'
alias grep='grep --color=auto'

alias la='ls -a'
alias ..='cd ..'
PS1='[\u@\h \W]\$ '

neofetch --source ~/.config/neofetch/logo
eval "$(starship init bash)"
