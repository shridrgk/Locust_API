from locust import HttpUser, task, between
import json
import uuid


class ELN(HttpUser):
    configFile = open('config.json')
    conf = json.load(configFile)
    i = 0
    j = 0
    host = "https://cloud.msa2.apps.yokogawa.build"
    headers = {
        "content-type": "application/json",
        'Authorization': 'Bearer eyJhbGciOiJIUzUxMiIsInR5cCI6IkpXVCJ9.eyJ1c2VySWQiOiJjYjIyMmM2MTkyY2Y0ODE0OGYwNmU4ZTY2YTcyZDY3NCIsImZpcnN0TmFtZSI6IlNocmlkaGFyYSIsImxhc3ROYW1lIjoiUmFtYXN3YW15IiwibG9jYXRpb24iOiJUZXN0IiwiZW1wbG95ZWVJZCI6IiIsImFwcGxpY2F0aW9uSWQiOiJFTE4iLCJ0ZW5hbnRJZCI6IjlhNThkZWJlLTRhYzAtNDdjMy1iMzZjLWVkYjU4MTNhYzBhYyIsInRlbmFudE5hbWUiOiJXSU5PUy1ERVYiLCJnbG9iYWxQZXJtaXNzaW9ucyI6IntcInJvbGVOYW1lXCI6XCJMYWIgTWFuYWdlclwiLFwicHJpdmlsZWdlc1wiOlt7XCJBc3NldFR5cGVcIjpcIlByb2plY3RcIixcInByaXZpbGVnZXNcIjpbXCJDcmVhdGVcIixcIlZpZXdcIixcIkVkaXRcIixcIkRlbGV0ZVwiLFwiRG93bmxvYWRcIl19LHtcIkFzc2V0VHlwZVwiOlwiVGFza1wiLFwicHJpdmlsZWdlc1wiOltcIkNyZWF0ZVwiLFwiVmlld1wiLFwiRWRpdFwiLFwiRG93bmxvYWRcIl19LHtcIkFzc2V0VHlwZVwiOlwiSW52ZW50b3J5XCIsXCJwcml2aWxlZ2VzXCI6W1wiQ3JlYXRlXCIsXCJWaWV3XCIsXCJFZGl0XCIsXCJEZWxldGVcIixcIkRvd25sb2FkXCJdfSx7XCJBc3NldFR5cGVcIjpcIkRvY3VtZW50XCIsXCJwcml2aWxlZ2VzXCI6W1wiQ3JlYXRlXCIsXCJWaWV3XCIsXCJFZGl0XCIsXCJEZWxldGVcIixcIkRvd25sb2FkXCJdfSx7XCJBc3NldFR5cGVcIjpcIlRlbXBsYXRlXCIsXCJwcml2aWxlZ2VzXCI6W1wiQ3JlYXRlXCIsXCJWaWV3XCIsXCJFZGl0XCIsXCJEZWxldGVcIixcIkRvd25sb2FkXCJdfSx7XCJBc3NldFR5cGVcIjpcIlJvbGVcIixcInByaXZpbGVnZXNcIjpbXCJDcmVhdGVcIixcIlZpZXdcIixcIkVkaXRcIixcIkRlbGV0ZVwiXX0se1wiQXNzZXRUeXBlXCI6XCJVc2VyXCIsXCJwcml2aWxlZ2VzXCI6W1wiVmlld1wiLFwiRWRpdFwiLFwiRG93bmxvYWRcIl19LHtcIkFzc2V0VHlwZVwiOlwiU2tpbGxcIixcInByaXZpbGVnZXNcIjpbXCJDcmVhdGVcIixcIlZpZXdcIixcIkVkaXRcIixcIkRlbGV0ZVwiLFwiRG93bmxvYWRcIl19LHtcIkFzc2V0VHlwZVwiOlwiQ29uZmlndXJhdGlvblwiLFwicHJpdmlsZWdlc1wiOltcIlZpZXdcIixcIkVkaXRcIl19XX0iLCJuYmYiOjE2ODcyMzc1NzgsImV4cCI6MTY4NzMyMzk3OCwiaWF0IjoxNjg3MjM3NTc4LCJpc3MiOiJodHRwczovL2Nsb3VkLm1zYTIuYXBwcy55b2tvZ2F3YS5idWlsZC8iLCJhdWQiOiJodHRwczovL2Nsb3VkLm1zYTIuYXBwcy55b2tvZ2F3YS5idWlsZC8ifQ.CCelBXzmzrXG-Nd9qESC8r_d2u8jQ737aYgfhHs7Ex1PDbCpojYpeLqppZxS49pX0coT_mtw-upUpGRM7ks3CQ'
    }

    def counterNum(self):
        while (True):
            self.i = self.i + 1
            return self.i

    def counterNum1(self):
        while (True):
            self.j = self.j + 1
            return self.j

    @task
    def createTask(self):
        taskBodyData = open('taskBody.json')
        taskBody = json.load(taskBodyData)

        taskBody['title'] = str(uuid.uuid4())
        taskBody['blocks'][0]['fields'][0]['value'] = str(uuid.uuid4())

        with self.client.post('/eln-project-mgmt-svc-nfr/v1/Task', name='createTask', catch_response=True,
                              headers=self.headers, data=json.dumps(taskBody)) as response:
            if response.status_code == 200:
                response.success()
            else:
                print(response.request.body)
                print(response.json())
                response.failure(response)
