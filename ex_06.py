"""
Пример ошибки "состояние гонки":

<код удалён>

Создаётся 10 потоков, каждый из которых увеличивает глобальный счетчик 100000 раз. 
Однако итоговое значение счетчика может быть неверным, почему? Объясните и напишите правильный вариант. 

Пример ошибки "deadlock":

<код удалён>

Два потока конкурируют за общие ресурсы, но в результате возникает взаимная блокировка, почему? Объясните и напишите правильный вариант.
"""
"""
I. Race conditions.
В отличие от Java (где 'race conditions' прекрасно было видно),
python оказался медленнее и не показал 'race conditions'.
Пришлось уменьшить добавить число повторов цикла и добавить задержку
между чтением counter и сохранения инкрементированного значения.
Сами race conditions возникли из-за того, что counter++ выполняется в 3 этапа
(взять текущее значение, прибавить 1, сохранить новое значение). Отстутсвие атомарности
приводит к тому, что несколько потоков одновременно берут одно и то же значение,
а также перезаписывают результат хаотично.
"""
"""
Исправление Race Conditions сделал в двух вариантах:
1) Использование threading.Lock (lock.acquire -> lock.release
      на время обновления счётчика).
2) Вместо счётчика использовать потокобезопасную очередь (queue - 
  помещать в неё что-либо, а потом считать длину).
Очередь быстрее, но требует больше памяти. 
Вариант с очередью на 40% медленнее, а вариант с lock почти в 3 раза медленнее.
"""
"""
II. Deadlock.
Добавлен timeout в 10 секунд в ожидание завершения потоков, иначе они бесконечно в Deadlock
будут находиться.
Сам Deadlock возникает из-за того, что оба потока устанавливают свою блокировку (дальнейший таймаут 50 мс
позволяет им точно успеть это сделать). А далее они оба не могут идти дальше, так как необходимая вторая
блокировка уже захвачена другим потоком.
"""
"""
Исправление Deadlock сделал в двух вариантах:
1) Одинаковый порядок "локов" в обоих потоках.
2) Сделать timeout в acquire (при втором "локе" и отрабатывать, смогли ли захватить).
Но в этом случае проблема - один из обработчиков какую-то часть обработки не делает.
"""


import queue
import time
from threading import Thread, Lock


NUMBER_OF_THREADS: int = 10
NUMBER_OF_REPETITIONS_IN_THE_LOOP: int = 100
PAUSE_BETWEEN_REPETITIONS_SECOND: float = 0.00001


class RaceConditionExample:
    counter: int = 0

    def __init__(self):
        start_time_seconds: time.datatime = time.time()

        threads: list[Thread] = [None] * NUMBER_OF_THREADS

        for i in range(NUMBER_OF_THREADS):
            threads[i] = Thread(
                target=self._increment,
                daemon = True
            )
            threads[i].start()

        for i in range(NUMBER_OF_THREADS):
            threads[i].join()

        end_time_seconds: time.datatime = time.time()

        print("1) Race conditions are present!")
        print(f"Final counter value: {self.counter}")
        print(f"There should have been {NUMBER_OF_THREADS * NUMBER_OF_REPETITIONS_IN_THE_LOOP}"
              + f" ({NUMBER_OF_THREADS} threads * {NUMBER_OF_REPETITIONS_IN_THE_LOOP} repetitions)")
        print(f"Duration of execution, seconds {end_time_seconds - start_time_seconds}")


    def _increment(self) -> None:
        for j in range(NUMBER_OF_REPETITIONS_IN_THE_LOOP):
            counter = self.counter
            time.sleep(PAUSE_BETWEEN_REPETITIONS_SECOND)
            self.counter = counter + 1


