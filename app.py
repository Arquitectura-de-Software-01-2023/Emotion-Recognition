import boto3
import os
import json
import uuid
# Libraries for emotion recognition
import cv2
import tensorflow.lite as lite
import numpy as np
import sys
import urllib3

# DynamoDB
dynamodb = boto3.resource('dynamodb')
table_name = os.environ['TABLE_NAME']

# Emotion Recognition
my_path = './ai'
interpreter = lite.Interpreter(model_path=my_path+'/model.tflite')
interpreter.allocate_tensors()
# Get input and output details
input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()
# Load the haar cascade classifier
haar_cascade_face = cv2.CascadeClassifier(my_path + '/haarcascade_frontalface_default.xml')


def handler(event, context):
    print('event=', event)
    print('body=', event['body'])
    print('If you reached here, overwriting the function did not work')
    return {
        'statusCode': 200,
        'headers': {
            'Content-Type': 'application/json'
        },
        'body': json.dumps({
            'message': 'If you reached here, overwriting the function did not work',
        })
    }


def emotion_recognition_handler(event, context):
    try:
        print('Begining emotion recognition')

        body = json.loads(event['body'])
        print('body: ' + str(body))

        image_url = body['image_url']
        print('image_url: ' + image_url)

        if image_url == None:
            return {
                'statusCode': 400,
                'headers': {
                    'Content-Type': 'application/json'
                },
                'body': json.dumps({
                    'data': None,
                    'message': 'Image URL is required',
                    'successful': False
                })
            }

        emotion = ''

        http = urllib3.PoolManager()
        print('Begining HTTP GET request')
        response = http.request("GET", image_url)
        print('Ending HTTP GET request')
        # Read the downloaded image data using cv2.imread
        image_data = np.asarray(bytearray(response.data), dtype="uint8")
        image = cv2.imdecode(image_data, cv2.IMREAD_COLOR)
        # Predict the emotion
        emotion = emotion_recognition(image)
        print('emotion: ' + emotion)

        if emotion == 'No face detected':
            return {
                'statusCode': 400,
                'headers': {
                    'Content-Type': 'application/json'
                },
                'body': json.dumps({
                    'data': None,
                    'message': 'No face detected',
                    'successful': False
                })
            }

        emotion_id = uuid.uuid4()
        print('emotion_id: ' + str(emotion_id))

        table = dynamodb.Table(table_name)
        print('Begining DynamoDB put_item')
        table.put_item(Item={'id': str(emotion_id), 'image_url': image_url, 'emotion': emotion})
        print('Ending DynamoDB put_item')

        return {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'application/json'
            },
            'body': json.dumps({
                'data': {
                    'image_url': image_url,
                    'emotion': emotion
                },
                'message': 'Successfully added emotion to database',
                'successful': True
            })
        }

    except Exception as e:
        return {
            'statusCode': 500,
            'headers': {
                'Content-Type': 'application/json'
            },
            'body': json.dumps({
                'data': None,
                'message': 'Failed to add emotion to database, error: ' + str(e),
                'successful': False
            })
        }


def image_processing(img):
    print('Begining image processing')
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    img = cv2.resize(img, (48, 48))
    img = img.reshape(-1, 48, 48, 1)
    img = img.astype('float32')
    img /= 255
    print('Ending image processing')
    return img


def emotion_recognition(img):
    print('Begining emotion recognition')
    faces_rects = haar_cascade_face.detectMultiScale(img, scaleFactor=1.2, minNeighbors=5)
    # Draw a rectangle around the faces
    if len(faces_rects) > 0:
        max_area = 0
        for face in faces_rects:
            x, y, w, h = face
            area = w*h
            if area > max_area:
                max_area = area
                face_x, face_y, face_w, face_h = x, y, w, h
        # Get the face data
        face_img = img[face_y:face_y+face_h, face_x:face_x+face_w]
        img = image_processing(face_img)
        # Predict the emotion
        interpreter.set_tensor(input_details[0]['index'], img)
        interpreter.invoke()
        output_data = interpreter.get_tensor(
            output_details[0]['index'])
        # Get the label of the prediction
        with open(my_path+'/labels.txt', 'r') as f:
            labels = [line.strip() for line in f.readlines()]
        prediction = np.argmax(output_data)
        return labels[prediction]
    else:
        return 'No face detected'
