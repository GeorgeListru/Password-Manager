#modul pentru citirea,scrierea json
import json
#modul pentru generarea numerelor random
import random
#modul pentru crearea interfetei grafice
import tkinter as tk
from tkinter import messagebox
#modul pentru trimiterea sms-urilor pe telefon
from twilio.rest import Client
#modul pentru copierea pe clipboard
import pyperclip

#in caz ca dorim ca entry-urile sa contina niste valori implicite, putem indica email-ul si telefonul
#in aceste 2 variabile
default_email = ""
default_phone = ""

#Date pentru conectarea cu twilio printr-un API. Va trebui sa introduceti
# datele dumneavoastre personale
account_sid = ''
auth_token = ''
phone_nr = ""

client = Client(account_sid, auth_token)

# Crearea ferestrei Tkinter
window = tk.Tk()
window.title("Password Manager")
window.config(padx=20, pady=20)

# Plasarea logo.png in fereastra
canvas = tk.Canvas(width=250, height=250)
logo = tk.PhotoImage(file="logo.png")
logo = logo.zoom(15)
logo = logo.subsample(32)
canvas.create_image(125, 125, image=logo)
canvas.grid(row=0, column=0, columnspan=3)

# Crearea label-urilor pentru website, email si password si folosirea
# grid-ului pentru plasarea in fereastra
websiteLabel = tk.Label(font=("Calibri", 13, "normal"), text="Website: ")
websiteLabel.grid(row=1, column=0)

EmailLabel = tk.Label(font=("Calibri", 13, "normal"), text="Username/Email: ")
EmailLabel.grid(row=2, column=0)

PasswordLabel = tk.Label(font=("Calibri", 13, "normal"), text="Password: ")
PasswordLabel.grid(row=3, column=0)

# Crearea Input-urilor pentru website, email si password si folosirea
# grid-ului pentru plasarea in fereastra
websiteInput = tk.Entry(width=24)
websiteInput.grid(row=1, column=1)
websiteInput.focus()

EmailInput = tk.Entry(width=36)
EmailInput.grid(row=2, column=1, columnspan=2)
EmailInput.insert(tk.END, string=default_email)

PasswordInput = tk.Entry(width=24)
PasswordInput.grid(row=3, column=1)


#Definirea unei functii ce cauta website-ul in baza de date json
def searchWebsite():
    try:
        #deschiderea fisierului
        with open("myPasswords.json", "r") as file:
            myData = json.load(file)#preluarea datelor folosind metoda load in modulul json
            dataToDisplay = myData[websiteInput.get()]
            #afisarea informatiilor intr-un messagebox odata ce au fost gasite
            myInfo = messagebox.showinfo(title="Your info", message=f"Website: {websiteInput.get()}"
                                                                    f"\nEmail: {dataToDisplay['email']}"
                                                                    f"\nPassword: {dataToDisplay['password']}")
            #copierea pe clipboard a parolei
            pyperclip.copy(dataToDisplay["password"])
    #in caz ca fisierul nu a fost gasit, vom afisa un messagebox cu un mesaj corespunzator
    except FileNotFoundError:
        messagebox.showinfo(title="Error", message="Fisierul salvarilor este gol")
    #in caz ca website-ul nu a fost gasit in baza de date, vom afisa un messagebox cu un mesaj corespunzator
    except KeyError:
        messagebox.showinfo(title="Error", message="Acest website nu exista in baza de date")

#plasarea butonului de cautare ce executa functia de mai sus
searchButton = tk.Button(text="Search", command=searchWebsite)
searchButton.grid(row=1, column=2, sticky="nsew")

#Crearea unei functii ce are ca scop generarea unei parole random
def generatePass():
    #stergerea continutului inputului de parola
    PasswordInput.delete(0, tk.END)
    #definirea posibilitatilor de litere ale parolei
    passLetters = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t",
                   "u", "v", "w", "x", "y", "z"]
    passNumbers = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "0"]
    passSymbols = ["!", "@", "#", "$", "%", "^", "&", "*", "(", ")", "_", "-", "+", "=", ";", "", ":", "<", ">", ",",
                   ".", "/", "?"]
    passList = []
    #parola va contine intre 4 si 8 litere
    for _ in range(0, random.randint(4, 8)):
        if random.randint(0, 1) == 1:
            passList.append(random.choice(passLetters))
        else:
            passList.append(random.choice(passLetters).capitalize())
    #parola va contine intre 1 si 3 cifre
    for _ in range(0, random.randint(1, 3)):
        passList.append(random.choice(passNumbers))
    #parola va contine intre 1 si 2 simboluri
    for _ in range(0, random.randint(1, 2)):
        passList.append(random.choice(passSymbols))
    #amestecarea caracterelor in parola
    random.shuffle(passList)
    password = ""
    for i in range(len(passList)):
        password += passList[i]
    #inserarea parolei in entry
    PasswordInput.insert(tk.END, password)
    #copierea parolei in clipboard
    pyperclip.copy(password)

#crearea botunului de generare a parolei ce executa functia de mai sus
generateButton = tk.Button(text="Generate", command=generatePass)
generateButton.grid(row=3, column=2, padx=4, sticky="nsew")

