# 날씨 얻어오는 함수들

from urllib.parse import urlencode, unquote
import datetime
import requests
import json

class Weather:
    # 초기화함수
    def __init__(self, api_key, nx, ny):
        self.api_key = api_key
        self.url = "http://apis.data.go.kr/1360000/VilageFcstInfoService_2.0/getUltraSrtNcst"
        self.now = datetime.datetime.now()
        self.r_item = ""
        self.nx = nx
        self.ny = ny

    # 쿼리 인자들을 만든다.
    def get_query_url(self):
        (date, time) = self.get_date()

        query_params = '?' + urlencode(
            {
                "ServiceKey" : unquote(self.api_key),
                "base_date" : date,
                "base_time" : time,
                "nx" : self.nx,
                "ny" : self.ny,
                "numOfRows" : "10",
                "pageNo" : "1",
                "dataType" : "JSON"
            }
        )

        return self.url + query_params
    
    # 유효할 날짜와 시간을 만든다.
    def get_date(self):
        # 현재시간 가져오기
        self.now = datetime.datetime.now()

        hour = self.now.hour
        minute = self.now.minute

        # 0030 을 보려면 0045에 요청해야함
        # 현재 0923이면 0930이 없으므로 0830을 요청해야함
        # 현재 0946이면 0930을 요청해야함
        # 현재 1000이면 0930을 요청해야함
        # 분이 00 ~ 44 이면 전단계꺼를 요청
        # 분이 45 ~ 59이면 현 단계꺼를 요청

        if(minute >= 00 and minute < 45):
            # 1시간 전 시간으로 설정하고 시간 가져오기
            self.now = datetime.datetime.now() - datetime.timedelta(hours=1)
            hour = str(self.now.hour)
            minute = str(30)
        else:
            hour = str(hour)
            minute = str(30)

        time = hour + minute
        date = self.now.strftime("%Y%m%d")

        return (date, time)

    # 요청을 보내서 JSON 형식의 정보를 가져오는 함수
    def call_request(self):
        response = requests.get(self.get_query_url())
        r_dict = json.loads(response.text)
        r_response = r_dict.get("response")
        r_header = r_response.get("header")
        r_result_code = r_header.get("resultCode")
        r_result_message = r_header.get("resultMsg")
        r_body = r_response.get("body")
        r_items = r_body.get("items")
        self.r_item = r_items.get("item")

        # 00 으로 정상적으로 받아오지 못하면 프로그램을 종료시킴
        assert r_result_code == "00", r_result_message

    
    # 가져온 정보에서 온도부분을 때어 반환하는 함수 
    def get_temp(self):
        for item in self.r_item:
            if(item.get("category") == "T1H"):
                return item.get("obsrValue")
        return "ERR"
    
    # 가져온 정보에서 강수량 부분만 때어 반환하는 함수 
    def get_rain(self):
        for item in self.r_item:
            if(item.get("category") == "RN1"):
                return item.get("obsrValue")
        return "ERR"

    # 가져온 정보에서 습도 부분만 때어 반환하는 함수 
    def get_humidity(self):
        for item in self.r_item:
            if(item.get("category") == "REH"):
                return item.get("obsrValue")
        return "ERR"

    # 가져온 정보에서 강수 형태 부분만 때어 반환하는 함수
    # 눈이나 비를 구분할 수 있다.
    def get_type_of_rain(self):
        for item in self.r_item:
            if(item.get("category") == "PTY"):
                return item.get("obsrValue")
        return "ERR"
