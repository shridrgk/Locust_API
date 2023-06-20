from locust import HttpUser, task, between
import json


class ELN(HttpUser):
    configFile = open('config.json')
    conf = json.load(configFile)
    i = 0
    host = "https://cloud.msa2.apps.yokogawa.build"
    headers = {
        "content-type": "application/json",
        'Authorization': 'Bearer eyJhbGciOiJIUzUxMiIsInR5cCI6IkpXVCJ9.eyJ1c2VySWQiOiJjYjIyMmM2MTkyY2Y0ODE0OGYwNmU4ZTY2YTcyZDY3NCIsImZpcnN0TmFtZSI6IlNocmlkaGFyYSIsImxhc3ROYW1lIjoiUmFtYXN3YW15IiwibG9jYXRpb24iOiJUZXN0IiwiZW1wbG95ZWVJZCI6IiIsImFwcGxpY2F0aW9uSWQiOiJFTE4iLCJ0ZW5hbnRJZCI6IjlhNThkZWJlLTRhYzAtNDdjMy1iMzZjLWVkYjU4MTNhYzBhYyIsInRlbmFudE5hbWUiOiJXSU5PUy1ERVYiLCJnbG9iYWxQZXJtaXNzaW9ucyI6IntcInJvbGVOYW1lXCI6XCJMYWIgTWFuYWdlclwiLFwicHJpdmlsZWdlc1wiOlt7XCJBc3NldFR5cGVcIjpcIlByb2plY3RcIixcInByaXZpbGVnZXNcIjpbXCJDcmVhdGVcIixcIlZpZXdcIixcIkVkaXRcIixcIkRlbGV0ZVwiLFwiRG93bmxvYWRcIl19LHtcIkFzc2V0VHlwZVwiOlwiVGFza1wiLFwicHJpdmlsZWdlc1wiOltcIkNyZWF0ZVwiLFwiVmlld1wiLFwiRWRpdFwiLFwiRG93bmxvYWRcIl19LHtcIkFzc2V0VHlwZVwiOlwiSW52ZW50b3J5XCIsXCJwcml2aWxlZ2VzXCI6W1wiQ3JlYXRlXCIsXCJWaWV3XCIsXCJFZGl0XCIsXCJEZWxldGVcIixcIkRvd25sb2FkXCJdfSx7XCJBc3NldFR5cGVcIjpcIkRvY3VtZW50XCIsXCJwcml2aWxlZ2VzXCI6W1wiQ3JlYXRlXCIsXCJWaWV3XCIsXCJFZGl0XCIsXCJEZWxldGVcIixcIkRvd25sb2FkXCJdfSx7XCJBc3NldFR5cGVcIjpcIlRlbXBsYXRlXCIsXCJwcml2aWxlZ2VzXCI6W1wiQ3JlYXRlXCIsXCJWaWV3XCIsXCJFZGl0XCIsXCJEZWxldGVcIixcIkRvd25sb2FkXCJdfSx7XCJBc3NldFR5cGVcIjpcIlJvbGVcIixcInByaXZpbGVnZXNcIjpbXCJDcmVhdGVcIixcIlZpZXdcIixcIkVkaXRcIixcIkRlbGV0ZVwiXX0se1wiQXNzZXRUeXBlXCI6XCJVc2VyXCIsXCJwcml2aWxlZ2VzXCI6W1wiVmlld1wiLFwiRWRpdFwiLFwiRG93bmxvYWRcIl19LHtcIkFzc2V0VHlwZVwiOlwiU2tpbGxcIixcInByaXZpbGVnZXNcIjpbXCJDcmVhdGVcIixcIlZpZXdcIixcIkVkaXRcIixcIkRlbGV0ZVwiLFwiRG93bmxvYWRcIl19LHtcIkFzc2V0VHlwZVwiOlwiQ29uZmlndXJhdGlvblwiLFwicHJpdmlsZWdlc1wiOltcIlZpZXdcIixcIkVkaXRcIl19XX0iLCJuYmYiOjE2ODY4MjA1MTYsImV4cCI6MTY4NjkwNjkxNiwiaWF0IjoxNjg2ODIwNTE2LCJpc3MiOiJodHRwczovL2Nsb3VkLm1zYTIuYXBwcy55b2tvZ2F3YS5idWlsZC8iLCJhdWQiOiJodHRwczovL2Nsb3VkLm1zYTIuYXBwcy55b2tvZ2F3YS5idWlsZC8ifQ.NPtI5xgYp5HHiRntCv8MhjRTfU2GZUPPmiu3kGhXzkRCH6mJ15pwZtmdo-LgRKvpqKVn_cI2ufTX63psHIvvtg'
    }

    def counterNum(self):
        while (True):
            self.i = self.i + 1
            return self.i

    @task
    def reserveInstrument(self):
        taskBodyData = open('InstrumentReserve.json')
        taskBody = json.load(taskBodyData)
        taskBody['subject'] = 'Updated' + str(self.counterNum())

        with self.client.post('/eln-inventory-mgmt-svc-nfr/v1/Instrument/00c332c9-7f54-4ca6-88a7-2db7357ddad2/reserve', name='InstrumentRserve', catch_response=True,
                              headers=self.headers, data=json.dumps(taskBody)) as response:
            if response.status_code == 200:
                response.success()
            else:
                print(response.json())
                response.failure(response)
