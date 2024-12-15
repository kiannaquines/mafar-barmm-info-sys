from android_sms_gateway import client, domain
import time
from core.settings import (
    SERVER_SMS_IP,
    SERVER_SMS_PORT,
    SERVER_SMS_PASSWORD,
    SERVER_SMS_USERNAME,
)

def send_sms(api_client, message):
    try:
        state = api_client.send(message)
        time.sleep(5)
        state = api_client.get_state(state.id)        
        return {"status": "success", "message": 'You have successfully approved beneficiary, and client has been successfully notified.'}
    except Exception as e:
        return {"status": "danger", "message": "There was an error while sending a notification to client, please check your SMS API server.", "error": str(e)}

def sms_send(ip, port, username, password, message):
    base_url = f"http://{ip}:{port}"
    try:
        with client.APIClient(username, password, base_url=base_url) as api_client:
            return send_sms(api_client, message)
    except Exception as e:
        return {"status": "danger", "message": "API Gateway is not running, or incorrect credentials.", "error": str(e)}

def send_sms_api_interface(message, mobile):
    mobile = [mobile]
    message = domain.Message(message, mobile)
    return sms_send(
        SERVER_SMS_IP,
        SERVER_SMS_PORT,
        SERVER_SMS_USERNAME,
        SERVER_SMS_PASSWORD,
        message,
    )