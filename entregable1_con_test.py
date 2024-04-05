from enum import Enum
from abc import ABCMeta, abstractmethod
import pytest

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

class Persona(metaclass=ABCMeta):   #clase abstracta ya que no pueden existir personas que no sean Estudiantes o MiembrosDepartamento
    def __init__(self, nombre, dni, direccion, sexo):
        try:
            self.nombre = nombre
            self.dni = dni
            self.direccion = direccion
            if isinstance(sexo, Sexo):  #comprobamos que el sexo sea instancia de la clase Sexo
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
    
    def __eq__(self, otro):     #definimos el método __eq__ para comparar dos instancias de Asignatura
        if isinstance(otro, Asignatura):
            return (self.codigo == otro.codigo) and (self.nombre == otro.nombre)
        return False

class Departamento(Enum):
        DIIC = 1
        DITEC = 2
        DIS = 3
        
class MiembroDepartamento(Persona): #no puede haber una instancia de MiembroDepartamento sin que sea Profesor o Investigador
    def __init__(self, nombre, dni, direccion, sexo, departamento):
        try:
            Persona.__init__(self, nombre, dni, direccion, sexo)
            if not isinstance(departamento, Departamento):      #comprobamos que el departamento sea de la clase Departamento
                raise TypeError()
            self.departamento = departamento
        except TypeError as e:
            print("El departamento debe ser de la clase Departamento", e)
        
    def cambiodepartamento(self, nuevodepartamento):
        try:
            if isinstance (nuevodepartamento, Departamento):      #comprobamos que el departamento sea de la clase Departamento
                self.departamento = nuevodepartamento
            else:
                raise TypeError()
        except TypeError as e:
            print("El departamento debe ser de la clase Departamento", e)

    @abstractmethod
    def __str__(self):
        pass

    def __eq__(self, otro):     #definimos el método __eq__ para comparar miembros (empleamos solo dni, ya que debería ser clave)
        if isinstance(otro, MiembroDepartamento):
            return self.dni == otro.dni
        return False

class Investigador(MiembroDepartamento):
    def __init__(self, nombre, dni, direccion, sexo, departamento, area_investigacion):
        MiembroDepartamento.__init__(self, nombre, dni, direccion, sexo, departamento)
        self.area_investigacion = area_investigacion

    def __eq__(self, otro):     #definimos el método __eq__ para comparar investigadores
        if isinstance(otro, Investigador):
            return self.dni == otro.dni
        return False

    def __str__(self):      #definimos el método __str__ para poder mostrar investigadores
        return f"Nombre: {self.nombre}, DNI: {self.dni}, Dirección: {self.direccion}, Sexo: {self.sexo.name}, Departamento: {self.departamento.name}, Área: {self.area_investigacion}, Rol: Investigador"

class Profesor(MiembroDepartamento): #no puede haber una instancia de Profesor sin que sea Asociado o Titular
    def __init__(self, nombre, dni, direccion, sexo, departamento, asignaturas):
        try:
            MiembroDepartamento.__init__(self, nombre, dni, direccion, sexo, departamento)
            if not isinstance(asignaturas, list):       #permite pasar tanto 1 como n instancias de Asginatura
                asignaturas = [asignaturas]
            for asignatura in asignaturas:
                if not isinstance(asignatura, Asignatura):  #comprobamos que sean instancias de Asignatura
                    raise TypeError()
            self.asignaturas = asignaturas
        except TypeError as e:
            print("Las asignaturas deben ser instancias de la clase Asignatura", e)

    def añadir_asignatura(self,asignatura):
        try:
            if isinstance(asignatura, Asignatura):
                if asignatura not in self.asignaturas:      #comprobamos que la asignatura sea instancia de Asignatura y que no esté en la lista
                    self.asignaturas.append(asignatura)
                else:
                    print(f"La asignatura ya está registrada para {self.dni}")
            else:
                raise TypeError()
        except TypeError as e:
            print("Asignatura tiene que ser de la clase Asignatura", e)

    def eliminar_asignatura(self,asignatura):
        try:
            if isinstance(asignatura, Asignatura):  #comprobamos que la asignatura sea instancia de Asignatura y que esté en la lista
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
            print(f"Lista de asignaturas del profesor {self.dni}: ", end="")    #de esta forma imprimimos en una sola línea todas las asignaturas
            for i in range(len(self.asignaturas) - 1):
                print(f"{self.asignaturas[i]}; ", end="")
            print(self.asignaturas[-1])
    
    @abstractmethod
    def __str__(self):
        pass

