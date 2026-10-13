import time
from threading import Thread, Lock


def thread_example() -> None:
    """
    Исходный вариант, в котором может пристуствовать эффект гонки.
    """
    
    counter: int = 0

    def task() -> None:
        """
        Добавлена локальная переменная и задержка времени
        чтобы продемонстрировать эффект гонки (без этого эффект не
        виден, но это только сейчас так на данном компьютере и при его данной загрузке)
        """
        nonlocal counter
        for i in range(1000):
            local_counter = counter
            time.sleep(0.00001)
            counter = local_counter + 1

    thread1: Thread =  Thread(target=task, daemon=True)
    thread2: Thread =  Thread(target=task, daemon=True)

    thread1.start()
    thread2.start()

    thread1.join()
    thread2.join()

    print(f"Counter: {counter}")


def thread_example_fixed() -> None:
    """
    Исправленный вариант - эффект гонки ликвидирован, так как добавили Lock 
    на время инкрементирования счётчика.
    Как вариант, можно использовать ещё потокобезопасную очередь (queue.Queue)
    или счётчик itertools.count - он также потокобезопасен.
    """
    
    counter: int = 0
    lock: Lock = Lock()

    def task() -> None:
        """
        Оставлена локальная переменная и задержка времени,
        тем не менее эффекта гонки нет.
        """
        nonlocal counter
        for i in range(1000):
            with lock:
                local_counter = counter
                time.sleep(0.00001)
                counter = local_counter + 1

    thread1: Thread =  Thread(target=task, daemon=True)
    thread2: Thread =  Thread(target=task, daemon=True)

    thread1.start()
    thread2.start()

    thread1.join()
    thread2.join()

    print(f"Counter: {counter}")


def main():

    thread_example()
    # Выведет "Counter: 1004" (или другую цифру от 1000 до 2000 включительно).

    thread_example_fixed()
    # Выведет "Counter: 2000".


if __name__ == "__main__":
    main()
