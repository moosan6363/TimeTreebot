import os
import requests
import datetime
import pytz

class TimeTreeAPI():

    Token = os.environ["YOUR_TIME_TREE_TOKEN"]
    headers = {
        "Accept": "application/vnd.timetree.v1+json",
        "Authorization": f"Bearer {Token}",
        "Content-Type": "application/json"
    }
    params = {
        "timezone" : "Asia/Tokyo",
        "days" : "5"
    }

    def __init__(self, order) :
        response = requests.get("https://timetreeapis.com/calendars", headers = self.headers)
        if response.status_code == 200 :
            data = response.json()
            calendarID = data["data"][order]["id"]
            self.timetreeURL = "https://timetreeapis.com/calendars" + "/" + calendarID
            self.memberDic = self.registMember()
    
    def registMember(self) :
        response = requests.get(self.timetreeURL + "/members", headers = self.headers)
        memberDic = {}
        if response.status_code == 200 :
            data = response.json()
            for member in data["data"] :
                memberDic[member["id"]] = member["attributes"]["name"]
            return memberDic
        else : return response.text

    def isotoDate(self, iso) :
        dt = datetime.datetime.strptime(iso, '%Y-%m-%dT%H:%M:%S.%fZ')
        dt = pytz.utc.localize(dt).astimezone(pytz.timezone(os.environ["TZ"]))
        return dt

    def getSchedule(self) :

        response = requests.get(self.timetreeURL + "/upcoming_events", headers = self.headers, params = self.params)
        if response.status_code == 200 :
            data = response.json()
            try :
                task = data["data"]
                returnStr = f"{self.params['days']}日以内の予定は{len(task)}件です。\n"
                returnStr += "----------------予定一覧----------------"
                for schedule in task :
                    start = self.isotoDate(schedule["attributes"]["start_at"])
                    end = self.isotoDate(schedule["attributes"]["end_at"])
                    returnStr += "\n\n"
                    returnStr += "予定: " + schedule["attributes"]["title"] + "\n"
                    returnStr += "作成者: " + self.memberDic[schedule["relationships"]["creator"]["data"]["id"]] + "\n"
                    if schedule["attributes"]["all_day"] :
                        returnStr += "時間: " + f"{start.year:04}/{start.month:02}/{start.day:02} " + "終日"
                    else :
                        returnStr += "時間: " + f"{start.year:04}/{start.month:02}/{start.day:02} {start.hour:02}:{start.minute:02}~{end.hour:02}:{end.minute:02}"
                return returnStr
            except :
                return f"{self.params['days']}日以内に予定はありません。\n"
    
    def updateSchedule(self) :

        response = requests.get(self.timetreeURL + "/upcoming_events", headers = self.headers, params = self.params)
        if response.status_code == 200 :
            data = response.json()
            try :
                task = data["data"]
                returnStr = "予定の更新を確認しました。" 
                dt_now = pytz.utc.localize(datetime.datetime.now()).astimezone(pytz.timezone(os.environ["TZ"]))
                print(dt_now)
                for schedule in task :
                    update = self.isotoDate(schedule["attributes"]["updated_at"])
                    td = dt_now-update
                    print(update, td.seconds)
                    if td.seconds < 14400 :   
                        start = self.isotoDate(schedule["attributes"]["start_at"])
                        end = self.isotoDate(schedule["attributes"]["end_at"])
                        returnStr += "\n\n"
                        returnStr += "予定: " + schedule["attributes"]["title"] + "\n"
                        returnStr += "作成者: " + self.memberDic[schedule["relationships"]["creator"]["data"]["id"]] + "\n"
                        if schedule["attributes"]["all_day"] :
                            returnStr += "時間: " + f"{start.year:04}/{start.month:02}/{start.day:02} " + "終日"
                        else :
                            returnStr += "時間: " + f"{start.year:04}/{start.month:02}/{start.day:02} {start.hour:02}:{start.minute:02}~{end.hour:02}:{end.minute:02}"
                if(returnStr == "予定の更新を確認しました。") : returnStr = ""
                return returnStr
            except :
                return ""
