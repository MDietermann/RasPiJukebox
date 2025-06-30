from sense_hat import SenseHat, ACTION_RELEASED
import time

sense = SenseHat()

speed = 0.1
DOUBLE_CLICK_THRESHOLD = 0.3

last_press_time = {}
press_count = {}

rot = (255,0,0)
gruen = (0,255,0)
blau = (0,0,255)
bg_off = (0,0,0)
"""ran_color = random.randint(0,255)"""

"""def visualizer():
    fox x in range(8):
        height = random.randint(0, intensity)
        for y in range(8):
            if y < height:
                sense.set_pixel(x, 7 -y, ran_color)"""
    
def klick_right(event):
    if event.action != ACTION_RELEASED:
        next_Song()
        
def klick_left(event):
    if event.action != ACTION_RELEASED:
        last_Song()
        
def klick_up(event):
    if event.action != ACTION_RELEASED:
        volume_Up()
        
def klick_down(event):
    if event.action != ACTION_RELEASED:
        volume_Down()
        
def klick_middle(event):
    if event.action != ACTION_RELEASED:
        key = event.action
        now = time.time()
        
        if key in last_press_time and now - last_press_time[key] <= DOUBLE_CLICK_THRESHOLD:
            press_count[key] += 1
        else:
            press_count[key] = 1
            
        last_press_time[key] = now
        
        if press_count[key] == 2:
            print(f"{key} double clicked")
            press_count[key] = 0
        else:
            def reset_if_single():
                time.sleep(DOUBLE_CLICK_THRESHOLD)
                if press_count[key] == 1:
                    print(f"{key} single clicked")
                    press_count[key] == 0
            
            import threading
            threading.Thread(target=reset_if_single, daemon=True).start()

        # start_Stop()
      
def next_Song():
    #print("Das aktuelle Lied: ", song)
    sense.show_message("Aktueller Song:", text_colour = gruen, scroll_speed = speed)
    
def last_Song():
    sense.show_message("Aktueller Song:", text_colour = rot,back_colour=bg_off, scroll_speed = speed)
    
def volume_Up():
    sense.show_message("Volume:", text_colour= blau, back_colour=bg_off, scroll_speed = speed)
    
def volume_Down():
    sense.show_message("Volume:", text_colour= blau, back_colour=bg_off, scroll_speed = speed)

"""def start_Stop():
    sense.show_message
    ("Pause", text_c
     
     olour= rot, back_colour = bg_off, scroll_speed = speed
                       )"""
try:
    while True:
        """current = sp.current_playback()"""
        sense.stick.direction_right = klick_right
        sense.stick.direction_left = klick_left
        sense.stick.direction_up = klick_up
        sense.stick.direction_down = klick_down
        sense.stick.direction_middle = klick_middle

        #if current and current['is_playing']:
      
      
except KeyboardInterrupt:
    sense.clear()
    print("Beendet")
    
       