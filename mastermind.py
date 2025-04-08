import itertools
import time
from logic_project import *

class Mastermind:
    def __init__(self):
        self.colors = ["azul", "rojo", "blanco", "negro", "verde", "purpura"]
        self.color_abbr = {"A": "azul", "R": "rojo", "B": "blanco", "N": "negro", "V": "verde", "P": "purpura"}
        self.code_length = 4
        self.all_possible_codes = list(itertools.product(self.colors, repeat=self.code_length))
        self.possible_codes = self.all_possible_codes.copy()
        self.guesses_history = []
        self.search_space_history = []
        
    def generar_feedback(self, guess, secret_code):
        secret_copy = list(secret_code)
        guess_copy = list(guess)
        black_pegs = 0
        white_pegs = 0
        
        for i in range(self.code_length):
            if guess_copy[i] == secret_copy[i]:
                black_pegs += 1
                guess_copy[i] = None
                secret_copy[i] = None
        
        for i in range(self.code_length):
            if guess_copy[i] is not None:
                if guess_copy[i] in secret_copy:
                    white_pegs += 1
                    secret_copy[secret_copy.index(guess_copy[i])] = None
        
        return (black_pegs, white_pegs)
    
    def is_consistent(self, code, guess, feedback):
        hypothetical_feedback = self.generar_feedback(guess, code)
        return hypothetical_feedback == feedback
    
    def reduce_search_space(self, guess, feedback):

        self.search_space_history.append(len(self.possible_codes))
        
        self.possible_codes = [code for code in self.possible_codes 
                              if self.is_consistent(code, guess, feedback)]
    
    def minimax_score(self, candidate_guess):

        possible_feedbacks = [(b, w) for b in range(5) for w in range(5-b+1)]
        
        feedback_counts = {}
        for feedback in possible_feedbacks:
            count = sum(1 for code in self.possible_codes 
                      if self.generar_feedback(candidate_guess, code) == feedback)
            feedback_counts[feedback] = count
        
        worst_case_elimination = min(feedback_counts.values()) if feedback_counts else 0
        return worst_case_elimination
    
    def select_next_guess(self):
        if not self.guesses_history:
            return (self.colors[0], self.colors[0], self.colors[1], self.colors[1])
        
        if len(self.possible_codes) == 1:
            return self.possible_codes[0]
        
        best_score = -1
        best_guesses = []
        
        for candidate in self.possible_codes:
            score = self.minimax_score(candidate)
            if score > best_score:
                best_score = score
                best_guesses = [candidate]
            elif score == best_score:
                best_guesses.append(candidate)
        
        if best_guesses:
            return best_guesses[0]
        
        for candidate in self.all_possible_codes:
            if candidate in self.possible_codes or candidate in self.guesses_history:
                continue
            score = self.minimax_score(candidate)
            if score > best_score:
                best_score = score
                best_guesses = [candidate]
            elif score == best_score:
                best_guesses.append(candidate)
        
        return best_guesses[0] if best_guesses else self.possible_codes[0]
    
    def solve_auto(self, secret_code):
        self.possible_codes = self.all_possible_codes.copy()
        self.guesses_history = []
        self.search_space_history = []
        
        attempts = 0
        solved = False
        
        print(f"Combinación secreta: {secret_code}")
        print("Iniciando resolución en modo automático...")
        
        while not solved and attempts < 10:  
            guess = self.select_next_guess()
            self.guesses_history.append(guess)
            attempts += 1
            
            feedback = self.generar_feedback(guess, secret_code)
            print(f"Intento {attempts}: {guess} -> Feedback: {feedback[0]} negros, {feedback[1]} blancos")
            
            if feedback[0] == self.code_length:  
                solved = True
                print(f"Solución encontrada en {attempts} intentos")
            else:
                self.reduce_search_space(guess, feedback)
                print(f"Espacio de búsqueda reducido a {len(self.possible_codes)} combinaciones")
        
        if not solved:
            print("No se pudo encontrar la solución dentro del límite de intentos.")
        
        return {
            "intentos": attempts,
            "resuelto": solved,
            "historia_espacio": self.search_space_history
        }
    
    def solve_interactive(self):

        self.possible_codes = self.all_possible_codes.copy()
        self.guesses_history = []
        self.search_space_history = []
        
        attempts = 0
        solved = False
        
        print("Modo en tiempo real iniciado.")
        print("Piensa en una combinación de 4 fichas con los colores:")
        for i, color in enumerate(self.colors):
            print(f"{i+1}. {color.capitalize()}")
        print("Puedes usar abreviaciones: A=azul, R=rojo, B=blanco, N=negro, V=verde, P=purpura")
        
        while not solved and attempts < 10:
            guess = self.select_next_guess()
            self.guesses_history.append(guess)
            attempts += 1
            
            print(f"\nIntento {attempts}: {[color.capitalize() for color in guess]}")
            
            while True:
                try:
                    feedback_input = input("Ingresa tu feedback (formato: negro blanco): ")
                    black_pegs, white_pegs = map(int, feedback_input.split())
                    if 0 <= black_pegs <= self.code_length and 0 <= white_pegs <= self.code_length and black_pegs + white_pegs <= self.code_length:
                        break
                    else:
                        print(f"Error: La suma de fichas negras y blancas no puede exceder {self.code_length}")
                except ValueError:
                    print("Error: Ingresa dos números separados por espacio (ej: 2 1)")
            
            feedback = (black_pegs, white_pegs)
            
            if feedback[0] == self.code_length:  
                solved = True
                print(f"Se adivinó tu combinación en {attempts} intentos")
            else:
                self.reduce_search_space(guess, feedback)
                print(f"Espacio de búsqueda reducido a {len(self.possible_codes)} combinaciones")
        
        if not solved:
            print("No he podido encontrar la solución dentro del límite de intentos.")
        
        return {
            "intentos": attempts,
            "resuelto": solved,
            "historia_espacio": self.search_space_history
        }
    
    def parse_code_input(self, code_input):
        code = []
        if len(code_input) == 4:
            for char in code_input.upper():
                if char in self.color_abbr:
                    code.append(self.color_abbr[char])
                else:
                    return None  
        else:
            parts = [p.strip().lower() for p in code_input.replace(",", " ").split()]
            if len(parts) != 4:
                return None  
            
            for part in parts:
                if part in self.colors:
                    code.append(part)
                else:
                    return None  
        
        return tuple(code) if len(code) == 4 else None

    def create_knowledge_base(self, guess, feedback):

        kb = And()
        black_pegs, white_pegs = feedback
        total_matches = black_pegs + white_pegs
        
        positions = {}
        for i in range(self.code_length):
            for color in self.colors:
                positions[(i, color)] = Symbol(f"P{i}_{color}")
        
        for i in range(self.code_length):
            for color in self.colors:
                position_constraint = And()
                position_constraint.add(positions[(i, color)])
                
                for other_color in self.colors:
                    if other_color != color:
                        position_constraint.add(Not(positions[(i, other_color)]))
                
                kb.add(position_constraint)
        

        return kb

