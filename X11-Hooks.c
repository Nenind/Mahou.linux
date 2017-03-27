/* include the X library headers */
#include <X11/Xlib.h>
#include <X11/Xutil.h>
#include <X11/Xos.h>
/* include some silly stuff */
#include <stdio.h>
#include <stdlib.h>
// Threading
#include <pthread.h>
/* !!: my stuff */
#include <X11/extensions/XTest.h>
#include <wchar.h>
#include <locale.h>
// Multi
#include <stdbool.h>
#include <unistd.h> 
// For device read
#include <linux/input.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <fcntl.h>

// X11 variables
Display* d;
Window root;
// Device read variables
char* dev;
bool works = false;

// For reading mouse events.
void *read_dev(void *data) {
	int fd = open(dev, O_RDONLY);
    struct input_event ev;
	
    while (1)
    {
        read(fd, &ev, sizeof(struct input_event));
        if(ev.type == 1)
            //printf("key %i state %i\n", ev.code, ev.value);
            if(ev.value == 0)
                printf(" : [key %i]\n ", ev.code);
    }
}


int main(int argc, char **argv) {
	setlocale(LC_ALL,"");
    if(argc < 2) {
        printf("usage: %s /dev/input/<your-mouse-device> \n", argv[0]);
        return 1;
    }
	dev = argv[1];
	int data = 0;
	pthread_t read_dev_thread;
	/* create a second thread which executes read_dev(&data) */
	if(pthread_create(&read_dev_thread, NULL, read_dev, &data)) {

		fprintf(stderr, "Error creating thread\n");
		return 1;

	}
	works = true;
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
	
	/* look for events forever... */
	while(1) {
		// WIN-ALTERNATIVE: CallNextHook(-Ex).
		XNextEvent(d, &event);
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
		}
		// TODO: Find or Create ToUnicodeEx function alternative in X11/Linux.
		
		// KeySym k = XStringToKeysym("Я");
		// printf("KSD: %lu, K: %lu\n", key_sym, k);
				   // WIN-ALTERNATIVE: ToUnicode(-Ex)? -> Not really... looks more like VkKeyScan(Ex).
		kc_bytes = XLookupString(&event.xkey,key_char,255,&key_sym,0);
		key_char[kc_bytes] = '\0';
				   // WIN-ALTERNATIVE: GetKeyNameText(-W)?
		key_name = XKeysymToString(key_sym);
		if (event.type == KeyPress) {
			printf("Key: [%s] with code: [%u] pressed", key_name, event.xkey.keycode);
			if (kc_bytes > 0) {
				printf (", char: [%s]", key_char);
			}
			printf(".\n");
			if (strcmp(key_name, "F4") == 0) {
				printf("Passed exit command.\n");
				exit(1);		
			}
			if (strcmp(key_name, "F7") == 0) {
				// WIN-ALTERNATIVE: keybd_event or SendInput
				XTestFakeKeyEvent(d, 10, True, 0);
				XTestFakeKeyEvent(d, 10, False, 0);
			}
		}
	}
}

