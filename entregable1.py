from enum import Enum
from abc import ABCMeta, abstractmethod

class AsignaturaError(Exception):
    pass

class MiembroError(Exception):
    pass

class EstudianteError(Exception):
    pass

class ListaVacia(Exception):
    pass

class Sexo(Enum):
        V = 1
        M = 2

class Persona(metaclass=ABCMeta):
    def __init__(self, nombre, dni, direccion, sexo):
        try:
            self.nombre = nombre
            self.dni = dni
            self.direccion = direccion
            if isinstance(sexo, Sexo):
                self.sexo = sexo
            else:
                raise TypeError()
        except TypeError as e:
            print("Sexo tiene que ser de la clase Sexo", e)

    @abstractmethod
    def __str__(self):
        pass

class Asignatura:
    def __init__(self, nombre, codigo):
        self.nombre = nombre
        self.codigo = codigo

    def __str__(self):
        return f"Nombre: {self.nombre}, Código: {self.codigo}"
    
    def __eq__(self, otro):
        if isinstance(otro, Asignatura):
            return (self.codigo == otro.codigo) and (self.nombre == otro.nombre)
        return False

class Departamento(Enum):
        DIIC = 1
        DITEC = 2
        DIS = 3
        
class MiembroDepartamento(Persona):
    def __init__(self, nombre, dni, direccion, sexo, departamento):
        try:
            Persona.__init__(self, nombre, dni, direccion, sexo)
            if not isinstance(departamento, Departamento):
                raise TypeError()
            self.departamento = departamento
        except TypeError as e:
            print("El departamento debe ser de la clase Departamento", e)
        
    def cambiodepartamento(self, nuevodepartamento):
        try:
            if isinstance (nuevodepartamento, Departamento):
                self.departamento = nuevodepartamento
            else:
                raise TypeError()
        except TypeError as e:
            print("El departamento debe ser de la clase Departamento", e)

    @abstractmethod
    def __str__(self):
        pass

    def __eq__(self, otro):
        if isinstance(otro, MiembroDepartamento):
            return self.dni == otro.dni
        return False

class Investigador(MiembroDepartamento):
    def __init__(self, nombre, dni, direccion, sexo, departamento, area_investigacion):
        MiembroDepartamento.__init__(self, nombre, dni, direccion, sexo, departamento)
        self.area_investigacion = area_investigacion

    def __eq__(self, otro):
        if isinstance(otro, Investigador):
            return self.dni == otro.dni
        return False

    def __str__(self):
        return f"Nombre: {self.nombre}, DNI: {self.dni}, Dirección: {self.direccion}, Sexo: {self.sexo.name}, Departamento: {self.departamento.name}, Área: {self.area_investigacion}, Rol: Investigador"

class Profesor(MiembroDepartamento):
    def __init__(self, nombre, dni, direccion, sexo, departamento, asignaturas):
        try:
            MiembroDepartamento.__init__(self, nombre, dni, direccion, sexo, departamento)
            if not isinstance(asignaturas, list):       #permite pasar tanto 1 como n instancias de Asginatura
                asignaturas = [asignaturas]
            for asignatura in asignaturas:
                if not isinstance(asignatura, Asignatura):
                    raise TypeError()
            self.asignaturas = asignaturas
        except TypeError as e:
            print("Las asignaturas deben ser instancias de la clase Asignatura", e)

    def añadir_asignatura(self,asignatura):
        try:
            if isinstance(asignatura, Asignatura):
                if asignatura not in self.asignaturas:
                    self.asignaturas.append(asignatura)
                else:
                    print(f"La asignatura ya está registrada para {self.dni}")
            else:
                raise TypeError()
        except TypeError as e:
            print("Asignatura tiene que ser de la clase Asignatura", e)

    def eliminar_asignatura(self,asignatura):
        try:
            if isinstance(asignatura, Asignatura):
                if asignatura in self.asignaturas:
                    self.asignaturas.remove(asignatura)
                else:
                    print(f"La asignatura no está registrada para {self.dni}")
            else:
                raise TypeError()
        except TypeError as e:
            print("Asignatura tiene que ser de la clase Asignatura", e)
    
    def mostrar_asignaturas(self):
        if self.asignaturas == []:
            print(f"{self.dni} no tiene asignaturas")
        else:
            print(f"Lista de asignaturas del profesor {self.dni}: ", end="")
            for i in range(len(self.asignaturas) - 1):
                print(f"{self.asignaturas[i]}; ", end="")
            print(self.asignaturas[-1])
    
    @abstractmethod
    def __str__(self):
        pass

