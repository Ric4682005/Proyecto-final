import time  # Biblioteca para medir tiempos de ejecución y simular tareas

def run_simulation(comm, rank, size, problem):
    """
    Ejecuta la simulación con balanceo dinámico.

    Args:
        comm: Comunicador MPI para la comunicación entre nodos.
        rank: Identificador único del proceso actual.
        size: Número total de procesos disponibles.
        problem: El problema seleccionado por el usuario.
    """
    num_tasks = 100 if problem == "traffic" else 200
    tasks = list(range(num_tasks))

    if rank == 0:
        active_nodes = size - 1
        start_time = time.time()  # Marca inicial

        for node in range(1, size):
            if tasks:
                task = tasks.pop(0)
                comm.send(task, dest=node)
            else:
                comm.send(None, dest=node)
                active_nodes -= 1

        while active_nodes > 0:
            completed_node = comm.recv(source=MPI.ANY_SOURCE, tag=0)
            if tasks:
                task = tasks.pop(0)
                comm.send(task, dest=completed_node)
            else:
                comm.send(None, dest=completed_node)
                active_nodes -= 1

        end_time = time.time()  # Marca final
        print(f"Tareas dinámicas completadas en {end_time - start_time:.2f} segundos.")
    else:
        while True:
            task = comm.recv(source=0)
            if task is None:
                break
            process_task(task, problem)
            comm.send(rank, dest=0, tag=0)

def process_task(task, problem):
    if problem == "traffic":
        time.sleep(0.1)
    elif problem == "finance":
        time.sleep(0.2)
    elif problem == "data_processing":
        time.sleep(0.15)
    elif problem == "physics":
        time.sleep(0.25)
    print(f"Tarea {task} completada.")
