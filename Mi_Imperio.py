from abc import ABCMeta, abstractmethod
from enum import Enum


# Excepciones

class ImperioError(Exception):
    pass

class RepuestoInvalidoError(ImperioError):
    pass

class CantidadInvalidaError(ImperioError):
    pass

class PrecioInvalidoError(ImperioError):
    pass

class RepuestoNoEncontradoError(ImperioError):
    pass

class RepuestoDuplicadoError(ImperioError):
    pass

class AlmacenNoDisponibleError(ImperioError):
    pass

class NaveNoRegistradaError(ImperioError):
    pass

class NaveInvalidaError(ImperioError):
    pass

class StockInsuficienteError(ImperioError):
    pass

#clases con enumeración

class Ubicacion(Enum):
    ENDOR = 1
    CUMULO_RAIMOS = 2
    NEBULOSA_KALIIDA = 3


class Clase(Enum):
    EJECUTOR = 1
    ECLIPSE = 2
    SOBERANO = 3

# Repuesto

class Repuesto:

    def __init__(self, nombre: str, proveedor: str, cantidad: int, precio: float):

        if not nombre or not isinstance(nombre, str):
            raise RepuestoInvalidoError()

        if not proveedor or not isinstance(proveedor, str):
            raise RepuestoInvalidoError()

        if not isinstance(cantidad, int) or cantidad < 0:
            raise CantidadInvalidaError()

        if not isinstance(precio, (int, float)) or precio < 0:
            raise PrecioInvalidoError()

        self.nombre = nombre
        self.proveedor = proveedor
        self._cantidad = cantidad
        self.precio = float(precio)

    def actualizar_cantidad(self, nueva_cantidad):
        #si la nueva cantidad no es un int o si la cantidad que queremos añadir es negativa 
        if not isinstance(nueva_cantidad, int) or nueva_cantidad < 0:
            print("la cantidad entrada no es valida")
            raise CantidadInvalidaError()

        self._cantidad = nueva_cantidad

    def obtener_cantidad(self):
        #devuelve la cantidad de un repuesto
        return self._cantidad

    def __str__(self):
        #devuelve el nombre del repuesto y su cantidad 
        return f"{self.nombre} ({self._cantidad})"

# Almacen

class Almacen:

    def __init__(self, nombre: str, localizacion: str):

        if not nombre:
            print("El nombre del almacen no puede estar vacío. ")
            raise ImperioError()

        if not localizacion:
            "la localización del almacen no puede estar vacío."
            raise ImperioError()

        self.nombre = nombre
        self.localizacion = localizacion
        self.catalogo: list[Repuesto] = []

    def agregar_repuesto(self, repuesto: Repuesto):
        if not isinstance(repuesto, Repuesto):
            print("El objeto proporcionado no es una instancia de Repuesto.")
            raise RepuestoInvalidoError()

        if self.buscar_repuestos(repuesto) is not None:
            print("El objeto proporcionado ay está en la lista de los Repuestos.")
            raise RepuestoDuplicadoError()

        self.catalogo.append(repuesto)

    def buscar_repuestos(self, repuesto: Repuesto) :

        if not isinstance(repuesto, Repuesto):
            print("El objeto proporcionado no es una instancia de Repuesto.")
            raise RepuestoInvalidoError()

        for r in self.catalogo:

            if r.nombre == repuesto.nombre:
                return r

        return None

    def actualizar_stock(self, repuesto: Repuesto, nueva_cantidad: int):

        encontrado = self.buscar_repuestos(repuesto)

        if encontrado is None:
            raise RepuestoNoEncontradoError()

        encontrado.actualizar_cantidad(nueva_cantidad)

#Unidad de Combate:

class UnidadCombate(metaclass=ABCMeta):

    def __init__(self, id_combate: str, clave_transmision: float):

        if not id_combate:
            raise ImperioError()

        if not isinstance(clave_transmision, (int, float)):
            raise ImperioError()

        self._id_combate = id_combate
        self._clave_transmision = float(clave_transmision)


#nave:

class Nave(UnidadCombate, metaclass=ABCMeta):

    def __init__(self, id_combate: str, clave_transmision: float, nombre: str):

        super().__init__(id_combate, clave_transmision)

        if not nombre:
            raise NaveInvalidaError()

        self.nombre = nombre
        self.catalogo_repuestos: list[Repuesto] = []

#tipos de naves:

