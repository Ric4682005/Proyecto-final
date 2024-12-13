from mpi4py import MPI
import static_balance
import dynamic_balance
import performance
import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import subprocess
import os
import multiprocessing
import math
import time

def select_file():
    file_path = filedialog.askopenfilename(
        title="Seleccione un archivo",
        filetypes=(
            ("Imágenes y Videos", "*.jpg *.jpeg *.png *.mp4 *.avi"),
            ("Todos los archivos", "*.*")
        )
    )
    if file_path:
        print(f"Archivo seleccionado: {file_path}")
        if file_path.lower().endswith((".jpg", ".jpeg", ".png")):
            show_image(file_path)
        elif file_path.lower().endswith((".mp4", ".avi")):
            play_video(file_path)
        else:
            messagebox.showwarning("Formato no soportado", "El archivo seleccionado no es compatible.")
    else:
        messagebox.showwarning("Sin selección", "No has seleccionado ningún archivo.")

def show_image(file_path):
    img_window = tk.Toplevel()
    img_window.title("Vista previa de la imagen")
    img = Image.open(file_path)
    img = img.resize((400, 400))
    img_tk = ImageTk.PhotoImage(img)
    tk.Label(img_window, image=img_tk).pack()
    img_window.geometry("420x420")
    img_window.mainloop()

def play_video(file_path):
    vlc_path = r"C:\\Program Files (x86)\\VideoLAN\\VLC\\vlc.exe"
    try:
        normalized_path = os.path.normpath(file_path)
        subprocess.run([vlc_path, '--play-and-exit', '--fullscreen', normalized_path], check=True)
    except FileNotFoundError:
        messagebox.showerror("Error", "No se encontró VLC en la ruta especificada.")
    except Exception as e:
        messagebox.showerror("Error", f"Error inesperado: {e}")

def process_task(task):
    """
    Simula el procesamiento de una tarea específica.
    """
    result = math.sqrt(task) ** 2 + math.sin(task)
    time.sleep(0.1)
    return result

def run_simulation_parallel(num_tasks):
    """
    Ejecuta la simulación usando multiprocessing.
    """
    tasks = range(num_tasks)

    with multiprocessing.Pool(processes=multiprocessing.cpu_count()) as pool:
        start_time = time.time()
        results = pool.map(process_task, tasks)
        end_time = time.time()

    print(f"Simulación completada con {len(results)} tareas en {end_time - start_time:.2f} segundos.")
    return results

def start_simulation():
    global problem_choice, balance_choice
    problem_choice = problem_var.get()
    balance_choice = balance_var.get()

    if not problem_choice or not balance_choice:
        messagebox.showerror("Error", "Debe seleccionar un problema y un tipo de balanceo.")
        return False

    if problem_choice == "data_processing":
        print("Iniciando simulación con procesamiento paralelo...")
        run_simulation_parallel(num_tasks=100)

    root.destroy()
    return True

def main_menu():
    global root, problem_var, balance_var
    root = tk.Tk()
    root.title("Simulación de Balanceo de Carga")
    root.geometry("400x400")
    root.update_idletasks()
    width = 400
    height = 400
    x = (root.winfo_screenwidth() // 2) - (width // 2)
    y = (root.winfo_screenheight() // 2) - (height // 2)
    root.geometry(f"{width}x{height}+{x}+{y}")

    tk.Label(root, text="Seleccione el problema a simular:", font=("Arial", 12)).pack(pady=10)
    problem_var = tk.StringVar(value="")
    balance_var = tk.StringVar(value="")

    tk.Radiobutton(root, text="Simulación de tráfico vehicular", variable=problem_var, value="traffic").pack(anchor="w", padx=20)
    tk.Radiobutton(root, text="Simulación de sistemas financieros", variable=problem_var, value="finance").pack(anchor="w", padx=20)
    tk.Radiobutton(root, text="Procesamiento masivo de datos (imágenes/videos)", variable=problem_var, value="data_processing").pack(anchor="w", padx=20)
    tk.Radiobutton(root, text="Análisis de sistemas físicos o químicos", variable=problem_var, value="physics").pack(anchor="w", padx=20)

    tk.Button(root, text="Seleccionar archivo (imágenes/videos)", command=select_file).pack(pady=10)
    tk.Label(root, text="Seleccione el tipo de balanceo:", font=("Arial", 12)).pack(pady=10)
    tk.Radiobutton(root, text="Balanceo Estático", variable=balance_var, value="static").pack(anchor="w", padx=20)
    tk.Radiobutton(root, text="Balanceo Dinámico", variable=balance_var, value="dynamic").pack(anchor="w", padx=20)
    tk.Button(root, text="Iniciar Simulación", command=lambda: start_simulation() and root.quit()).pack(pady=20)
    root.mainloop()

def ask_to_continue():
    result = messagebox.askquestion("¿Desea continuar?", "¿Desea realizar otra simulación?")
    if result == 'yes':
        return True
    else:
        return False

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()

try:
    while True:
        if rank == 0:
            main_menu()
        else:
            problem_choice = None
            balance_choice = None

        problem_choice = comm.bcast(problem_choice, root=0)
        balance_choice = comm.bcast(balance_choice, root=0)

        if balance_choice == "static":
            static_balance.run_simulation(comm, rank, size, problem_choice)
        elif balance_choice == "dynamic":
            dynamic_balance.run_simulation(comm, rank, size, problem_choice)
        else:
            if rank == 0:
                print("Modo no válido. Seleccione una opción válida.")

        if rank == 0:
            performance.compare_performance()
            if not ask_to_continue():
                break
except KeyboardInterrupt:
    print("Programa interrumpido.")