def logical_mastermind_gui():
    mastermind = Mastermind()
    
    while True:
        print("\n=== MASTERMIND LÓGICO ===")
        print("1. Modo Automático")
        print("2. Modo Tiempo Real")
        print("3. Salir")
        choice = input("Elige una opción: ")
        
        if choice == "1":
            while True:
                code_input = input("\nIngresa la combinación secreta (4 colores, separados por espacios o usar abreviaturas A,R,B,N,V,P): ")
                secret_code = mastermind.parse_code_input(code_input)
                if secret_code:
                    break
                else:
                    print("Código inválido. Intenta nuevamente.")
            
            start_time = time.time()
            results = mastermind.solve_auto(secret_code)
            end_time = time.time()
            
            print("\n--- Resultados ---")
            print(f"Intentos necesarios: {results['intentos']}")
            print(f"Problema resuelto: {'Sí' if results['resuelto'] else 'No'}")
            print(f"Tiempo total: {end_time - start_time:.2f} segundos")
            print("\nEvolución del espacio de búsqueda:")
            for i, size in enumerate(results['historia_espacio']):
                print(f"Después del intento {i+1}: {size} combinaciones")
        
        elif choice == "2":
            results = mastermind.solve_interactive()
            
            print("\n--- Resultados ---")
            print(f"Intentos necesarios: {results['intentos']}")
            print(f"Problema resuelto: {'Sí' if results['resuelto'] else 'No'}")
            print("\nEvolución del espacio de búsqueda:")
            for i, size in enumerate(results['historia_espacio']):
                print(f"Después del intento {i+1}: {size} combinaciones")
        
        elif choice == "3":
            print("Adiós")
            break
        
        else:
            print("Opción inválida. Intenta nuevamente.")

if __name__ == "__main__":
    logical_mastermind_gui()