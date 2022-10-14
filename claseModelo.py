import tkinter as tk
from tkinter import HORIZONTAL, VERTICAL, Button, Entry, Frame, IntVar, Label, Scrollbar, StringVar, Tk, ttk
from tkinter import messagebox
from tkinter import scrolledtext as st
from unicodedata import numeric
from unittest.util import _MAX_LENGTH
from webbrowser import BackgroundBrowser
from capaDatos import *

class Registro(Frame):
    def __init__(self, master, *args,**kwargs):
        super().__init__(master,*args,**kwargs)

        self.frame1= Frame(master)
        self.frame1.grid(columnspan=2,column=0,row=0)

        self.frame2= Frame(master,bg='navy')
        self.frame2.grid(column=0,row=1)

        self.frame3= Frame(master)
        self.frame3.grid(rowspan=2,column=1,row=1)

        self.frame4= Frame(master,bg='black')
        self.frame4.grid(column=0,row=2)

        self.legajo =StringVar()
        self.apellido=StringVar()
        self.nombre=StringVar()
        self.dni=StringVar()
        self.domicilio=StringVar()
        self.buscar=IntVar()


        self.base_datos=RegistroDatos()
        self.create_widgets()

    def create_widgets(self):
        Label(self.frame1, text='Registro \t de \t Datos',bg='gray',fg='white',font=('Orbitron',15,'bold')).grid(column=0,row=0)
        
        Label(self.frame2, text='Agregar nuevos datos',bg='navy',fg='white',font=('Rockwell',12,'bold')).grid(columnspan=2,column=0,row=0,pady=5)
        Label(self.frame2, text='Legajo',bg='navy',fg='white',font=('Rockwell',13,'bold')).grid(column=0,row=1,pady=15)
        Label(self.frame2, text='Apellido',bg='navy',fg='white',font=('Rockwell',13,'bold')).grid(column=0,row=2,pady=15)
        Label(self.frame2, text='Nombre',bg='navy',fg='white',font=('Rockwell',13,'bold')).grid(column=0,row=3,pady=15)
        Label(self.frame2, text='DNI',bg='navy',fg='white',font=('Rockwell',13,'bold')).grid(column=0,row=4,pady=15)
        Label(self.frame2, text='Domicilio',bg='navy',fg='white',font=('Rockwell',13,'bold')).grid(column=0,row=5,pady=15)


        Entry(self.frame2,textvariable=self.legajo,font=('Arial',12)).grid(column=1,row=1,padx=5)
        Entry(self.frame2,textvariable=self.apellido,font=('Arial',12)).grid(column=1,row=2)
        Entry(self.frame2,textvariable=self.nombre,font=('Arial',12)).grid(column=1,row=3)
        Entry(self.frame2,textvariable=self.dni,font=('Arial',12)).grid(column=1,row=4)
        Entry(self.frame2,textvariable=self.domicilio,font=('Arial',12)).grid(column=1,row=5)

        Label(self.frame4, text='Control',bg='black',fg='white',font=('Rockwell',12,'bold')).grid(columnspan=3,column=0,row=0,pady=1,padx=4)
        
        Button(self.frame4,command=self.agregar_datos,text= 'Registrar',font=('Arial',10,'bold'),bg='magenta2').grid(column=0,row=1,pady=10,padx=4)
        Button(self.frame4,command=self.limpiar_campos_tabla,text= 'Limpiar',font=('Arial',10,'bold'),bg='magenta2').grid(column=0,row=2,pady=10,padx=4)
        Button(self.frame4,command=self.eliminar_fila,text= 'Eliminar',font=('Arial',10,'bold'),bg='magenta2').grid(column=0,row=3,pady=10,padx=4)
        Button(self.frame4,command=self.buscar_legajo,text= 'Buscar por Legajo',font=('Arial',10,'bold'),bg='magenta2').grid(column=1,row=4,pady=10,padx=4)
        Entry(self.frame4,textvariable=self.buscar,font=('Arial',12),width=10).grid(column=0,row=4,pady=1,padx=8)
        Button(self.frame4,command=self.mostrar_todo,text= 'Mostrar datos de SQL',font=('Arial',10,'bold'),bg='green2').grid(columnspan=3,column=1,row=1,pady=10,padx=4)

        self.tabla = ttk.Treeview(self.frame3,height=21)
        self.tabla.grid(column=0,row=0)

        ladox= Scrollbar(self.frame3, orient= HORIZONTAL,command=self.tabla.xview)
        ladox.grid(column=0,row=1,sticky='ew')
        ladoy=Scrollbar(self.frame3, orient= VERTICAL,command=self.tabla.yview)
        ladoy.grid(column=1,row=0,sticky='ns')

        self.tabla.configure(xscrollcommand=ladox.set,yscrollcommand=ladoy.set)
        self.tabla['columns'] = ('Apellido','Nombre','DNI','Domicilio')

        #se crea por defecto con el treeview
        self.tabla.column('#0',minwidth=100,width=120,anchor='center')
        self.tabla.column('Apellido',minwidth=100,width=130,anchor='center')
        self.tabla.column('Nombre',minwidth=100,width=130,anchor='center')
        self.tabla.column('DNI',minwidth=100,width=110,anchor='center')
        self.tabla.column('Domicilio',minwidth=100,width=150,anchor='center')

        self.tabla.heading('#0',text='Legajo',anchor='center')
        self.tabla.heading('Apellido',text='Apellido',anchor='center')
        self.tabla.heading('Nombre',text='Nombre',anchor='center')
        self.tabla.heading('DNI',text='DNI',anchor='center')
        self.tabla.heading('Domicilio',text='Domicilio',anchor='center')


        estilo= ttk.Style(self.frame3)
        estilo.theme_use('alt')
        estilo.configure(".",font=('Helvetica',12,'bold'),foreground='red2')
        estilo.configure("Treeview",font=('Helvetica',12,'bold'),foreground='black',background='white')
        estilo.map('Treeview',background=[('selected','green2')],foreground=[('selected','black')])

        self.tabla.bind("<<TreeviewSelect>>",self.obtener_fila)
 
    def agregar_datos(self):
        self.tabla.get_children()
        legajo=self.legajo.get()
        apellido=self.apellido.get()
        nombre=self.nombre.get()
        dni=self.dni.get()
        domicilio=self.domicilio.get()
        datos = (apellido, nombre, dni,domicilio)
        if legajo and apellido and nombre and dni and domicilio !='':
            legajo_numerico(self,legajo)
            dni_numerico(self,dni)
            if self.base_datos.traerDni(dni) is False:
               limpio_Dni(self)
               return
            validar_apellido(self,apellido)
            validar_nombre(self,nombre)
            self.tabla.insert('',0,text=legajo, values=datos)
            self.base_datos.insertar(legajo,apellido,nombre,dni,domicilio)
            limpiar_campos(self)
        else:
            messagebox.showerror(title="Opcion inválida",message="Debe completar todos los campos porque son obligatorios.")

  

    def limpiar_campos_tabla(self):
        self.tabla.delete(*self.tabla.get_children())
        self.legajo.set('')
        self.apellido.set('')
        self.nombre.set('')
        self.dni.set('')
        self.domicilio.set('')

    def buscar_legajo(self):
        legajo=self.buscar.get()
        legajoBuscado=self.base_datos.buscarAlumno(legajo)
        self.tabla.delete(*self.tabla.get_children())
        i=-1
        for dato in legajoBuscado:
            i=i+1 
            self.tabla.insert('',i,text=legajoBuscado[i][1:2],values=legajoBuscado[i][2:6])
    
    def mostrar_todo(self):
        self.tabla.delete(*self.tabla.get_children())
        registro=self.base_datos.mostrar()
        i= -1
        for dato in registro:
            i=i+1
            self.tabla.insert('',i,text=registro[i][1:2], values=registro[i][2:6])

    def eliminar_fila(self):
        fila=self.tabla.selection()
        if len(fila)!=0:
            #legajo=self.legajo.get()
            self.tabla.delete(fila)
            alumno = self.dniBorrar
            self.base_datos.eliminarAlumno(alumno)

    def obtener_fila(self,event):
        current_item= self.tabla.focus()
        if not current_item:
            return
        data = self.tabla.item(current_item)
        self.dniBorrar = data['values'][2]
        #self.apellidoBorrar = data['values'][0]

