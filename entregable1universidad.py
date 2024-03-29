from enum import Enum



class Sexo(Enum):
        V = 1
        M = 2
    

class Persona:
    def __init__(self, nombre, dni, direccion, sexo):
        self.nombre = nombre
        self.dni = dni
        self.direccion = direccion
        self.sexo = sexo


class Asignatura:
    def __init__(self, nombre, codigo):
        self.nombre = nombre
        self.codigo = codigo

class Departamento(Enum):
        DIIC = 1
        DITEC= 2
        DIS=3
        
class MiembroDepartamento(Persona):
    def __init__(self, nombre, dni, direccion, sexo, departamento):
        super().__init__(nombre, dni, direccion, sexo)
        self.departamento = departamento
    def cambiodepartamento(self, nuevodepartamento):
        self.departamento=nuevodepartamento
        
    def __str__(self):
        return f"Nombre: {self.nombre}, Edad: {self.dni}, Direccion: {self.direccion}, Sexo: {self.sexo}, Departamento: {self.departamento}"


class Investigador(MiembroDepartamento):
    def __init__(self, nombre, dni, direccion, sexo, area_investigacion):
        super().__init__(nombre, dni, direccion, sexo)
        self.area_investigacion = area_investigacion
        
        

class Profesor(MiembroDepartamento):
    def __init__(self, nombre, dni, direccion, sexo, asignaturas):
        super().__init__(nombre, dni, direccion, sexo)
        self.asignaturas = asignaturas
        
class Asociado(Profesor):
    def __init__(self, nombre, dni, direccion, sexo):
        super().__init__(nombre, dni, direccion, sexo)
        
class Titular(Profesor, Investigador):
    def __init__(self, nombre, dni, direccion, sexo, area_investigacion):
        super(Profesor).__init__(nombre, dni, direccion, sexo)
        super(Investigador).__init__(area_investigacion)


class Estudiante(Persona):
    def __init__(self, nombre, dni, direccion, sexo):
        super().__init__(nombre, dni, direccion, sexo)
    def __str__(self):
        return f"Nombre: {self.nombre}, Edad: {self.dni}, Direccion: {self.direccion}, Sexo: {self.sexo}"


class Universidad:
    def __init__(self, nombre, ubicacion):
        self.nombre=nombre
        self.ubicacion=ubicacion
        self.listaalumno = []
        self.listamiembros = []
    def añadir_miembrodep(self,nombre, dni, direccion, sexo, departamento):
        for i in self.listamiembros:
            if (i.nombre == nombre):
                print ("Miembro de departamento <"+nombre+"> ya exite")
                return
        self.listamiembros.append(MiembroDepartamento(nombre, dni, direccion, sexo, departamento))    
        
    def eliminar_miembrodep(self,nombre, dni, direccion, sexo, departamento):
        for c in self.listamiembros:
            if (c.nombre == nombre):
                self.listamiembros.remove(MiembroDepartamento(nombre, dni, direccion, sexo, departamento))
                return
        print ("Miembro de departamento <"+nombre+"> no exite")

    def añadir_alumno(self, nombre, dni, direccion, sexo):
        for i in self.listaalumno:
            if (i.nombre == nombre):
                print ("Alumno <"+nombre+"> ya exite")
                return
        self.listaalumno.append (Estudiante(nombre, dni, direccion, sexo))
        
    def eliminar_alumno(self, nombre, dni, direccion, sexo):
        for c in self.listaalumno:
            if (c.nombre == nombre):
                self.listaalumno.remove(Estudiante(nombre, dni, direccion, sexo))
                return
        print ("Alumno <"+nombre+"> no exite")
        
        
    def cambio_departamento(self, nombre, dni, direccion, sexo, departamento, nuevodepartamento):
        if nuevodepartamento in [Departamento.DIIC,Departamento.DITEC,Departamento.DIS]:
            for c in self.listamiembros:
                if (c.nombre == nombre):
                    MiembroDepartamento(nombre, dni, direccion, sexo, departamento).cambiodepartamento(nuevodepartamento)
                    return
            print ("Miembro de departamento <"+nombre+"> no exite")
        else:
            print("El nuevo departamento introducido <"+nuevodepartamento+"> no existe")
            
    def mostrar_miembros(self):
        if self.listamiembros == []:
            print(f"No hay miembros de departamento todavía")          
        else:
            print("La lista de miembros de departamento es: ")
            for i in self.listamiembros:
                print(i)
    def mostrar_alumnos(self):
        if self.listaalumno == []:
            print("No hay alumnos todavía")          
        else:
            print("La lista de alumnos es: ")
            for i in self.listaalumno:
                print(i)
            



umu = Universidad ("Universidad de Murcia", "Espinardo, Murcia")

umu.añadir_alumno ("Lucas","3452566A", "Av del Campo 13",  Sexo.V)
umu.añadir_alumno ("Marcos","6326725G", "Carril torremolina", Sexo.V)
umu.añadir_alumno ("Lucia","2398409P", "Calle abe",  Sexo.M)
umu.mostrar_alumnos()


umu.añadir_miembrodep ("Fernando","2183293Ñ", "Carril lobo", Sexo.V ,Departamento.DIIC )
umu.añadir_miembrodep ("Pepe","3267836P", "Calle ñoro",  Sexo.V,Departamento.DITEC)
umu.añadir_miembrodep ("Carlota","3467387Y", "Calle radamel falcao", Sexo.M, Departamento.DIS)
umu.mostrar_miembros()

umu.eliminar_alumno("Marcos","6326725G", "Carril torremolina", Sexo.V)   #esto no va porque la llista tiene objetosy no lo identifica 
umu.eliminar_miembrodep("Carlota","3467387Y", "Calle radamel falcao", Sexo.M, Departamento.DIS)
umu.eliminar_alumno("Marlucas","322346U", "Carril piruleta",  Sexo.V)
umu.eliminar_miembrodep("Lolalolita","438I", "Calle bartolo", Sexo.V, Departamento.DIS)

umu.cambio_departamento("Fernando","2183293Ñ", "Carril lobo", Sexo.V ,Departamento.DIIC, Departamento.DIS )     #esto no lo actualiza

umu.mostrar_alumnos()
umu.mostrar_miembros()

