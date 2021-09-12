class timeTable:
    dic = {
        "Œ—j“ú":"Monday", 
        "‰Î—j“ú":"Tuesday",
        "…—j“ú":"Wednesday",
        "–Ø—j“ú":"Thursday",
        "‹à—j“ú":"Friday"
    }

    def getResponse(self, message):
        for _dic in self.dic:
            if _dic == message:
                return self.dic[message]
        return "•s–¾‚ÈƒŠƒeƒ‰ƒ‹‚Å‚·. "