class Asociado(Profesor):
    def __init__(self, nombre, dni, direccion, sexo, departamento, asignaturas):
        Profesor.__init__(self, nombre, dni, direccion, sexo, departamento, asignaturas)

    def __eq__(self, otro):     #definimos el método __eq__ para comparar profesores asociados (empleamos solo dni, ya que debería ser clave)
        if isinstance(otro, Asociado):
            return self.dni == otro.dni
        return False

    def __str__(self):  #definimos el método __str__ para mostrar asociados
        asignaturas_str = ["; ".join(str(asignatura) for asignatura in self.asignaturas)] #creamos una cadena para el listado de asignaturas, ya que imprimiendo self.asignaturas se muestran las referencias de memoria
        return f"Nombre: {self.nombre}, DNI: {self.dni}, Dirección: {self.direccion}, Sexo: {self.sexo.name}, Departamento: {self.departamento.name}, Asignaturas: {asignaturas_str}, Rol: Profesor asociado"
            
class Titular(Profesor, Investigador):
    def __init__(self, nombre, dni, direccion, sexo, departamento, asignaturas, area_investigacion):
        Profesor.__init__(self, nombre, dni, direccion, sexo, departamento, asignaturas)
        Investigador.__init__(self, nombre, dni, direccion, sexo, departamento, area_investigacion)

    def __eq__(self, otro): #definimos el método __eq__ para comparar profesores titulares (empleamos solo dni, ya que debería ser clave)
        if isinstance(otro, Titular):
            return self.dni == otro.dni
        return False

    def __str__(self):  #definimos el método __str__ para mostrar titulares
        asignaturas_str = ["; ".join(str(asignatura) for asignatura in self.asignaturas)] #creamos una cadena para el listado de asignaturas, ya que imprimiendo self.asignaturas se muestran las referencias de memoria
        return f"Nombre: {self.nombre}, DNI: {self.dni}, Dirección: {self.direccion}, Sexo: {self.sexo.name}, Departamento: {self.departamento.name}, Asignaturas: {asignaturas_str}, Área: {self.area_investigacion}, Rol: Profesor titular"

class Estudiante(Persona):
    def __init__(self, nombre, dni, direccion, sexo, asignaturas):
        try:
            Persona.__init__(self, nombre, dni, direccion, sexo)
            if not isinstance(asignaturas, list):
                asignaturas = [asignaturas]
            for asignatura in asignaturas:
                if not isinstance(asignatura, Asignatura):  #comprobamos que las asignaturas sean instancias de Asignatura
                    raise TypeError()
            self.asignaturas = asignaturas
        except TypeError as e:
            print("Las asignaturas deben ser instancias de la clase Asignatura", e)
    
    def añadir_asignatura(self,asignatura):
        try:
            if isinstance(asignatura, Asignatura): #comprobamos que la asignatura sea instancia de Asignatura
                if asignatura not in self.asignaturas: #comprobamos que no se encuentre en la lista
                    self.asignaturas.append(asignatura)
                else:
                    print(f"La asignatura ya está registrada para {self.dni}")
            else:
                raise TypeError()
        except TypeError as e:
            print("Asignatura tiene que ser de la clase Asignatura", e)

    def eliminar_asignatura(self,asignatura):
        try:
            if isinstance(asignatura, Asignatura): #comprobamos que la asignatura sea instancia de Asignatura
                if asignatura in self.asignaturas: #comprobamos que se encuentre en la lista
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
            print(f"Lista de asignaturas del alumno {self.dni}: ", end="") #de esta forma imprimimos todas en una línea
            for i in range(len(self.asignaturas) - 1):
                print(f"{self.asignaturas[i]}; ", end="")
            print(self.asignaturas[-1])

    def __str__(self): #creamos el método __str__ para mostrar estudiantes
        asignaturas_str = ["; ".join(str(asignatura) for asignatura in self.asignaturas)] #creamos una cadena para el listado de asignaturas, ya que imprimiendo self.asignaturas se muestran las referencias de memoria
        return f"Nombre: {self.nombre}, DNI: {self.dni}, Direccion: {self.direccion}, Sexo: {self.sexo.name}, Asignaturas: {asignaturas_str}, Rol: Estudiante"
    
    def __eq__(self, otro): #definimos el método __eq__ para comparar estudiantes (empleamos solo dni, ya que debería ser clave)
        if isinstance(otro, Estudiante):
            return self.dni == otro.dni
        return False

