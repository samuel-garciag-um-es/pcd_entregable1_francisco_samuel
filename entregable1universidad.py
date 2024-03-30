from enum import Enum
from abc import ABCMeta, abstractmethod

class Sexo(Enum):
        V = 1
        M = 2

class Persona(metaclass=ABCMeta):
    def __init__(self, nombre, dni, direccion, sexo):
        self.nombre = nombre
        self.dni = dni
        self.direccion = direccion
        self.sexo = sexo

    @abstractmethod
    def __str__(self):
        pass

    # def __eq__(self, other):
    #     if isinstance(other, Persona):
    #         return self.dni == other.dni
    #     return False

class Asignatura:
    def __init__(self, nombre, codigo):
        self.nombre = nombre
        self.codigo = codigo

    def __str__(self):
        return f"Nombre: {self.nombre}, Código: {self.codigo}"
    
    def __eq__(self, otro):
        if isinstance(otro, Asignatura):
            return self.codigo == otro.codigo
        return False

class Departamento(Enum):
        DIIC = 1
        DITEC = 2
        DIS = 3
        
class MiembroDepartamento(Persona):
    def __init__(self, nombre, dni, direccion, sexo, departamento):
        Persona.__init__(self, nombre, dni, direccion, sexo)
        if not isinstance(departamento, Departamento):
            raise TypeError("El departamento debe ser de la clase Departamento")
        self.departamento = departamento
        
    def cambiodepartamento(self, nuevodepartamento):
        if isinstance (nuevodepartamento, Departamento):
            self.departamento = nuevodepartamento
        else:
            raise TypeError("El departamento debe ser de la clase Departamento")
      
    @abstractmethod
    def __str__(self):
        pass

    def __eq__(self, other):
        if isinstance(other, MiembroDepartamento):
            return self.dni == other.dni
        return False

class Investigador(MiembroDepartamento):
    def __init__(self, nombre, dni, direccion, sexo, departamento, area_investigacion):
        MiembroDepartamento.__init__(self, nombre, dni, direccion, sexo, departamento)
        self.area_investigacion = area_investigacion
    
    def __eq__(self, other):
        if isinstance(other, Investigador):
            return self.dni == other.dni
        return False
    
    def __str__(self):
        return f"Nombre: {self.nombre}, DNI: {self.dni}, Dirección: {self.direccion}, Sexo: {self.sexo.name}, Departamento: {self.departamento.name}, Área: {self.area_investigacion}, Rol: Investigador"

class Profesor(MiembroDepartamento):
    def __init__(self, nombre, dni, direccion, sexo, departamento, asignaturas):
        MiembroDepartamento.__init__(self, nombre, dni, direccion, sexo, departamento)
        if not isinstance(asignaturas, list):       #permite pasar tanto 1 como n instancias de Asginatura
            asignaturas = [asignaturas]
        for asignatura in asignaturas:
            if not isinstance(asignatura, Asignatura):
                raise TypeError("Las asignaturas deben ser instancias de la clase Asignatura")
        self.asignaturas = asignaturas

    def __eq__(self, other):
        if isinstance(other, Profesor):
            return self.dni == other.dni
        return False

    @abstractmethod
    def __str__(self):
        pass

class Asociado(Profesor):
    def __init__(self, nombre, dni, direccion, sexo, departamento, asignaturas):
        Profesor.__init__(self, nombre, dni, direccion, sexo, departamento, asignaturas)

    def __eq__(self, other):
        if isinstance(other, Asociado):
            return self.dni == other.dni
        return False

    def __str__(self):
        asignaturas_str = ["; ".join(str(asignatura) for asignatura in self.asignaturas)]
        return f"Nombre: {self.nombre}, DNI: {self.dni}, Dirección: {self.direccion}, Sexo: {self.sexo.name}, Departamento: {self.departamento.name}, Asignaturas: {asignaturas_str}, Rol: Profesor asociado"
            
