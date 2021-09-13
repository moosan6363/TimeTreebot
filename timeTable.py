class timeTable:
    dic = {
        "a":"Monday", 
        "b":"Tuesday",
        "c":"Wednesday",
        "d":"Thursday",
        "e":"Friday"
    }

    def getResponse(self, message):
        for _dic in self.dic:
            if _dic == message:
                return self.dic[message]
        return "unknown literal "