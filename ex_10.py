from concurrent.futures import ThreadPoolExecutor
from typing import Final
import random
import threading
import time


def complex_multi_thread_processing() -> None:
    """
    Повтор исходного примера только на Python.
    Добавлен замер скорости выполнения.
    """      

    SIZE: Final[int] = 1_000_000
    THREADS: Final[int] = 4
    data: list[int] = []
    sum = 0

    lock = threading.Lock()
    random.seed(42) # Используется для повторяемости результатов исходной и упрощенной функции.

    def handler(start: int, end: int) -> None:
        nonlocal sum
        local_sum: int = 0
        for j in range(start, end):
            local_sum += data[j]
        with lock:
            sum += local_sum

    for _ in range(SIZE):
        data.append(random.randint(0, 100))

    start_time = time.perf_counter()

    threads: list[threading.Thread] = []
    chunk_size: int = SIZE // THREADS # Допускаем, что всегда будет делиться нацело.

    start: int
    end: int
    for i in range(THREADS):
        start = i * chunk_size
        end = (i + 1) * chunk_size
        threads.append(threading.Thread(target=handler, args=(start, end,), daemon=True))
        threads[i].start()

    for i in range(THREADS):
        threads[i].join()

    end_time = time.perf_counter()

    print(f"Sum of all elements (in {end_time - start_time:.6f} seconds): {sum}")


def simple_multi_thread_processing() -> None:
    """
    Упрощение исходного примера.
    """

    SIZE: Final[int] = 1_000_000
    THREADS: Final[int] = 4

    # Используется для повторяемости результатов исходной и упрощенной функции.
    random.seed(42) 
    # Списковое включение нагляднее простого цикла.
    data: list[int] = [random.randint(0, 100) for _ in range(SIZE)]

    # Переменная переименована, чтобы не было смешения с функцией sum.
    result_sum = 0

    start_time = time.perf_counter()

    chunk_size: int = SIZE // THREADS
    # Разбиваем весь список на части. Каждый поток будет работать со своей частью.
    # Минус - дополнительная память, плюс - у всех обработчиков независимые части.
    # Дополнительный плюс - теперь не важно - разделится ли SIZE на THREADS
    # нацело. В исходном примере остаток массива не обрабатывался,
    # здесь будет дополнительная часть, которая нормально обработается.
    chunks = [data[i:i + chunk_size] for i in range(0, SIZE, chunk_size)]

    # Во "внутренней sum" при параллельном вычислении проблем не будет, так как
    # части списка независимы и никакие переменные не используются.
    # Во "внешней sum" эффекта гонки также не будет,
    # так как pool.map - это итератор и sum уже в основном цикле просто
    # суммирует результаты всех потоков.
    with ThreadPoolExecutor(THREADS) as pool:
        result_sum = sum(pool.map(sum, chunks))

    end_time = time.perf_counter()

    print(f"Sum of all elements (in {end_time - start_time:.6f} seconds): {result_sum}")


def main():
    print("Пример с java переписан на python с минимальными изменениями.")
    complex_multi_thread_processing()
    # Вывело: "Sum of all elements (in 0.343691 seconds): 49995219"

    print("Существенно упрощенный вариант кода (и быстрее почти на порядок).")
    simple_multi_thread_processing()
    # Вывело: "Sum of all elements (in 0.037313 seconds): 49995219"


if __name__ == "__main__":
    main()
