import requests

# import firebase_admin
# from firebase_admin import credentials
# from firebase_admin import messaging

# cred = credentials.Certificate('/root/sts_crm/config/file.json')
# firebase_admin.initialize_app(cred)
# print('Successfully:', cred)
# # Create a message to send
# message = messaging.Message(
#     notification=messaging.Notification(
#         title='azamat',
#         body='This is a test notification'
#     ),
#     topic='998998260747'
# )

# # Send the message
# response = messaging.send(message)
# print('Successfully sent message:', response)

def user_notification(phone, title, body_data):
    body = {
    "notification": {"title": title, "body": body_data, "sound": True},
    "android": {"priority": "high"},
    "apns": {
    "headers": {"apns-priority": "5"}
    },

    "data": {
    "click_action": "FLUTTER_NOTIFICATION_CLICK",
    "id": "1",
    "status": "done"
    },
    "to": f"/topics/{phone}"

    }
    headers_data = {
              'Content-Type': 'application/json',
              'Authorization':'key=AAAAXB3zJOY:APA91bEQjqIL5z0pyyJJvryzlwM4rPI7fS-RYWd5JqI-2tVu8zzEOKBTS5v87qodAiqOiENKVDqz05FGHKR9bQD5I1ArCn1sZ_5WK-X248pHRSnU1FpC2xtWVxb-Z1lxzjNzzksfTDkO'

    }
    data = requests.post(url="https://fcm.googleapis.com/fcm/send/", json= body, headers=headers_data)
    print(data)

# user_notification(phone=998998260747 , title="kamera" , body_data="daat")