def limpiar_campos(self):
        self.legajo.set('')
        self.apellido.set('')
        self.nombre.set('')
        self.dni.set('')
        self.domicilio.set('')

def limpio_Dni(self):
     self.dni.set('')

def legajo_numerico(self,legajo):
        while len (legajo) not in range (4,6) or any(num.isalpha() for num in legajo):
            messagebox.showerror(title="Opcion inválida",message="El campo Legajo acepta sólo números. Mínimo de caracteres: 4 y máximo de caracteres: 6")
            self.legajo.set('')
            legajo_numerico(legajo)
        else:
            legajoInt = int(legajo)
            return True

def dni_numerico(self,dni):
        while len (dni) not in range (6, 9) or any(num.isalpha() for num in dni):
            messagebox.showerror(title="Opcion inválida",message="El campo DNI acepta sólo números.Mínimo de caracteres: 6 y máximo de caracteres: 9")
            self.dni.set('')
            dni_numerico(dni)
        else:
            dniInt = int(dni)
            return True
  
def validar_apellido(self,a):
    while (a.isspace() or len(a) <= 2):
        messagebox.showerror(title="Opcion inválida",message="Mínimo de carácteres en Apellido: 2 y no debe comenzar con un espacio")
        self.apellido.set('')
        validar_apellido(a)
    else:
        return True

def validar_nombre(self,a):
    while (a.isspace() or len(a) <= 1):
        messagebox.showerror(title="Opcion inválida",message="Mínimo de carácteres en Nombre: 3 y no debe comenzar con un espacio")
        self.nombre.set('')
        validar_nombre(a)
    else:
        return True
def main():
    ventana= Tk()
    ventana.wm_title=("Registro de Alumnos en Mysql")
    ventana.config(bg='gray22')
    ventana.geometry('1100x600')
    ventana.resizable(0,0)
    app= Registro(ventana)
    app.mainloop()

if __name__ =="__main__":
    main()