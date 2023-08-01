from weather import Weather
import RPi_I2C_driver
import time
import RPi.GPIO as GPIO
from datetime import datetime

def run():
    # api 키 설정
    api_key = "여기에 본인의 api키 입력"
    # 지역 좌표설정
    # 기상청 api 페이지에서 참고자료를 받으면 엑셀파일 내에 각 지역의 좌표가 있음 
    nx = "여기에 본인지역의 nx 입력"
    ny = "여기에 본인지역의 ny 입력"

    # 초기화
    lcd = RPi_I2C_driver.lcd(0x3F)
    lcd.home()
    lcd.print("Initializing...")
    time.sleep(1)
    
    # Weather 객체 생성 
    weather = Weather(api_key, nx, ny)

    # GPIO 설정 시작 
    lcd.clear()
    lcd.print("GPIO Setup...")

    # BCM 모드로 핀맵
    GPIO.setmode(GPIO.BCM)
    
    # 파란 led GPIO14에 맵핑 
    led_rain = 14
    # 하얀 led GPIO 15에 맵핑 
    led_snow = 15
    
    lcd.clear()
    lcd.print("led test..")

    GPIO.setup(led_rain, GPIO.OUT)
    GPIO.setup(led_snow, GPIO.OUT)
    
    GPIO.output(led_rain, GPIO.HIGH)
    GPIO.output(led_snow, GPIO.HIGH)
    
    time.sleep(1)
    
    GPIO.output(led_rain, GPIO.LOW)
    GPIO.output(led_snow, GPIO.LOW)
    
    # rgb led 핀 맵핑 
    rgb_r = 21
    rgb_g = 20
    rgb_b = 16
    
    GPIO.setup(rgb_r, GPIO.OUT)
    GPIO.setup(rgb_g, GPIO.OUT)
    GPIO.setup(rgb_b, GPIO.OUT)
    
    lcd.clear()
    lcd.print("rgb led test..")

    GPIO.output(rgb_r, GPIO.HIGH)
    time.sleep(1)
    
    GPIO.output(rgb_g, GPIO.HIGH)
    time.sleep(1)
    
    GPIO.output(rgb_b, GPIO.HIGH)
    time.sleep(1)
    
    GPIO.output(rgb_b, GPIO.LOW)
    time.sleep(1)
    GPIO.output(rgb_g, GPIO.LOW)
    time.sleep(1)
    GPIO.output(rgb_r, GPIO.LOW)
    time.sleep(1)
    
    lcd.clear()
    lcd.print("Complete!")
    time.sleep(1)
    lcd.clear()

    # call_request하기
    # 정보 가져와 lcd와 led에 출력하기

    while True:
        # 요청을 보내 JSON 정보를 가져오기 
        lcd.print("call_request...")
        weather.call_request()
        lcd.clear()
        lcd.print("complete!")
        
        # 가져온 정보에서 필요한 부분만 가져오기 
        temp = weather.get_temp()
        rain = weather.get_rain()
        humidity = weather.get_humidity()
        type_of_rain = weather.get_type_of_rain()
        
    
        # 첫 번째 줄과 두 번째 줄을 만들기 
        today = datetime.now()
        first_line = today.strftime("   %Y-%m-%d")
        second_line = " " + temp + "C " + humidity + "% " + rain + "mm "
        
        # 디버깅을 위해 터미널에 출력 
        print(first_line)
        print(second_line)
    
        # lcd에 정보를 출력한다. 
        lcd.clear()
        lcd.print(first_line)
        lcd.setCursor(0, 1)
        lcd.print(second_line)
        
        # 표시전에 LED 초기화 
        GPIO.output(led_rain, GPIO.LOW)
        GPIO.output(led_snow, GPIO.LOW)
        GPIO.output(rgb_r, GPIO.LOW)
        GPIO.output(rgb_b, GPIO.LOW)
        GPIO.output(rgb_g, GPIO.LOW)
    
        # 비오면 파란 led 켜기
        if(type_of_rain == 1 or type_of_rain == 2 or type_of_rain == 5 or type_of_rain == 6):
            GPIO.output(led_rain, GPIO.HIGH)
        
        # 눈오면 하얀 led 켜기
        if(type_of_rain == 2 or type_of_rain == 6 or type_of_rain == 7):
            GPIO.output(led_snow, GPIO.HIGH)
    
        # 3색 LED 설정
        # 30도 이상이면 빨간색, 25도 이상이면 노란색, 10도 이상이면 초록색, 그 이하면 파란색
        if float(temp) > 29:
            GPIO.output(rgb_r, GPIO.HIGH)
        elif float(temp) > 24:
            GPIO.output(rgb_r, GPIO.HIGH)
            GPIO.output(rgb_g, GPIO.HIGH)
        elif float(temp) > 10:
            GPIO.output(rgb_g, GPIO.HIGH)
        else:
            GPIO.output(rgb_b, GPIO.HIGH)
        
        # 1시간 대기하기 
        time.sleep(3600)
            
        # 00시면 백라이트끄고 8시면 백라이트 켜기
        if(today.hour == 0):
            lcd.backlight(False)
        elif(today.hour == 8):
            lcd.backlight(True)
    
        
  
# main 함수 
if __name__=="__main__":
    # 오류가 발생하면 처음부터 다시 시작을 무한반복
    # 프로그램을 종료하기 위해서는 Ctrl + D 를 입력해야함 
    while True:
        try:
            run()
        finally:
            print("Error 발생, 재시작")
            run()
