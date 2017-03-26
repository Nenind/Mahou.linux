/* include the X library headers */
#include <X11/Xlib.h>
#include <X11/Xutil.h>
#include <X11/Xos.h>

/* include some silly stuff */
#include <stdio.h>
#include <stdlib.h>

/* !!: my stuff */
#include <X11/extensions/XTest.h>
#include <wchar.h>
#include <locale.h>

/* here are our X variables */
int screen;
GC gc;
Display* d;
Window root;
/* here are our X routines declared! */
void init_x();
void close_x();
void redraw();

int main () {
	setlocale(LC_ALL,"");
	// WIN-ALTERNATIVE: HookCallback's WParam.
	XEvent event;		/* the XEvent declaration !!! */
	// WIN-ALTERNATIVE: HookCallback's LParam.
	KeySym key_sym;		/* a dealie-bob to handle KeyPress Events */	
	char text[255+1];		/* a char buffer for KeyPress Events */
	int kc_bytes = 0;
	char key_char[256+1];
	char *key_name;
	int revert;
	int masks = KeyPressMask|KeyReleaseMask|FocusChangeMask|ButtonPressMask|Expose;
    d = XOpenDisplay(NULL);
    root = DefaultRootWindow(d);
    Window curFocus;
	
    XGetInputFocus (d, &curFocus, &revert);
    XSelectInput(d, curFocus, masks);
	// XGrabPointer(d, root, False, ButtonPressMask | ButtonReleaseMask |
                     // PointerMotionMask, GrabModeAsync, GrabModeAsync, None,
                     // None, CurrentTime);
    int root_x, root_y; //<--two
    unsigned int mask; //<--three
	// XQueryPointer(d, root, &root, &root, &root_x, &root_y, &root_x, &root_y, &mask);
	init_x();

	/* look for events forever... */
	while(1) {
		// WIN-ALTERNATIVE: CallNextHook(-Ex).
		XNextEvent(d, &event);
		XQueryPointer (d, root,
                 &event.xbutton.root, &event.xbutton.window,
                 &event.xbutton.x_root, &event.xbutton.y_root,
                 &event.xbutton.x, &event.xbutton.y,
				 &mask);
		if (event.type == ButtonPressMask) {
			sprintf(text, "You pressed mouse button [%u].\n", event.xbutton.button);
			XDrawString(d,root,gc,0,1, text, strlen(text));
			// printf();
		}
		if (event.type == FocusOut) {
			printf ("Focus changed!\n");
			printf ("Old focus is %d\n", (int)curFocus);
			if (curFocus != root)
				XSelectInput(d, curFocus, 0);
			XGetInputFocus (d, &curFocus, &revert);
			printf ("New focus is %d\n", (int)curFocus);
			if (curFocus == PointerRoot)
				curFocus = root;
			XSelectInput(d, curFocus, masks);
			// break;
		}
		if (event.type==Expose && event.xexpose.count==0) {
			/* the window was exposed redraw it! */
			redraw();
		}		   // WIN-ALTERNATIVE: ToUnicode(-Ex)?
		kc_bytes = XLookupString(&event.xkey,key_char,255,&key_sym,0);
		key_char[kc_bytes] = '\0';
				   // WIN-ALTERNATIVE: GetKeyNameText(-W)?
		key_name = XKeysymToString(key_sym);
		if (event.type == KeyPress) {
			printf("Key: [%s] with code: [%u] pressed", key_name, event.xkey.keycode);
			if (kc_bytes > 0) {
				printf (", char: [%s]", key_char);
			}
			printf (".\n");
			if (strcmp(key_name, "F4") == 0) {
				printf("Passed exit command.\n");
				close_x();
			}
			if (strcmp(key_name, "F7") == 0) {
				XTestFakeKeyEvent(d, 10, True, 0);
				XTestFakeKeyEvent(d, 10, False, 0);
			}
		}
		if (event.type == ButtonPress) {
			/* tell where the mouse Button was Pressed */
			int x = event.xbutton.x,
			    y = event.xbutton.y;
			strcpy(text,"You clicked here!");
			XSetForeground(d,gc,rand()%event.xbutton.x%255);
			XDrawString(d,root,gc,x,y, text, strlen(text));
		}
	}
}

void init_x() {
/* get the colors black and white (see section for details) */        
	unsigned long black,white;
   	screen=DefaultScreen(d);
	black=BlackPixel(d,screen),
	white=WhitePixel(d, screen);
   	root=XCreateSimpleWindow(d,DefaultRootWindow(d),0,0,	
		300, 300, 5,black, white);
	XSetStandardProperties(d,root,"Howdy","Hi",None,NULL,0,NULL);
	XSelectInput(d, root, ExposureMask|ButtonPressMask|KeyPressMask);
        gc=XCreateGC(d, root, 0,0);        
	XSetBackground(d,gc,white);
	XSetForeground(d,gc,black);
	XClearWindow(d, root);
	XMapRaised(d, root);
};

void close_x() {
	XFreeGC(d, gc);
	XDestroyWindow(d,root);
	XCloseDisplay(d);	
	exit(1);				
};

void redraw() {
	XClearWindow(d, root);
};

