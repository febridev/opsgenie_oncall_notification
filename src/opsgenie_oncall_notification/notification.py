import os
import datetime
from json import dumps
import json
from dotenv import load_dotenv
from httplib2 import Http


def get_oncall(opsgenie_url, opsgenie_token):
    opsgenie_api = opsgenie_url
    token_api = opsgenie_token
    msg_headers = {
        "Authorization": token_api,
    }
    http_obj = Http()
    response, content = http_obj.request(opsgenie_api, "GET", headers=msg_headers)

    if response.status == 200:
        data = json.loads(content.decode("utf-8"))

        on_call_recipients = data.get("data", {}).get("onCallRecipients", [])
        return on_call_recipients

        # print("On Call Recipients:", on_call_recipients)
    else:
        return "Failed to retrieve data"


def get_userid(email):
    base_path = os.path.dirname(os.path.abspath(__file__))
    with open(f"{base_path}/gchat_userid.json", "r") as file:
        users = json.load(file)
    for user in users:
        if user["email"] == email:
            return str(user["user_id"])
    return None


def create_message(team, header_message, body_message, mention_all):
    now = datetime.datetime.now().strftime("%A")
    msg_concat = ""
    if mention_all == str.lower(now) or mention_all == "everyday":
        h_message = f"{header_message} <users/all>"
        msg_concat += h_message + body_message
    else:
        msg_concat += header_message + body_message
    return msg_concat


def main():
    load_dotenv()
    opsgenie_token = os.environ.get("TOKENOPSGENIE")
    piconcall = ""
    msg = ""
    base_path = os.path.dirname(os.path.abspath(__file__))
    with open(f"{base_path}/gchat_space.json", "r") as file:
        space_data = json.load(file)
    for lspace in space_data:
        msg = create_message(
            lspace["team"],
            lspace["header_message"],
            lspace["body_message"],
            lspace["mention_all"],
        )
        oncallname = get_oncall(lspace["opsgenie_url"], opsgenie_token)
        # CEK EMAIL TO USERID
        for iname in oncallname:
            piconcall = get_userid(iname)
            msg += f"<users/{piconcall}>\n"

        """Google Chat incoming webhook that starts or replies to a message thread."""
        url = lspace["space_url"]
        msg += lspace["footer_message"]
        app_message = {
            "text": msg
            # To start a thread, set threadKey to an arbitratry string.
            # To reply to a thread, specify that thread's threadKey value.
            # "thread": {"threadKey": "THREAD_KEY_VALUE"},
        }
        message_headers = {"Content-Type": "application/json; charset=UTF-8"}
        http_obj = Http()
        response = http_obj.request(
            uri=url,
            method="POST",
            headers=message_headers,
            body=dumps(app_message),
        )
        print(msg, lspace["team"])
