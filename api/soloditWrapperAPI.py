from flask import Flask, request, jsonify
from flask.views import MethodView
import requests
from dotenv import load_dotenv
import os
import pathlib

app = Flask(__name__)

#TO DO add logic to handle big contents and files by ommiting them
#TO DO add logic to only give certain number of issues and not too much

# Determine the path to the directory containing the .env file
env_path = pathlib.Path('..') / '.env'  # Adjust the path according to your directory structure

# Load the .env file
load_dotenv(dotenv_path=env_path)

# Now you can access your environment variables
solodit_auth_token = os.getenv('SOLODIT_AUTH_TOKEN')

class Request:
    # Define your API base URL and authorization header
    DEFAULT_BASE_API_URL = 'https://solodit.xyz/api/'
    DEFAULT_AUTHORIZATION_HEADER = {
        'Authorization': f'Token {solodit_auth_token}' # Replace with your actual authorization token
    }
    #allowlisted enpoints
    DEFAULT_VALID_ENDPOINTS=["issues", "tags", "protocols/categories", "auditfirms"]

    def __init__(self, 
                 BaseApiUrl : str = DEFAULT_BASE_API_URL, 
                 AuthHeader : dict = DEFAULT_AUTHORIZATION_HEADER,
                 validEndpoints : list = DEFAULT_VALID_ENDPOINTS):
        self.baseApiUrl = BaseApiUrl
        self.AuthHeader = AuthHeader
        self.validEndpoints = validEndpoints

    def validEndpoint(self, endpoint):
        if(endpoint in self.validEndpoints):
            return True
        return False

    def issuesEndpoint(self, endpoint, params):
        if(endpoint == "issues"):
            # Default values for each parameter
            queryParams  = {
                "source": "",  # Empty string as default
                "impact": "HIGH,MEDIUM",  # Default value
                "finder": "",
                "protocol": "",
                "pcategories": "",
                "protocol_forked_from": "",
                "min_finders": "1",  # Default value
                "report_date": "",
                "quality_scores": "",
                "general_scores": "",
                "tags": "",
                "bookmarked": "False",  # Default value
                "markasread": "All",  # Default value
                "keyword": "",
                "page": "1"  # Default value
            }

            # Update default_params with values from params if they exist
            for key in queryParams:
                if key in params:
                    queryParams[key] = params[key]

            return "issues/rest/", queryParams
        else:
            #need to add / for solodit
            return endpoint + "/", None

    # Create a function to make authorized requests to the original API
    def make(self, endpoint, params=None):
        url = self.baseApiUrl + endpoint
        headers = self.AuthHeader
        response = requests.get(url, headers=headers, params=params)
        return response
        
    def check(self, response: requests.Response):
        try:
            response.raise_for_status()
            return {"noerror": True}
        except requests.HTTPError as http_err:
            return {"error": f"HTTP error occurred: {http_err}"}
        except requests.RequestException as req_err:
            return {"error": f"Request error occurred: {req_err}"}
        except Exception as e:
            return {"error": f"Request error occurred: {e}"}

    def extractAndFormat(self, response: requests.Response, endpoint):

        if (endpoint == "auditfirms/"):
            formattedResponse  = self.formatAuditFirms(response.json())
        elif(endpoint == "issues/rest/"):
            formattedResponse = self.formatIssues(response.json())
        else:
            return response.json()

        return formattedResponse

    def formatAuditFirms(self, response):
        # Filter out and keep only 'name' and 'has_contest' fields
        formattedData = [
            {"name": firm["name"], "has_contest": firm["has_contest"]} 
            for firm in response
        ]
        return formattedData
        
    def formatIssues(self, response):
        # Fields to remove
        fields_to_remove = [
            "bookmarked", 
            "bookmarked_total",
            "change_logs",
            "contest_link", 
            "contest_prize_txt", 
            "editor_comments",
            "finder_list",
            "general_score",
            "finders_count",
            "github_dicussion_no",
            "github_link",
            "id",
            "issue_source",
            "kind",
            "markasread",
            "openai_explained",
            "pdf_link",
            "pdf_page_from",
            "quality_score",
            "slug",
            "sponsor_name",
            "user_note"
        ]  

        formattedData = []

        for issue in response["results"]:
            # Create a copy of the firm's dictionary
            issueCopy = issue.copy()

            #remove id from issueProtocol
            issueCopy["issue_protocol"].pop("id", None)

            #if there is a resume or content too long give resume and not content
            if(issue["openai_explained"] or len(issue["content"]) > 500):
                issueCopy.pop("content", None)

            #if tags_list is empty remove
            if(len(issue["tag_list"]) == 0):
                issueCopy.pop("tag_list", None)

            #if issueProtocols category list empty remove
            if(len(issue["issue_protocol"]["category_list"]) == 0):
                issueCopy["issue_protocol"].pop("category_list", None)

            #keep only title for similar issues
            for similarIssue in issueCopy["similar_issue_list"]:
                similarIssue.pop("id", None)
                similarIssue.pop("slug", None)

            # Remove unwanted fields according to the fields_to_remove array
            for field in fields_to_remove:
                issueCopy.pop(field, None)  # Use pop to remove the field, 'None' ensures no error if the field does not exist
            formattedData.append(issueCopy)

        return formattedData

    def result(self, endpoint, params=None):
        #check if endpoint is in the allowlist
        if(not self.validEndpoint(endpoint)):
            return {"error": 
                    f"the endpoint {endpoint} is not valid here are the valid endpoints: {self.validEndpoints}"}
        #check if endpoint is /issues to make the correct request
        endpoint, params = self.issuesEndpoint(endpoint, params)
        
        response = self.make(endpoint, params)
        #check if we got other than status code 200-399
        result = self.check(response)
        if("error" in result):
            return result
        return self.extractAndFormat(response, endpoint)
    
requestInstance = Request()

class ApiWrapperView(MethodView):
    def get(self, endpoint):
        
        
        if(endpoint == "issues"):
            queryParams = request.args
        else:
            queryParams = None

        jsonResponse = requestInstance.result(endpoint, queryParams)
        # Return the simplified data as JSON
        return jsonify(jsonResponse)


apiWrapperView = ApiWrapperView.as_view('ApiWrapperView')
app.add_url_rule('/api/v1/<endpoint>/', view_func=apiWrapperView)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=False)
