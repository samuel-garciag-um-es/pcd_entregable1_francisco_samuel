import pytest
from entregable1 import Universidad, Estudiante, Asignatura, Departamento, Sexo, Titular, Asociado, Investigador

# Creamos una fixture para la Universidad
@pytest.fixture
def universidad():
    return Universidad("Universidad de Prueba", "Ubicación de Prueba")


    
# Test para añadir un estudiante a la universidad
def test_crear_asignatura(universidad):
    matematicas=Asignatura("Matemáticas", 101)
    universidad.crear_asignatura(matematicas)
    assert matematicas in universidad._listaasignaturas


# Test para añadir un estudiante a la universidad
def test_eliminar_asignatura(universidad):
    matematicas=Asignatura("Matemáticas", 101)
    universidad.crear_asignatura(matematicas)
    universidad.eliminar_asignatura(matematicas)
    assert matematicas not in universidad._listaasignaturas
    
    
# Test para añadir un estudiante a la universidad
def test_mostrar_asignaturas(universidad):
    matematicas=Asignatura("Matemáticas", 101)
    fisica=Asignatura("Física", 71)
    biologia=Asignatura("Biología", 34)
    universidad.crear_asignatura(matematicas)
    universidad.crear_asignatura(fisica)
    universidad.crear_asignatura(biologia)
    assert matematicas in universidad._listaasignaturas
    assert fisica in universidad._listaasignaturas
    assert biologia in universidad._listaasignaturas
    

# Test para añadir un estudiante a la universidad
def test_añadir_alumno(universidad):
    universidad.crear_asignatura(Asignatura("Matemáticas", 101))
    alumno = Estudiante("Juan", "12345678A", "Dirección de Prueba", Sexo.M, Asignatura("Matemáticas", 101))
    universidad.añadir_alumno(alumno)
    assert alumno in universidad._listaalumno

# Test para eliminar un estudiante de la universidad
def test_eliminar_alumno(universidad):
    universidad.crear_asignatura(Asignatura("Matemáticas", 101))
    alumno = Estudiante("Juan", "12345678A", "Dirección de Prueba", Sexo.M, [Asignatura("Matemáticas", 101)])
    universidad.añadir_alumno(alumno)
    universidad.eliminar_alumno(alumno)
    assert alumno not in universidad._listaalumno

# Test para añadir un miembro del departamento a la universidad
def test_añadir_miembrodep(universidad):
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

# Test para eliminar un miembro del departamento de la universidad
def test_eliminar_miembrodep(universidad):
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

# Test para cambiar el departamento de un miembro del departamento
def test_cambio_departamento(universidad):
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


# Test para mostrar la lista de miembros del departamento
def test_mostrar_miembros(universidad, capsys):
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

# Test para mostrar la lista de alumnos
def test_mostrar_alumnos(universidad, capsys):
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

# Test para añadir un estudiante a la universidad
def test_añadir_asignatura_persona(universidad):
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

# Test para eliminar un estudiante de la universidad
def test_eliminar_asignatura_persona(universidad):
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