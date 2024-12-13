import matplotlib.pyplot as plt  # Biblioteca para graficar datos

def compare_performance():
    """
    Compara el rendimiento entre el balanceo estático y dinámico.

    Crea gráficos que muestran las diferencias de tiempo de ejecución.
    """
    static_times = [5.5, 5.3, 5.8, 5.6]
    dynamic_times = [4.8, 4.5, 4.7, 4.9]

    # Crear el gráfico
    plt.plot(static_times, label="Balanceo Estático")
    plt.plot(dynamic_times, label="Balanceo Dinámico")
    plt.legend()
    plt.title("Comparación de Rendimiento")
    plt.xlabel("Ejecución")
    plt.ylabel("Tiempo (s)")
    plt.grid(True)

    # Centrar ventana del gráfico
    mng = plt.get_current_fig_manager()
    mng.window.wm_geometry("+{}+{}".format(
        (mng.window.winfo_screenwidth() // 2) - 300,
        (mng.window.winfo_screenheight() // 2) - 200
    ))

    plt.show()
