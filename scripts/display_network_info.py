# @Auth Xtrans Solutions Pvt. Ltd.
# Program to test 16x2 LCD and display network information
# Connect from CN3 to CN6
# Before Executing the program make sure that pin number 7 of raspberry pi is enabled as GPIO Pin
# open config file using command
# sudo nano /boot/config.txt
# Disable the following line by adding # in front of the line
# dtoverlay = w1-gpio

# import
import RPi.GPIO as GPIO
import time
import subprocess

# Define GPIO to LCD mapping
LCD_RS = 15  # 35
LCD_E  = 12  # 37
LCD_D4 = 23  # 33
LCD_D5 = 21  # 7
LCD_D6 = 19  # 31
LCD_D7 = 24  # 29

# Define some device constants
LCD_WIDTH = 16    # Maximum characters per line
LCD_CHR = True
LCD_CMD = False

LCD_LINE_1 = 0x80 # LCD RAM address for the 1st line
LCD_LINE_2 = 0xC0 # LCD RAM address for the 2nd line

# Timing constants
E_PULSE = 0.0005
E_DELAY = 0.0005

def get_eth0_inet():
    try:
        result = subprocess.run(['hostname', '-I'], capture_output=True, text=True)
        eth0_inet = result.stdout.strip().split()[0]
        return eth0_inet
    except Exception as e:
        print(f"LAN down: {e}")
        return "Error"

def check_wlan0():
    try:
        result = subprocess.run(['ip', 'link', 'show', 'wlan0'], capture_output=True, text=True)
        if "state UP" in result.stdout:
            return "wlan0 present"
        else:
            return "wlan0 down"
    except Exception as e:
        print(f"WLAN0 down: {e}")
        return "Error"

def main():
    # Main program block
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BOARD)       # Use BCM GPIO numbers
    GPIO.setup(LCD_E, GPIO.OUT)  # E
    GPIO.setup(LCD_RS, GPIO.OUT) # RS
    GPIO.setup(LCD_D4, GPIO.OUT) # DB4
    GPIO.setup(LCD_D5, GPIO.OUT) # DB5
    GPIO.setup(LCD_D6, GPIO.OUT) # DB6
    GPIO.setup(LCD_D7, GPIO.OUT) # DB7

    # Initialise display
    lcd_init()

    while(True):
     # Get eth0 inet and wlan0 status
     eth0_inet = get_eth0_inet()
     wlan0_status = check_wlan0()
    
     # Display on LCD
     lcd_string(f"eth0: {eth0_inet}", LCD_LINE_1)
     lcd_string(wlan0_status, LCD_LINE_2)
    
     # Display on screen
     #print(f"eth0: {eth0_inet}")
     #print(wlan0_status)
    
     #time.sleep(5) # 5 second delay
    
def lcd_init():
    # Initialise display
    lcd_byte(0x33, LCD_CMD)  # 110011 Initialise
    lcd_byte(0x32, LCD_CMD)  # 110010 Initialise
    lcd_byte(0x06, LCD_CMD)  # 000110 Cursor move direction
    lcd_byte(0x0C, LCD_CMD)  # 001100 Display On, Cursor Off, Blink Off
    lcd_byte(0x28, LCD_CMD)  # 101000 Data length, number of lines, font size
    lcd_byte(0x01, LCD_CMD)  # 000001 Clear display
    time.sleep(E_DELAY)

def lcd_byte(bits, mode):
    # Send byte to data pins
    # bits = data
    # mode = True  for character
    #        False for command

    GPIO.output(LCD_RS, mode)  # RS

    # High bits
    GPIO.output(LCD_D4, False)
    GPIO.output(LCD_D5, False)
    GPIO.output(LCD_D6, False)
    GPIO.output(LCD_D7, False)
    if bits & 0x10 == 0x10:
        GPIO.output(LCD_D4, True)
    if bits & 0x20 == 0x20:
        GPIO.output(LCD_D5, True)
    if bits & 0x40 == 0x40:
        GPIO.output(LCD_D6, True)
    if bits & 0x80 == 0x80:
        GPIO.output(LCD_D7, True)

    # Toggle 'Enable' pin
    lcd_toggle_enable()

    # Low bits
    GPIO.output(LCD_D4, False)
    GPIO.output(LCD_D5, False)
    GPIO.output(LCD_D6, False)
    GPIO.output(LCD_D7, False)
    if bits & 0x01 == 0x01:
        GPIO.output(LCD_D4, True)
    if bits & 0x02 == 0x02:
        GPIO.output(LCD_D5, True)
    if bits & 0x04 == 0x04:
        GPIO.output(LCD_D6, True)
    if bits & 0x08 == 0x08:
        GPIO.output(LCD_D7, True)

    # Toggle 'Enable' pin
    lcd_toggle_enable()

def lcd_toggle_enable():
    # Toggle enable
    time.sleep(E_DELAY)
    GPIO.output(LCD_E, True)
    time.sleep(E_PULSE)
    GPIO.output(LCD_E, False)
    time.sleep(E_DELAY)

def lcd_string(message, line):
    # Send string to display

    message = message.ljust(LCD_WIDTH, " ")

    lcd_byte(line, LCD_CMD)

    for i in range(LCD_WIDTH):
        lcd_byte(ord(message[i]), LCD_CHR)

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        pass
    finally:
        lcd_byte(0x01, LCD_CMD)
        lcd_string("Goodbye!", LCD_LINE_1)
        GPIO.cleanup()
