class timeTable:
    dic = {
        "���j��":"Monday", 
        "�Ηj��":"Tuesday",
        "���j��":"Wednesday",
        "�ؗj��":"Thursday",
        "���j��":"Friday"
    }

    def getResponse(self, message):
        for _dic in self.dic:
            if _dic == message:
                return self.dic[message]
        return "�s���ȃ��e�����ł�. "