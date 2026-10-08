from __future__ import annotations

import datetime
import multiprocessing
import random
import threading
import time


# -======================================================-
# Пример 1 - семафоры.
# -======================================================-
# Ограничение одновременного подключения к базе данных 
# 3-мя потоками.
# -======================================================-

MAX_SIMULTANEOUS_CONNECTIONS_TO_DB = 3
NUMBER_OF_THREADS = 10


class Connection:

    def __init__(self, pool: ConnectionPool, connection_id: int) -> None:
        self._pool = pool
        self._connection_id = connection_id

    def __enter__(self) -> Self:
        return self

    def __exit__(self, exc_type, exc, tb) -> None:
        self._pool.release_connection(self._connection_id)
        if exc_type:
            print(f"Исключение: {exc_type}")
        return False

    def execute_sql(self, sql_query: str) -> None:
        print(f"Executing SQL: {sql_query}...")
        time_for_executing_sql = random.uniform(0.2, 2.0)
        time.sleep(time_for_executing_sql) # Иммитация 
        print(f"... Ready in {time_for_executing_sql} sec SQL: {sql_query}")



class ConnectionPool:

    def __init__(self, max_simultaneous_connections_to_db: int) -> None:
        self._semaphore = threading.Semaphore(max_simultaneous_connections_to_db)
        self._number_of_connections = 0 # Текущее число соединений к базе
        self._lock = threading.Lock() # для корректной работы счётчика

    def get_connection(self, connection_id: int) -> Connection:
        self._semaphore.acquire()
        with self._lock:
            self._number_of_connections += 1
            print(f"[{self._number_of_connections}/{MAX_SIMULTANEOUS_CONNECTIONS_TO_DB}]"
                  + f"Start connection number {connection_id}"
            )
        return Connection(self, connection_id)

    def release_connection(self, connection_id: int) -> None:
        with self._lock:
            self._number_of_connections -= 1
            print(f"[{self._number_of_connections}/{MAX_SIMULTANEOUS_CONNECTIONS_TO_DB}]"
                  + f"Stop connection number {connection_id}"
            )
        self._semaphore.release()


def start_connection(pool: ConnectionPool, connection_id: int) -> None:
    connection = pool.get_connection(connection_id)
    with connection:
        connection.execute_sql(f"SELECT * FROM TABLE WHERE ID = {connection_id}")


def example_1() -> None:
    pool = ConnectionPool(MAX_SIMULTANEOUS_CONNECTIONS_TO_DB)
    threads = [threading.Thread(target=start_connection, args=(pool, id,), daemon=True) for id in range(NUMBER_OF_THREADS)]
    for id in range(NUMBER_OF_THREADS):
        threads[id].start()
    for id in range(NUMBER_OF_THREADS):
        threads[id].join()


# -======================================================-
# Пример 2 - барьер.
# -======================================================-
# В определенной точке программы потоки "ждут" другие потоки:
# продвижение дальше только когда "соберутся все".
# -======================================================-

NUMBER_OF_THREADS = 3

def worker(barrier: threading.Barrier) -> None:
    thread_name = threading.current_thread().name
    print(f"Поток {thread_name} запущен в {datetime.datetime.now().strftime("%H:%M:%S.%f")}")
    print(f"Без текущего потока перед барьером {barrier.n_waiting} из {NUMBER_OF_THREADS} потоков")
    barrier.wait()
    print(f"Поток {thread_name} прошёл барьер в {datetime.datetime.now().strftime("%H:%M:%S.%f")}")


def example_2() -> None:
    barrier = threading.Barrier(NUMBER_OF_THREADS)
    for threads_id in range(NUMBER_OF_THREADS):
        thread = threading.Thread(
            name = f"thread N{threads_id}",
            target=worker,
            args = (barrier,)
        )
        thread.start()
        time.sleep(0.5) # Запускаем потоки с интервалом в 0,5 секунды

    for threads_id in range(NUMBER_OF_THREADS):
        thread.join()


# -======================================================-
# Пример 3 - события.
# -======================================================-
# Consumer ожидает событие от Producer и 
# только тогда продолжает работу.
# -======================================================-

def producer(event: threading.Event) -> None:
    print(f"Producer start at {datetime.datetime.now().strftime("%H:%M:%S.%f")}")
    time.sleep(3) # Имитация работы Продюсера
    print(f"Producer end at {datetime.datetime.now().strftime("%H:%M:%S.%f")}")
    event.set()

def consumer(event: threading.Event) -> None:
    print(f"Consumer start at {datetime.datetime.now().strftime("%H:%M:%S.%f")}")
    event.wait()
    print(f"Consumer end at {datetime.datetime.now().strftime("%H:%M:%S.%f")}")

def example_3() -> None:
    event = threading.Event()
    thread_producer = threading.Thread(target=producer, args=(event,))
    thread_consumer = threading.Thread(target=consumer, args=(event,))
    thread_producer.start()
    thread_consumer.start()

    thread_producer.join()
    thread_consumer.join()


# -======================================================-
# Пример 4 - использование reentrant lock (блокировки с повторной входимостью)
# -======================================================-
# Обычный lock при рекурсивном вызове сделает deadlock,
# поэтому для рекурсивного вызова нужен reentrant lock.
# -======================================================-

NUMBER_OF_THREADS = 10

counter: int = 0

def process(rlock, depth=0) -> None:
    global counter
    rlock.acquire()
    print(f"Depth = {depth}, counter = {counter}")
    counter += 1
    time.sleep(0.05)
    if depth < 10:
        process(rlock, depth + 1)
    rlock.release()

def example_4() -> None:
    rlock: threading.RLock = threading.RLock()
    threads = []
    
    for thread_id in range(NUMBER_OF_THREADS):
        threads.append(threading.Thread(
            target=process,
            args=(rlock, 0,),
            daemon=True
        ))
        threads[thread_id].start()

    for thread_id in range(NUMBER_OF_THREADS):
        threads[thread_id].join()

    print(f"Final counter = {counter}")
    

# -======================================================-
# Пример 5 - атомарные значения
# -======================================================-
# В python есть встроенно только для процессов, для потоков
# есть отдельная библиотека.
# -======================================================-

NUMBER_OF_THREADS = 10

def increment(shared_value: multiprocessing.Value) -> None:
    for _ in range(10000):
        with shared_value.get_lock():
            shared_value.value += 1

def example_5() -> None:
    counter: multiprocessing.Value = multiprocessing.Value('i', 0)
    processes: list[multiprocessing.Process] = [multiprocessing.Process(target=increment, args=(counter,)) for _ in range(NUMBER_OF_THREADS)]

    for p in processes:
        p.start()

    for p in processes:
        p.join()

    print(f"Counter = {counter.value}") # Counter = 100000


def main():
    print("-======================================================-")
    print("Пример 1 - семафоры.")
    print("-======================================================-")
    example_1()
    print("-======================================================-")
    print("-======================================================-")
    print("Пример 2 - барьеры.")
    print("-======================================================-")
    example_2()
    print("-======================================================-")
    print("-======================================================-")
    print("Пример 3 - события.")
    print("-======================================================-")
    example_3()
    print("-======================================================-")
    print("-======================================================-")
    print("Пример 4 - reentrant lock.")
    print("-======================================================-")
    example_4()
    print("-======================================================-")
    print("-======================================================-")
    print("Пример 5 - атомарные значения.")
    print("-======================================================-")
    example_5()
    print("-======================================================-")

if __name__ == "__main__":
    main()
