# Install boto3
'''
	pip install boto3
'''

# Import req. libraries
import json
import boto3
import random
import datetime

from datetime import datetime, timedelta

# Set variable for kinesis stream name
DataStreamName = "late-data-1"

# Create a kinesis client
client = boto3.client('kinesis')

# Send on time data
MessageTimeStamp = datetime.now()
print(str(MessageTimeStamp)[0:19])

# Send late data
#MessageTimeStamp = datetime.now() - timedelta(hours=0, seconds=60)
#print("Late message time = " + str(MessageTimeStamp)[0:19] + " | Time now = " + str(datetime.now())[0:19])

# Create event message
MessageJSON = {
	"event_timestamp": str(MessageTimeStamp),
	"value1" : 1
}

# Send message to Kinesis DataStream
response = client.put_record(
	StreamName = DataStreamName,
	Data = json.dumps(MessageJSON),
	PartitionKey = str(hash(random.randint(0,2)))
)

# If the message was not sucssfully sent print an error message
if response['ResponseMetadata']['HTTPStatusCode'] != 200:
	print('Error!')
	print(response)