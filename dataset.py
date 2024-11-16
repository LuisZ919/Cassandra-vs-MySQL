import csv
from faker import Faker
import random
from tqdm import tqdm

Numero_Record = 1000000
Output_File = 'data.csv'

fake = Faker()
emails = set()

with open(Output_File, mode= 'w', newline='', encoding='utf-8') as file:
	writer = csv.writer(file)
	writer.writerow(["name", "email", "age"])

	count = 0
	with tqdm(total=Numero_Record, desc = "Escribiendo datos...", unit="datos") as pbar:
		while count < Numero_Record:
			email = fake.email()
			if email not in emails:
				emails.add(email)
				writer.writerow([
					fake.name(),
					email,
					random.randint(0, 99)
				])
				count +=1
				pbar.update(1)

print(f'{Numero_Record} registros unicos generados en el archivo {Output_File}')
