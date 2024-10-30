Ejercicio Cassandra vs MySQL.

Parte git.

Se crea un repositorio en git y dos ramas una para cassandra y otra par mysql.
Zayra trabajará en MySQL y Luis trabajará en cassandra.


Parte Cassandra
Teniendo ya descargado la imagen de cassandra en el docker, creamos un contenedor cassandra con los siguientes parámetros.

docker run --rm -d --name cassandra --hostname cassandra --network cassandra_network cassandra

docker exec -it cassandra bash -c 'cqlsh'



Los datasets para mysql y cassandra son los siguientes.

-- Conéctate a la base de datos y crea las tablas
CREATE TABLE products (
    product_id INT PRIMARY KEY,
    name VARCHAR(100),
    category VARCHAR(50),
    price DECIMAL(10, 2)
);

CREATE TABLE sales (
    sale_id INT PRIMARY KEY,
    product_id INT,
    sale_date DATE,
    quantity INT,
    FOREIGN KEY (product_id) REFERENCES products(product_id)
);

-- Inserta datos en la tabla products
INSERT INTO products (product_id, name, category, price) VALUES
(1, 'Laptop', 'Electronics', 1200.00),
(2, 'Headphones', 'Electronics', 150.00),
(3, 'Desk Chair', 'Furniture', 350.00),
(4, 'Monitor', 'Electronics', 200.00),
(5, 'Coffee Table', 'Furniture', 100.00);

-- Inserta datos en la tabla sales
INSERT INTO sales (sale_id, product_id, sale_date, quantity) VALUES
(1, 1, '2023-01-10', 1),
(2, 2, '2023-01-15', 2),
(3, 3, '2023-01-20', 1),
(4, 4, '2023-01-25', 3),
(5, 1, '2023-02-10', 2),
(6, 5, '2023-02-15', 1);
Con el editor nano creamos este dataset y lo caragamos con un contenedor temporal en docker.

docker run --rm --network cassandra_network -v "$(pwd)/dataset.cql:/scripts/dataset.cql" -e CQLSH_HOST=cassandra -e CQLSH_PORT=9042 -e CQLVERSION=3.
4.7 nuvo/docker-cqlsh

Keyspace system_virtual_schema
------------------------------
columns  keyspaces  tables

cqlsh> describe keyspaces

store   system_auth         system_schema  system_views
system  system_distributed  system_traces  system_virtual_schema

cqlsh> use stores;
InvalidRequest: Error from server: code=2200 [Invalid query] message="Keyspace 'stores' does not exist"
cqlsh> use store;
cqlsh:store> describe tables

products  sales

cqlsh:store> select * from products
         ... ;

 product_id | category    | name         | price
------------+-------------+--------------+---------
          5 |   Furniture | Coffee Table |  100.00
          1 | Electronics |       Laptop | 1200.00
          2 | Electronics |   Headphones |  150.00
          4 | Electronics |      Monitor |  200.00
          3 |   Furniture |   Desk Chair |  350.00

(5 rows)
cqlsh:store>





Una vez creado, para medir el tiempo usaremos un notebook con el siguiente código de python.

from cassandra.cluster import Cluster
import time

# Configuración de la conexión
cluster = Cluster(['localhost'])  # Cambia 'localhost' si es necesario
session = cluster.connect('store')  # Nombre del keyspace

# Medir el tiempo de la consulta
start_time = time.time()
rows = session.execute("SELECT * FROM sales WHERE sale_id=1;")
end_time = time.time()

# Mostrar el tiempo en segundos
print(f"Tiempo de ejecución: {end_time - start_time} segundos")

# Mostrar los resultados
for row in rows:
    print(row)



Usamos pip para instalar cassandra-driver.
