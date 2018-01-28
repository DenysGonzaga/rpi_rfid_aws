import boto3
import json
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)

sh = logging.StreamHandler()
sh.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - line %(lineno)s - function %(funcName)s - '
                                  '%(message)s'))

logger.addHandler(sh)


def get_table_value(rfid_value):
    try:
        client = boto3.client('dynamodb')
        response = client.get_item(TableName='tbl-rfid', Key={'id': {'S': rfid_value}})['Item']

        return 1 if len(response) > 0 else 0
    except KeyError:
        logger.info("RFID code %s not found." % rfid_value)
        return 0


def pub_iot(topic, data):
    try:
        client = boto3.client('iot-data', region_name='us-west-2')
        client.publish(
            topic=topic,
            qos=1,
            payload=json.dumps(data)
        )
    except Exception as e:
        logger.error("Erro on IOT MQTT message publishing on topic %s." % topic)
        logger.error(str(e))
        exit(-1)


def lambda_handler(event, context):
    rfid = str(event)
    is_registered = bool(get_table_value(rfid))
    pub_iot('rfid-out', {"is_registered": is_registered})
    logger.info("Process executed successfully.")