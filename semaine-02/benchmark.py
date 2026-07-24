import time
from collections import deque
import matplotlib.pyplot as plt


MAX_N_BUBBLE = 10000 

def bubble_sort(arr):
    data = list(arr)
    n = len(data)
    for i in range(n):
        for j in range(0, n - i - 1):
            if data[j] > data[j + 1]:
                data[j], data[j + 1] = data[j + 1], data[j]
    return data

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

    for n in sizes:
        # Données de test
        data_list = list(range(n))
        data_set = set(data_list)
        data_deque = deque(data_list)
        data_dict = {i: True for i in range(n)}
        
        target = -1  
        repeats = 100 if n <= 10000 else 10  

       
        start = time.perf_counter()
        for _ in range(repeats):
            _ = target in data_list
        results["x in list"].append((time.perf_counter() - start) / repeats)

    
        start = time.perf_counter()
        for _ in range(repeats):
            _ = target in data_set
        results["x in set"].append((time.perf_counter() - start) / repeats)

        
        start = time.perf_counter()
        l_copy = list(data_list)
        for _ in range(100):
            l_copy.insert(0, 0)
        results["list.insert(0)"].append((time.perf_counter() - start) / 100)

        
        start = time.perf_counter()
        d_copy = deque(data_list)
        for _ in range(100):
            d_copy.appendleft(0)
        results["deque.appendleft"].append((time.perf_counter() - start) / 100)

       
        if n <= MAX_N_BUBBLE:
            start = time.perf_counter()
            _ = bubble_sort(data_list[::-1]) # Pire cas : liste inversée
            results["Bubble Sort"].append(time.perf_counter() - start)
        else:
            results["Bubble Sort"].append(None) # Omit pour 100 000

       
        start = time.perf_counter()
        _ = sorted(data_list[::-1])
        results["sorted()"].append(time.perf_counter() - start)

       
        start = time.perf_counter()
        for _ in range(repeats):
            for k in data_dict.keys():
                _ = k
        results["for k in dict.keys()"].append((time.perf_counter() - start) / repeats)

        
        start = time.perf_counter()
        for _ in range(repeats):
            for k in data_dict:
                _ = k
        results["for k in dict"].append((time.perf_counter() - start) / repeats)

    return sizes, results

def show_results(sizes, results):
    
    header = f"{'Opération':<22} | " + " | ".join([f"N={n:<8}" for n in sizes])
    print("-" * len(header))
    print(header)
    print("-" * len(header))

    for op, times in results.items():
        row = f"{op:<22} | "
        for t in times:
            if t is None:
                row += f"{'N/A (trop long)':<10} | "
            elif t < 1e-4:
                row += f"{t*1e6:>7.2f} µs | "
            elif t < 1:
                row += f"{t*1e3:>7.2f} ms | "
            else:
                row += f"{t:>7.2f} s  | "
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
        for op in ops:
            valid_data = [(sizes[i], results[op][i]) for i in range(len(sizes)) if results[op][i] is not None]
            if valid_data:
                x, y = zip(*valid_data)
                ax.plot(x, y, marker='o', label=op)
        
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