class Titular(Profesor, Investigador):                                      # hay que ver lo del departamento
    def __init__(self, nombre, dni, direccion, sexo, departamento, asignaturas, area_investigacion):
        Profesor.__init__(self, nombre, dni, direccion, sexo, departamento, asignaturas)
        Investigador.__init__(self, nombre, dni, direccion, sexo, departamento, area_investigacion)

    def __eq__(self, other):
        if isinstance(other, Titular):
            return self.dni == other.dni
        return False
    
    def __str__(self):
        asignaturas_str = ["; ".join(str(asignatura) for asignatura in self.asignaturas)]
        return f"Nombre: {self.nombre}, DNI: {self.dni}, Dirección: {self.direccion}, Sexo: {self.sexo.name}, Departamento: {self.departamento.name}, Asignaturas: {asignaturas_str}, Área: {self.area_investigacion}, Rol: Profesor titular"


class Estudiante(Persona):
    def __init__(self, nombre, dni, direccion, sexo, asignaturas):
        Persona.__init__(self, nombre, dni, direccion, sexo)
        if not isinstance(asignaturas, list):       #permite pasar tanto 1 como n instancias de Asginatura
            asignaturas = [asignaturas]
        for asignatura in asignaturas:
            if not isinstance(asignatura, Asignatura):
                raise TypeError("Las asignaturas deben ser instancias de la clase Asignatura")
        self.asignaturas = asignaturas

    def __str__(self):
        asignaturas_str = ["; ".join(str(asignatura) for asignatura in self.asignaturas)]
        return f"Nombre: {self.nombre}, Edad: {self.dni}, Direccion: {self.direccion}, Sexo: {self.sexo.name}, asignaturas {asignaturas_str}, Rol: Estudiante"
    
    def __eq__(self, other):
        if isinstance(other, Estudiante):
            return self.dni == other.dni
        return False

class Universidad:
    def __init__(self, nombre, ubicacion):
        self.nombre = nombre
        self.ubicacion = ubicacion
        self.listaalumno = []
        self.listamiembros = []
    
    def añadir_miembrodep(self, miembro):
        for i in self.listamiembros:
            if (i.dni == miembro.dni):
                print ("Miembro de departamento <"+miembro.nombre+"> ya existe")                   
                return
        self.listamiembros.append(miembro)
    
    def eliminar_miembrodep(self, miembro):
        for i in self.listamiembros:
            if (i.dni == miembro.dni):
                self.listamiembros.remove(miembro)
                return
        print ("Miembro de departamento <"+miembro.nombre+"> no existe")

    def añadir_alumno(self, alumno):
        for i in self.listaalumno:
            if (i.dni == alumno.dni):
                print ("Alumno <"+alumno.nombre+"> ya existe")
                return
        self.listaalumno.append(alumno)
        
    def eliminar_alumno(self, alumno):
        for i in self.listaalumno:
            if (i.dni == alumno.dni):
                self.listaalumno.remove(alumno)
                return
        print ("Alumno <"+alumno.nombre+"> no existe")

    def cambio_departamento(self, miembro, nuevodepartamento):
        encontrado = False
        i = 0
        while i < len(self.listamiembros) and not encontrado:
            if self.listamiembros[i] == miembro:
                self.listamiembros[i].cambiodepartamento(nuevodepartamento)
                encontrado = True
                print(f"Se ha actualizado el departamento del miembro con DNI {miembro.dni}.")
            i += 1
        
        if not encontrado:
            print(f"No se encontró ningún miembro con el DNI {miembro.dni}.")
            
    def mostrar_miembros(self):
        if not self.listamiembros:
            print("No hay miembros de departamento todavía")          
        else:
            print("La lista de miembros de departamento es: ")
            print('\n'.join(str(miembro) for miembro in self.listamiembros))

    def mostrar_alumnos(self):
        if not self.listaalumno:
            print("No hay alumnos todavía")          
        else:
            print("La lista de alumnos es: ")
            print('\n'.join(str(alumno) for alumno in self.listaalumno))
    
    def mostrar_asignaturas_profesor(self,persona=None):
        if persona != None:
            if persona.asignaturas == []:
                print(f"{persona.nombre} no tiene asignaturas")
            elif isinstance(persona, Profesor):
                print(f"Lista de asignaturas del profesor {persona.nombre}: ", end="")
                for i in range(len(persona.asignaturas) - 1):
                    print(f"{persona.asignaturas[i]}; ", end="")
                print(persona.asignaturas[-1])
            else:
                raise TypeError("El parámetro debe ser de la clase Profesor")
        else:
            for miembro in self.listamiembros:
                if isinstance(miembro, Profesor):
                    self.mostrar_asignaturas_profesor(miembro)

    def mostrar_asignaturas_alumno(self,persona=None):
        if persona != None:
            if persona.asignaturas == []:
                print(f"{persona.nombre} no tiene asignaturas")
            elif isinstance(persona, Estudiante):
                print(f"Lista de asignaturas del estudiante {persona.nombre}: ", end="")
                for i in range(len(persona.asignaturas) - 1):
                    print(f"{persona.asignaturas[i]}; ", end="")
                print(persona.asignaturas[-1])
            else:
                raise TypeError("El parámetro debe ser de la clase Estudiante")
        else:
            for estudiante in self.listaalumno:
                self.mostrar_asignaturas_alumno(estudiante)

    def añadir_asignatura(self,profesor,asignatura):
        if isinstance(profesor, Profesor):
            if isinstance(asignatura, Asignatura):
                profesor.asignaturas.append(asignatura)
            else:
                raise TypeError("Asignatura tiene que ser de la clase Asignatura")
        else:
            raise TypeError("Profesor tiene que ser de la clase Profesor")

    def eliminar_asignatura(self,profesor,asignatura):
        if isinstance(profesor, Profesor):
            if isinstance(asignatura, Asignatura):
                profesor.asignaturas.remove(asignatura)
            else:
                raise TypeError("Asignatura tiene que ser de la clase Asignatura")
        else:
            raise TypeError("Profesor tiene que ser de la clase Profesor")


