from locust import HttpUser, task, between
import json


class ELN(HttpUser):
    configFile = open('config.json')
    conf = json.load(configFile)
    i = 0
    host = "https://cloud.msa2.apps.yokogawa.build"
    headers = {
        "content-type": "application/json",
        'Authorization': 'Bearer eyJhbGciOiJIUzUxMiIsInR5cCI6IkpXVCJ9.eyJ1c2VySWQiOiI1NzM2NmI4MTZiMDI0NDNlYmFjMGI1NjNlZTU0YzMyZSIsImZpcnN0TmFtZSI6IlByYXZpbCIsImxhc3ROYW1lIjoiUmFqIiwibG9jYXRpb24iOiJCYW5nYWxvcmUiLCJlbXBsb3llZUlkIjoiNDc3eHh4eHgiLCJhcHBsaWNhdGlvbklkIjoiRUxOIiwidGVuYW50SWQiOiI5YTU4ZGViZS00YWMwLTQ3YzMtYjM2Yy1lZGI1ODEzYWMwYWMiLCJ0ZW5hbnROYW1lIjoiV0lOT1MtREVWIiwiZ2xvYmFsUGVybWlzc2lvbnMiOiJ7XCJyb2xlTmFtZVwiOlwiTGFiIE1hbmFnZXJcIixcInByaXZpbGVnZXNcIjpbe1wiQXNzZXRUeXBlXCI6XCJQcm9qZWN0XCIsXCJwcml2aWxlZ2VzXCI6W1wiQ3JlYXRlXCIsXCJWaWV3XCIsXCJFZGl0XCIsXCJEZWxldGVcIixcIkRvd25sb2FkXCJdfSx7XCJBc3NldFR5cGVcIjpcIlRhc2tcIixcInByaXZpbGVnZXNcIjpbXCJDcmVhdGVcIixcIlZpZXdcIixcIkVkaXRcIixcIkRvd25sb2FkXCJdfSx7XCJBc3NldFR5cGVcIjpcIkludmVudG9yeVwiLFwicHJpdmlsZWdlc1wiOltcIkNyZWF0ZVwiLFwiVmlld1wiLFwiRWRpdFwiLFwiRGVsZXRlXCIsXCJEb3dubG9hZFwiXX0se1wiQXNzZXRUeXBlXCI6XCJEb2N1bWVudFwiLFwicHJpdmlsZWdlc1wiOltcIkNyZWF0ZVwiLFwiVmlld1wiLFwiRWRpdFwiLFwiRGVsZXRlXCIsXCJEb3dubG9hZFwiXX0se1wiQXNzZXRUeXBlXCI6XCJUZW1wbGF0ZVwiLFwicHJpdmlsZWdlc1wiOltcIkNyZWF0ZVwiLFwiVmlld1wiLFwiRWRpdFwiLFwiRGVsZXRlXCIsXCJEb3dubG9hZFwiXX0se1wiQXNzZXRUeXBlXCI6XCJSb2xlXCIsXCJwcml2aWxlZ2VzXCI6W1wiQ3JlYXRlXCIsXCJWaWV3XCIsXCJFZGl0XCIsXCJEZWxldGVcIl19LHtcIkFzc2V0VHlwZVwiOlwiVXNlclwiLFwicHJpdmlsZWdlc1wiOltcIlZpZXdcIixcIkVkaXRcIixcIkRvd25sb2FkXCJdfSx7XCJBc3NldFR5cGVcIjpcIlNraWxsXCIsXCJwcml2aWxlZ2VzXCI6W1wiQ3JlYXRlXCIsXCJWaWV3XCIsXCJFZGl0XCIsXCJEZWxldGVcIixcIkRvd25sb2FkXCJdfSx7XCJBc3NldFR5cGVcIjpcIkNvbmZpZ3VyYXRpb25cIixcInByaXZpbGVnZXNcIjpbXCJWaWV3XCIsXCJFZGl0XCJdfV19IiwibmJmIjoxNjg2NTg4OTA2LCJleHAiOjE2ODY2NzUzMDYsImlhdCI6MTY4NjU4ODkwNiwiaXNzIjoiaHR0cHM6Ly9jbG91ZC5tc2EyLmFwcHMueW9rb2dhd2EuYnVpbGQvIiwiYXVkIjoiaHR0cHM6Ly9jbG91ZC5tc2EyLmFwcHMueW9rb2dhd2EuYnVpbGQvIn0.kTaNH7fAPsOw3xz4xyjpziaf1WIOFeOJUYvJ29lnc9hNv-THMvngoJUMYKYYendaQE5pAXoCp9JWoKYfE81R0A'
    }

    @task
    def addSchedule(self):
        taskBodyData = open('AddSchedule.json')
        taskBody = json.load(taskBodyData)

        with self.client.post('/eln-project-mgmt-svc-nfr/v1/UserScheduleTask/add', name='UserScheduleTask', catch_response=True,
                              headers=self.headers, data=json.dumps(taskBody)) as response:
            if response.status_code == 200:
                response.success()
            else:
                print(response.json())
                response.failure(response)
