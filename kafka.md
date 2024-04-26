# ##Удалите старые настройки
curl -X POST https://order-gen-service.sprint9.tgcloudenv.ru/delete_kafka \
-H 'Content-Type: application/json; charset=utf-8' \
--data-binary @- << EOF
{
    "student": "viktoriya16022003"
}
EOF
### Новый топик
curl -X POST https://order-gen-service.sprint9.tgcloudenv.ru/register_kafka \
-H 'Content-Type: application/json; charset=utf-8' \
--data-binary @- << EOF
{
    "student": "viktoriya16022003",
    "kafka_connect":{
        "host": "rc1b-a80ute8jsvg0ve2t.mdb.yandexcloud.net",
        "port": 9091,
        "topic": "reg_kafka",
        "producer_name": "producer_consumer",
        "producer_password": "producer_consumer"
    }
}
EOF

cd /Users/viktoriaserebrakova/Desktop/de-project-sprint-9/solution/docker-compose.yaml
docker compose up -d --build