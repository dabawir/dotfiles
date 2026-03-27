#include <X11/Xlib.h>
#include <X11/Xutil.h>
#include <X11/Xft/Xft.h>
#include <X11/Xatom.h>
#include <X11/keysym.h>
#include <iostream>
#include <vector>
#include <string>
#include <unistd.h>
#include <algorithm>
#include <signal.h>
#include <sys/wait.h>

using namespace std;

#define BORDER_NORMAL 0x444444
#define BORDER_FOCUS  0xbbbbbb 
#define BORDER_WIDTH  2
#define BAR_HEIGHT    25

Display *display;
vector<Window> ws_clients[2]; 
int current_ws = 0;

#define clients ws_clients[current_ws]

string input_buffer = "";
bool menu_active = false;
Window menu_win = None;
XftFont *xft_font;
XftColor xft_col;

float master_ratio = 0.5f; 
int focus_idx = 0;

int x_error_handler(Display *d, XErrorEvent *e) { (void)d; (void)e; return 0; }
void cleanup_zombies(int sig) { (void)sig; while (waitpid(-1, NULL, WNOHANG) > 0); }

void kill_client(Window w) {
    Atom *protocols; int n; bool supports_delete = false;
    Atom wm_delete = XInternAtom(display, "WM_DELETE_WINDOW", False);
    if (XGetWMProtocols(display, w, &protocols, &n)) {
        while (!supports_delete && n--) supports_delete = protocols[n] == wm_delete;
        XFree(protocols);
    }
    if (supports_delete) {
        XEvent ev; ev.type = ClientMessage; ev.xclient.window = w;
        ev.xclient.message_type = XInternAtom(display, "WM_PROTOCOLS", False);
        ev.xclient.format = 32; ev.xclient.data.l[0] = wm_delete;
        ev.xclient.data.l[1] = CurrentTime;
        XSendEvent(display, w, False, NoEventMask, &ev);
    } else { XKillClient(display, w); }
}

void tile() {
    if (clients.empty()) return;
    int sw = 800, sh = 600; 
    int actual_sh = sh - (menu_active ? BAR_HEIGHT : 0);
    int n = (int)clients.size();

    if (n == 1) {
        XMoveResizeWindow(display, clients[0], 0, 0, sw - 2*BORDER_WIDTH, actual_sh - 2*BORDER_WIDTH);
    } else {
        int mw = (int)(sw * master_ratio);
        XMoveResizeWindow(display, clients[0], 0, 0, mw - BORDER_WIDTH, actual_sh - 2*BORDER_WIDTH);
        int sh_stack = actual_sh / (n - 1);
        for (int i = 1; i < n; i++) {
            XMoveResizeWindow(display, clients[i], mw, (i-1) * sh_stack, sw - mw - BORDER_WIDTH, sh_stack - 2*BORDER_WIDTH);
        }
    }
}

void update_focus() {
    if (clients.empty()) {
        XSetInputFocus(display, DefaultRootWindow(display), RevertToParent, CurrentTime);
        return;
    }
    for (size_t i = 0; i < clients.size(); i++) {
        XSetWindowBorder(display, clients[i], (i == (size_t)focus_idx) ? BORDER_FOCUS : BORDER_NORMAL);
    }
    XSetInputFocus(display, clients[focus_idx], RevertToParent, CurrentTime);
    XRaiseWindow(display, clients[focus_idx]);
}

void view_workspace(int ws) {
    if (ws == current_ws) return;
    for (auto w : ws_clients[current_ws]) XUnmapWindow(display, w);
    current_ws = ws;
    focus_idx = 0;
    for (auto w : ws_clients[current_ws]) XMapWindow(display, w);
    tile();
    update_focus();
}

// FUNGSI BARU: Lempar jendela ke workspace sebelah
void send_to_workspace(int target_ws) {
    if (target_ws == current_ws || clients.empty()) return;
    Window w = clients[focus_idx];
    clients.erase(clients.begin() + focus_idx);
    ws_clients[target_ws].push_back(w);
    XUnmapWindow(display, w); // Sembunyiin dari ws sekarang
    if (focus_idx >= (int)clients.size()) focus_idx = max(0, (int)clients.size()-1);
    tile();
    update_focus();
}