class Asociado(Profesor):
    def __init__(self, nombre, dni, direccion, sexo, departamento, asignaturas):
        Profesor.__init__(self, nombre, dni, direccion, sexo, departamento, asignaturas)

    def __eq__(self, otro):
        if isinstance(otro, Asociado):
            return self.dni == otro.dni
        return False

    def __str__(self):
        asignaturas_str = ["; ".join(str(asignatura) for asignatura in self.asignaturas)]
        return f"Nombre: {self.nombre}, DNI: {self.dni}, Dirección: {self.direccion}, Sexo: {self.sexo.name}, Departamento: {self.departamento.name}, Asignaturas: {asignaturas_str}, Rol: Profesor asociado"
            
class Titular(Profesor, Investigador):
    def __init__(self, nombre, dni, direccion, sexo, departamento, asignaturas, area_investigacion):
        Profesor.__init__(self, nombre, dni, direccion, sexo, departamento, asignaturas)
        Investigador.__init__(self, nombre, dni, direccion, sexo, departamento, area_investigacion)

    def __eq__(self, otro):
        if isinstance(otro, Titular):
            return self.dni == otro.dni
        return False

    def __str__(self):
        asignaturas_str = ["; ".join(str(asignatura) for asignatura in self.asignaturas)]
        return f"Nombre: {self.nombre}, DNI: {self.dni}, Dirección: {self.direccion}, Sexo: {self.sexo.name}, Departamento: {self.departamento.name}, Asignaturas: {asignaturas_str}, Área: {self.area_investigacion}, Rol: Profesor titular"

class Estudiante(Persona):
    def __init__(self, nombre, dni, direccion, sexo, asignaturas):
        try:
            Persona.__init__(self, nombre, dni, direccion, sexo)
            if not isinstance(asignaturas, list):
                asignaturas = [asignaturas]
            for asignatura in asignaturas:
                if not isinstance(asignatura, Asignatura):
                    raise TypeError()
            self.asignaturas = asignaturas
        except TypeError as e:
            print("Las asignaturas deben ser instancias de la clase Asignatura", e)
    
    def añadir_asignatura(self,asignatura):
        try:
            if isinstance(asignatura, Asignatura):
                if asignatura not in self.asignaturas:
                    self.asignaturas.append(asignatura)
                else:
                    print(f"La asignatura ya está registrada para {self.dni}")
            else:
                raise TypeError()
        except TypeError as e:
            print("Asignatura tiene que ser de la clase Asignatura", e)

    def eliminar_asignatura(self,asignatura):
        try:
            if isinstance(asignatura, Asignatura):
                if asignatura in self.asignaturas:
                    self.asignaturas.remove(asignatura)
                else:
                    print(f"La asignatura no está registrada para {self.dni}")
            else:
                raise TypeError()
        except TypeError as e:
            print("Asignatura tiene que ser de la clase Asignatura", e)

    def mostrar_asignaturas(self):
        if self.asignaturas == []:
            print(f"{self.dni} no tiene asignaturas")
        else:
            print(f"Lista de asignaturas del alumno {self.dni}: ", end="")
            for i in range(len(self.asignaturas) - 1):
                print(f"{self.asignaturas[i]}; ", end="")
            print(self.asignaturas[-1])

    def __str__(self):
        asignaturas_str = ["; ".join(str(asignatura) for asignatura in self.asignaturas)]
        return f"Nombre: {self.nombre}, DNI: {self.dni}, Direccion: {self.direccion}, Sexo: {self.sexo.name}, Asignaturas: {asignaturas_str}, Rol: Estudiante"
    
    def __eq__(self, otro):
        if isinstance(otro, Estudiante):
            return self.dni == otro.dni
        return False

