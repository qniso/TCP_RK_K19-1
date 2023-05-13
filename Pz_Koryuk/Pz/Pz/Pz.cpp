#include <iostream>
#include <vector>
#include <cmath>
#include <omp.h>

using namespace std;
// Функція решета Ератосфена
void sieve_of_eratosthenes(int n, int num_threads) { 
    // Створюємо вектор булевих значень розміру n + 1
    vector<bool> primes(n + 1, true); 
    // Розпочинаємо паралельний блок коду
#pragma omp parallel num_threads(num_threads) 
    {
        // Отримуємо номер потоку
        int tid = omp_get_thread_num(); 
        // Розраховуємо розмір блоку чисел, які оброблює кожен потік
        int chunk_size = n / omp_get_num_threads() + 1;
        // Розраховуємо початкове та кінцеве значення для обробки поточним потоком
        int start = tid * chunk_size + 2; 
        int end = min(start + chunk_size - 1, n);
        // Обчислюємо прості числа від 2 до sqrt(n)
        for (int i = 2; i <= sqrt(n); i++) {  
            // Якщо поточне число є простим, то відзначаємо всі його кратні як непрості
            if (primes[i]) {
#pragma omp for schedule(static, chunk_size)
                for (int j = i * i; j <= n; j += i) {
                    primes[j] = false;
                }
            }
        }
        // Виводимо прості числа, які були знайдені поточним потоком
#pragma omp for schedule(static, chunk_size)
        for (int i = start; i <= end; i++) {
            if (primes[i]) {
                // Критична секція для синхронізації виводу
#pragma omp critical
                {
                    cout << i << " ";
                }
            }
        }
    }
    cout << endl;
}

int main() {
    setlocale(LC_ALL, "Russian");
    int n = 100;
    int num_threads_values[] = { 1, 2, 4, 6, 8, 10, 20 };
    // Виконуємо решето Ератосфена для кожної кількості потоків
    for (int i = 0; i < sizeof(num_threads_values) / sizeof(int); i++) {
        int num_threads = num_threads_values[i];
        double start_time = omp_get_wtime();
        sieve_of_eratosthenes(n, num_threads);
        double end_time = omp_get_wtime();
        double time_taken = end_time - start_time;
        cout << "Час, витрачений на " << num_threads << " потiк: " << time_taken << " секунд" << endl;
    }
    return 0;
}