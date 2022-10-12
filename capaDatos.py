import mysql.connector

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

    def eliminarAlumno(self,legajo):
        con = self.conexion.cursor()
        sql='''DELETE FROM alumno where Apellido = {}'''.format(legajo)
        con.execute(sql)
        self.conexion.commit()
        con.close()
    

