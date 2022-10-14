from operator import contains
from queue import Empty
import mysql.connector
from tkinter import messagebox as mb

class RegistroDatos:
    def __init__ (self):
        self.conexion=mysql.connector.connect(host="localhost",user="root",
                                    passwd="123456789",database="bddpruebatkinter")
        

    def insertar(self,legajo,apellido,nombre,dni,domicilio):
        con = self.conexion.cursor()
        #LOS NOMBRES DE COLUMNAS TAL CUAL COMO ESTAN EN LA BASE
        sql='''INSERT INTO alumno (Legajo,Apellido,Nombre,DNI,Domicilio)
        VALUES('{}','{}','{}','{}','{}')'''.format(legajo,apellido,nombre,dni,domicilio)
        con.execute(sql)
        self.conexion.commit()
        con.close()
        mb.showinfo(title="Opcion válida",message="Datos almacenados con éxito")
        

    def mostrar(self):
        con = self.conexion.cursor()
        sql="SELECT * FROM alumno"
        con.execute(sql)
        registro = con.fetchall()
        return registro

    def buscarAlumno(self,Legajo_alumno):
        con = self.conexion.cursor()
        sql="SELECT * FROM alumno where Legajo = {}".format(Legajo_alumno)
        con.execute(sql)
        registroX = con.fetchall()
        con.close()
        return registroX

    def eliminarAlumno(self,dni):
        con = self.conexion.cursor()
        sql='''DELETE FROM alumno where DNI = {}'''.format(dni)
        con.execute(sql)
        self.conexion.commit()
        con.close()

    def traerDni(self,dni):
        con = self.conexion.cursor()
        sql="SELECT * FROM alumno where DNI = {}".format(dni)
        con.execute(sql)
        registroX = con.fetchall()
        con.close()
        if len(registroX)>0:            
            mb.showerror(title="Opcion inválida",message="El DNI ingresado existe en la base de datos") 
            return False
        