class timeTable:
    dic = {
        "月曜日":"Monday", 
        "火曜日":"Tuesday",
        "水曜日":"Wednesday",
        "木曜日":"Thursday",
        "金曜日":"Friday"
    }

    def getResponse(self, message):
        for _dic in self.dic:
            if _dic == message:
                return self.dic[message]
        return "不明なリテラルです. "