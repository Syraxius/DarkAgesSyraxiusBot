import win32api
import win32con
import win32gui


def mouse_click(hwnd, coords, button='left'):
    mk_code = {
        'left': win32con.MK_LBUTTON,
        'right': win32con.MK_LBUTTON,
    }.get(button)
    click_coords = win32api.MAKELONG(*coords)
    win32api.PostMessage(hwnd, win32con.WM_MOUSEMOVE, None, click_coords)
    if mk_code:
        win32api.PostMessage(hwnd, win32con.WM_LBUTTONDOWN, win32con.MK_LBUTTON, click_coords)
        win32api.PostMessage(hwnd, win32con.WM_LBUTTONUP, None, click_coords)


def keyboard_send_vk_as_scan_code(hwnd, vk, extended=0):
    scan_code = win32api.MapVirtualKey(vk, 0)
    lparam = extended << 24 | scan_code << 16
    win32gui.SendMessage(hwnd, win32con.WM_KEYDOWN, vk, lparam)
    win32gui.SendMessage(hwnd, win32con.WM_KEYUP, vk, lparam)
