from locust import HttpUser, task, between
import json


class ELN(HttpUser):
    configFile = open('config.json')
    conf = json.load(configFile)
    i = 0
    host = "https://cloud.msa2.apps.yokogawa.build"
    headers = {
        "content-type": "application/json",
        'Authorization': 'Bearer eyJhbGciOiJIUzUxMiIsInR5cCI6IkpXVCJ9.eyJ1c2VySWQiOiJjYjIyMmM2MTkyY2Y0ODE0OGYwNmU4ZTY2YTcyZDY3NCIsImZpcnN0TmFtZSI6IlNocmlkaGFyYSIsImxhc3ROYW1lIjoiUmFtYXN3YW15IiwibG9jYXRpb24iOiJUZXN0IiwiZW1wbG95ZWVJZCI6IiIsImFwcGxpY2F0aW9uSWQiOiJFTE4iLCJ0ZW5hbnRJZCI6IjlhNThkZWJlLTRhYzAtNDdjMy1iMzZjLWVkYjU4MTNhYzBhYyIsInRlbmFudE5hbWUiOiJXSU5PUy1ERVYiLCJnbG9iYWxQZXJtaXNzaW9ucyI6IntcInJvbGVOYW1lXCI6XCJMYWIgTWFuYWdlclwiLFwicHJpdmlsZWdlc1wiOlt7XCJBc3NldFR5cGVcIjpcIlByb2plY3RcIixcInByaXZpbGVnZXNcIjpbXCJDcmVhdGVcIixcIlZpZXdcIixcIkVkaXRcIixcIkRlbGV0ZVwiLFwiRG93bmxvYWRcIl19LHtcIkFzc2V0VHlwZVwiOlwiVGFza1wiLFwicHJpdmlsZWdlc1wiOltcIkNyZWF0ZVwiLFwiVmlld1wiLFwiRWRpdFwiLFwiRG93bmxvYWRcIl19LHtcIkFzc2V0VHlwZVwiOlwiSW52ZW50b3J5XCIsXCJwcml2aWxlZ2VzXCI6W1wiQ3JlYXRlXCIsXCJWaWV3XCIsXCJFZGl0XCIsXCJEZWxldGVcIixcIkRvd25sb2FkXCJdfSx7XCJBc3NldFR5cGVcIjpcIkRvY3VtZW50XCIsXCJwcml2aWxlZ2VzXCI6W1wiQ3JlYXRlXCIsXCJWaWV3XCIsXCJFZGl0XCIsXCJEZWxldGVcIixcIkRvd25sb2FkXCJdfSx7XCJBc3NldFR5cGVcIjpcIlRlbXBsYXRlXCIsXCJwcml2aWxlZ2VzXCI6W1wiQ3JlYXRlXCIsXCJWaWV3XCIsXCJFZGl0XCIsXCJEZWxldGVcIixcIkRvd25sb2FkXCJdfSx7XCJBc3NldFR5cGVcIjpcIlJvbGVcIixcInByaXZpbGVnZXNcIjpbXCJDcmVhdGVcIixcIlZpZXdcIixcIkVkaXRcIixcIkRlbGV0ZVwiXX0se1wiQXNzZXRUeXBlXCI6XCJVc2VyXCIsXCJwcml2aWxlZ2VzXCI6W1wiVmlld1wiLFwiRWRpdFwiLFwiRG93bmxvYWRcIl19LHtcIkFzc2V0VHlwZVwiOlwiU2tpbGxcIixcInByaXZpbGVnZXNcIjpbXCJDcmVhdGVcIixcIlZpZXdcIixcIkVkaXRcIixcIkRlbGV0ZVwiLFwiRG93bmxvYWRcIl19LHtcIkFzc2V0VHlwZVwiOlwiQ29uZmlndXJhdGlvblwiLFwicHJpdmlsZWdlc1wiOltcIlZpZXdcIixcIkVkaXRcIl19XX0iLCJuYmYiOjE2ODY4Mzg2NTQsImV4cCI6MTY4NjkyNTA1NCwiaWF0IjoxNjg2ODM4NjU0LCJpc3MiOiJodHRwczovL2Nsb3VkLm1zYTIuYXBwcy55b2tvZ2F3YS5idWlsZC8iLCJhdWQiOiJodHRwczovL2Nsb3VkLm1zYTIuYXBwcy55b2tvZ2F3YS5idWlsZC8ifQ.HcJrk2h068UP2auF1TLQ5pQY5tIycgIAd1PkFnEsqmSGOoWRpcTWbTLUaMUhxL8E2vFyD_MCwSZZWe8Pp-LzrQ',
        'AccessToken': 'st2.s.AcbHfU9hrQ.bMHmbtJJlx47LdIfW6-Q42-ijOqPB0koJihKLOcXwbj1JjkDwB2MAOeWn9M0FuWoYNGQoZmqYuqHCHDWLMSMB0UsJHUS7v_GivsdEjABc6c.YqsQkYeJeJUncfzb3E5z7mZNZ-LxAQ-gAEIR_CV_boOW5STnDevH-KB4pzq2cNYQ7zpjQZdP7Ws0caBUE1u1xg.sc3'
    }

    @task
    def AccessCheck(self):
        taskBodyData = open('AccessCheck.json')
        taskBody = json.load(taskBodyData)
        taskBody['RouteDataValues'][2]['RouteValue'] = 'YG_PJ__DEMO_0001'

        with self.client.post('/eln-authz-svc-nfr/v1/AccessCheck', name='AccessCheck', catch_response=True,
                              headers=self.headers, data=json.dumps(taskBody)) as response:
            if response.status_code == 200:
                response.success()
            else:
                print(response.json())
                response.failure(response)
