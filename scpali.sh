#!/usr/bin/env bash

option=$1
file_dir=$2
given_dir=$3


if [ "$option" = "--up" -o "$option" = "--down" -o "$option" = "--updir" -o "$option" = "--downdir" ];then
    echo -e "\033[32m*************************\033[0m"
    echo -e "\033[32mYou choose "$option" mode\033[0m"
    echo -e "\033[32m*************************\n\033[0m"
    echo -e "\033[32mStarting...\033[0m"
    echo -e "\033[33mscp command debug log: \n\033[0m"
else
    echo -e "\033[31m********\033[0m"
    echo -e "\033[31mCommand arguments error!\033[0m"
    echo -e "\033[31m********\n\033[0m"
    echo -e "Usage:"
    echo -e "   --up <yourfile absolute path or current folder path>"
    echo -e "   --down <yourfile absolute path or current folder path>"
    echo -e "   --updir <yourdir absolute path or current folder path>"
    echo -e "   --downdir <yourdir absolute path or current folder path>"
    echo -e "\n"
fi


function PrintInfo()
{
    if [ "$?" = "0" ]; then
        echo -e "\033[32m
         ________
        < Sucess >
         --------
                \   ^__^
                 \  (oo)\_______
                    (__)\       )\/\

                        ||----w |
                        ||     ||
        \033[0m"
        if [[ "$1" = *"dir" ]]; then
            # echo -e "\033[32m****** Your directory [ ${file_dir##*/} ] has been --downloaded ******\033[0m"
            if [[ "$1" = "--up"*  ]]; then
                if [[ -z "$given_dir" ]]; then
                    echo -e "\033[32m****** uploaded remote directory path [ ~/${file_dir##*/} ] ******\033[0m"
                else
                    echo -e "\033[32m****** uploaded remote directory path [ "$given_dir"~/${file_dir##*/} ] ******\033[0m"
                fi
            else
                if [[ -z "$given_dir" ]]; then
                    echo -e "\033[32m****** downloaded local directory path [ ~/"$file_dir" ] ******\033[0m"
                else
                    echo -e "\033[32m****** downloaded local directory path [ "$given_dir"/"$file_dir" ] ******\033[0m"
                fi
            fi
        else
            # echo -e "\033[32m****** Your file [ ${file_dir##*/} ] has been --downloaded ******\033[0m"
            if [[ "$1" = "--up"*  ]]; then
                if [[ -z "$given_dir" ]]; then
                    echo -e "\033[32m****** uploaded remote file path [ ~/${file_dir##*/} ] ******\033[0m"
                else
                    echo -e "\033[32m****** uploaded remote file path [ "$given_dir"${file_dir##*/} ] ******\033[0m"
                fi
            else
                if [[ -z "$given_dir" ]]; then
                    echo -e "\033[32m****** downloaded local file path [ ~/${file_dir##*/} ] ******\033[0m"
                else
                    echo -e "\033[32m****** downloaded local file path [ "$given_dir"${file_dir##*/} ] ******\033[0m"
                fi
            fi
        fi
    else
        echo -e "\033[31m
 ____                                _____
|  _ \ _ __ ___   ___ ___  ___ ___  | ____|_ __ _ __ ___  _ __
| |_) | '__/ _ \ / __/ _ \/ __/ __| |  _| | '__| '__/ _ \| '__|
|  __/| | | (_) | (_|  __/\__ \__ \ | |___| |  | | | (_) | |
|_|   |_|  \___/ \___\___||___/___/ |_____|_|  |_|  \___/|_|
        \033[0m"
    fi
}

if [ "$option" = "--up" ]; then
    if [ -z "$given_dir" ]; then
        scp -i ~/.ssh/aliadminrsa -v "$file_dir" admin@120.78.128.108:~/
    else
        scp -i ~/.ssh/aliadminrsa -v "$file_dir" admin@120.78.128.108:"$given_dir"
    fi
    PrintInfo "$file_dir"
elif [ "$option" = "--down" ]; then
    if [ -z "$given_dir" ]; then
        scp -i ~/.ssh/aliadminrsa -v admin@120.78.128.108:"$file_dir" ~/
    else
        scp -i ~/.ssh/aliadminrsa -v admin@120.78.128.108:"$file_dir" "$given_dir"
    fi
    PrintInfo "$file_dir"
elif [ "$option" = "--updir" ]; then
    if [ -z "$given_dir" ]; then
        scp -i ~/.ssh/aliadminrsa -v -r "$file_dir" admin@120.78.128.108:~/
    else
        scp -i ~/.ssh/aliadminrsa -v -r "$file_dir" admin@120.78.128.108:"$given_dir"
    fi
    PrintInfo "$file_dir"
elif [ "$option" = "--downdir" ]; then
    if [ -z "$given_dir" ]; then
        scp -i ~/.ssh/aliadminrsa -v -r admin@120.78.128.108:"$file_dir" ~/
    else
        scp -i ~/.ssh/aliadminrsa -v -r admin@120.78.128.108:"$file_dir" "$given_dir"
    fi
    PrintInfo "$file_dir"
fi

