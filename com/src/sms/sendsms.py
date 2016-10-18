# -*- coding: utf8 -*-

"""
 vi:set et ts=4 fenc=utf8:
 Copyright (C) 2008-2010 D&SOFT
 http://open.coolsms.co.kr
"""

import sys
import coolsms

class sms(object):
    def sms(self, id, pw, sender, receiver, msg):

        cs = coolsms.sms()

        cs.appversion("TEST/1.0")

        # 한글인코딩 방식을 설정합니다.  (생략시 euckr로 설정)
        # 지원 인코딩: euckr, utf8
        cs.charset("utf8")

        cs.setuser(id, pw)

        cs.addsms(receiver, sender, msg)

        nsent = 0
        if cs.connect():
            # add 된 모든 메세지를 서버로 보냅니다.
            nsent = cs.send()
        else:
            print "서버에 접속할 수 없습니다. 네트워크 상태를 확인하세요."

        # 연결 해제
        cs.disconnect()
        cs.emptyall()


if __name__ == "__main__":
    main()
    sys.exit(0)
