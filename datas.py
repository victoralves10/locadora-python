import os
os.system("cls")

from datetime import date, datetime

# Apenas a data de hoje
hoje = date.today()
print("Data de hoje: ", hoje)

agora = datetime.now()
print("Agora: ",agora)

# Formatando datas - CONVERTE DATA EM STRING
os.system("cls")
print(agora.strftime("%d/%m/%Y")) # .strftime -> converte uma data em string
print(agora.strftime("%H:%M:%S"))
print(agora.strftime("%A, %d de %B"))

# Formatando datas - CONVERTE STRING EM DATA
os.system("cls")
texto = "02/10/2025 11:06"
dt = datetime.strptime(texto, "%d/%m/%Y %H:%M") # .strptime -> Converte string em data
print("Convertido: ", dt)

# operacoes com datas e horas - timedelta
os.system("cls")
from datetime import timedelta
amanha = hoje + timedelta(days = 1,weeks=2)
ontem = hoje - timedelta(days = 1)
print("Amanha: ", amanha)
print("Ontem: ", ontem)

# diferença entre datas
os.system("cls")
d1 = date(2025,10,2)
d2 = date(2026, 1, 15)
diferenca = d2 - d1
print("diferença em dias: ",diferenca.days)