import openpyxl
wb = openpyxl.load_workbook(filename = 'pattern.xlsx')

sheet1 = wb['Шаблоны Photolab (2020-02-10)']
sheet2 = wb['Лист1']

effects = set()

for i in range(3, 1771, 1):
    name = sheet1['A' + str(i)].value
    id = sheet1['C' + str(i)].value
    if id:
        effects.add((name, int(id)))
    else:
        effects.add((name, 'no_id'))

for i in range(3, 2022, 1):
    name = sheet2['A' + str(i)].value
    id = sheet2['C' + str(i)].value
    if id:
        effects.add((name, int(id)))
    else:
        effects.add((name, 'no_id'))
f = open("effects.txt", "w+")
for tuple in effects:
    f.write(str(tuple[0]) + ' ' + str(tuple[1]) + '\n')
f.close()
print(len(effects))
