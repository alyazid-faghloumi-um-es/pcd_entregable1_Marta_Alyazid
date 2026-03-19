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
            raise RepuestoInvalidoError("el nombre del repuesto no es valido")

        if not proveedor or not isinstance(proveedor, str):
            raise RepuestoInvalidoError("el nombre del proveedor no es valido")

        if not isinstance(cantidad, int) or cantidad < 0:
            raise CantidadInvalidaError("la cantidad no es valida")

        if not isinstance(precio, (int, float)) or precio < 0:
            raise PrecioInvalidoError("el precio no es valido")

        self.nombre = nombre
        self.proveedor = proveedor
        self._cantidad = cantidad
        self.precio = float(precio)

    def actualizar_cantidad(self, nueva_cantidad):
        #si la nueva cantidad no es un int o si la cantidad que queremos añadir es negativa 
        if not isinstance(nueva_cantidad, int) or nueva_cantidad < 0:
            raise CantidadInvalidaError("la cantidad entrada no es valida")

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
            raise ImperioError("la localización del almacen no puede estar vacío.")

        self.nombre = nombre
        self.localizacion = localizacion
        self.catalogo: list[Repuesto] = []

    def agregar_repuesto(self, repuesto: Repuesto):
        if not isinstance(repuesto, Repuesto):
            raise RepuestoInvalidoError("El objeto proporcionado no es una instancia de Repuesto.")

        if self.buscar_repuestos(repuesto) is not None:
            raise RepuestoDuplicadoError("El objeto proporcionado ay está en la lista de los Repuestos.")

        self.catalogo.append(repuesto)

    def buscar_repuestos(self, repuesto: Repuesto) :

        if not isinstance(repuesto, Repuesto):
            raise RepuestoInvalidoError("El objeto proporcionado no es una instancia de Repuesto.")

        for r in self.catalogo:

            if r.nombre == repuesto.nombre:
                return r

        return None

    def actualizar_stock(self, repuesto: Repuesto, nueva_cantidad: int):

        encontrado = self.buscar_repuestos(repuesto)

        if encontrado is None:
            raise RepuestoNoEncontradoError("el repuesto no se encuentra en el almacen")

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

class MiImperio:

    def __init__(self):
        self._naves: list[Nave] = []
        self._almacenes: list[Almacen] = []

    def agregar_nave(self, nave: Nave):
        if not isinstance(nave, Nave):
            raise NaveInvalidaError("Objeto no válido como nave")
        self._naves.append(nave)

    def agregar_almacen(self, almacen: Almacen):
        if not isinstance(almacen, Almacen):
            raise ImperioError("Objeto no válido como almacén")
        self._almacenes.append(almacen)

    def _verificar_almacenes(self):
        if not self._almacenes:
            raise AlmacenNoDisponibleError("No hay almacenes disponibles")

    def _verificar_nave(self, nave: Nave):
        if not isinstance(nave, Nave):
            raise NaveInvalidaError("Objeto no es una nave")

        if nave not in self._naves:
            raise NaveNoRegistradaError("La nave no está registrada")


    def adquirir_repuesto(self, repuesto: Repuesto, cantidad: int):

        if not isinstance(repuesto, Repuesto):
            raise RepuestoInvalidoError("Repuesto no válido")

        if not isinstance(cantidad, int) or cantidad <= 0:
            raise CantidadInvalidaError("Cantidad inválida")

        self._verificar_almacenes()

        for almacen in self._almacenes:
            encontrado = almacen.buscar_repuestos(repuesto)

            if encontrado is not None:
                stock_actual = encontrado.obtener_cantidad()

                if stock_actual < cantidad:
                    raise StockInsuficienteError("Stock insuficiente")

                nuevo_stock = stock_actual - cantidad
                almacen.actualizar_stock(encontrado, nuevo_stock)

                return True  # éxito

        raise RepuestoNoEncontradoError("Repuesto no encontrado")

    def listar_repuestos(self):
        self._verificar_almacenes()

        return [almacen.catalogo for almacen in self._almacenes]

    def eliminar_repuesto(self, repuesto: Repuesto):

        if not isinstance(repuesto, Repuesto):
            raise RepuestoInvalidoError("Repuesto no válido")

        self._verificar_almacenes()

        for almacen in self._almacenes:
            encontrado = almacen.buscar_repuestos(repuesto)

            if encontrado is not None:
                almacen.catalogo.remove(encontrado)
                return True

        raise RepuestoNoEncontradoError("Repuesto no encontrado")
    

if __name__ == "__main__":

    print("=== INICIO DEL SISTEMA IMPERIAL ===")

    sistema = MiImperio() #crear la instancia MiImperio
    try:

        print("\n*****CREAR ALMACEN Y REPUESTOS*****")
        almacen1 = Almacen("Almacen Central", "Zona Norte")

        r1 = Repuesto("motor", "Corellia", 10, 5000)
        r2 = Repuesto("laser", "Kuat", 5, 2000)
        r3 = Repuesto("escudo", "Naboo", 2, 8000)

        almacen1.agregar_repuesto(r1)
        almacen1.agregar_repuesto(r2)
        almacen1.agregar_repuesto(r3)

        sistema.agregar_almacen(almacen1)

        print("*****Almacén y repuestos creados*****")

        
        print("\n**crear Naves**")
        nave1 = NaveEstelar("ID-001", 1234, "Destructor", 1000, 200, Clase.EJECUTOR)
        nave2 = CazaEstelar("ID-002", 5678, "TIE Fighter", 1)

        sistema.agregar_nave(nave1)
        sistema.agregar_nave(nave2)

        print("*****Naves registradas******")

        print("\n*****Compra correcta*****")
        sistema.adquirir_repuesto(r1, 3)
        print(f"Stock restante motor: {r1.obtener_cantidad()}")

        # compra total
        print("Compra total")
        sistema.adquirir_repuesto(r3, 2)
        print(f"Stock restante escudo: {r3.obtener_cantidad()}")

        # comprar con un stock insuficiente
        print("\nCompra con error")
        try:
            sistema.adquirir_repuesto(r2, 100)
        except ImperioError as e:
            print(f"-Error: {e}")

        #respuesto no valido
        print("Error tipo de repuesto")
        try:
            sistema.adquirir_repuesto("no_es_repuesto", 1)
        except ImperioError as e:
            print(f"-Error: {e}")

        # cantidad no valida
        print("Error cantidad negativa")
        try:
            sistema.adquirir_repuesto(r1, -5)
        except ImperioError as e:
            print(f"-Error: {e}")

        #listar los respuestos
        print("\nListado de repuestos")
        for catalogo in sistema.listar_repuestos():
            for rep in catalogo:
                print(rep)

        #eliminar un repuesto
        print("\nEliminando repuesto")
        sistema.eliminar_repuesto(r2)
        print("Repuesto eliminado")

        print("\n******** Detección de errores:**********")
        print("\nError eliminando repuesto inexistente")
        try:
            sistema.eliminar_repuesto(r2)
        except ImperioError as e:
            print(f"Error: {e}")

        #crear un repuesto no valido
        print("\ncreando repuesto inválido")
        try:
            r4 = Repuesto("", "ProveedorX", 5, 100)
        except ImperioError as e:
            print(f"-Error: {e}")

        # ERROR: DUPLICAR REPUESTO
        print("\nError repuesto duplicado")
        try:
            almacen1.agregar_repuesto(r1)
        except ImperioError as e:
            print(f"-Error:{e}")

    except ImperioError as e:
        print(f"Error del sistema: {e}")

    print("\n=== FIN DEL SISTEMA ===")