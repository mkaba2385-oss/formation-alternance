import time
from collections import deque
import matplotlib.pyplot as plt

MAX_N_BUBBLE = 10000 

def bubble_sort(numbers):
    data_to_sort = list(numbers)
    length = len(data_to_sort)
    for i in range(length):
        for j in range(0, length - i - 1):
            if data_to_sort[j] > data_to_sort[j + 1]:
                data_to_sort[j], data_to_sort[j + 1] = data_to_sort[j + 1], data_to_sort[j]
    return data_to_sort

def benchmark():
    sizes = [100, 1000, 10000, 100000]
    
    results = {
        "x in list": [],
        "x in set": [],
        "list.insert(0)": [],
        "deque.appendleft": [],
        "Bubble Sort": [],
        "sorted()": [],
        "for k in dict.keys()": [],
        "for k in dict": []
    }

    print("Exécution des benchmarks en cours...\n")

    for size in sizes:
        # Données de test
        data_list = list(range(size))
        data_set = set(data_list)
        data_deque = deque(data_list)
        data_dict = {index: True for index in range(size)}
        
        target = -1  
        repeats = 100 if size <= 10000 else 10  

        # 1. Recherche list (O(n))
        start = time.perf_counter()
        for _ in range(repeats):
            _ = target in data_list
        results["x in list"].append((time.perf_counter() - start) / repeats)

        # 2. Recherche set (O(1))
        start = time.perf_counter()
        for _ in range(repeats):
            _ = target in data_set
        results["x in set"].append((time.perf_counter() - start) / repeats)

        # 3. Insertion list (O(n)) - Copie préparée avant le chrono
        list_copy = list(data_list)
        start = time.perf_counter()
        for _ in range(100):
            list_copy.insert(0, 0)
        results["list.insert(0)"].append((time.perf_counter() - start) / 100)

        # 4. Insertion deque (O(1)) - Copie préparée avant le chrono
        deque_copy = deque(data_list)
        start = time.perf_counter()
        for _ in range(100):
            deque_copy.appendleft(0)
        results["deque.appendleft"].append((time.perf_counter() - start) / 100)

        # 5. Tri Bubble Sort (O(n²))
        if size <= MAX_N_BUBBLE:
            start = time.perf_counter()
            _ = bubble_sort(data_list[::-1])  # Pire cas : liste inversée
            results["Bubble Sort"].append(time.perf_counter() - start)
        else:
            results["Bubble Sort"].append(None)  # Omis pour 100 000 (trop long)

        # 6. Tri Timsort / sorted() (O(n log n))
        start = time.perf_counter()
        _ = sorted(data_list[::-1])
        results["sorted()"].append(time.perf_counter() - start)

        # 7. Itération dict.keys() (O(n))
        start = time.perf_counter()
        for _ in range(repeats):
            for key in data_dict.keys():
                _ = key
        results["for k in dict.keys()"].append((time.perf_counter() - start) / repeats)

        # 8. Itération dict (O(n))
        start = time.perf_counter()
        for _ in range(repeats):
            for key in data_dict:
                _ = key
        results["for k in dict"].append((time.perf_counter() - start) / repeats)

    return sizes, results

def show_results(sizes, results):
    header = f"{'Opération':<22} | " + " | ".join([f"N={size:<8}" for size in sizes])
    print("-" * len(header))
    print(header)
    print("-" * len(header))

    for operation, execution_times in results.items():
        row = f"{operation:<22} | "
        for duration in execution_times:
            if duration is None:
                row += f"{'N/A (trop long)':<10} | "
            elif duration < 1e-4:
                row += f"{duration * 1e6:>7.2f} µs | "
            elif duration < 1:
                row += f"{duration * 1e3:>7.2f} ms | "
            else:
                row += f"{duration:>7.2f} s  | "
        print(row)
    print("-" * len(header))

def plot_results(sizes, results):
    fig, axes = plt.subplots(2, 2, figsize=(12, 10))
    fig.suptitle("Prouver les complexités algorithmiques théoriques", fontsize=14, fontweight='bold')

    pairs = [
        (("x in list", "x in set"), "(a) Recherche (O(n) vs O(1))", axes[0, 0]),
        (("list.insert(0)", "deque.appendleft"), "(b) Insertion en tête (O(n) vs O(1))", axes[0, 1]),
        (("Bubble Sort", "sorted()"), "(c) Tri (O(n²) vs O(n log n))", axes[1, 0]),
        (("for k in dict.keys()", "for k in dict"), "(d) Parcours de Dictionnaire (Les deux O(n))", axes[1, 1])
    ]

    for ops, title, ax in pairs:
        for operation in ops:
            valid_data = [(sizes[i], results[operation][i]) for i in range(len(sizes)) if results[operation][i] is not None]
            if valid_data:
                x_values, y_values = zip(*valid_data)
                ax.plot(x_values, y_values, marker='o', label=operation)
        
        ax.set_title(title)
        ax.set_xlabel("Taille de la structure (n)")
        ax.set_ylabel("Temps moyen (secondes)")
        ax.set_xscale('log')
        
        if "Recherche" in title or "Insertion" in title or "Tri" in title:
            ax.set_yscale('log')
            
        ax.grid(True, which="both", ls="--", linewidth=0.5)
        ax.legend()

    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    sizes, results = benchmark()
    show_results(sizes, results)
    plot_results(sizes, results)