class NaveEstelar(Nave):

    def __init__(self, id_combate, clave_transmision,
                 nombre, tripulacion, pasaje, clase):

        super().__init__(id_combate, clave_transmision, nombre)

        if not isinstance(tripulacion, int) or tripulacion < 0:
            raise NaveInvalidaError()

        if not isinstance(pasaje, int) or pasaje < 0:
            raise NaveInvalidaError()

        if not isinstance(clase, Clase):
            raise NaveInvalidaError()

        self.tripulacion = tripulacion
        self.pasaje = pasaje
        self.clase = clase


class EstacionEspacial(Nave):

    def __init__(self, id_combate, clave_transmision,
                 nombre, tripulacion, pasaje, ubicacion):

        super().__init__(id_combate, clave_transmision, nombre)

        if not isinstance(ubicacion, Ubicacion):
            raise NaveInvalidaError()

        self.tripulacion = tripulacion
        self.pasaje = pasaje
        self.ubicacion = ubicacion


class CazaEstelar(Nave):

    def __init__(self, id_combate, clave_transmision,
                 nombre, dotacion):

        super().__init__(id_combate, clave_transmision, nombre)

        if not isinstance(dotacion, int) or dotacion < 0:
            raise NaveInvalidaError()

        self.dotacion = dotacion

#mi imperio

class MiImperio:

    def __init__(self):
        self._naves: list[Nave] = []
        self._almacenes: list[Almacen] = []

    def agregar_nave(self, nave: Nave):
        #añadir una nave
        if not isinstance(nave, Nave):
            raise NaveInvalidaError()

        self._naves.append(nave)

    def agregar_almacen(self, almacen: Almacen):
        #añadir un almacen a la lista de almacenes
        if not isinstance(almacen, Almacen):
            raise ImperioError()

        self._almacenes.append(almacen)

    def _verificar_almacenes(self):
        #verificar si hay almacenes
        if not self._almacenes:
            raise AlmacenNoDisponibleError()

    def _verificar_nave(self, nave: Nave):
        #verificar si hay 
        if not isinstance(nave, Nave):
            print("el valor introduciod no hace parte de la clase Nave")
            raise NaveInvalidaError()

        if nave not in self._naves:
            print("la nave introducida no esta en la ista de las naves")
            raise NaveNoRegistradaError()
    #para los comandantes:

    def consultar_repuestos(self, nave: Nave):

        self._verificar_nave(nave)
        self._verificar_almacenes()

        almacen = self._almacenes[0]

        resultado = []

        for repuesto in nave.catalogo_repuestos:

            encontrado = almacen.buscar_repuestos(repuesto)

            if encontrado:
                resultado.append(encontrado)

        return resultado

    def adquirir_repuesto(self, repuesto: Repuesto, cantidad: int):
        #en caso de introducir un elemento que no pertenece a la clase Repuesto
        if not isinstance(repuesto, Repuesto):
            raise RepuestoInvalidoError()
        #en el caso donde la antidad adquirida es menor que 0 o que la cantidad no es un entero
        if not isinstance(cantidad, int) or cantidad <= 0:
            raise CantidadInvalidaError()
        #verificar que hay almacenes en la Clase MiImperio
        self._verificar_almacenes()

        for almacen in self._almacenes:
            #recorre todo los almacenes  ,buscando por el repuesto que queremos adquirir
            encontrado = almacen.buscar_repuestos(repuesto)

            if encontrado ==True :
                #añadimos la cantidad del repuesto adquirido a la cantidad anterior dentro del almacen
                nueva_cantidad = encontrado.obtener_cantidad() + cantidad
                almacen.actualizar_stock(encontrado, nueva_cantidad)

        raise RepuestoNoEncontradoError()

    def listar_repuesto(self):
        #verifica que en la clase MiIperio hay almacenes para recorrer y buscar repuestos
        self._verificar_almacenes()
        lista_respuesto = []

        for almacen in self._almacenes:
            #devolver el catalogo de repuesto de cada almacen dentro de la clase MiImperio
            lista_respuesto.append(almacen.catalogo)

        return lista_respuesto
    
    def eliminar_repuesto(self,repuesto:Repuesto):
        if not isinstance(repuesto, Repuesto):
            raise RepuestoInvalidoError()
        self._verificar_almacenes()

        for almacen in self._almacenes:
            #recorremos los almacenes presentes en la clase MiImperio
            encontrado = almacen.buscar_repuestos(repuesto)
            almacen_encontrado=almacen
            #guardo las 2 variables del almacen y el repuesto 
            if encontrado ==True :
                #quito el repuesto , y devuelvo un mensaje 
                almacen_encontrado.catalogo.pop(encontrado)
                print(f"el repuesto {repuesto} ha sido eliminado del almacen {almacen_encontrado}")

        raise RepuestoNoEncontradoError()