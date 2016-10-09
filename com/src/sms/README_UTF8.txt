
  개요

CTM은 별도의 서버없이 SKT, KTF, LGT 3개 이동통신사의 가입자 핸드폰으로 문자메시
지(SMS)를 전송하는 기능을 포함하는 모듈입니다. GSLB시스템을 기반으로 365일 무정
지(failover) 서비스를 구현하여 안정성을 보장합니다.


  소스코드 라이센스

기본적으로 BSD 라이센스에 따라 소스코드를 수정 및 배포가능하며 자세한 사항은 COP
YRIGHT.txt 파일을 참고바랍니다.


  계정만들기

문자전송을 위해 쿨에스엠에스(http://www.coolsms.co.kr)에서 회원가입을 통하여 서
비스 계정을 만듭니다.


  파일구성

사용하시는 한글인코딩에 따라 EUC-KR 혹은 UTF-8 으로 작성된 예제를 선택하세요.
--------------------------------------------------------------------------------
 파일명                     | 내용
----------------------------+---------------------------------------------------
 coolsms.py                 | (공통)문자메시지 전송 모듈
 example_euckr_sendsms.py   | (EUC-KR)문자메시지 전송 예제
 example_euckr_sendlms.py   | (EUC-KR)장문(1,000자) LMS 전송 예제
 example_euckr_remain.py    | (EUC-KR)캐쉬, 포인트, 문자방울 잔량 확인 예제
 example_euckr_localkey.py  | (EUC-KR)클라이언트측 메시지ID 생성 예제
 example_euckr_rcheck.py    | (EUC-KR)핸드폰 수신결과 확인 예제
 example_utf8_sendsms.py    | (UTF-8)문자메시지 전송 예제
 example_utf8_sendlms.py    | (UTF-8)장문(1,000자) LMS 전송 예제
 example_utf8_remain.py     | (UTF-8)캐쉬, 포인트, 문자방울 잔량 확인 예제
 example_utf8_localkey.py   | (UTF-8)클라이언트측 메시지ID 생성 예제
 example_utf8_rcheck.py     | (UTF-8)핸드폰 수신결과 확인 예제
--------------------------------------------------------------------------------


  Quick Start

문자 1건을 보내는 간단한 예제를 만드는 방법을 설명합니다.

1. coolsms.py 파일과 example_euckr_sendsms.py(혹은 example_utf8_sendsms.py)파
   일을 작업 디렉토리로 복사해옵니다.

2. example_euckr_sendsms.py 파일을 열어서 20번째 줄에 cs_id와 cs_passwd를 쿨에스
   엠에스 사이트에서 가입할 때 입력한 아이디와 비밀번호를 그대로 입력합니다.

     cs.setuser("example", "example-password");

3. 28번째 줄에 addsms 메소드 호출에서 받는번호(반드시 SMS를 받을 수 있는 핸드폰
   번호로 입력), 회신번호, 문자내용을 입력해 줍니다.

     cs.addsms("01012123434", "01012123434", "테스트 문자")

4. python으로 실행하여 핸드폰으로 "테스트 문자"라는 문자가 수신됨을 확인하세요. 

     python example_euckr_sendsms.py

5. 문자가 수신되지 않을 경우 전송결과(http://www.coolsms.co.kr/?mid=mysmsReport&
   act=dispTextingserviceResult)에서 전송상태를 확인하세요.
