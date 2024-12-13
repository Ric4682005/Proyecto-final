import time  # Biblioteca para medir tiempos

def run_simulation(comm, rank, size, problem):
    # Determinar el número total de tareas según el problema
    num_tasks = 100 if problem == "traffic" else 200

    # Dividir tareas de forma estática entre nodos
    tasks_per_node = num_tasks // size
    start = rank * tasks_per_node
    end = start + tasks_per_node

    # Ajustar para el último nodo si las tareas no son divisibles equitativamente
    if rank == size - 1:
        end += num_tasks % size

    tasks = range(start, end)  # Lista de tareas asignadas al nodo actual

    # Procesar tareas y medir tiempo
    start_time = time.time()
    results = [process_task(task, problem) for task in tasks]
    end_time = time.time()

    print(f"Proceso {rank} completó {len(results)} tareas en {end_time - start_time:.2f} segundos.")

def process_task(task, problem):
    # Simular procesamiento basado en el tipo de problema
    if problem == "traffic":
        time.sleep(0.1)  # Simula el tiempo de procesamiento
    elif problem == "finance":
        time.sleep(0.2)
    elif problem == "data_processing":
        time.sleep(0.15)
    elif problem == "physics":
        time.sleep(0.25)
    return task * 2  # Resultado simulado de la tarea
