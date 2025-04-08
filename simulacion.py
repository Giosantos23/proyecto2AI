import random
import itertools
import matplotlib.pyplot as plt
import numpy as np
from mastermind import Mastermind 

def run_simulation(num_games=200):
    mastermind = Mastermind()
    colors = ["azul", "rojo", "blanco", "negro", "verde", "purpura"]
    
    attempts_needed = []
    search_space_sizes = []
    max_attempts = 0
    
    print(f"Simulando {num_games} juegos de Mastermind...")
    
    for game in range(num_games):
        secret_code = tuple(random.choice(colors) for _ in range(4))
        
        results = mastermind.solve_auto(secret_code)
        
        attempts_needed.append(results["intentos"])
        
        if results["intentos"] > max_attempts:
            max_attempts = results["intentos"]
        
        space_history = results["historia_espacio"]
        search_space_sizes.append(space_history + [space_history[-1]] * (max_attempts - len(space_history)))
        
        if (game + 1) % 20 == 0:
            print(f"Completados {game + 1} juegos")
    
    avg_attempts = np.mean(attempts_needed)
    max_attempts_game = max(attempts_needed)
    min_attempts_game = min(attempts_needed)
    
    for i in range(len(search_space_sizes)):
        if len(search_space_sizes[i]) < max_attempts:
            search_space_sizes[i].extend([search_space_sizes[i][-1]] * (max_attempts - len(search_space_sizes[i])))
    
    avg_search_space = np.mean(search_space_sizes, axis=0)
    
    plt.figure(figsize=(12, 6))
    
    plt.subplot(1, 2, 1)
    plt.hist(attempts_needed, bins=range(1, max_attempts_game + 2), alpha=0.7, color='blue', edgecolor='black')
    plt.axvline(avg_attempts, color='red', linestyle='dashed', linewidth=2, label=f'Promedio: {avg_attempts:.2f}')
    plt.xlabel('Número de intentos')
    plt.ylabel('Frecuencia')
    plt.title('Distribución de intentos necesarios')
    plt.legend()
    plt.grid(True, alpha=0.3)
    
    plt.subplot(1, 2, 2)
    plt.plot(range(1, len(avg_search_space) + 1), avg_search_space, marker='o', linestyle='-', color='green')
    plt.yscale('log')  
    plt.xlabel('Número de intento')
    plt.ylabel('Tamaño promedio del espacio de búsqueda')
    plt.title('Reducción del espacio de búsqueda por intento')
    plt.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('mastermind_analysis.png')
    plt.show()
    
    print("\n--- Resultados de la simulación ---")
    print(f"Número de juegos: {num_games}")
    print(f"Promedio de intentos necesarios: {avg_attempts:.2f}")
    print(f"Mínimo de intentos: {min_attempts_game}")
    print(f"Máximo de intentos: {max_attempts_game}")
    print(f"Tamaño inicial del espacio de búsqueda: 1296")
    print(f"Tamaño final promedio del espacio de búsqueda: {avg_search_space[-1]:.2f}")
    
    return {
        "avg_attempts": avg_attempts,
        "avg_search_space": avg_search_space,
        "attempts_distribution": attempts_needed
    }

if __name__ == "__main__":
    results = run_simulation(200)