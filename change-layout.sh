#!/bin/bash
current=`sh ./current-layout.sh`
all=`sh ./all-layouts.sh`
layout1=`echo $all | cut -d',' -f1`
layout2=`echo $all | cut -d',' -f2`
if [ "$layout1" == "$current" ]; then
    setxkbmap -layout "$layout2,$layout1"
elif [ "$layout2" == "$current" ]; then
    setxkbmap -layout "$layout1,$layout2"
fi
