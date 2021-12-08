#tfault-tolerant (FT) device (D) schematiC (S) optimization (O) = FTDSO
#Программа оптимизации структурной схемы отказоусточивого глобально-асинхронного локально-произвольного цифрового устройства
#класс схем - глобально-асинхронных локально-синхронных (GALS) от этого зависит функция calc_parameters
#расчеты моделей резервирования выполнены для GALS-схем.
import math
from tkinter import Label, Button, Entry, Canvas, Tk, Grid, Frame
global circuit 
class Circuit():
#При инициализации класса создаем пустое устройство с заданным набором статических параметров:
#напряжение, время работы и интенсивность отказов
    def __init__(self):
        self.device = list()
        self.VOLTAGE = 3
        self.FTdevice = list()
        self.operation_time = 10** 4
        self.failure_rate = 10** -7
#Метод для добавления нового блока в устройство       
    def add_unit(self, unit):
        self.device.append(unit)
#Метод расчета параметров устройства по параметрам его блоков
    def calc_parameters(self, device):
        E = 0
        L = device[0][2]
        P = 1
        for i in range (0, len(device)):
            E += device[i][0]
            P *= device[i][1]
            if device[i][2] > L:
                L = device[i][2]
        return (round(E,2),round(P,2),round(L,2))
 #Метод создания блока - для создания необходимо задать все параметры       
    def unit(self, I, L, n, O, Lt):
        #Параметры схемы I - ток потребляемый схемой
        # P - вероятность безотказной работы блока
        # L - задержка блока
        # n - количество транзисторов в блоке
        # O - количество выходов блока
        # Lt - минимальная задержка эквивалетная задержка 1го инвертера в заданной технологии
        E = round (self.VOLTAGE * I, 2)
        P = round (math.exp(-n * self.failure_rate * self.operation_time), 2)
        unit = E, P, L, n, O, Lt
        return unit
#Метод мажоритарного резервирования 2-из-3 для блока устройства
    def TMR(self, unit):
        t = self.operation_time
        h = self.failure_rate
        Pi = round(math.exp(-unit[3] * h * t), 2)
        Pc = round(math.exp(-10* unit[4] * h * t), 2)
        P = round(((3 * Pi ** 2 - 2 * Pi ** 3) * Pc), 2)
        E = 3 * unit[0] + 28 * unit[4] * self.VOLTAGE
        L = unit[2] + 2.7 * unit[5]
        n = 3 * unit[3] + unit[4] * 10
        O = unit[4]
        Lt = unit[5]
        new_unit = E,P, L, n, O, Lt
        return new_unit
#Метод резервирования на транзисторном уровне для блока устройства
    def TLR(self, unit):
        t = self.operation_time
        h = self.failure_rate
        P = round((math.exp(- 4 * h * t) + 4 * math.exp(-3 * h * t)*(1 - math.exp(-h * t))  )** unit[3], 2)
        E = 2.5 * unit[0] 
        L = unit[2] * 2.5
        n = 4 * unit[3]
        O = unit[4]
        Lt = unit[5]
        new_unit = E, P, L, n, O, Lt
        return new_unit
#Метод комплексного резервирования устройства
    def CR(self):
        #во-первых ищем какая подсхема самая медленная
        FTMethods = list()
        j = 0
        for i in range(1, len(self.device)):           
            Pl = self.device[0][2]
            if self.device[i][2]> Pl:
                Pl = self.device[i][2]
                j = i          
    #затем резервируем оставшиеся
        for i in range (0, len(self.device)):
            if i == j:
                self.FTdevice.append(circuit.TMR(self.device[i]))
                FTMethods.append(f'For unit = {i} TMR choosen')
            else:
                if circuit.TLR(self.device[i])[2] < Pl:
                    self.FTdevice.append(circuit.TLR(self.device[i]))
                    FTMethods.append(f'For unit = {i} TLR choosen')
                else:
                    self.FTdevice.append(circuit.TMR(self.device[i]))
                    FTMethods.append(f'For unit = {i} TMR choosen')
        return FTMethods
#Методы GUI
def add_seq_stage():
    stage = circuit.unit( int(parameters[0].get()),
                        int(parameters[1].get()),
                         int(parameters[2].get()),
                          int(parameters[3].get()),
                           int(parameters[4].get()))
    circuit.add_unit(stage)
    i = len(circuit.device)
    x1 = 10 + (i-1)*70
    x2 = 70 + (i-1)*70
    canvas.create_rectangle(x1,10,x2,80,outline='black', fill='white')
    canvas.create_line(x1-10,45,x1,45)
    canvas.create_text(x2-50,40, text=f'{i-1}')

def complex_redundancy():
    text = circuit.CR()
    i = 0
    for a in text:
        i +=1      
        canvas.create_text(120, 90+i*20, text=a, font=("Times New Roman", 12))

def reset_device():
    circuit.device = list()
    canvas.delete('all')

#Запуск графического интерфейса программы
circuit = Circuit()
window = Tk()  
window.title("FTDSO GALS")  
canvas = Canvas(bg='white')
canvas.grid(column=0,columnspan = 4, row=8)
#Поля данных
lbl1 = Label(window, text="Unit parameters:", font=("Times New Roman", 24))
text_list = ["1) Current consumption, mA",
            "2) Delay, ns",
            "3) Transistors, units.",
            "4) Number of outputs, units.", 
            "5) Minimal delay of logic gate, ns"]
parameters = []
for i in range (0,5):
    lbl = Label(window, text=text_list[i], font=("Times New Roman", 14)) 
    lbl.grid(sticky='W', column=0, row=i+2, columnspan=2)
    txt = Entry(window, width=10)
    txt.insert(0,'0')
    parameters.append(txt)
    txt.grid(sticky='W', column=2, row=i+2)
 
btn1 = Button(window, text="Add unit in device", command=add_seq_stage)
btn2 = Button(window, text="Calculate FTDevice", command=complex_redundancy)
btn_rst = Button(window, text="Rebuild device", command=reset_device)
#Решетка расположения      
lbl1.grid(sticky='W', column=0, row=0,columnspan=2) 
btn1.grid(sticky='W', column=0, row=7) 
btn2.grid(sticky='W', column=1, row=7)     
btn_rst.grid(sticky='W', column=2, row=7)     
#Запуск окно
window.mainloop()

#Пример программы
#Пример №1 расчет параметров для заданного блока
#circuit = Circuit()
#nr = circuit.unit(30,250,100,4,150)
#tmr = circuit.TMR(nr)
#tlr = circuit.TLR(nr)
#print(nr)
#print(tmr)
#print(tlr)
#Пример №2 Добавление двух блоков в устройство и расчет параметров устройства
#circuit.add_unit(nr)
#circuit.add_unit(nr)
#print(circuit.calc_parameters(circuit.device))

#Пример №3 Расчет параметров отказоустойчивого устройства методом комбинированного резервирования
#circuit.CR()
#print(circuit.FTdevice)
