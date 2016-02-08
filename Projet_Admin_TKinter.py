from tkinter import *
import json

class App(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent)
        self.pack()
        self.createWidgets()

    def createWidgets(self):
        land = Label(self, text='Name of the country')
        land.pack()
        self.landValue = Entry(self)
        self.landValue.pack()
        capital = Label(self, text='Capital of the country')
        capital.pack()
        self.capitalValue = Entry(self)
        self.capitalValue.pack()
        population = Label(self, text='Population of the country')
        population.pack()
        self.populationValue = Entry(self)
        self.populationValue.pack()
        superficy = Label(self, text='Area of the country')
        superficy.pack()
        self.superficyValue = Entry(self)
        self.superficyValue.pack()
        currency = Label(self, text='Currency of the country')
        currency.pack()
        self.currencyValue = Entry(self)
        self.currencyValue.pack()
        flag = Label(self, text='Flag of the country')
        flag.pack()
        self.flagValue = Entry(self)
        self.flagValue.pack()
        language = Label(self, text='Language of the country')
        language.pack()
        self.languageValue = Entry(self)
        self.languageValue.pack()
        visit = Label(self, text='Have you ever been ?')
        visit.pack()
        self.visitValue = Entry(self)
        self.visitValue.pack()
        add = Button(self, text='add', command = self.addcountry)
        add.pack()


    def addcountry(self):

        dicocountry = {}
        with open ('fichierpays.txt', 'r') as file:
            Database = json.loads(file.read())

        with open ('fichierpays.txt', 'w') as file:

            dicocountry = {'capital': self.capitalValue.get(), 'population': self.populationValue.get(), 'superficy': self.superficyValue.get(), 'currency': self.currencyValue.get(),'flag': self.flagValue.get(),  'language': self.languageValue.get(),'visit': self.visitValue.get()== 'oui'}
            Database[self.landValue.get()] = dicocountry
            file.write(json.dumps(Database,ensure_ascii=False,sort_keys=True,indent=4))
        window.destroy()




window =Tk()
app = App(window)
window.title('ajouter un pays')
app.mainloop()


'''window =Tk()

text = Label(window, text='Tell me a country')
text.pack()

land = Entry(window).pack()

window.title('ajouter un pays')
window.mainloop()'''