class NoRaceConditionExampleWithLock:
    counter: int = 0

    def __init__(self):
        start_time_seconds: time.datatime = time.time()

        lock = Lock()
        threads: list[Thread] = [None] * NUMBER_OF_THREADS

        for i in range(NUMBER_OF_THREADS):
            threads[i] = Thread(
                target=self._increment,
                args=(lock,),
                daemon = True
            )
            threads[i].start()

        for i in range(NUMBER_OF_THREADS):
            threads[i].join()

        end_time_seconds: time.datatime = time.time()

        print("2) No Race conditions (Lock).")
        print(f"Final counter value: {self.counter}")
        print(f"There should have been {NUMBER_OF_THREADS * NUMBER_OF_REPETITIONS_IN_THE_LOOP}"
              + f" ({NUMBER_OF_THREADS} threads * {NUMBER_OF_REPETITIONS_IN_THE_LOOP} repetitions)")
        print(f"Duration of execution, seconds {end_time_seconds - start_time_seconds}")


    def _increment(self, lock: Lock) -> None:
        for j in range(NUMBER_OF_REPETITIONS_IN_THE_LOOP):
            lock.acquire()
            counter = self.counter
            time.sleep(PAUSE_BETWEEN_REPETITIONS_SECOND)
            self.counter = counter + 1
            lock.release()


class NoRaceConditionExampleWithQueue:
    counter: queue.Queue = queue.Queue()

    def __init__(self):
        start_time_seconds: time.datatime = time.time()

        threads: list[Thread] = [None] * NUMBER_OF_THREADS

        for i in range(NUMBER_OF_THREADS):
            threads[i] = Thread(
                target=self._increment,
                daemon = True
            )
            threads[i].start()

        for i in range(NUMBER_OF_THREADS):
            threads[i].join()

        end_time_seconds: time.datatime = time.time()

        print("3) No Race conditions (Queue).")
        print(f"Final counter value: {self.counter.qsize()}")
        print(f"There should have been {NUMBER_OF_THREADS * NUMBER_OF_REPETITIONS_IN_THE_LOOP}"
              + f" ({NUMBER_OF_THREADS} threads * {NUMBER_OF_REPETITIONS_IN_THE_LOOP} repetitions)")
        print(f"Duration of execution, seconds {end_time_seconds - start_time_seconds}")


    def _increment(self) -> None:
        for j in range(NUMBER_OF_REPETITIONS_IN_THE_LOOP):
            counter = self.counter
            time.sleep(PAUSE_BETWEEN_REPETITIONS_SECOND)
            self.counter.put(1)


class DeadlockExample:
    
    lock1: Lock = Lock()
    lock2: Lock = Lock()

    def __init__(self) -> None:
        start_time_seconds: time.datatime = time.time()
        
        print("4) Deadlock!")

        thread1 = Thread(
            target=self._execute1,
            daemon = True
        )

        thread2 = Thread(
            target=self._execute2,
            daemon = True
        )

        thread1.start()
        thread2.start()

        thread1.join(timeout=5) # таймаут 5 секунд чтобы остановить зависший обработчик
        thread2.join(timeout=5) # таймаут 5 секунд чтобы остановить зависший обработчик

        end_time_seconds: time.datatime = time.time()

        print("Finished")
        print(f"Duration of execution, seconds {end_time_seconds - start_time_seconds}")


    def _execute1(self):
        with self.lock1:
            print("Thread 1 acquired lock1")
            time.sleep(0.05) # 50 мс
            with self.lock2:
                print("Thread 1 acquired lock2")
            print("Thread 1 released lock2")
        print("Thread 1 released lock1")


    def _execute2(self):
        with self.lock2:
            print("Thread 2 acquired lock2")
            time.sleep(0.05) # 50 мс
            with self.lock1:
                print("Thread 2 acquired lock1")
            print("Thread 2 released lock1")
        print("Thread 2 released lock2")


class NoDeadlockExampleSameOrderLocks:
    
    lock1: Lock = Lock()
    lock2: Lock = Lock()

    def __init__(self) -> None:
        start_time_seconds: time.datatime = time.time()
        
        print("5) No deadlock (same order locks).")

        thread1 = Thread(
            target=self._execute1,
            daemon = True
        )

        thread2 = Thread(
            target=self._execute2,
            daemon = True
        )

        thread1.start()
        thread2.start()

        thread1.join(timeout=5) # таймаут 5 секунд чтобы остановить зависший обработчик
        thread2.join(timeout=5) # таймаут 5 секунд чтобы остановить зависший обработчик

        end_time_seconds: time.datatime = time.time()

        print("Finished")
        print(f"Duration of execution, seconds {end_time_seconds - start_time_seconds}")


    def _execute1(self):
        with self.lock1:
            print("Thread 1 acquired lock1")
            time.sleep(0.05) # 50 мс
            with self.lock2:
                print("Thread 1 acquired lock2")
            print("Thread 1 released lock2")
        print("Thread 1 released lock1")


    def _execute2(self):
        with self.lock1:
            print("Thread 2 acquired lock1")
            time.sleep(0.05) # 50 мс
            with self.lock2:
                print("Thread 2 acquired lock2")
            print("Thread 2 released lock2")
        print("Thread 2 released lock1")


