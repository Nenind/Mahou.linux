#!/bin/sh
# return current keyboard layout
setxkbmap -v | awk -F "+" '/symbols/ {print $2}'