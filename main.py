def test_func(data):
    start = data[0]
    end = data[1]
    liczby = [
        15972490,
        80247910,
        92031257,
        75940266,
        97986012,
        87599664,
        75231321,
        11138524,
        68870499,
        11872796,
        79132533,
        40649382,
        63886074,
        53146293,
        36914087,
        62770938,
    ]

    res = []
    for liczba in liczby[start:end]:
        wynik = 0
        for i in range(1, liczba+1):
            wynik += (liczba-i)*i
        res.append(wynik)
    return res


def test_func_threads(four_threads=False):
    num_of_threads = 4 if four_threads else 1
    result = []
    step = 16 // num_of_threads
    start = 0
    end = 17
    data = []
    for i in range(num_of_threads):
        data.append([start, min(end, start + step)])
        start += step
    with ThreadPoolExecutor(max_workers=num_of_threads) as executor:
        result += executor.map(test_func, data)
    return result


def test_func_processes(optimal=False):
    max_p = multiprocessing.cpu_count() if optimal else 4
    step = 16//max_p
    start = 0
    end = 17
    result = []
    data = []
    for i in range(max_p):
        data.append([start, min(end, start + step)])
        start += step
    with ProcessPoolExecutor(max_workers=max_p) as pool:
        result += pool.map(test_func, data)
    return result


def generate_report_file(single, four, four_proc, optimal_proc):
    with open('report.html', 'w') as file:
        file.write(('<h1>Multithreading/Multiprocessing benchmark results</h1>'
                    '<h2>Execution environment</h2>'
                    'Python version: {}<br>'
                    'Interpreter: {}<br>'
                    'Interpreter version: {}<br>'
                    'Operating system: Windows: {}<br>'
                    'Operating system version: {}<br>'
                    'Processor: {}<br>'
                    'CPUs: {}<br>').format(python_version(), python_implementation(), version,
                                           system(), release(), processor(), cpu_count()))
        file.write('<h2>Test results</h2>'
                   'The following table shows detailed results:<br>'
                   '<table><thead><tr>'
                   '<th>Execution:</th><th>1 thread [s]</th><th>4 threads [s]</th>'
                   '<th>4 processes [s]</th><th>processes based<br>on number of CPUs [s]<br>'
                   '</tr></thead><tbody>')
        for i in range(1, 6):
            file.write('<tr>'
                       f'<td>{i}</td>'
                       f'<td>{single[i]:.2f}</td>'
                       f'<td>{four[i]:.2f}</td>'
                       f'<td>{four_proc[i]:.2f}</td>'
                       f'<td>{optimal_proc[i]:.2f}</td>'
                       '</tr>')
        file.write('</tbody></table>')
        file.write('<h2>Summary</h2><br>'
                   'The following table shows the median of all results:'
                   '<table><thead><tr>'
                   '<th>Execution:</th><th>1 thread [s]</th><th>4 threads [s]</th>'
                   '<th>4 processes [s]</th><th>processes based<br>on number of CPUs [s]<br>'
                   '</tr></thead><tbody>'
                   '<tr>'
                   f'<td>-</td>'
                   f'<td>{median(single.values()):.2f}</td>'
                   f'<td>{median(four.values()):.2f}</td>'
                   f'<td>{median(four_proc.values()):.2f}</td>'
                   f'<td>{median(optimal_proc.values()):.2f}</td>'
                   '</tr>'
                   '</tbody></table><br>'
                   'App author: Kamil Kurzawa'
                   )


if __name__ == '__main__':
    from platform import (python_version, python_implementation,
                          system, release, processor)
    from sys import version
    from os import cpu_count
    import multiprocessing
    import timeit
    from statistics import median
    from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor

    num_of_tests = 5
    results_single_thread = {}
    results_four_threads = {}
    results_four_processes = {}
    results_optimal_processes = {}
    for n in range(1, num_of_tests+1):
        results_single_thread[n] = timeit.timeit("test_func_threads(False)",
                                                 setup="from __main__ import test_func_threads", number=1)
        results_four_threads[n] = timeit.timeit("test_func_threads(True)",
                                                setup="from __main__ import test_func_threads", number=1)
        results_four_processes[n] = timeit.timeit("test_func_processes(False)",
                                                  setup="from __main__ import test_func_processes", number=1)
        results_optimal_processes[n] = timeit.timeit("test_func_processes(True)",
                                                     setup="from __main__ import test_func_processes", number=1)

    generate_report_file(results_single_thread, results_four_threads, results_four_processes, results_optimal_processes)
