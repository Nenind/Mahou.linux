# This repository contains things that may help making Mahou for linux.

Nothing special, just hooks, event listeners etc.

# Also projects which source code may be helpful:

- xinput
- xev
- ...

# keyboard-testing.py

Has ability to change last word on f7 key press, clear last word on space, though needs improvements.

# X11-EventListener.c

compile with `gcc X11-EventListener.c -lX11 -lXtst -oX11-Listener`.
Listens to keyboard events globally, need mouse events listening implementation too. Has no conversion functions at moment.

# current-layout.sh and all-layouts.sh

Details in files.