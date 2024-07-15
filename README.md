# PowerSync
## KR
APC 사의BE400 같은 서버/컴퓨터와 통신기능이 없는 저가형 UPS를위한 파이선 스크립트
https://github.com/gunu3371/m1s_ups_control 이 레포지토리의 기능을 활용합니다
+ ### 기능
  + 브로드캐스팅된 데이터및 핑를 이용하여 전원상태 판단
  + 전원상태를 로그에 저장
+ ### 설치방법
  + 1.```git clone https://github.com/gunu3371/PowerSync.git``` 실행
  + 2.```sh install_service.sh``` 실행
+ ### 사용방법
  + ```systemctl status powersync``` 로 상태확인
  + ```/etc/powersync/log/``` 에서 로그확인
## EN
Python script for low-cost UPS without communication function with server/computer, such as APC BE400
https://github.com/gunu3371/m1s_ups_control Take advantage of the features of this repository
+ ### Features
  + Determine power status using broadcasted data and ping
  + Save power status in log
+ ### Installation method
  + 1. Run ```git clone https://github.com/gunu3371/PowerSync.git```
  + 2. Run ```sh install_service.sh```
+ ### How to use
  + Check status with ```systemctl status powersync```
  + Check log in ```/etc/powersync/log/```
