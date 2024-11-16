import pymysql
import pandas as pd
from tqdm import tqdm  # Asegúrate de importar tqdm
import time

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
        df = pd.read_csv('data.csv')  # Puedes agregar más parámetros si es necesario
        cursor = conexion.cursor()

        # Crear la tabla si no existe
        create_table = """
            CREATE TABLE IF NOT EXISTS datos(
                name VARCHAR(100),
                email VARCHAR(100),
                age INT
            )
        """
        cursor.execute(create_table)
        conexion.commit()

        # Insertar los datos del DataFrame
        datos = [tuple(x) for x in df.to_records(index=False)]
        insert_query = """INSERT INTO datos (name, email, age) VALUES (%s, %s, %s)"""

        # Usar tqdm para mostrar el progreso mientras insertamos los registros
        with tqdm(total=len(datos), desc="Insertando datos...", unit="registro") as pbar:
            for data in datos:
                cursor.execute(insert_query, data)  # Insertar un solo registro a la vez
                pbar.update(1)  # Actualizar la barra de progreso

        conexion.commit()  # Confirmar la transacción después de insertar todos los datos
        print("Datos introducidos")

    except Exception as e:
        print("Ocurrió un error al procesar los datos CSV:", e)

finally:
    # Asegurarse de que la conexión se cierre correctamente
    if conexion.open:
        conexion.close()
    print("Conexión cerrada")
