from datetime import datetime, timedelta
import time
import uuid
from concurrent.futures import ThreadPoolExecutor
import threading
import random


class OrdersManager:
    __orders = []
    __orders_processed = 0
    __last_printed_log = datetime.now()
    __db = {}

    def __init__(self) -> None:
        self.__generate_fake_orders(quantity=1_000)


    def __generate_fake_orders(self, quantity):
        self.__log(f"Generating fake orders")
        self.__orders = [(uuid.uuid4(), x) for x in range(quantity)]
        self.__log(f"{len(self.__orders)} generated...")

    def __log(self, message):
        print(f"{datetime.now()} > {message}")

    def __fake_save_on_db(self, order):
        for id, number in order:
            self.__db[id] = number
            self.__log(
            message=f"Order [{id}] {number} was successfully prosecuted."
            )
            self.__orders_processed += 1
        time.sleep(random.uniform(0, 1))



    def process_orders(self):
        with ThreadPoolExecutor(max_workers=10) as executor:
            executor.submit(self.__fake_save_on_db(self.__orders))

            if datetime.now() > self.__last_printed_log:
                self.__last_printed_log = datetime.now() + timedelta(seconds=5)
                self.__log(
                    message=f"Total orders executed: {self.__orders_processed}/{len(self.__orders)}"
                )


if __name__ == '__main__':
    orders_manager = OrdersManager()

    start_time = time.time()
    orders_manager.process_orders()
    delay = time.time() - start_time

    print(f"{datetime.now()} > Tiempo de ejecucion: {delay} segundos...")