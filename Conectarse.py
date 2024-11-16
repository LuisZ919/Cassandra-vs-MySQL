import pymysql

try:
	conexion = pymysql.connect(host='127.0.0.1',
			     port = 3307,
                             user='root',
                             password='strong_password',
                             db='store')
	print("Conexión correcta")

except (pymysql.err.OperationalError, pymysql.err.InternalError) as e:
	print("Ocurrió un error al conectar: ", e)
