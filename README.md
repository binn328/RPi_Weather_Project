# RPi_Weather_Project
라즈베리파이로 LCD와 LED를 이용해 현재 날씨 표시기를 만드는 레포입니다.

# weather_rpi.py
api_key와 nx, ny를 직접 설정해주어야합니다.

해당 정보는 기상청 openapi에서 확인할 수 있습니다.

# weather.py
기상청에서 JSON 형식의 정보를 가져와 필요한 정보만을 가져올 수 있는 클래스입니다.
생성자에 api_key, nx, ny가 들어갑니다.