class Universidad:
    def __init__(self, nombre, ubicacion):
        self.nombre = nombre
        self.ubicacion = ubicacion
        #creamos tres listas para almacenar estudiantes, miembros y asignaturas, si alguna instancia no se encuentra en la lista correspondiente, no existe en nuestra "base de datos"
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
                miembro.cambiodepartamento(nuevodepartamento)   #llamamos al método de MiembroDepartamento
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
    
    def mostrar_asignaturas_profesor(self,persona=None): #si no se le pasa el parámetro persona, imprimirá todas las asignaturas de todos los profesores
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

    def mostrar_asignaturas_alumno(self,persona=None): #si no se le pasa el parámetro persona, imprimirá todas las asignaturas de todos los estudiantes
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

    def añadir_asignatura_persona(self,persona,asignatura): #método que se utiliza tanto para añadir asignaturas a profesores como a estudiantes
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

    def eliminar_asignatura_persona(self,persona,asignatura): #método que se utiliza tanto para eliminar asignaturas de profesores como de estudiantes
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

    def crear_asignatura(self,asignatura):  #de esta forma añadimos la asignatura introducida a la base de datos (self._listaasignaturas)
        try:
            if asignatura in self._listaasignaturas:
                raise AsignaturaError()
            else:
                self._listaasignaturas.append(asignatura)
                print(f"Asignatura {asignatura.codigo} introducida")
        except AsignaturaError as e:
            print('Nombre o código ya en la lista de asignaturas', e)

    def eliminar_asignatura(self, asignatura): #de esta forma retiramos la asignatura de la base de datos (self._listaasignaturas)
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

# Funciones para pytest:
def test_crear_asignatura():
    universidad = Universidad("Universidad de Prueba", "Ubicación de Prueba")
    matematicas=Asignatura("Matemáticas", 101)
    universidad.crear_asignatura(matematicas)
    assert matematicas in universidad._listaasignaturas

def test_eliminar_asignatura():
    universidad = Universidad("Universidad de Prueba", "Ubicación de Prueba")
    matematicas=Asignatura("Matemáticas", 101)
    universidad.crear_asignatura(matematicas)
    universidad.eliminar_asignatura(matematicas)
    assert matematicas not in universidad._listaasignaturas

def test_mostrar_asignaturas():
    universidad = Universidad("Universidad de Prueba", "Ubicación de Prueba")
    matematicas=Asignatura("Matemáticas", 101)
    fisica=Asignatura("Física", 71)
    biologia=Asignatura("Biología", 34)
    universidad.crear_asignatura(matematicas)
    universidad.crear_asignatura(fisica)
    universidad.crear_asignatura(biologia)
    assert matematicas in universidad._listaasignaturas
    assert fisica in universidad._listaasignaturas
    assert biologia in universidad._listaasignaturas

def test_añadir_alumno():
    universidad = Universidad("Universidad de Prueba", "Ubicación de Prueba")
    universidad.crear_asignatura(Asignatura("Matemáticas", 101))
    alumno = Estudiante("Juan", "12345678A", "Dirección de Prueba", Sexo.M, Asignatura("Matemáticas", 101))
    universidad.añadir_alumno(alumno)
    assert alumno in universidad._listaalumno

def test_eliminar_alumno():
    universidad = Universidad("Universidad de Prueba", "Ubicación de Prueba")
    universidad.crear_asignatura(Asignatura("Matemáticas", 101))
    alumno = Estudiante("Juan", "12345678A", "Dirección de Prueba", Sexo.M, [Asignatura("Matemáticas", 101)])
    universidad.añadir_alumno(alumno)
    universidad.eliminar_alumno(alumno)
    assert alumno not in universidad._listaalumno

