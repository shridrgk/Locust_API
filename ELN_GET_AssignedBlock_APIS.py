from codecs import encode
import http.client
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
    localboundary = 'wL36Yn8afVp8Ag7AmP8qZ0SA4n1v9T'
    host = "https://cloud.msa2.apps.yokogawa.build"
    headers = {
        'Content-type': 'multipart/form-data; boundary={}'.format(localboundary),
        'Authorization': 'Bearer eyJhbGciOiJIUzUxMiIsInR5cCI6IkpXVCJ9.eyJ1c2VySWQiOiJjYjIyMmM2MTkyY2Y0ODE0OGYwNmU4ZTY2YTcyZDY3NCIsImZpcnN0TmFtZSI6IlNocmlkaGFyYSIsImxhc3ROYW1lIjoiUmFtYXN3YW15IiwibG9jYXRpb24iOiJUZXN0IiwiZW1wbG95ZWVJZCI6IiIsImFwcGxpY2F0aW9uSWQiOiJFTE4iLCJ0ZW5hbnRJZCI6IjlhNThkZWJlLTRhYzAtNDdjMy1iMzZjLWVkYjU4MTNhYzBhYyIsInRlbmFudE5hbWUiOiJXSU5PUy1ERVYiLCJnbG9iYWxQZXJtaXNzaW9ucyI6IntcInJvbGVOYW1lXCI6XCJMYWIgTWFuYWdlclwiLFwicHJpdmlsZWdlc1wiOlt7XCJBc3NldFR5cGVcIjpcIlByb2plY3RcIixcInByaXZpbGVnZXNcIjpbXCJDcmVhdGVcIixcIlZpZXdcIixcIkVkaXRcIixcIkRlbGV0ZVwiLFwiRG93bmxvYWRcIl19LHtcIkFzc2V0VHlwZVwiOlwiVGFza1wiLFwicHJpdmlsZWdlc1wiOltcIkNyZWF0ZVwiLFwiVmlld1wiLFwiRWRpdFwiLFwiRG93bmxvYWRcIl19LHtcIkFzc2V0VHlwZVwiOlwiSW52ZW50b3J5XCIsXCJwcml2aWxlZ2VzXCI6W1wiQ3JlYXRlXCIsXCJWaWV3XCIsXCJFZGl0XCIsXCJEZWxldGVcIixcIkRvd25sb2FkXCJdfSx7XCJBc3NldFR5cGVcIjpcIkRvY3VtZW50XCIsXCJwcml2aWxlZ2VzXCI6W1wiQ3JlYXRlXCIsXCJWaWV3XCIsXCJFZGl0XCIsXCJEZWxldGVcIixcIkRvd25sb2FkXCJdfSx7XCJBc3NldFR5cGVcIjpcIlRlbXBsYXRlXCIsXCJwcml2aWxlZ2VzXCI6W1wiQ3JlYXRlXCIsXCJWaWV3XCIsXCJFZGl0XCIsXCJEZWxldGVcIixcIkRvd25sb2FkXCJdfSx7XCJBc3NldFR5cGVcIjpcIlJvbGVcIixcInByaXZpbGVnZXNcIjpbXCJDcmVhdGVcIixcIlZpZXdcIixcIkVkaXRcIixcIkRlbGV0ZVwiXX0se1wiQXNzZXRUeXBlXCI6XCJVc2VyXCIsXCJwcml2aWxlZ2VzXCI6W1wiVmlld1wiLFwiRWRpdFwiLFwiRG93bmxvYWRcIl19LHtcIkFzc2V0VHlwZVwiOlwiU2tpbGxcIixcInByaXZpbGVnZXNcIjpbXCJDcmVhdGVcIixcIlZpZXdcIixcIkVkaXRcIixcIkRlbGV0ZVwiLFwiRG93bmxvYWRcIl19LHtcIkFzc2V0VHlwZVwiOlwiQ29uZmlndXJhdGlvblwiLFwicHJpdmlsZWdlc1wiOltcIlZpZXdcIixcIkVkaXRcIl19XX0iLCJuYmYiOjE2ODY4MjA1MTYsImV4cCI6MTY4NjkwNjkxNiwiaWF0IjoxNjg2ODIwNTE2LCJpc3MiOiJodHRwczovL2Nsb3VkLm1zYTIuYXBwcy55b2tvZ2F3YS5idWlsZC8iLCJhdWQiOiJodHRwczovL2Nsb3VkLm1zYTIuYXBwcy55b2tvZ2F3YS5idWlsZC8ifQ.NPtI5xgYp5HHiRntCv8MhjRTfU2GZUPPmiu3kGhXzkRCH6mJ15pwZtmdo-LgRKvpqKVn_cI2ufTX63psHIvvtg'
    }

    @task
    def AssignedBlock(self):

        dataList = []
        boundary = 'wL36Yn8afVp8Ag7AmP8qZ0SA4n1v9T'
        dataList.append(encode('--' + boundary))
        dataList.append(encode('Content-Disposition: form-data; name=Name;'))

        dataList.append(encode('Content-Type: {}'.format('text/plain')))
        dataList.append(encode(''))

        dataList.append(encode("{{name}}"))
        dataList.append(encode('--' + boundary))
        dataList.append(encode('Content-Disposition: form-data; name=Author;'))

        dataList.append(encode('Content-Type: {}'.format('text/plain')))
        dataList.append(encode(''))

        dataList.append(encode("Vixen"))
        dataList.append(encode('--' + boundary))
        dataList.append(
            encode('Content-Disposition: form-data; name=DocumentNumber;'))

        dataList.append(encode('Content-Type: {}'.format('text/plain')))
        dataList.append(encode(''))

        dataList.append(encode("{{DocNum}}"))
        dataList.append(encode('--' + boundary))
        dataList.append(
            encode('Content-Disposition: form-data; name=CreatedBy;'))

        dataList.append(encode('Content-Type: {}'.format('text/plain')))
        dataList.append(encode(''))

        dataList.append(encode("cb222c6192cf48148f06e8e66a72d674"))
        dataList.append(encode('--' + boundary))
        dataList.append(
            encode('Content-Disposition: form-data; name=VersionNumber;'))

        dataList.append(encode('Content-Type: {}'.format('text/plain')))
        dataList.append(encode(''))

        dataList.append(encode("1.001"))
        dataList.append(encode('--' + boundary))
        dataList.append(encode('Content-Disposition: form-data; name=Tags;'))

        dataList.append(encode('Content-Type: {}'.format('text/plain')))
        dataList.append(encode(''))

        dataList.append(encode("a,i"))
        dataList.append(encode('--' + boundary))
        dataList.append(
            encode('Content-Disposition: form-data; name=DocumentIdentityNumber;'))

        dataList.append(encode('Content-Type: {}'.format('text/plain')))
        dataList.append(encode(''))

        dataList.append(encode("0"))
        dataList.append(encode('--' + boundary))
        dataList.append(
            encode('Content-Disposition: form-data; name=DocumentNumbers;'))

        dataList.append(encode('Content-Type: {}'.format('text/plain')))
        dataList.append(encode(''))

        dataList.append(encode("1234"))
        dataList.append(encode('--' + boundary))
        dataList.append(
            encode('Content-Disposition: form-data; name=FileJson;'))

        dataList.append(encode('Content-Type: {}'.format('text/plain')))
        dataList.append(encode(''))

        dataList.append(encode("{\"sections\":[{\"sectionFormat\":{\"pageWidth\":612,\"pageHeight\":792,\"leftMargin\":72,\"rightMargin\":72,\"topMargin\":72,\"bottomMargin\":72,\"differentFirstPage\":false,\"differentOddAndEvenPages\":false,\"headerDistance\":36,\"footerDistance\":36,\"bidi\":false},\"blocks\":[{\"paragraphFormat\":{\"styleName\":\"Normal\",\"listFormat\":{}},\"characterFormat\":{},\"inlines\":[{\"characterFormat\":{\"bidi\":false},\"text\":\"sfsdfs\"}]}],\"headersFooters\":{\"header\":{\"blocks\":[{\"paragraphFormat\":{\"listFormat\":{}},\"characterFormat\":{},\"inlines\":[]}]},\"footer\":{\"blocks\":[{\"paragraphFormat\":{\"listFormat\":{}},\"characterFormat\":{},\"inlines\":[]}]},\"evenHeader\":{},\"evenFooter\":{},\"firstPageHeader\":{},\"firstPageFooter\":{}}}],\"characterFormat\":{\"bold\":false,\"italic\":false,\"fontSize\":11,\"fontFamily\":\"Calibri\",\"underline\":\"None\",\"strikethrough\":\"None\",\"baselineAlignment\":\"Normal\",\"highlightColor\":\"NoColor\",\"fontColor\":\"#00000000\",\"boldBidi\":false,\"italicBidi\":false,\"fontSizeBidi\":11,\"fontFamilyBidi\":\"Calibri\",\"allCaps\":false},\"paragraphFormat\":{\"leftIndent\":0,\"rightIndent\":0,\"firstLineIndent\":0,\"textAlignment\":\"Left\",\"beforeSpacing\":0,\"afterSpacing\":0,\"lineSpacing\":1,\"lineSpacingType\":\"Multiple\",\"listFormat\":{},\"bidi\":false,\"keepLinesTogether\":false,\"keepWithNext\":false,\"widowControl\":true},\"defaultTabWidth\":36,\"trackChanges\":false,\"enforcement\":false,\"hashValue\":\"\",\"saltValue\":\"\",\"formatting\":false,\"protectionType\":\"NoProtection\",\"dontUseHTMLParagraphAutoSpacing\":false,\"formFieldShading\":true,\"compatibilityMode\":\"Word2013\",\"styles\":[{\"name\":\"Normal\",\"type\":\"Paragraph\",\"paragraphFormat\":{\"listFormat\":{}},\"characterFormat\":{},\"next\":\"Normal\"},{\"name\":\"Heading 1\",\"type\":\"Paragraph\",\"paragraphFormat\":{\"leftIndent\":0,\"rightIndent\":0,\"firstLineIndent\":0,\"textAlignment\":\"Left\",\"beforeSpacing\":12,\"afterSpacing\":0,\"lineSpacing\":1.0791666507720947,\"lineSpacingType\":\"Multiple\",\"outlineLevel\":\"Level1\",\"listFormat\":{}},\"characterFormat\":{\"fontSize\":16,\"fontFamily\":\"Calibri Light\",\"fontColor\":\"#2F5496\",\"fontSizeBidi\":16,\"fontFamilyBidi\":\"Calibri Light\"},\"basedOn\":\"Normal\",\"link\":\"Heading 1 Char\",\"next\":\"Normal\"},{\"name\":\"Heading 1 Char\",\"type\":\"Character\",\"characterFormat\":{\"fontSize\":16,\"fontFamily\":\"Calibri Light\",\"fontColor\":\"#2F5496\",\"fontSizeBidi\":16,\"fontFamilyBidi\":\"Calibri Light\"},\"basedOn\":\"Default Paragraph Font\"},{\"name\":\"Default Paragraph Font\",\"type\":\"Character\",\"characterFormat\":{}},{\"name\":\"Heading 2\",\"type\":\"Paragraph\",\"paragraphFormat\":{\"leftIndent\":0,\"rightIndent\":0,\"firstLineIndent\":0,\"textAlignment\":\"Left\",\"beforeSpacing\":2,\"afterSpacing\":0,\"lineSpacing\":1.0791666507720947,\"lineSpacingType\":\"Multiple\",\"outlineLevel\":\"Level2\",\"listFormat\":{}},\"characterFormat\":{\"fontSize\":13,\"fontFamily\":\"Calibri Light\",\"fontColor\":\"#2F5496\",\"fontSizeBidi\":13,\"fontFamilyBidi\":\"Calibri Light\"},\"basedOn\":\"Normal\",\"link\":\"Heading 2 Char\",\"next\":\"Normal\"},{\"name\":\"Heading 2 Char\",\"type\":\"Character\",\"characterFormat\":{\"fontSize\":13,\"fontFamily\":\"Calibri Light\",\"fontColor\":\"#2F5496\",\"fontSizeBidi\":13,\"fontFamilyBidi\":\"Calibri Light\"},\"basedOn\":\"Default Paragraph Font\"},{\"name\":\"Heading 3\",\"type\":\"Paragraph\",\"paragraphFormat\":{\"leftIndent\":0,\"rightIndent\":0,\"firstLineIndent\":0,\"textAlignment\":\"Left\",\"beforeSpacing\":2,\"afterSpacing\":0,\"lineSpacing\":1.0791666507720947,\"lineSpacingType\":\"Multiple\",\"outlineLevel\":\"Level3\",\"listFormat\":{}},\"characterFormat\":{\"fontSize\":12,\"fontFamily\":\"Calibri Light\",\"fontColor\":\"#1F3763\",\"fontSizeBidi\":12,\"fontFamilyBidi\":\"Calibri Light\"},\"basedOn\":\"Normal\",\"link\":\"Heading 3 Char\",\"next\":\"Normal\"},{\"name\":\"Heading 3 Char\",\"type\":\"Character\",\"characterFormat\":{\"fontSize\":12,\"fontFamily\":\"Calibri Light\",\"fontColor\":\"#1F3763\",\"fontSizeBidi\":12,\"fontFamilyBidi\":\"Calibri Light\"},\"basedOn\":\"Default Paragraph Font\"},{\"name\":\"Heading 4\",\"type\":\"Paragraph\",\"paragraphFormat\":{\"leftIndent\":0,\"rightIndent\":0,\"firstLineIndent\":0,\"textAlignment\":\"Left\",\"beforeSpacing\":2,\"afterSpacing\":0,\"lineSpacing\":1.0791666507720947,\"lineSpacingType\":\"Multiple\",\"outlineLevel\":\"Level4\",\"listFormat\":{}},\"characterFormat\":{\"italic\":true,\"fontFamily\":\"Calibri Light\",\"fontColor\":\"#2F5496\",\"italicBidi\":true,\"fontFamilyBidi\":\"Calibri Light\"},\"basedOn\":\"Normal\",\"link\":\"Heading 4 Char\",\"next\":\"Normal\"},{\"name\":\"Heading 4 Char\",\"type\":\"Character\",\"characterFormat\":{\"italic\":true,\"fontFamily\":\"Calibri Light\",\"fontColor\":\"#2F5496\",\"italicBidi\":true,\"fontFamilyBidi\":\"Calibri Light\"},\"basedOn\":\"Default Paragraph Font\"},{\"name\":\"Heading 5\",\"type\":\"Paragraph\",\"paragraphFormat\":{\"leftIndent\":0,\"rightIndent\":0,\"firstLineIndent\":0,\"textAlignment\":\"Left\",\"beforeSpacing\":2,\"afterSpacing\":0,\"lineSpacing\":1.0791666507720947,\"lineSpacingType\":\"Multiple\",\"outlineLevel\":\"Level5\",\"listFormat\":{}},\"characterFormat\":{\"fontFamily\":\"Calibri Light\",\"fontColor\":\"#2F5496\",\"fontFamilyBidi\":\"Calibri Light\"},\"basedOn\":\"Normal\",\"link\":\"Heading 5 Char\",\"next\":\"Normal\"},{\"name\":\"Heading 5 Char\",\"type\":\"Character\",\"characterFormat\":{\"fontFamily\":\"Calibri Light\",\"fontColor\":\"#2F5496\",\"fontFamilyBidi\":\"Calibri Light\"},\"basedOn\":\"Default Paragraph Font\"},{\"name\":\"Heading 6\",\"type\":\"Paragraph\",\"paragraphFormat\":{\"leftIndent\":0,\"rightIndent\":0,\"firstLineIndent\":0,\"textAlignment\":\"Left\",\"beforeSpacing\":2,\"afterSpacing\":0,\"lineSpacing\":1.0791666507720947,\"lineSpacingType\":\"Multiple\",\"outlineLevel\":\"Level6\",\"listFormat\":{}},\"characterFormat\":{\"fontFamily\":\"Calibri Light\",\"fontColor\":\"#1F3763\",\"fontFamilyBidi\":\"Calibri Light\"},\"basedOn\":\"Normal\",\"link\":\"Heading 6 Char\",\"next\":\"Normal\"},{\"name\":\"Heading 6 Char\",\"type\":\"Character\",\"characterFormat\":{\"fontFamily\":\"Calibri Light\",\"fontColor\":\"#1F3763\",\"fontFamilyBidi\":\"Calibri Light\"},\"basedOn\":\"Default Paragraph Font\"}],\"lists\":[],\"abstractLists\":[],\"comments\":[],\"revisions\":[],\"customXml\":[]}"))
        dataList.append(encode('--' + boundary))
        dataList.append(
            encode('Content-Disposition: form-data; name=FileName;'))

        dataList.append(encode('Content-Type: {}'.format('text/plain')))
        dataList.append(encode(''))

        dataList.append(encode("Doc555.docx"))
        dataList.append(encode('--' + boundary))
        dataList.append(encode('Content-Disposition: form-data; name=TaskId;'))

        dataList.append(encode('Content-Type: {}'.format('text/plain')))
        dataList.append(encode(''))

        dataList.append(encode("{{TaskId}}"))
        dataList.append(encode('--'+boundary+'--'))
        dataList.append(encode(''))

        body = b'\r\n'.join(dataList)
        with self.client.post('/eln-docs-mgmt-svc-nfr/v1/Document/CreateByTask', name='CreateByTask', catch_response=True,
                              headers=self.headers, data=body) as response:
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


