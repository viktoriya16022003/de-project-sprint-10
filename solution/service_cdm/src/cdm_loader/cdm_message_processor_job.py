from datetime import datetime 
from logging import Logger  
from uuid import UUID 

from lib.kafka_connect import KafkaConsumer  # Импорт класса KafkaConsumer из модуля lib.kafka_connect
from cdm_loader.repository import CdmRepository  # Импорт класса CdmRepository из модуля cdm_loader.repository


class CdmMessageProcessor:
    def __init__(self,
                 consumer: KafkaConsumer,
                 cdm_repository: CdmRepository,
                 logger: Logger,
                 ) -> None:
        # Инициализация класса CdmMessageProcessor с переданными аргументами
        self._consumer = consumer  # Инициализация KafkaConsumer для получения сообщений
        self._cdm_repository = cdm_repository  # Инициализация CdmRepository для взаимодействия с хранилищем данных CDM
        self._logger = logger  # Инициализация Logger для логгирования событий
        self._batch_size = 100  # Размер пакета для обработки сообщений

    def run(self) -> None:
        # Логгирование начала работы метода
        self._logger.info(f"{datetime.utcnow()}: START")

        # Цикл для обработки сообщений в пределах батча
        for _ in range(self._batch_size):
            msg = self._consumer.consume()  # Получение сообщения от Kafka-потребителя
            if not msg:
                break

            user_id = msg['user_id']  # Извлечение идентификатора пользователя из сообщения
            products_info = list(zip(
                msg['product_id'], 
                msg['product_name'], 
                msg['category_id'], 
                msg['category_name'], 
                msg['order_cnt']
            ))  # Извлечение информации о продуктах из сообщения и формирование списка кортежей

            # Обработка информации о продуктах
            for product in products_info:
                # Вставка данных о продуктах пользователя в хранилище данных CDM
                self._cdm_repository.user_product_counters_insert(user_id, product[0], product[1], product[4])
                # Вставка данных о категориях продуктов пользователя в хранилище данных CDM
                self._cdm_repository.user_category_counters_insert(user_id, product[2], product[3])

        # Логгирование завершения работы метода
        self._logger.info(f"{datetime.utcnow()}: FINISH")