class Universidad:
    def __init__(self, nombre, ubicacion):
        self.nombre = nombre
        self.ubicacion = ubicacion
        self._listaalumno = []
        self._listamiembros = []
        self._listaasignaturas = []
    
    def añadir_miembrodep(self, miembro):
        try:
            if miembro not in self._listamiembros:
                if isinstance(miembro, Profesor):
                    for asignatura in miembro.asignaturas:
                        if asignatura not in self._listaasignaturas:
                            raise AsignaturaError()
                self._listamiembros.append(miembro)
                print(f"{miembro.dni} ha sido añadido")
            else:
                raise MiembroError()
        except MiembroError as e:
            print(f"Miembro de departamento {miembro.dni} ya existe", e)
        except AsignaturaError as e:
            print(f"Alguna asignatura no introducida en la lista", e)
    
    def eliminar_miembrodep(self, miembro):
        try:
            if miembro in self._listamiembros:
                self._listamiembros.remove(miembro)
                print(f"{miembro.dni} ha sido eliminado")
            else:
                raise MiembroError()
        except MiembroError as e:
            print (f"Miembro de departamento {miembro.dni} no existe", e)

    def añadir_alumno(self, alumno):
        try:
            if alumno not in self._listaalumno:
                for asignatura in alumno.asignaturas:
                    if asignatura not in self._listaasignaturas:
                        raise AsignaturaError()
                self._listaalumno.append(alumno)
                print(f"{alumno.dni} ha sido añadido")
            else:
                raise EstudianteError()
        except EstudianteError as e:
            print(f"Estudiante {alumno.dni} ya existe", e)
        except AsignaturaError as e:
            print("Alguna asignatura no introducida en la lista", e)
        
    def eliminar_alumno(self, alumno):
        try:
            if alumno in self._listaalumno:
                self._listaalumno.remove(alumno)
                print(f"{alumno.dni} ha sido eliminado")
            else:
                raise EstudianteError()
        except EstudianteError as e:
            print(f"Estudiante {alumno.dni} no existe", e)

    def cambio_departamento(self, miembro, nuevodepartamento):
        try:
            if miembro in self._listamiembros:
                miembro.cambiodepartamento(nuevodepartamento)
                print(f"Se ha actualizado el departamento del miembro con DNI {miembro.dni}.")
            else:
                raise MiembroError()
        except MiembroError as e:
            print(f"No se encontró ningún miembro con el DNI {miembro.dni}", e)
            
    def mostrar_miembros(self):
        if not self._listamiembros:
            print("No hay miembros de departamento todavía")
        else:
            print("La lista de miembros de departamento es: ")
            for miembro in self._listamiembros:
                print(f'\t {str(miembro)}')

    def mostrar_alumnos(self):
        if not self._listaalumno:
            print("No hay alumnos todavía")          
        else:
            print("La lista de alumnos es: ")
            for alumno in self._listaalumno:
                print(f'\t {str(alumno)}')
    
    def mostrar_asignaturas_profesor(self,persona=None):
        try:
            if persona != None:
                if isinstance(persona, Profesor):
                    persona.mostrar_asignaturas()
                else:
                    raise TypeError()
            else:
                for miembro in self._listamiembros:
                    if isinstance(miembro, Profesor):
                        miembro.mostrar_asignaturas()
        except TypeError as e:
            print("El parámetro debe ser de la clase Profesor", e)

    def mostrar_asignaturas_alumno(self,persona=None):
        try:
            if persona != None:
                if isinstance(persona, Estudiante):
                    persona.mostrar_asignaturas()
                else:
                    raise TypeError()
            else:
                for alumno in self._listaalumno:
                    alumno.mostrar_asignaturas()
        except TypeError as e:
            print("El parámetro debe ser de la clase Estudiante", e)

    def añadir_asignatura_persona(self,persona,asignatura):
        try:
            if isinstance(persona, Profesor) or isinstance(persona, Estudiante):
                if asignatura not in self._listaasignaturas:
                    raise AsignaturaError()
                else:
                    persona.añadir_asignatura(asignatura)
            else:
                raise TypeError()
        except TypeError as e:
            print("Persona tiene que ser de la clase Profesor o Estudiante", e)
        except AsignaturaError as e:
            print("Asignatura incorrecta", e)

    def eliminar_asignatura_persona(self,persona,asignatura):
        try:
            if isinstance(persona, Profesor) or isinstance(persona, Estudiante):
                if asignatura not in self._listaasignaturas:
                    raise AsignaturaError()
                else:
                    persona.eliminar_asignatura(asignatura)
            else:
                raise TypeError()
        except TypeError as e:
            print("Persona tiene que ser de la clase Profesor o Estudiante", e)
        except AsignaturaError as e:
            print("Asignatura incorrecta", e)

    def crear_asignatura(self,asignatura):
        try:
            if asignatura in self._listaasignaturas:
                raise AsignaturaError()
            else:
                self._listaasignaturas.append(asignatura)
                print(f"Asignatura {asignatura.codigo} introducida")
        except AsignaturaError as e:
            print('Nombre o código ya en la lista de asignaturas', e)

    def eliminar_asignatura(self, asignatura):
        try:
            if asignatura not in self._listaasignaturas:
                raise AsignaturaError()
            else:
                self._listaasignaturas.remove(asignatura)
                print(f"Asignatura {asignatura.codigo} eliminada")
        except AsignaturaError as e:
            print('La asignatura no se encuentra en la lista', e)

    def mostrar_asignaturas(self):
        if self._listaasignaturas == []:
            print("No hay asignaturas")
        else:
            asignaturas_str = ["; ".join(str(asignatura) for asignatura in self._listaasignaturas)]
            print(f"Lista de asignaturas: {asignaturas_str}")
        