def test_añadir_miembrodep():
    universidad = Universidad("Universidad de Prueba", "Ubicación de Prueba")
    universidad.crear_asignatura(Asignatura("PCD", 1))
    universidad.crear_asignatura(Asignatura("BBDD", 5))
    universidad.crear_asignatura(Asignatura("Matemáticas", 2))
    titular=Titular("Fernando", "21832936L", "Carril Lobo", Sexo.V, Departamento.DIIC, Asignatura("BBDD", 5), "Bases de datos relacionales")
    asociado=Asociado("Pepe", "32678360P", "Calle Quevedo",  Sexo.V, Departamento.DITEC, [Asignatura("PCD", 1), Asignatura("Matemáticas", 2)])
    investigador=Investigador("Carlota", "33467387N", "Calle Colombia", Sexo.M, Departamento.DIS, "POO")
    universidad.añadir_miembrodep(titular)
    universidad.añadir_miembrodep(asociado)
    universidad.añadir_miembrodep(investigador)
    assert investigador in universidad._listamiembros
    assert titular in universidad._listamiembros
    assert asociado in universidad._listamiembros

def test_eliminar_miembrodep():
    universidad = Universidad("Universidad de Prueba", "Ubicación de Prueba")
    universidad.crear_asignatura(Asignatura("PCD", 1))
    universidad.crear_asignatura(Asignatura("BBDD", 5))
    universidad.crear_asignatura(Asignatura("Matemáticas", 2))
    titular=Titular("Fernando", "21832936L", "Carril Lobo", Sexo.V, Departamento.DIIC, Asignatura("BBDD", 5), "Bases de datos relacionales")
    asociado=Asociado("Pepe", "32678360P", "Calle Quevedo",  Sexo.V, Departamento.DITEC, [Asignatura("PCD", 1), Asignatura("Matemáticas", 2)])
    investigador=Investigador("Carlota", "33467387N", "Calle Colombia", Sexo.M, Departamento.DIS, "POO")
    universidad.añadir_miembrodep(titular)
    universidad.añadir_miembrodep(asociado)
    universidad.añadir_miembrodep(investigador)
    universidad.eliminar_miembrodep(titular)
    universidad.eliminar_miembrodep(asociado)
    universidad.eliminar_miembrodep(investigador)
    assert investigador not in universidad._listamiembros
    assert titular not in universidad._listamiembros
    assert asociado not in universidad._listamiembros

def test_cambio_departamento():
    universidad = Universidad("Universidad de Prueba", "Ubicación de Prueba")
    universidad.crear_asignatura(Asignatura("PCD", 1))
    universidad.crear_asignatura(Asignatura("BBDD", 5))
    universidad.crear_asignatura(Asignatura("Matemáticas", 2))
    titular=Titular("Fernando", "21832936L", "Carril Lobo", Sexo.V, Departamento.DIIC, Asignatura("BBDD", 5), "Bases de datos relacionales")
    asociado=Asociado("Pepe", "32678360P", "Calle Quevedo",  Sexo.V, Departamento.DITEC, [Asignatura("PCD", 1), Asignatura("Matemáticas", 2)])
    investigador=Investigador("Carlota", "33467387N", "Calle Colombia", Sexo.M, Departamento.DIS, "POO")
    universidad.añadir_miembrodep(titular)
    universidad.añadir_miembrodep(asociado)
    universidad.añadir_miembrodep(investigador)
    universidad.cambio_departamento(titular, Departamento.DIS)
    universidad.cambio_departamento(asociado, Departamento.DIS)
    universidad.cambio_departamento(investigador, Departamento.DITEC)
    assert titular.departamento == Departamento.DIS
    assert asociado.departamento == Departamento.DIS
    assert investigador.departamento == Departamento.DITEC

