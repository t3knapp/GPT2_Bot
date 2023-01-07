import json
from datetime import date, datetime
import boto3


# Helper method to serialize datetime fields
def json_datetime_serializer(obj):
    if isinstance(obj, (datetime, date)):
        return obj.isoformat()
    raise TypeError("Type %s not serializable" % type(obj))


AWS_REGION = "us-west-1"

ssm_client = boto3.client("ssm", region_name=AWS_REGION)

get_response = ssm_client.get_parameter(Name='DISCORD_TOKEN',
                                        WithDecryption=True)

print('Parameter information:')
print(
    json.dumps(get_response['Parameter'],
               indent=4,
               default=json_datetime_serializer))