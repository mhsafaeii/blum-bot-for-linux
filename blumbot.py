import pyautogui
import time
import random
from pynput.mouse import Button, Controller
import subprocess
from pynput import keyboard as kb
from Xlib import X, display

mouse = Controller()
time.sleep(0.5)
paused = False

def on_press(key):
    global paused
    try:
        if key.char == 'k':
            paused = not paused
            if paused:
                print("Bot paused... Press 'K' again to continue")
            else:
                print("Bot continue working...")
    except AttributeError:
        pass

listener = kb.Listener(on_press=on_press)
listener.start()

while True:
    if paused:
        continue
    try:
        language_choice = int(input("Select language (1 - English, 2 - Bahasa Indonesia): "))
        if language_choice in [1, 2]:
            break
        else:
            print("Invalid choice. Please enter 1 or 2.")
    except ValueError:
        print("Invalid input. Please enter a number.")

if language_choice == 1:
    window_input = "Enter Window (1 - TelegramDesktop): "
    window_not_found = "Window - {} not found!"
    window_found = "Window found - {}\nNow bot working... Press 'K' on the keyboard to pause."
elif language_choice == 2:
    window_input = "Masukin Window nya (1 - TelegramDesktop): "
    window_not_found = "Window - {} gak di temukan!"
    window_found = "Window ditemukan - {}\nSekarang bot berjalan... Pencet 'K' di keyboard buat jeda."

def click(x, y):
    mouse.position = (x, y + random.randint(1, 3))
    mouse.press(Button.left)
    mouse.release(Button.left)

def get_window_id(window_name):
    try:
        window_id = subprocess.check_output(['wmctrl', '-l']).decode('utf-8')
        for line in window_id.splitlines():
            if window_name in line:
                return line.split()[0]
    except Exception as e:
        print(f"Error: {e}")
    return None

def activate_window(window_id):
    try:
        subprocess.call(['wmctrl', '-ia', window_id])
    except Exception as e:
        print(f"Error: {e}")

def get_window_rect(window_id):
    try:
        xlib_display = display.Display()
        window = xlib_display.create_resource_object('window', int(window_id, 16))
        window_info = window.get_geometry()
        return (window_info.x, window_info.y, window_info.width, window_info.height)
    except Exception as e:
        print(f"Error: {e}")
        return (0, 0, 0, 0)

window_name = input(window_input)

if window_name == '1':
    window_name = "TelegramDesktop"

if window_name == '2':
    window_name = "KotatogramDesktop"

window_id = get_window_id(window_name)

if not window_id:
    print(window_not_found.format(window_name))
    print("Make sure you use the TelegramDesktop application (not Telegram Web).")
else:
    print(window_found.format(window_name))
    paused = False

    while True:
        if paused:
            continue

        activate_window(window_id)

        window_rect = get_window_rect(window_id)
        scrn = pyautogui.screenshot(region=window_rect)

        width, height = scrn.size
        pixel_found = False

        for x in range(0, width, 20):
            for y in range(0, height, 20):
                r, g, b = scrn.getpixel((x, y))
                if (b in range(0, 125)) and (r in range(102, 220)) and (g in range(200, 255)):
                    screen_x = window_rect[0] + x
                    screen_y = window_rect[1] + y
                    click(screen_x + 4, screen_y)
                    time.sleep(0.001)
                    pixel_found = True
                    break
            if pixel_found:
                break
