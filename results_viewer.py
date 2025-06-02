import matplotlib.pyplot as plt
import json

with open("results/results_view_speed.json", "r") as fh:
    data = json.load(fh) # загружаем структуру из файла
    print(data)

    d1 = data["1"]
    x1 = []
    y1 = []
    for i in d1:
        x1.append(i[0])
        y1.append(i[1])

    d2 = data["2"]
    x2 = []
    y2 = []
    for i in d2:
        x2.append(i[0])
        y2.append(i[1])
        
plt.plot(x1, y1)
plt.plot(x2, y2)
plt.legend(['act', 'rot'])
plt.show()

print(x1)
print(y1)
print(y2)