#Crearea unei functii ce salveaza continutul din entry-uri in fisierul myPasswords.json
def Save(*args):
    myData = {args[0]: {
        "email": args[1],
        "password": args[2]
    }}
    try:
        #in caz ca fisierul exista, vom copia intreg continutul
        with open("myPasswords.json", "r") as file:
            dataFromFile = json.load(file)
    except FileNotFoundError:
        #in caz ca nu, vom crea un fisier nou
        with open("myPasswords.json", "w") as file:
            json.dump(myData, file, indent=4)
    else:
        #in caz ca exista, vom continua operatia din blocul try
        #si vom actualiza fisierul cu noile valori
        dataFromFile.update(myData)
        with open("myPasswords.json", "w") as file:
            json.dump(dataFromFile, file, indent=4)

#Functia are ca scop afisarea tuturor mesajelor corespunsatoare pentru conformarea
#datelor introduse in entry-uri
def SaveData():
    #verificarea daca continutul entry-urilor este valid
    if len(websiteInput.get()) != 0 and len(EmailInput.get()) != 0 and len(PasswordInput.get()) != 0:
        #afisarea unui messagebox pentru a confirma decizia de salvare a datelor
        sure = messagebox.askokcancel(title=websiteInput.get(), message=f"Esti sigur?\nWebsite: {websiteInput.get()}"
                                                                        f"\nEmail: {EmailInput.get()}\nPassword:"
                                                                        f" {PasswordInput.get()}")
        #in caz ca utilizatorul confirma, datele vor fi salvate, iar entry-urile - resetate
        if sure:
            Save(websiteInput.get(), EmailInput.get(), PasswordInput.get())
            websiteInput.delete(0, tk.END)
            PasswordInput.delete(0, tk.END)
            pyperclip.copy(PasswordInput.get())
    #in caz ca continutul entry-urilor este invalid, va fi afisat un messagebox column
    #un mesaj corespunzator
    else:
        messagebox.showinfo(title="Error!", message="Unul sau mai multe campuri sunt goale")

#Plasarea butonului de adaugare a parolei
addButton = tk.Button(text="Add", command=SaveData)
addButton.grid(row=4, column=1, columnspan=2, pady=5, sticky="nsew")

#Functia are a scop trimiterea unui SMS pe telefonul utlizatorului cu datele
#website-ului introdus in entry
def sendToPhone():
    #afisarea unei casute in care utilizatorul va introduce numarul de telefon
    top=tk.Toplevel(window)
    label = tk.Label(top,font=("Calibri", 13, "normal"), text="Introduceti numarul: ", width=30, pady=10)
    label.pack()
    entry = tk.Entry(top, width=30,)
    entry.insert(tk.END, string=default_phone)
    entry.pack()

    def sendSMS():
        #preluam numarul din entry
        number = entry.get()
        #verificam daca numarul este valid
        if number.replace("+","").isdecimal():
            #in caz ca utilizatorul nu a introdus codul tarii (+373), programul il va adauga
            #cu scopul de a trimite SMS-ul cu succes
            if "*" not in number:
                number = "+373"+number
            #Incercarea preluarii datelor website-ului din baza de date JSON
            try:
                #preluarea datelor website-ului din baza de date
                with open("myPasswords.json", "r") as file:
                    myData = json.load(file)
                    dataToDisplay = myData[websiteInput.get()]
                    #trimiterea SMS-ului catre numarul introdus de utilizator cu datele despre website
                    message = client.messages.create(
                    body=f"\nWebsite: {websiteInput.get()}\nEmail:{dataToDisplay['email']}\nPassword:{dataToDisplay['password']}",
                    from_= phone_nr,
                    to = number
                    )
            #in caz ca baza de date JSON nu exista, vom afisa un messagebox cu un mesaj corespunzator
            except FileNotFoundError:
                messagebox.showinfo(title="Error", message="Fisierul salvarilor este gol!")
            except KeyError:
                #in caz ca utilizatorul nu a introdus niciun entry, vom afisa un messagebox cu un mesaj corespunzator
                if len(websiteInput.get()) == 0:
                    messagebox.showinfo(title="Error", message="Introduceti un website in entry")
                #in caz ca website-ului nu exista in baza de date, vom afisa un messagebox cu un mesaj corespunzator
                else:
                    messagebox.showinfo(title="Error", message="Acest website nu exista in baza de date")
            #in caz ca nu primim nicio eroare listata mai sus, cel mai probabil numarul introdus este invalid,
            #deci vom afisa un messagebox cu un mesaj corespunzator
            except:
                messagebox.showinfo(title="Error", message="Numarul introdus este invalid")
            #indiferent de rezultat, vom inchide casuta de introducere a numarului de telefon
            top.destroy()

    #plasarea butonului de trimitere a SMS-ului ce executa comanda sendSMS
    button = tk.Button(top, text="Send",command=sendSMS, width=30)
    button.pack()
    tk.Label(top, pady=5).pack()
#plasarea butonului de trimitere pe telefon ce porneste functia sendToPhone
sendToPhone = tk.Button(text="Send to your Phone", command=sendToPhone)
sendToPhone.grid(row=5, column=0, columnspan=3, sticky="nsew", pady=5)

#metoda mainloop are ca scop mentinerea ferestrei deschise
window.mainloop()
