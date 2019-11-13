import dialogflow
from google.api_core.exceptions import InvalidArgument
from google.oauth2 import service_account

DIALOGFLOW_PROJECT_ID = 'test-visual-255019'
DIALOGFLOW_LANGUAGE_CODE = 'en-US'
SESSION_ID = 'current-user-id'
USE_DIALOGFLOW = False

credentials = service_account.Credentials.from_service_account_file('../credentials/dialogflow.json')

def get_type(text_to_be_analyzed):
    if not USE_DIALOGFLOW:
        return None
    try:
        session_client = dialogflow.SessionsClient(credentials=credentials)
        session = session_client.session_path(DIALOGFLOW_PROJECT_ID, SESSION_ID)
        text_input = dialogflow.types.TextInput(text=text_to_be_analyzed, language_code=DIALOGFLOW_LANGUAGE_CODE)
        query_input = dialogflow.types.QueryInput(text=text_input)
        response = session_client.detect_intent(session=session, query_input=query_input)
        return response.query_result.parameters['chart_type']
    except:
        return None
