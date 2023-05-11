import multiprocessing

# Функція для підрахунку кількості входжень підпослідовності subseq у послідовності seq
def count_occurrences(subseq, seq, start, end):
    count = 0
    for i in range(start, end):
        if seq[i:i+len(subseq)] == subseq:  # Якщо підпослідовність знаходиться на поточній позиції
            count += 1  
    return count  

# Функція для паралельного підрахунку кількості входжень підпослідовності subseq у послідовності seq
def parallel_count(subseq, seq, num_processes):
    seq_len = len(seq)  # Знаходимо довжину послідовності
    chunk_size = seq_len // num_processes  # Обчислюємо розмір кожної частини послідовності, яка буде оброблятись окремим процесом
    pool = multiprocessing.Pool(processes=num_processes)  # Створюємо пул процесів
    results = []  
    for i in range(num_processes):
        start = i * chunk_size  # Визначаємо початкову позицію для кожного процесу
        end = start + chunk_size  # Визначаємо кінцеву позицію для кожного процесу
        if i == num_processes - 1:  
            end = seq_len  # Закінчуємо на останній позиції послідовності
        results.append(pool.apply_async(count_occurrences, (subseq, seq, start, end)))  # Запускаємо підрахунок в окремому процесі та зберігаємо об'єкт результату
    pool.close()  # Закриваємо пул процесів
    pool.join()  # Очікуємо завершення всіх процесів
    return sum([r.get() for r in results])

if __name__ == '__main__':
    multiprocessing.freeze_support()
    seq = "ACGTTACGT" # Рядок, який містить послідовність, в якій потрібно знайти входження підпослідовності
    subseq = "AC" # Рядок, який містить підпослідовність, яку потрібно знайти у послідовності 'seq'
    num_processes = 4 # Змінна, яка містить кількість процесів, які будуть створені для обчислення
    result = parallel_count(subseq, seq, num_processes)
    print("Кількість входжень послідовності {0} у послідовність {1}: {2}".format(subseq, seq, result))