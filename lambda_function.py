import os
from email.message import EmailMessage

import boto3
import email
from botocore.exceptions import ClientError
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email import policy
from email_template import EMAIL_BODY_HEADER

region = os.environ['Region']


def generate_sender_address(from_addresses, sender_suffix):
    split_arr = from_addresses.split()
    from_email = split_arr.pop()
    from_name = None
    if len(split_arr) > 0:
        from_name = " ".join(split_arr)
    from_email = from_email.replace('@', '_at_')
    from_email = from_email.replace('.', '_dot_')
    from_email = from_email.replace('+', '_plus_')
    from_email = from_email + '_' + sender_suffix
    if from_name:
        return from_name + ' <' + from_email + '>'
    else:
        return from_email


def get_message_from_s3(message_id):
    incoming_email_bucket = os.environ['MailS3Bucket']
    incoming_email_prefix = os.environ['MailS3Prefix']

    if incoming_email_prefix:
        object_path = (incoming_email_prefix + "/" + message_id)
    else:
        object_path = message_id

    object_http_path = (
        f"http://s3.console.aws.amazon.com/s3/object/{incoming_email_bucket}/{object_path}?region={region}")

    client_s3 = boto3.client("s3")
    object_s3 = client_s3.get_object(Bucket=incoming_email_bucket,
                                     Key=object_path)
    file = object_s3['Body'].read()

    file_dict = {
        "file": file,
        "path": object_http_path
    }

    return file_dict


def create_message(file_dict):
    separator = ";"
    mail_object = email.message_from_string(file_dict['file'].decode('utf-8'), policy=policy.default)

    from_list = separator.join(mail_object.get_all('From'))
    from_list = from_list.replace('<', '')
    from_list = from_list.replace('>', '')
    to_address = separator.join(mail_object.get_all('To'))
    to_address = to_address.replace('<', '')
    to_address = to_address.replace('>', '')
    msg = MIMEMultipart()
    header_html = EMAIL_BODY_HEADER.format(email_from=from_list,
                                           email_to=to_address,
                                           email_archive_url=file_dict['path'])
    header_part = MIMEText(header_html, _subtype="html")
    msg.attach(header_part)

    message_body = mail_object.get_body()
    msg.attach(message_body)

    for payload in mail_object.get_payload():
        if isinstance(payload, EmailMessage) and payload.is_attachment():
            msg.attach(payload)

    subject = mail_object['Subject']
    recipient = os.environ['MailRecipient']
    sender = generate_sender_address(from_list, to_address.replace(' ', '_'))
    # Add subject, from and to lines.
    msg['Subject'] = subject
    msg['From'] = sender
    msg['To'] = recipient

    message = {
        "Source": sender,
        "Destinations": recipient,
        "Data": msg.as_string()
    }

    return message


def send_email(message):
    client_ses = boto3.client('ses', region)
    try:
        response = client_ses.send_raw_email(
            Source=message['Source'],
            Destinations=[
                message['Destinations']
            ],
            RawMessage={
                'Data': message['Data']
            }
        )

    except ClientError as e:
        output = e.response['Error']['Message']
    else:
        output = "Email sent! Message ID: " + response['MessageId']

    return output


def lambda_handler(event, context):
    message_id = event['Records'][0]['ses']['mail']['messageId']
    print(f"Received message ID {message_id}")

    file_dict = get_message_from_s3(message_id)

    message = create_message(file_dict)

    result = send_email(message)
    print(result)