def test_mostrar_miembros(capsys):
    universidad = Universidad("Universidad de Prueba", "Ubicación de Prueba")
    universidad.crear_asignatura(Asignatura("PCD", 1))
    universidad.crear_asignatura(Asignatura("BBDD", 5))
    universidad.crear_asignatura(Asignatura("Matemáticas", 2))
    titular=Titular("Fernando", "21832936L", "Carril Lobo", Sexo.V, Departamento.DIIC, Asignatura("BBDD", 5), "Bases de datos relacionales")
    asociado=Asociado("Pepe", "32678360P", "Calle Quevedo",  Sexo.V, Departamento.DITEC, [Asignatura("PCD", 1), Asignatura("Matemáticas", 2)])
    investigador=Investigador("Carlota", "33467387N", "Calle Colombia", Sexo.M, Departamento.DIS, "POO")
    universidad.añadir_miembrodep(titular)
    universidad.añadir_miembrodep(asociado)
    universidad.añadir_miembrodep(investigador)
    universidad.mostrar_miembros()
    captured = capsys.readouterr()
    assert "La lista de miembros de departamento es:" in captured.out
    assert "Fernando" in captured.out
    assert "Pepe" in captured.out
    assert "Carlota" in captured.out

def test_mostrar_alumnos(capsys):
    universidad = Universidad("Universidad de Prueba", "Ubicación de Prueba")
    universidad.crear_asignatura(Asignatura("PCD", 1))
    universidad.crear_asignatura(Asignatura("SSySS", 3))
    universidad.crear_asignatura(Asignatura("Matemáticas", 2))
    alumno1 = Estudiante("Lucas", "34525662A", "Av del Campo 13", Sexo.V, [Asignatura("PCD", 1), Asignatura("SSySS", 3)])
    alumno2 = Estudiante("Marcos", "63267251G", "Carril Pencho", Sexo.V, Asignatura("PCD", 1))
    alumno3 = Estudiante("Lucia", "42398409P", "Calle Garza",  Sexo.M, Asignatura("Matemáticas", 2))
    universidad.añadir_alumno(alumno1)
    universidad.añadir_alumno(alumno2)
    universidad.añadir_alumno(alumno3)
    universidad.mostrar_alumnos()
    captured = capsys.readouterr()
    assert "La lista de alumnos es:" in captured.out
    assert "Lucas" in captured.out
    assert "Marcos" in captured.out
    assert "Lucia" in captured.out

def test_añadir_asignatura_persona():
    universidad = Universidad("Universidad de Prueba", "Ubicación de Prueba")
    filosofia=Asignatura("Filosofía", 23)
    pcd=Asignatura("PCD", 1)
    matematicas=Asignatura("Matemáticas", 2)
    universidad.crear_asignatura(filosofia)
    universidad.crear_asignatura(pcd)
    universidad.crear_asignatura(matematicas)
    asociado=Asociado("Pepe", "32678360P", "Calle Quevedo",  Sexo.V, Departamento.DITEC, [Asignatura("PCD", 1), Asignatura("Matemáticas", 2)])
    alumno = Estudiante("Juan", "12345678A", "Dirección de Prueba", Sexo.M, Asignatura("Filosofía", 23))
    universidad.añadir_asignatura_persona(alumno, Asignatura("PCD", 1))
    universidad.añadir_asignatura_persona(asociado, Asignatura("Filosofía", 23))
    assert filosofia in asociado.asignaturas
    assert pcd in alumno.asignaturas

def test_eliminar_asignatura_persona():
    universidad = Universidad("Universidad de Prueba", "Ubicación de Prueba")
    filosofia=Asignatura("Filosofía", 23)
    pcd=Asignatura("PCD", 1)
    matematicas=Asignatura("Matemáticas", 2)
    universidad.crear_asignatura(filosofia)
    universidad.crear_asignatura(pcd)
    universidad.crear_asignatura(matematicas)
    asociado=Asociado("Pepe", "32678360P", "Calle Quevedo",  Sexo.V, Departamento.DITEC, [Asignatura("PCD", 1), Asignatura("Matemáticas", 2)])
    alumno = Estudiante("Juan", "12345678A", "Dirección de Prueba", Sexo.M, Asignatura("Filosofía", 23))
    universidad.añadir_asignatura_persona(alumno, Asignatura("PCD", 1))
    universidad.añadir_asignatura_persona(asociado, Asignatura("Filosofía", 23))
    universidad.eliminar_asignatura_persona(alumno, Asignatura("PCD", 1))
    universidad.eliminar_asignatura_persona(asociado, Asignatura("Filosofía", 23))
    assert filosofia not in asociado.asignaturas
    assert pcd not in alumno.asignaturas
        
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