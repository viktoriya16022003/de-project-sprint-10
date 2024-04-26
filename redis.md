### Как обновить данные в Redis
### Для загрузки пользователей выполните команду

curl -X POST https://redis-data-service.sprint9.tgcloudenv.ru/load_users \
-H 'Content-Type: application/json; charset=utf-8' \
--data-binary @- << EOF
{
    "redis":{
        "host": "rc1d-0j2ldnv97cvvb9pu.mdb.yandexcloud.net",
        "port": 6380,
        "password": "vika2003!"
    }
}
EOF
### Для загрузки ресторанов выполните команду:
curl -X POST https://redis-data-service.sprint9.tgcloudenv.ru/load_restaurants \
-H 'Content-Type: application/json; charset=utf-8' \
--data-binary @- << EOF
{
    "redis":{
        "host": "rc1d-0j2ldnv97cvvb9pu.mdb.yandexcloud.net",
        "port": 6380,
        "password": "vika2003!"
    }
}
EOF