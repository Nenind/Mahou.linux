#!/bin/sh
# returns all avaible keyboard layouts
setxkbmap -query | grep layout | awk -F " " ' {print $2} '