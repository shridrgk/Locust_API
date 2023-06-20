from locust import HttpUser, task
from psycopg2 import connect
import json


def getDBConnection(self, stateName):
    connection = connect(
        host='20.205.157.165',
        port='5432',
        database='app-eln-project-nfr',
        user='elndev',
        password='tyIgqa%5Apio'
    )
    cursor = connection.cursor()
    cursor.execute(
        """
        SELECT
            COUNT(*) FILTER (WHERE state = 'idle') AS idle_connections,
            COUNT(*) FILTER (WHERE state = 'active') AS active_connections
        FROM
            pg_stat_activity
        WHERE
            state IN ('idle', 'active');
        """
    )
    result = cursor.fetchone()
    print(
        f"Idle connections on {stateName}: {result[0]}, Active connections: {result[1]}")
    cursor.close()


class ELN(HttpUser):
    def on_start(self):
        getDBConnection(self, "Start")

    def on_stop(self):
        getDBConnection(self, "End")

    configFile = open('config.json')
    conf = json.load(configFile)

    host = "https://cloud.msa2.apps.yokogawa.build"
    headers = {
        "content-type": "application/json",
        'Authorization': 'Bearer eyJhbGciOiJIUzUxMiIsInR5cCI6IkpXVCJ9.eyJ1c2VySWQiOiJjYjIyMmM2MTkyY2Y0ODE0OGYwNmU4ZTY2YTcyZDY3NCIsImZpcnN0TmFtZSI6IlNocmlkaGFyYSIsImxhc3ROYW1lIjoiUmFtYXN3YW15IiwibG9jYXRpb24iOiJUZXN0IiwiZW1wbG95ZWVJZCI6IiIsImFwcGxpY2F0aW9uSWQiOiJFTE4iLCJ0ZW5hbnRJZCI6IjlhNThkZWJlLTRhYzAtNDdjMy1iMzZjLWVkYjU4MTNhYzBhYyIsInRlbmFudE5hbWUiOiJXSU5PUy1ERVYiLCJnbG9iYWxQZXJtaXNzaW9ucyI6IntcInJvbGVOYW1lXCI6XCJMYWIgTWFuYWdlclwiLFwicHJpdmlsZWdlc1wiOlt7XCJBc3NldFR5cGVcIjpcIlByb2plY3RcIixcInByaXZpbGVnZXNcIjpbXCJDcmVhdGVcIixcIlZpZXdcIixcIkVkaXRcIixcIkRlbGV0ZVwiLFwiRG93bmxvYWRcIl19LHtcIkFzc2V0VHlwZVwiOlwiVGFza1wiLFwicHJpdmlsZWdlc1wiOltcIkNyZWF0ZVwiLFwiVmlld1wiLFwiRWRpdFwiLFwiRG93bmxvYWRcIl19LHtcIkFzc2V0VHlwZVwiOlwiSW52ZW50b3J5XCIsXCJwcml2aWxlZ2VzXCI6W1wiQ3JlYXRlXCIsXCJWaWV3XCIsXCJFZGl0XCIsXCJEZWxldGVcIixcIkRvd25sb2FkXCJdfSx7XCJBc3NldFR5cGVcIjpcIkRvY3VtZW50XCIsXCJwcml2aWxlZ2VzXCI6W1wiQ3JlYXRlXCIsXCJWaWV3XCIsXCJFZGl0XCIsXCJEZWxldGVcIixcIkRvd25sb2FkXCJdfSx7XCJBc3NldFR5cGVcIjpcIlRlbXBsYXRlXCIsXCJwcml2aWxlZ2VzXCI6W1wiQ3JlYXRlXCIsXCJWaWV3XCIsXCJFZGl0XCIsXCJEZWxldGVcIixcIkRvd25sb2FkXCJdfSx7XCJBc3NldFR5cGVcIjpcIlJvbGVcIixcInByaXZpbGVnZXNcIjpbXCJDcmVhdGVcIixcIlZpZXdcIixcIkVkaXRcIixcIkRlbGV0ZVwiXX0se1wiQXNzZXRUeXBlXCI6XCJVc2VyXCIsXCJwcml2aWxlZ2VzXCI6W1wiVmlld1wiLFwiRWRpdFwiLFwiRG93bmxvYWRcIl19LHtcIkFzc2V0VHlwZVwiOlwiU2tpbGxcIixcInByaXZpbGVnZXNcIjpbXCJDcmVhdGVcIixcIlZpZXdcIixcIkVkaXRcIixcIkRlbGV0ZVwiLFwiRG93bmxvYWRcIl19LHtcIkFzc2V0VHlwZVwiOlwiQ29uZmlndXJhdGlvblwiLFwicHJpdmlsZWdlc1wiOltcIlZpZXdcIixcIkVkaXRcIl19XX0iLCJuYmYiOjE2ODY4MjA1MTYsImV4cCI6MTY4NjkwNjkxNiwiaWF0IjoxNjg2ODIwNTE2LCJpc3MiOiJodHRwczovL2Nsb3VkLm1zYTIuYXBwcy55b2tvZ2F3YS5idWlsZC8iLCJhdWQiOiJodHRwczovL2Nsb3VkLm1zYTIuYXBwcy55b2tvZ2F3YS5idWlsZC8ifQ.NPtI5xgYp5HHiRntCv8MhjRTfU2GZUPPmiu3kGhXzkRCH6mJ15pwZtmdo-LgRKvpqKVn_cI2ufTX63psHIvvtg'
    }

    @task
    def getNotificationList(self):

        body = {"PageNumber": 1, "PageSize": 10,
                "OrderByDir": "desc", "searchFilters": []}
        with self.client.get('/eln-core-svc-nfr/v1/Notification/list', name='GetNotificationList', catch_response=True,
                             headers=self.headers, data=json.dumps(body)) as response:
            if response.status_code == 200:
                response.success()
            else:
                response.failure(response)

    # @task
    # def getTemplateList(self):

    #     body = {"PageNumber":1,"PageSize":10,"OrderByDir":"desc","searchFilters":[]}
    #     with self.client.post('/eln-template-mgmt-svc-nfr/v1/Template/Search',name='getTemplateList', catch_response=True,
    #                           headers=self.headers, data=json.dumps(body)) as response:
    #         if response.status_code == 200:
    #             response.success()
    #         else:
    #             response.failure(response)

    # @task
    # def getProjectList(self):

    #     body = {"PageNumber":1,"PageSize":10,"OrderByColumn":"CreatedOn","OrderByDir":"desc","SearchFilters":[]}
    #     with self.client.post('/eln-project-mgmt-svc-nfr/v1/Project/Search',name='getProjectList', catch_response=True, headers=self.headers, data=json.dumps(body)) as response:
    #         if response.status_code == 200:
    #             response.success()
    #         else:
    #             response.failure(response)

    # @task
    # def getTaskList(self):

        # body = {
        #     "PageNumber": 1,
        #     "PageSize": 10,
        #     "taskTypeId": self.conf['taskTypeId'],
        #     "OrderByColumn": "id",
        #     "OrderByDir": "desc",
        #     "searchFilters": []
        #     }
    #     with self.client.post('/eln-project-mgmt-svc-nfr/v1/Task/Search',name='getTaskList', catch_response=True,
    #                           headers=self.headers, data=json.dumps(body)) as response:
    #         if response.status_code == 200:
    #             response.success()
    #         else:
    #             response.failure(response)

    # @task
    # def getDocList(self):

    #     body = {"PageNumber":1,"PageSize":10,"SearchFilters":[]}
    #     with self.client.post('/eln-docs-mgmt-svc-nfr/v1/Document/search',name='getDocList', catch_response=True,
    #                           headers=self.headers, data=json.dumps(body)) as response:
    #         if response.status_code == 200:
    #             response.success()
    #         else:
    #             response.failure(response)

    # @task
    # def getUserList(self):

    #     body = {"PageNumber":1,"PageSize":10,"SearchFilters":[]}
    #     with self.client.post('/eln-user-mgmt-nfr/v1/User/Search',name='getUserList', catch_response=True,
    #                           headers=self.headers, data=json.dumps(body)) as response:
    #         if response.status_code == 200:
    #             response.success()
    #         else:
    #             response.failure(response)

    # @task
    # def getEquipmentList(self):

    #     body = {"PageNumber":1,"PageSize":10,"searchFilters":[]}
    #     with self.client.post('/eln-inventory-mgmt-svc-nfr/v1/Equipment/search',name='getEquipmentList', catch_response=True,
    #                           headers=self.headers, data=json.dumps(body)) as response:
    #         if response.status_code == 200:
    #             response.success()
    #         else:
    #             response.failure(response)

    # @task
    # def getInstrumentList(self):

    #     body = {"PageNumber":1,"PageSize":10,"SearchFilters":[]}
    #     with self.client.post('/eln-inventory-mgmt-svc-nfr/v1/Instrument/search',name='getInstrumentList', catch_response=True,
    #                           headers=self.headers, data=json.dumps(body)) as response:
    #         if response.status_code == 200:
    #             response.success()
    #         else:
    #             response.failure(response)

    # @task
    # def getReagentList(self):

    #     body = {"PageNumber":1,"PageSize":10,"searchFilters":[]}
    #     with self.client.post('/eln-inventory-mgmt-svc-nfr/v1/Reagent/search',name='getReagentList', catch_response=True,
    #                           headers=self.headers, data=json.dumps(body)) as response:
    #         if response.status_code == 200:
    #             response.success()
    #         else:
    #             response.failure(response)

    # @task
    # def getSampleList(self):

    #     body = {"PageNumber":1,"PageSize":10,"SearchFilters":[]}
    #     with self.client.post('/eln-inventory-mgmt-svc-nfr/v1/Sample/search',name='getSampleList', catch_response=True,
    #                           headers=self.headers, data=json.dumps(body)) as response:
    #         if response.status_code == 200:
    #             response.success()
    #         else:
    #             response.failure(response)