void draw_menu() {
    if (!menu_active || menu_win == None) return;
    XClearWindow(display, menu_win);
    XftDraw *draw = XftDrawCreate(display, menu_win, DefaultVisual(display, 0), DefaultColormap(display, 0));
    string text = "WS " + to_string(current_ws + 1) + " | " + input_buffer + "|"; 
    XftDrawStringUtf8(draw, &xft_col, xft_font, 10, 17, (const FcChar8*)text.c_str(), (int)text.length());
    XftDrawDestroy(draw);
}

void spawn_app(const char* app) {
    if (fork() == 0) {
        if (display) close(ConnectionNumber(display));
        setsid(); 
        execlp(app, app, NULL);
        exit(0);
    }
}

int main() {
    display = XOpenDisplay(NULL);
    if (!display) return 1;
    Window root = DefaultRootWindow(display);
    XEvent ev;

    XSetErrorHandler(x_error_handler);
    signal(SIGCHLD, cleanup_zombies);

    xft_font = XftFontOpenName(display, 0, "monospace:size=10");
    XftColorAllocName(display, DefaultVisual(display, 0), DefaultColormap(display, 0), "#ffffff", &xft_col);

    XSelectInput(display, root, SubstructureRedirectMask | SubstructureNotifyMask | KeyPressMask);
    
    unsigned int mod = Mod1Mask; 
    unsigned int shift = ShiftMask;

    XGrabKey(display, XKeysymToKeycode(display, XK_Return), mod | shift, root, True, GrabModeAsync, GrabModeAsync);
    XGrabKey(display, XKeysymToKeycode(display, XK_c), mod | shift, root, True, GrabModeAsync, GrabModeAsync);
    XGrabKey(display, XKeysymToKeycode(display, XK_q), mod | shift, root, True, GrabModeAsync, GrabModeAsync);
    XGrabKey(display, XKeysymToKeycode(display, XK_p), mod, root, True, GrabModeAsync, GrabModeAsync);
    
    // Grab key buat Workspace (View & Move)
    XGrabKey(display, XKeysymToKeycode(display, XK_1), mod, root, True, GrabModeAsync, GrabModeAsync);
    XGrabKey(display, XKeysymToKeycode(display, XK_2), mod, root, True, GrabModeAsync, GrabModeAsync);
    XGrabKey(display, XKeysymToKeycode(display, XK_1), mod | shift, root, True, GrabModeAsync, GrabModeAsync);
    XGrabKey(display, XKeysymToKeycode(display, XK_2), mod | shift, root, True, GrabModeAsync, GrabModeAsync);

    KeySym keys[] = { XK_h, XK_j, XK_k, XK_l, XK_Left, XK_Down, XK_Up, XK_Right };
    for(auto k : keys) {
        XGrabKey(display, XKeysymToKeycode(display, k), mod, root, True, GrabModeAsync, GrabModeAsync);
        if(k == XK_h || k == XK_l) XGrabKey(display, XKeysymToKeycode(display, k), mod | shift, root, True, GrabModeAsync, GrabModeAsync);
    }

    while (true) {
        XNextEvent(display, &ev);

        if (ev.type == MapRequest) {
            Window w = ev.xmaprequest.window;
            clients.push_back(w);
            XMapWindow(display, w);
            XSetWindowBorderWidth(display, w, BORDER_WIDTH);
            focus_idx = (int)clients.size() - 1;
            tile();
            update_focus();
        }

        if (ev.type == KeyPress) {
            KeySym ks = XLookupKeysym(&ev.xkey, 0);

            if (menu_active) {
                if (ks == XK_Return) {
                    if (!input_buffer.empty()) spawn_app(input_buffer.c_str());
                    goto exit_menu;
                } else if (ks == XK_Escape) {
                    goto exit_menu;
                } else if (ks == XK_BackSpace) {
                    if (!input_buffer.empty()) input_buffer.pop_back();
                    draw_menu();
                } else {
                    char buf[32]; int len = XLookupString(&ev.xkey, buf, sizeof(buf), NULL, NULL);
                    if (len > 0) { input_buffer += string(buf, len); draw_menu(); }
                }
                continue;
                exit_menu:
                menu_active = false; input_buffer = ""; XUngrabKeyboard(display, CurrentTime);
                XDestroyWindow(display, menu_win); menu_win = None; tile(); update_focus();
                continue;
            }

            // Workspace Logic: Alt+1/2 (View) vs Alt+Shift+1/2 (Move)
            if (ks == XK_1) {
                if (ev.xkey.state & shift) send_to_workspace(0);
                else view_workspace(0);
            }
            if (ks == XK_2) {
                if (ev.xkey.state & shift) send_to_workspace(1);
                else view_workspace(1);
            }

            if ((ks == XK_j || ks == XK_l || ks == XK_Down || ks == XK_Right) && (ev.xkey.state & mod)) {
                if (!clients.empty()) { focus_idx = (focus_idx + 1) % (int)clients.size(); update_focus(); }
            }
            if ((ks == XK_k || ks == XK_h || ks == XK_Up || ks == XK_Left) && (ev.xkey.state & mod)) {
                if (!clients.empty()) { focus_idx = (focus_idx - 1 + (int)clients.size()) % (int)clients.size(); update_focus(); }
            }

            if (ks == XK_h && (ev.xkey.state & (mod | shift))) { master_ratio -= 0.05f; if(master_ratio < 0.1f) master_ratio = 0.1f; tile(); }
            if (ks == XK_l && (ev.xkey.state & (mod | shift))) { master_ratio += 0.05f; if(master_ratio > 0.9f) master_ratio = 0.9f; tile(); }

            if (ks == XK_Return && (ev.xkey.state & (mod | shift))) spawn_app("alacritty");
            if (ks == XK_p && (ev.xkey.state & mod)) {
                menu_active = true;
                menu_win = XCreateSimpleWindow(display, root, 0, 600 - BAR_HEIGHT, 800, BAR_HEIGHT, 0, BORDER_NORMAL, 0x111111);
                XSetWindowAttributes attrs; attrs.override_redirect = True;
                XChangeWindowAttributes(display, menu_win, CWOverrideRedirect, &attrs);
                XMapWindow(display, menu_win);
                XGrabKeyboard(display, menu_win, True, GrabModeAsync, GrabModeAsync, CurrentTime);
                tile(); draw_menu();
            }

            if (ks == XK_c && (ev.xkey.state & (mod | shift))) {
                Window focused; int r; XGetInputFocus(display, &focused, &r);
                if (focused != root && focused != None && focused != menu_win) {
                    auto it = find(clients.begin(), clients.end(), focused);
                    if (it != clients.end()) { 
                        clients.erase(it); kill_client(focused); XSync(display, False); 
                        if (focus_idx >= (int)clients.size()) focus_idx = max(0, (int)clients.size()-1); 
                        tile(); update_focus(); 
                    }
                }
            }

            if (ks == XK_q && (ev.xkey.state & (mod | shift))) break;
        }

        if (ev.type == DestroyNotify) {
            Window w = ev.xdestroywindow.window;
            if (w == menu_win) continue;
            for(int i=0; i<2; i++) {
                auto it = find(ws_clients[i].begin(), ws_clients[i].end(), w);
                if (it != ws_clients[i].end()) { 
                    ws_clients[i].erase(it); 
                    if (i == current_ws) {
                        if (focus_idx >= (int)clients.size()) focus_idx = max(0, (int)clients.size()-1); 
                        tile(); update_focus(); 
                    }
                }
            }
        }
        
        if (ev.type == UnmapNotify) {
            tile(); update_focus();
        }
    }
    XCloseDisplay(display); return 0;
}