class NoDeadlockExampleAcquireTimeout:
    
    lock1: Lock = Lock()
    lock2: Lock = Lock()

    def __init__(self) -> None:
        start_time_seconds: time.datatime = time.time()
        
        print("6) No deadlock (acquire timeout).")

        thread1 = Thread(
            target=self._execute1,
            daemon = True
        )

        thread2 = Thread(
            target=self._execute2,
            daemon = True
        )

        thread1.start()
        thread2.start()

        thread1.join(timeout=5) # таймаут 5 секунд чтобы остановить зависший обработчик
        thread2.join(timeout=5) # таймаут 5 секунд чтобы остановить зависший обработчик

        end_time_seconds: time.datatime = time.time()

        print("Finished")
        print(f"Duration of execution, seconds {end_time_seconds - start_time_seconds}")


    def _execute1(self):
        self.lock1.acquire()
        print("Thread 1 acquired lock1")
        time.sleep(0.05) # 50 мс
        is_acquire2 = self.lock2.acquire(timeout=1) # таймаут 1 секунда чтобы отпустить lock
        if is_acquire2:
            print("Thread 1 acquired lock2")
            self.lock2.release()
            print("Thread 1 released lock2")
            self.lock1.release()
            print("Thread 1 released lock1")
            return
        print("Thread 1 failed to acquire lock2")
        self.lock1.release()
        print("Thread 1 released lock1")


    def _execute2(self):
        self.lock2.acquire()
        print("Thread 2 acquired lock2")
        time.sleep(0.05) # 50 мс
        is_acquire1 = self.lock1.acquire(timeout=1) # таймаут 1 секунда чтобы отпустить lock
        if is_acquire1:
            print("Thread 2 acquired lock1")
            self.lock1.release()
            print("Thread 2 released lock1")
            self.lock2.release()
            print("Thread 2 released lock2")
            return
        print("Thread 2 failed to acquire lock1")
        self.lock2.release()
        print("Thread 2 released lock2")


def main() -> None:
    race_condition_example = RaceConditionExample()
    # Вывело:
    # 1) Race conditions are present!
    # Final counter value: 114
    # There should have been 1000 (10 threads * 100 repetitions)
    # Duration of execution, seconds 0.10901069641113281

    no_race_condition_example_with_lock = NoRaceConditionExampleWithLock()
    # Вывело:
    # 2) No Race conditions (Lock).
    # Final counter value: 1000
    # There should have been 1000 (10 threads * 100 repetitions)
    # Duration of execution, seconds 0.28029704093933105

    no_race_condition_example_with_queue = NoRaceConditionExampleWithQueue()
    # Вывело:
    # 3) No Race conditions (Queue).
    # Final counter value: 1000
    # There should have been 1000 (10 threads * 100 repetitions)
    # Duration of execution, seconds 0.16119146347045898

    dead_lock_example = DeadlockExample()
    # Вывело:
    # 4) Deadlock!
    # Thread 1 acquired lock1
    # Thread 2 acquired lock2
    # Finished
    # Duration of execution, seconds 10.026820659637451

    no_dead_lock_example_same_order_locks = NoDeadlockExampleSameOrderLocks()
    # Вывело:
    # 5) No deadlock (same order locks).
    # Thread 1 acquired lock1
    # Thread 1 acquired lock2
    # Thread 1 released lock2
    # Thread 1 released lock1
    # Thread 2 acquired lock1
    # Thread 2 acquired lock2
    # Thread 2 released lock2
    # Thread 2 released lock1
    # Finished
    # Duration of execution, seconds 0.15439271926879883

    no_dead_lock_example_acquire_timeout = NoDeadlockExampleAcquireTimeout()
    # Вывело:
    # 6) No deadlock (acquire timeout).
    # Thread 1 acquired lock1
    # Thread 2 acquired lock2
    # Thread 1 failed to acquire lock2
    # Thread 1 released lock1
    # Thread 2 acquired lock1
    # Thread 2 released lock1
    # Thread 2 released lock2
    # Finished


if __name__ == "__main__":
    main()
