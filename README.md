# RPi_Weather_Project
라즈베리파이로 LCD와 LED를 이용해 현재 날씨 표시기를 만드는 레포입니다.
```
blue led   = GPIO14 ( 8번 자리 핀)
white led  = GPIO15 (10번 자리 핀)

rgb_r = GPIO21 (40번 자리 핀)
rgb_g = GPIO20 (38번 자리 핀)
rgb_b = GPIO16 (36번 자리 핀)

I2C_GND = GND   (9번 자리 핀)
I2C_VCC = 3.3V  (1번 자리 핀)
I2C_SDA = GPIO2 (3번 자리 핀)
I2C_SCK = GPIO3 (5번 자리 핀)
```
# weather_rpi.py
api_key와 nx, ny를 직접 설정해주어야합니다.

해당 정보는 기상청 openapi에서 확인할 수 있습니다.

또한 i2c_lcd의 주소값이 0x3F가 아니라면 수정이 필요합니다.

주소값은 아래 명령어를 통해 확인할 수 있습니다. 
만약 아무것도 표시되지 않는다면 i2c_lcd 연결에 문제가 있는 것입니다.

```bash
i2cdetect -y 1
```

# weather.py
기상청에서 JSON 형식의 정보를 가져와 필요한 정보만을 가져올 수 있는 클래스입니다.
생성자에 api_key, nx, ny가 들어갑니다.

# 실행하기
라즈베리파이에서 해당 명령어를 통해 레포지토리를 복제합니다.
```bash
cd ~
git clone https://github.com/binn328/RPi_Weather_Project/
```

다음 명령어를 통해 복제한 레포지토리에 들어갑니다.
```bash
cd ./RPi_Weather_Project
```

다음 명령어를 통해 동작을 시작합니다.
```bash
python3 weather_rpi.py
```

tmux를 사용하면 터미널을 닫아도 동작합니다.
```bash
tmux
python3 weather_rpi.py
```

이후 해당 명령어를 통해 tmux 터미널에 접근할 수 있습니다.
```bash
tmux attach -t 0
```

