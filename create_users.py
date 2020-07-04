
import csv
import random
import string
from password_generator import PasswordGenerator

participants = []
email = []

import boto3
iam = boto3.client("iam")
pwo = PasswordGenerator()

def randomStringwithDigitsAndSymbols(stringLength=10):
    password_characters = string.ascii_letters + string.digits + string.punctuation
    return "".join(random.choice(password_characters) for i in range(stringLength))
	
with open("users.csv", "rt") as f:
    data = csv.reader(f, delimiter=";")
    next(data)
    for row in data:
        participants.append(row[0])

with open('user_details.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    for username in participants:
        print(username)
        password = pwo.generate()
        print(password)
        createuserResponse = iam.create_user(UserName=username)
        createLoginProfileResponse = iam.create_login_profile(
          Password=password, PasswordResetRequired=False, UserName=username
        )
        createAccesskeyResponse = iam.create_access_key(UserName=username)
        addUserToGroupResponse =iam.add_user_to_group(
          GroupName="devops", UserName=username
        )
        accessKeyId = createAccesskeyResponse['AccessKey']['AccessKeyId']
        print(accessKeyId)
        secretAccessKey = createAccesskeyResponse['AccessKey']['SecretAccessKey']
        print(secretAccessKey)
        writer.writerow([username, password, accessKeyId, secretAccessKey])

# with open('user_details.csv', 'w', newline='') as file:
#     writer = csv.writer(file)
#         writer.writerow([username, password, accessKeyId, secretAccessKey])
