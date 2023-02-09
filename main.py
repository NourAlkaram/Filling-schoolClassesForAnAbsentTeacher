from pandas import read_csv
from numpy import nan
import tkinter as tk
from tkinter import ttk
import tkinter.font as font
import tkinter.messagebox as msgbox
from tabula import convert_into

class Operation:
    def __init__(self):
        convert_into('doc.pdf' , 'output.csv' , output_format='csv', pages='all')
        self.d = read_csv('output.csv' , encoding='cp1256',names=['c1' , 'c2', 'c3', 'c4', 'c5', 'c6', 'c7' , 'name'])
        self.d =  self.d.fillna(0)
        self.tch = list() #Teacher Names
        cnt = 0
        for i in range (len(self.d['name'])):
            if(cnt%6==0): 
                self.tch.append(self.d['name'][i])
            cnt+=1
                
        self.tchNum = len(self.tch) #Teachers number

    def nullTeacherTable(self , j):
        tb = list()
        for i in range(self.tchNum):
            for k in range(7):
                if(self.d['c'+str(k+1)][(i*6)+j+1]!=0 and self.d['c'+str(k+1)][(i*6)+j+1]!='0'):
                    tb.append(self.tch[i])
        return [*set(tb)]

    def replaceTeacherInClass(self , day , cls):
        tb = list()
        val={'أحد' : 0,
             'اثنين' : 1,
             'ثلاثاء' : 2,
             'أربعاء' : 3,
             'خميس' : 4
            }
        for i in range(self.tchNum):
            if(self.d['c'+str(cls)][(i*6)+val[day]+1] == 0 or self.d['c'+str(cls)][(i*6)+val[day]+1] == '0'):
                tb.append(self.tch[i])
        return tb 

    def checkTeacherClasses(self , teacher , day):
        idx = 0
        for i in range(self.tchNum):
            if self.tch[i] == teacher:
                idx = i
                break
        val={'أحد' : 0,
             'اثنين' : 1,
             'ثلاثاء' : 2,
             'أربعاء' : 3,
             'خميس' : 4
            }
        tchClassList = list()
        for i in range(7):
            if (self.d['c'+str(i+1)][(idx*6)+val[day]+1] != 0  and self.d['c'+str(i+1)][(idx*6)+val[day]+1] != '0'):
                tchClassList.append(7-i)
        return tchClassList


class t1page(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title('Waeel kh')
        self.fnt = font.Font(family='Arial' , size=16)

        self.dayLabel = ttk.Label(self , text=':اختر اليوم' , justify='right' , font=self.fnt)
        self.dayCombo = ttk.Combobox(self, values=['أحد' , 'اثنين' , 'ثلاثاء' , 'أربعاء' , 'خميس'] , justify='center' , width=25)
        self.tchLabel = ttk.Label(self , text=':اختر المعلم' , justify='right' , font=self.fnt)
        self.teacherCombo = ttk.Combobox(self , width=25 , justify='center')
        self.nxt = ttk.Button(self , text='شغل صفوف هذا المعلم' , command=self.next , width=25)

        self.dayLabel.grid(row=0 , column=1)
        self.dayCombo.grid(row=0 , column=0)
        self.tchLabel.grid(row=1 , column=1)
        self.teacherCombo.grid(row=1 , column=0)
        self.nxt.grid(row=4 , column=0)

        self.dayCombo.bind("<<ComboboxSelected>>", self.getData)

    def getData(self , evenet):
        self.ob = Operation()
        val={'أحد' : 0,
             'اثنين' : 1,
             'ثلاثاء' : 2,
             'أربعاء' : 3,
             'خميس' : 4
            }
        day = val[self.dayCombo.get()]
        tb = self.ob.nullTeacherTable(day)
        self.teacherCombo['values'] = tb

    def next(self):
        classList = self.ob.checkTeacherClasses(teacher=self.teacherCombo.get() , day=self.dayCombo.get())
        t2page(teacherName=self.teacherCombo.get() , Day=self.dayCombo.get() , clList=classList , data = self.ob)


class t2page(tk.Tk):
    def __init__(self , teacherName , Day , clList , data):
        tk.Tk.__init__(self)
        fnt = font.Font(family='Arial' , size=16)
        self.teacher = teacherName
        self.day = Day
        self.classes = clList
        self.dta = data
        self.replaceTeachersList = {}
        for i in data.tch:
            self.replaceTeachersList[i]=0
        self.chkdk = {}
        for i in data.tch:
            self.chkdk[i] = list()

        self.title("شغل صفوف المعلم")
        
        self.lableNote = ttk.Label(self , text='قائمة فصول المعلم التي يجب شغلها' , justify='center')
        self.claCombo = ttk.Combobox(self , justify='center' , values=self.classes)
        self.tchCombo = ttk.Combobox(self, justify='center')
        self.lableNote2 = ttk.Label(self, text=':المعلمون المتاحون' , justify='center')
        self.checkbtn = ttk.Button(self , text='سجل المعلم' , command=self.check)
        self.results = ttk.Button(self, text='عرض النتائج' , command=self.finish)

        self.lableNote.grid(row=0 , column=0)
        self.claCombo.grid(row=1 , column=0)
        self.lableNote2.grid(row=2 , column=0)
        self.tchCombo.grid(row=3 , column=0)
        self.checkbtn.grid(row=4 , column=0)
        self.results.grid(row=5 , column=0)

        self.claCombo.bind("<<ComboboxSelected>>", self.getData)
        
    def getData(self , event):
        tb = self.dta.replaceTeacherInClass(day=self.day , cls=8-int(self.claCombo.get()))
        self.tchCombo['values'] = tb
        
    def check(self):
        if (not(self.claCombo.get() in self.chkdk[self.tchCombo.get()])):
            if(self.replaceTeachersList[self.tchCombo.get()]<2):
                self.replaceTeachersList[self.tchCombo.get()]+=1
                self.chkdk[self.tchCombo.get()].append(self.claCombo.get())
            else:
                msgbox.showwarning("Warning", "لقد اخترت هذا المعلم مرتين بالفعل")

    def finish(self):
        t3page(dic=self.chkdk)


class t3page(tk.Tk):
    def __init__(self , dic):
        tk.Tk.__init__(self)
        stri = ''
        for i in dic:
            for j in dic[i]:
                if j!=0:
                    stri+=i+' في الفصل '+j+'\n'
        self.lbl = ttk.Label(self , text=stri , justify='right' , font=('Arial' , 14))
        self.lbl.grid(row=0 , column=0)
        

if __name__ == "__main__":
    app = t1page()
    app.mainloop()