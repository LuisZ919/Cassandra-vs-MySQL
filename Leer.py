import pymysql
import pandas as pd
from tqdm import tqdm  # Asegúrate de importar tqdm

try:
    # Establecer la conexión
    conexion = pymysql.connect(
        host='127.0.0.1',
        port=3307,
        user='root',
        password='strong_password',
        db='store'
    )
    print("Conexión correcta")

    try:
        # Leer los datos desde el archivo CSV
        df = pd.read_csv('data.csv')  # Esto ya está bien para leer los datos CSV
        cursor = conexion.cursor()

        # Ejecutar una consulta SELECT para leer todos los datos de la tabla
        reading_table = "SELECT * FROM datos"
        cursor.execute(reading_table)

        # Obtener todos los resultados de la consulta
        datos = cursor.fetchall()  # fetchall() recupera todos los registros de la tabla

        # Usar tqdm para mostrar el progreso mientras procesamos los registros
        with tqdm(total=len(datos), desc="Leyendo datos...", unit="registro") as pbar:
            for data in datos:
                # Procesar cada fila de datos
                pbar.update(1)  # Actualizar el progreso

        print("Datos leídos correctamente")

    except Exception as e:
        print("Ocurrió un error al procesar los datos CSV:", e)

finally:
    # Asegurarse de que la conexión se cierre correctamente
    if conexion.open:
        conexion.close()
    print("Conexión cerrada")
