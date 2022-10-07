import json

import RabbitClient as rabbit
from TopflytechCodec import *


def myconverter(o) -> str:
    if isinstance(o, datetime.datetime):
        return o.isoformat()


def sendDataToTrackin(message: Message)  -> None:
    if isinstance(message, LocationMessage):
        #Si el tiempo que viene del GPS es mayor al tiempo de ahora, no lo manda a trackin
        if message.date > datetime.datetime.now(message.date.tzinfo) + timedelta(days=5):
            return
    
    json_str = json.dumps(message.__dict__, default=myconverter)

    print(json_str)

    

    rabbit.canal.basic_publish("carmind", "trackin.data.log.decoded", json_str)
    # response = requests.post("http://trackin:4762/data", data=json_str, headers=headers)

    # print(str(message.imei) + " Respuesta Trackin: " + str(response.status_code))

