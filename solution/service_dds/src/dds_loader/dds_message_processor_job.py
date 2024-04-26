from datetime import datetime
from logging import Logger
import uuid
from lib.kafka_connect import KafkaConsumer, KafkaProducer
from dds_loader.repository import DdsRepository


class DdsMessageProcessor:
    def __init__(self,
                 consumer: KafkaConsumer,
                 producer: KafkaProducer,
                 dds_repository: DdsRepository,
                 logger: Logger) -> None:
        # Инициализация класса DdsMessageProcessor с переданными аргументами
        self.consumer = consumer
        self.producer = producer
        self.dds_repository = dds_repository
        self._logger = logger
        self._batch_size = 100

    # Функция для генерации UUID на основе переданных аргументов
    def generate_uuid(self, *args):
        return str(uuid.uuid5(uuid.NAMESPACE_DNS, "".join(map(str, args))))

    # Метод для обработки сообщений
    def run(self) -> None:
        # Логгирование начала работы метода
        self._logger.info(f"{datetime.utcnow()}: START")

        # Цикл для обработки сообщений в пределах батча
        for _ in range(self._batch_size):
            # Получение сообщения от Kafka-потребителя
            msg = self.consumer.consume()
            if not msg:
                break

            payload = msg['payload']

            # Проверка статуса заказа: если не "CLOSED", прервать цикл
            if payload['status'] != 'CLOSED':
                break

            # Получение текущей даты и источника загрузки
            load_dt = datetime.now()
            load_src = self.consumer.topic

            # Извлечение данных о заказе из сообщения
            order_id = payload['id']
            order_dt = payload['date']

            # Извлечение данных о пользователе из сообщения
            user = payload['user']
            user_id = user['id']
            username = user['name']
            userlogin = user['login']

            # Извлечение данных о ресторане из сообщения
            restaurant_id = payload['restaurant']['id']
            restaurant_name = payload['restaurant']['name']

            # Извлечение данных о стоимости заказа из сообщения
            order_cost = payload['cost']
            order_payment = payload['payment']
            order_status = payload['status']

            # Извлечение списка продуктов из сообщения
            products = payload['products']

            # Генерация UUID для уникальных идентификаторов
            h_user_pk = self.generate_uuid(user_id)
            h_restaurant_pk = self.generate_uuid(restaurant_id)
            h_order_pk = self.generate_uuid(order_id)
            hk_order_user_pk = self.generate_uuid(h_order_pk, h_user_pk)
            hk_user_names_hashdiff = self.generate_uuid(h_user_pk, username, userlogin)
            hk_restaurant_names_hashdiff = self.generate_uuid(h_restaurant_pk, restaurant_name)
            hk_order_cost_hashdiff = self.generate_uuid(h_order_pk, order_cost, order_payment)
            hk_order_status_hashdiff = self.generate_uuid(h_order_pk, order_status)

            # Вставка данных в хранилище DDS
            self.dds_repository.h_user_insert(h_user_pk, user_id, load_dt, load_src)
            self.dds_repository.h_restaurant_insert(h_restaurant_pk, restaurant_id, load_dt, load_src)
            self.dds_repository.h_order_insert(h_order_pk, order_id, load_dt, order_dt, load_src)
            self.dds_repository.l_order_user_insert(hk_order_user_pk, h_order_pk, h_user_pk, load_dt, load_src)
            self.dds_repository.s_user_names_insert(h_user_pk, username, userlogin, load_dt, load_src, hk_user_names_hashdiff)
            self.dds_repository.s_restaurant_names_insert(h_restaurant_pk, restaurant_name, load_dt, load_src, hk_restaurant_names_hashdiff)
            self.dds_repository.s_order_cost_insert(h_order_pk, order_cost, order_payment, load_dt, load_src, hk_order_cost_hashdiff)
            self.dds_repository.s_order_status_insert(h_order_pk, order_status, load_dt, load_src, hk_order_status_hashdiff)

            # Списки для данных о продуктах
            h_product_pk_list = []
            h_category_pk_list = []
            product_name_list = []
            category_name_list = []
            prod_quantity_list = []

            # Обработка каждого продукта в заказе
            for product in products:
                product_id = product['id']
                category_name = product['category']
                product_name = product['name']

                # Генерация UUID для продукта и категории
                h_product_pk = self.generate_uuid(product_id)
                h_category_pk = self.generate_uuid(category_name)

                # Генерация UUID для связей между продуктом и заказом, рестораном и категорией
                hk_order_product_pk = self.generate_uuid(h_order_pk, h_product_pk)
                hk_product_restaurant_pk = self.generate_uuid(h_product_pk, h_restaurant_pk)
                hk_product_category_pk = self.generate_uuid(h_product_pk, h_category_pk)
                hk_product_names_hashdiff = self.generate_uuid(h_product_pk, product_name)

                # Вставка данных о продукте и категории в хранилище DDS
                self.dds_repository.h_product_insert(h_product_pk, product_id, load_dt, load_src)
                self.dds_repository.h_category_insert(h_category_pk, category_name, load_dt, load_src)
                self.dds_repository.l_order_product_insert(hk_order_product_pk, h_order_pk, h_product_pk, load_dt, load_src)
                self.dds_repository.l_product_restaurant_insert(hk_product_restaurant_pk, h_product_pk, h_restaurant_pk, load_dt, load_src)
                self.dds_repository.l_product_category_insert(hk_product_category_pk, h_product_pk, h_category_pk, load_dt, load_src)
                self.dds_repository.s_product_names_insert(h_product_pk, product_name, load_dt, load_src, hk_product_names_hashdiff)

                # Добавление данных о продукте в соответствующие списки
                h_product_pk_list.append(h_product_pk)
                h_category_pk_list.append(h_category_pk)
                product_name_list.append(product_name)
                category_name_list.append(category_name)
                prod_quantity_list.append(product['quantity'])

        # Логгирование завершения работы метода
        self._logger.info(f"{datetime.utcnow()}: FINISH")
