from Modules import misc 
import time 
import tls_client
import httpx 
import traceback 

class Capsolver:
    def __init__(self, captcha_key):
        self.key = captcha_key
        self.client = tls_client.Session(
            client_identifier="firefox_110"
        )

    def CreateTask(self, rqdata: str, sitekey: str, proxy: str):
        username = proxy.split(":")[1]
        password = proxy.split(":")[2].split("@")[0]
        ip = proxy.split(":")[2].split("@")[1]
        port = proxy.split(":")[3]
        proxy = "http:%s:%s:%s:%s" % (ip, port, username, password)

        response = self.client.post("https://api.capsolver.com/createTask", json={
            "clientKey": self.key,
            "task": {
                "type": "HCaptchaTurboTask",
                "websiteURL": "https://discord.com/channels/@me",
                "websiteKey": sitekey,
                "proxy": proxy,
                "enterprisePayload": {
                    "rqdata": rqdata
                },
            }
        })
        return response.json()["taskId"]

    def GetSolution(self, taskId: str):
        response = self.client.post("https://api.capsolver.com/getTaskResult", json={
            "clientKey": self.key,
            "taskId": taskId
        })
        while response.json()["status"] == "processing":
            time.sleep(3)
            response = self.client.post("https://api.capsolver.com/getTaskResult", json={
                "clientKey": self.key,
                "taskId": taskId
            })  
            if response.json()["status"] == "ready":
                print(response.text)
                if response.json()["solution"]["captchaKey"] != "":
                    return response.json()["solution"]["captchaKey"]
                else:
                    return response.json()["solution"]["gRecaptchaResponse"]
                
class Hcoptcha:
    def __init__(self, captcha_key):
        self.key = captcha_key
        self.client = tls_client.Session(
            client_identifier="firefox_110"
        )

import httpx 
import time 
import tls_client

class Hcoptcha:
    def __init__(self, captcha_key):
        self.key = captcha_key
        self.client = tls_client.Session(
            client_identifier="firefox_110"
        )

    def Solve(self, rqdata, sitekey, proxy: str):
        try:
            task = httpx.post(
                'https://api.hcoptcha.online/api/createTask',
                json={
                    "api_key": self.key,
                    "task_type": "hcaptchaEnterprise",
                    "data": {
                        "rqdata": rqdata,
                        "sitekey": sitekey,
                        "proxy": proxy,
                        "host": "discord.com"
                    }
                }
            ).json()["task_id"]

            result = httpx.post(
                'https://api.hcoptcha.online/api/getTaskData',
                json={
                    "api_key": self.key,
                    "task_id": task
                }
            ).json()

            while result['task']['state'] == "processing":
                result = httpx.post(
                    'https://api.hcoptcha.online/api/getTaskData',
                    json={
                        "api_key": self.key,
                        "task_id": task
                    }
                ).json()
                time.sleep(2)
            if result['task']['state'] == "error":
                raise Exception("Failed to solve")
            return result['task']['captcha_key']
        except Exception as err:
            print(err)