# umu = Universidad ("Universidad de Murcia", "Espinardo, Murcia")

# persona1 = Profesor("P1", "DNI1", "D1", Sexo.V, Departamento.DIIC, [Asignatura("nombre",234)])
# persona2 = Titular("P2", "DNI2", "D2", Sexo.M, Departamento.DITEC, Asignatura("nombre",234), "area1")
# persona3 = Investigador("P3", "DNI3", "D3", Sexo.V, Departamento.DIIC, "area2")
# umu.añadir_miembrodep(persona1)
# umu.añadir_miembrodep(persona2)
# umu.añadir_miembrodep(persona3)
# persona4 = Investigador("P3", "DNI3", "D3", Sexo.V, Departamento.DIIC, "area2")
# umu.añadir_miembrodep(persona4)

# umu.cambio_departamento("DNI2", Departamento.DIIC)
# umu.mostrar_miembros()

umu = Universidad ("Universidad de Murcia", "Espinardo, Murcia")

p1 = Estudiante("Lucas","3452566A", "Av del Campo 13",  Sexo.V, [Asignatura("1", 23), Asignatura("2",345)])
marcos = Estudiante("Marcos","6326725G", "Carril torremolina", Sexo.V, Asignatura("ashas",234))
p3=Estudiante("Lucia","2398409P", "Calle abe",  Sexo.M, Asignatura("ashas",234))
umu.añadir_alumno (p1)
umu.añadir_alumno (marcos)
umu.añadir_alumno (p3)
umu.mostrar_alumnos()

p4=Titular("Fernando","2183293Ñ", "Carril lobo", Sexo.V ,Departamento.DIIC,Asignatura("ashas",234),"area1" )
p5=Asociado("Pepe","3267836P", "Calle ñoro",  Sexo.V,Departamento.DITEC, [Asignatura("1", 23), Asignatura("2",345)])
p6=Investigador("Carlota","3467387Y", "Calle radamel falcao", Sexo.M, Departamento.DIS,"area2")
umu.añadir_miembrodep (p4)
umu.añadir_miembrodep (p5)
umu.añadir_miembrodep (p6)
umu.mostrar_miembros()

umu.eliminar_alumno(marcos)   #esto no va porque la llista tiene objetosy no lo identifica 
umu.eliminar_miembrodep(p6)
p7=Estudiante("Marlucas","322346U", "Carril piruleta",  Sexo.V, Asignatura("ds",1231))
umu.eliminar_alumno(p7)
umu.eliminar_miembrodep(p7)

umu.cambio_departamento(p4, Departamento.DIS)     #esto no lo actualiza

umu.mostrar_alumnos()
umu.mostrar_miembros()
umu.mostrar_asignaturas_profesor(p5)
umu.eliminar_asignatura(p5, Asignatura("1", 23))
umu.mostrar_asignaturas_profesor(p5)
umu.mostrar_asignaturas_profesor()
umu.mostrar_asignaturas_alumno()