umu = Universidad("Universidad de Murcia", "Espinardo, Murcia")

umu.crear_asignatura(Asignatura("Matematicas", 3))
umu.crear_asignatura(Asignatura("Matematicas", 3))
umu.mostrar_asignaturas()
umu.eliminar_asignatura(Asignatura("No_existe", 20))
umu.eliminar_asignatura(Asignatura("Matematicas", 3))
umu.mostrar_asignaturas()
print("---------------------------------")

umu.crear_asignatura(Asignatura("PCD", 1))
umu.crear_asignatura(Asignatura("SSySS", 3))
umu.crear_asignatura(Asignatura("Matemáticas", 2))
umu.crear_asignatura(Asignatura("BBDD", 5))
p1 = Estudiante("Lucas", "34525662A", "Av del Campo 13", Sexo.V, [Asignatura("PCD", 1), Asignatura("SSySS", 3), Asignatura("None", 213)])
p2 = Estudiante("Marcos", "63267251G", "Carril Pencho", Sexo.V, Asignatura("PCD", 1))
p3 = Estudiante("Lucia", "42398409P", "Calle Garza",  Sexo.M, Asignatura("Matemáticas", 2))
p4 = Titular("Fernando", "21832936L", "Carril Lobo", Sexo.V, Departamento.DIIC, Asignatura("BBDD", 5), "Bases de datos relacionales")
p5 = Asociado("Pepe", "32678360P", "Calle Quevedo",  Sexo.V, Departamento.DITEC, [Asignatura("PCD", 1), Asignatura("Matemáticas", 2)])
p6 = Investigador("Carlota", "33467387N", "Calle Colombia", Sexo.M, Departamento.DIS, "POO")

umu.añadir_alumno(p1)
umu.añadir_alumno(p2)
umu.añadir_alumno(p3)
umu.mostrar_alumnos()
umu.añadir_alumno(p2)
umu.eliminar_alumno(p1)
umu.eliminar_alumno(p4)
umu.mostrar_alumnos()
print("---------------------------------")

umu.añadir_miembrodep(p4)
umu.añadir_miembrodep(p5)
umu.añadir_miembrodep(p6)
umu.mostrar_miembros()
umu.añadir_miembrodep(p4)
umu.eliminar_miembrodep(p5)
umu.eliminar_miembrodep(p5)
umu.mostrar_miembros()
print("---------------------------------")

umu.añadir_alumno(p2)
umu.añadir_asignatura_persona(p2,Asignatura("PCD", 1))
umu.añadir_asignatura_persona(p2,Asignatura("Matemáticas", 2))
umu.añadir_asignatura_persona(p2,Asignatura("Hola", 3))
umu.mostrar_asignaturas_alumno()
umu.mostrar_asignaturas_alumno(p2)

umu.añadir_miembrodep(p5)
umu.añadir_asignatura_persona(p5,Asignatura("PCD", 1))
umu.añadir_asignatura_persona(p5,Asignatura("Matemáticas", 2))
umu.añadir_asignatura_persona(p5,Asignatura("Hola", 3))
umu.mostrar_asignaturas_profesor()
umu.mostrar_asignaturas_profesor(p5)
print("---------------------------------")

umu.añadir_miembrodep(p5)
umu.mostrar_miembros()
umu.cambio_departamento(p5,"Departamento")
umu.cambio_departamento(p2,Departamento.DIIC)
umu.cambio_departamento(p5,Departamento.DIIC)
umu.cambio_departamento(p5,Departamento.DIS)
umu.mostrar_miembros()
print("---------------------------------")