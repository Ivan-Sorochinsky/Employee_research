import glob, os, csv, sqlite3

path = 'C:\csv_db'

#csv_reader
def csv_reader():
    project_list = [] #список кортежей
    # перебор всех csv файлов в папке C:\csv_db
    for filePath in glob.glob(os.path.join(path, '*.csv')):
        csvFile = open(filePath, encoding='windows-1251')
        csvReader = csv.reader(csvFile, delimiter=',')
        next(csvReader) #переход на следующую строку
        for row in csvReader:
            list_row = []
            for value in row:
                list_row.append(value)
            #print(list_row) #test list_row
            tuple_row = tuple(list_row) #преобразование списка в кортеж, необходимо для бд
            project_list.append(tuple_row)
        csvFile.close()
    return project_list

#csv_writer (csv many to one)
def csv_writer():
    csvFile = open('out.csv', 'w', encoding='windows-1251', newline='')
    csvWriter = csv.writer(csvFile, delimiter=',')

    for row in csv_reader():
        csvWriter.writerow(row)

    csvFile.close()

#SQLite connect
conn = sqlite3.connect('db.db')
cursor = conn.cursor() #объект для отправки запросов и обработки результатов
#запрос на чтение из бд
cursor.execute("SELECT * FROM Project")
#получение результата запроса
results = cursor.fetchall()
print(results)
print(csv_reader())

#запрос на запись в бд
cursor.executemany("insert into Project values (?,?,?,?,?,?);", csv_reader())
#сортировка по дате сдачи проекта
cursor.execute("SELECT * FROM 'Project' ORDER BY 'Дата сдачи' DESC;")
#сохраняем транзакцию
conn.commit()
conn.close() #connect off


# CREATE TABLE "Project" (
# 	"Название проекта"	TEXT,
# 	"Руководитель"	TEXT,
# 	"Дата сдачи"	TEXT,
# 	"Иванов"	INTEGER,
# 	"Петров"	INTEGER,
# 	"Сидоров"	INTEGER
# );

#сортировка по дате сдачи проекта
#SELECT * FROM "Project" ORDER BY "Дата сдачи" DESC
#нужно писать свой метод сортировки, т.к. СУБД не поддерживает данную функцию (отсутствует тип date)
#sqlite->csv = pandas