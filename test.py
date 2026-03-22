import pytest
from Mi_Imperio import (
    Repuesto, Almacen, MiImperio,
    RepuestoInvalidoError, CantidadInvalidaError,
    PrecioInvalidoError, RepuestoDuplicadoError,
    RepuestoNoEncontradoError, StockInsuficienteError,
    AlmacenNoDisponibleError, NaveEstelar, CazaEstelar,
    Clase
)

@pytest.fixture
def repuesto_valido():
    return Repuesto("motor", "Corellia", 10, 5000)

@pytest.fixture
def almacen_con_repuestos(repuesto_valido):
    a = Almacen("Central", "Zona Norte")
    a.agregar_repuesto(repuesto_valido)
    return a

@pytest.fixture
def sistema(almacen_con_repuestos):
    s = MiImperio()
    s.agregar_almacen(almacen_con_repuestos)
    return s

#test sobre el repuesto

def test_creacion_repuesto_valido():
    r = Repuesto("laser", "Kuat", 5, 2000)
    assert r.nombre == "laser"
    assert r.obtener_cantidad() == 5

def test_repuesto_nombre_invalido():
    with pytest.raises(RepuestoInvalidoError):
        Repuesto("", "Proveedor", 5, 100)

def test_repuesto_cantidad_invalida():
    with pytest.raises(CantidadInvalidaError):
        Repuesto("motor", "Proveedor", -1, 100)

def test_repuesto_precio_invalido():
    with pytest.raises(PrecioInvalidoError):
        Repuesto("motor", "Proveedor", 5, -100)

def test_actualizar_cantidad():
    r = Repuesto("motor", "Corellia", 10, 5000)
    r.actualizar_cantidad(20)
    assert r.obtener_cantidad() == 20


#test del almacen

def test_agregar_repuesto(almacen_con_repuestos):
    r2 = Repuesto("laser", "Kuat", 5, 2000)
    almacen_con_repuestos.agregar_repuesto(r2)
    assert len(almacen_con_repuestos.catalogo) == 2


def test_repuesto_duplicado(almacen_con_repuestos, repuesto_valido):
    with pytest.raises(RepuestoDuplicadoError):
        almacen_con_repuestos.agregar_repuesto(repuesto_valido)


def test_buscar_repuesto(almacen_con_repuestos, repuesto_valido):
    encontrado = almacen_con_repuestos.buscar_repuestos(repuesto_valido)
    assert encontrado is not None


def test_actualizar_stock(almacen_con_repuestos, repuesto_valido):
    almacen_con_repuestos.actualizar_stock(repuesto_valido, 5)
    assert repuesto_valido.obtener_cantidad() == 5


def test_actualizar_stock_no_existente(almacen_con_repuestos):
    r = Repuesto("otro", "X", 1, 10)
    with pytest.raises(RepuestoNoEncontradoError):  #con pytest.raises manejamos el error así para que no cae el test al ejecutarlo 
        almacen_con_repuestos.actualizar_stock(r, 5)


#test de mi imperior

def test_adquirir_repuesto_correcto(sistema, repuesto_valido):
    sistema.adquirir_repuesto(repuesto_valido, 5)
    assert repuesto_valido.obtener_cantidad() == 5

def test_stock_insuficiente(sistema, repuesto_valido):
    with pytest.raises(StockInsuficienteError):  #con pytest.raises manejamos el error así para que no cae el test al ejecutarlo 
        sistema.adquirir_repuesto(repuesto_valido, 100)

def test_repuesto_no_encontrado(sistema):
    r = Repuesto("otro", "X", 1, 10)
    with pytest.raises(RepuestoNoEncontradoError): #con pytest.raises manejamos el error así para que no cae el test al ejecutarlo 
        sistema.adquirir_repuesto(r, 1)

def test_sin_almacenes():
    s = MiImperio()
    r = Repuesto("motor", "Corellia", 10, 5000)

    with pytest.raises(AlmacenNoDisponibleError):
        s.adquirir_repuesto(r, 1)


def test_eliminar_repuesto(sistema, repuesto_valido):
    sistema.eliminar_repuesto(repuesto_valido)
    with pytest.raises(RepuestoNoEncontradoError):
        sistema.eliminar_repuesto(repuesto_valido)

#test de naves

def test_crear_nave_estelar():
    n = NaveEstelar("ID-1", 1234, "Destructor", 100, 50, Clase.EJECUTOR)
    assert n.nombre == "Destructor"

def test_crear_caza_estelar():
    n = CazaEstelar("ID-2", 5678, "TIE", 1)
    assert n.dotacion == 1
    