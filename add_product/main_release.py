import pandas as pd
import numpy as np


# Функция, заполняющая Датафрейм коэффициентами
def label_koef(row):
   if row['family'] == 'мама':
      return k_mother
   if row["family"] == 'папа':
      return k_father
   if row['family'] == 'сын':
      return k_son
   return k_family

#Считываем таблицу
df = pd.read_excel("C:\List\Products.xlsx")

# df['name'] = ['товар1', 'товар2','товар3','товар4','товар5','товар6','товар7','товар8','товар9','товар10','товар11','товар12','товар13', 'товар14']
# df['family'] = ['семья', 'семья', 'семья', 'семья', 'семья', 'папа', 'папа', 'папа', 'папа', 'мама', 'мама', 'мама', 'сын', 'сын'] 

# Высчитываем основание для деления
Base = df['family'].value_counts()['мама'] + df['family'].value_counts()['папа'] + df['family'].value_counts()['сын'] + 1 # сумма товаров 

# Считаем коэффициенты
k_mother = 1 - (df['family'].value_counts()['мама'] / Base)
k_father = 1 - (df['family'].value_counts()['папа'] / Base)
k_son = 1 - (df['family'].value_counts()['сын'] / Base)
k_family = 1 - (1 / Base)

cheker = k_family + k_father + k_mother + k_son
k_mother = k_mother / cheker
k_father = k_father / cheker
k_son = k_son / cheker
k_family = k_family / cheker

# Проверка суммы, должна быть равна 1
cheker = k_family + k_father + k_mother + k_son
# Применяем функцию для конечного результата
df['koef'] = df.apply(label_koef, axis=1)
# Смотрим промежуточный результат
print(df)
print(Base)
print(cheker)


# Размер матриц(потом будем высчитывать)
size = 5

# Создаем единичные матрицы A, B и C
# A = np.eye(size)
# B = np.eye(size)
# C = np.eye(size)


A = np.random.randint(0, 2, size=(size, size))
B = np.random.randint(0, 2, size=(size, size))
C = np.random.randint(0, 2, size=(size, size))

# Далее идут циклы с опросами
# print("Опрос для папы")
# for i, name in enumerate(df['name']):
#    k = i
#    for j in range(k, size - 1):
#       print(f"Choose {df["name"][i]} - 1 or {df['name'][j+1]} - 0")
#       res = input()
#       if res == '1':            # Первый товар в приоритете
#          A[i][j+1] = 1
#       elif res == '0':
#          A[j+1][i] = 1
#       else:
#          print("неверное значение")

# print("Опрос для мамы")
# for i, name in enumerate(df['name']):
#    k = i
#    for j in range(k, size - 1):
#       print(f"Choose {df["name"][i]} - 1 or {df['name'][j+1]} - 0")
#       res = input()
#       if res == '1':            # Первый товар в приоритете
#          B[i][j+1] = 1
#       elif res == '0':
#          B[j+1][i] = 1
#       else:
#          print("неверное значение")

# print("Опрос для сына")
# for i, name in enumerate(df['name']):
#    k = i
#    for j in range(k, size - 1):
#       print(f"Choose {df["name"][i]} - 1 or {df['name'][j+1]} - 0")
#       res = input()
#       if res == '1':            # Первый товар в приоритете
#          C[i][j+1] = 1
#       elif res == '0':
#          C[j+1][i] = 1
#       else:
#          print("неверное значение")

# Суммируем матрицы A, B и C
D = A + B + C

# Выводим матрицы A, B, C и D (результат суммирования)
print("Матрица Папа:")
print(A)
print("\nМатрица Мама:")
print(B)
print("\nМатрица Cын:")
print(C)
print("\nМатрица D (результат суммирования):")
print(D)


# Считаем сумму строк
count = []
for i, name in enumerate(df['family']):
   count.append(D[i].sum())

df['count'] = count

# Умножаем сумму на коэффициент
df['C3'] = df['count'] * df['koef']
# Считаем норму
norm_base = df['C3'].sum()
df['norm'] = df['C3'] / norm_base
# Считаем ранг и сортируем, основываясь на норме
df["rank"] = df.groupby("family")["norm"].rank(ascending=False) # Сортировка внутри группы
df["rank_all"] = df["norm"].rank(ascending=False) # Общая сортировка

# Создаем ДФ с финальным результатом
fin_df = pd.DataFrame()
fin_df['Наименование'] = df['name']
fin_df['Приоритет'] = df['rank_all']
fin_df.sort_values('Приоритет', inplace=True)

# Проверяем конечный результат
print(df)
print(df['norm'].sum(), 'проверка нормы')
print(fin_df)

# Сохраняем в excel\
fin_df.to_excel("output.xlsx", index=False)