# not needed

# conn = http.client.HTTPSConnection("cloud.msa2.apps.yokogawa.build")

# body = b'\r\n'.join(dataList)
# payload = body
# headers = {
#     'Authorization': 'Bearer eyJhbGciOiJIUzUxMiIsInR5cCI6IkpXVCJ9.eyJ1c2VySWQiOiJjYjIyMmM2MTkyY2Y0ODE0OGYwNmU4ZTY2YTcyZDY3NCIsImZpcnN0TmFtZSI6IlNocmlkaGFyYSIsImxhc3ROYW1lIjoiUmFtYXN3YW15IiwibG9jYXRpb24iOiJUZXN0IiwiZW1wbG95ZWVJZCI6IiIsImFwcGxpY2F0aW9uSWQiOiJFTE4iLCJ0ZW5hbnRJZCI6IjlhNThkZWJlLTRhYzAtNDdjMy1iMzZjLWVkYjU4MTNhYzBhYyIsInRlbmFudE5hbWUiOiJXSU5PUy1ERVYiLCJnbG9iYWxQZXJtaXNzaW9ucyI6IntcInJvbGVOYW1lXCI6XCJMYWIgTWFuYWdlclwiLFwicHJpdmlsZWdlc1wiOlt7XCJBc3NldFR5cGVcIjpcIlByb2plY3RcIixcInByaXZpbGVnZXNcIjpbXCJDcmVhdGVcIixcIlZpZXdcIixcIkVkaXRcIixcIkRlbGV0ZVwiLFwiRG93bmxvYWRcIl19LHtcIkFzc2V0VHlwZVwiOlwiVGFza1wiLFwicHJpdmlsZWdlc1wiOltcIkNyZWF0ZVwiLFwiVmlld1wiLFwiRWRpdFwiLFwiRG93bmxvYWRcIl19LHtcIkFzc2V0VHlwZVwiOlwiSW52ZW50b3J5XCIsXCJwcml2aWxlZ2VzXCI6W1wiQ3JlYXRlXCIsXCJWaWV3XCIsXCJFZGl0XCIsXCJEZWxldGVcIixcIkRvd25sb2FkXCJdfSx7XCJBc3NldFR5cGVcIjpcIkRvY3VtZW50XCIsXCJwcml2aWxlZ2VzXCI6W1wiQ3JlYXRlXCIsXCJWaWV3XCIsXCJFZGl0XCIsXCJEZWxldGVcIixcIkRvd25sb2FkXCJdfSx7XCJBc3NldFR5cGVcIjpcIlRlbXBsYXRlXCIsXCJwcml2aWxlZ2VzXCI6W1wiQ3JlYXRlXCIsXCJWaWV3XCIsXCJFZGl0XCIsXCJEZWxldGVcIixcIkRvd25sb2FkXCJdfSx7XCJBc3NldFR5cGVcIjpcIlJvbGVcIixcInByaXZpbGVnZXNcIjpbXCJDcmVhdGVcIixcIlZpZXdcIixcIkVkaXRcIixcIkRlbGV0ZVwiXX0se1wiQXNzZXRUeXBlXCI6XCJVc2VyXCIsXCJwcml2aWxlZ2VzXCI6W1wiVmlld1wiLFwiRWRpdFwiLFwiRG93bmxvYWRcIl19LHtcIkFzc2V0VHlwZVwiOlwiU2tpbGxcIixcInByaXZpbGVnZXNcIjpbXCJDcmVhdGVcIixcIlZpZXdcIixcIkVkaXRcIixcIkRlbGV0ZVwiLFwiRG93bmxvYWRcIl19LHtcIkFzc2V0VHlwZVwiOlwiQ29uZmlndXJhdGlvblwiLFwicHJpdmlsZWdlc1wiOltcIlZpZXdcIixcIkVkaXRcIl19XX0iLCJuYmYiOjE2ODY4MjA1MTYsImV4cCI6MTY4NjkwNjkxNiwiaWF0IjoxNjg2ODIwNTE2LCJpc3MiOiJodHRwczovL2Nsb3VkLm1zYTIuYXBwcy55b2tvZ2F3YS5idWlsZC8iLCJhdWQiOiJodHRwczovL2Nsb3VkLm1zYTIuYXBwcy55b2tvZ2F3YS5idWlsZC8ifQ.NPtI5xgYp5HHiRntCv8MhjRTfU2GZUPPmiu3kGhXzkRCH6mJ15pwZtmdo-LgRKvpqKVn_cI2ufTX63psHIvvtg',
#     'Content-type': 'multipart/form-data; boundary={}'.format(boundary)
# }
# conn.request(
#     "POST", "/eln-docs-mgmt-svc-nfr/v1/Document/CreateByTask", payload, headers)
# res = conn.getresponse()
# data = res.read()
# print(data.decode("utf-8"))
