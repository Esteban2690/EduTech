from conexionbd import ConexionBD
from carrito import CarritoCompras
import os

class Cliente:
    def __init__(self, idcliente, nombre, apellido, telefono):
        self.idcliente = idcliente
        self.nombre = nombre
        self.apellido = apellido
        self.telefono = telefono

    def __str__(self):
        return f'{self.nombre} {self.apellido}'

class Producto:
    def __init__(self, idproducto, nombre, cantidad, precio):
        self.idproducto = idproducto
        self.nombre = nombre
        self.cantidad = cantidad
        self.precio = precio

    def __str__(self):
        return f'{self.nombre} - {self.cantidad} - ${self.precio}'

def mostrar_menu():
    print("\n¡Bienvenido al carrito de compras de Edutech!")
    print("Por favor, elija una opción:")
    print("1. Agregar un producto al carrito")
    print("2. Ver productos agregados al carrito")
    print("3. Comprar")
    print("4. Limpiar")
    print("5. Salir")

def limpiar_pantalla():
    os.system('cls' if os.name == 'nt' else 'clear')

def ejecutar_carrito_compras(conexion):
    while True:
        carrito = CarritoCompras(conexion)
        opcion = 0
        while opcion != 5:
            limpiar_pantalla()
            mostrar_menu()
            try:
                opcion = int(input("Ingrese el número de la opción que desea: "))
                if opcion == 1:
                    agregar_producto_al_carrito(conexion, carrito)
                elif opcion == 2:
                    ver_carrito(carrito)
                elif opcion == 3:
                    comprar(conexion, carrito)
                elif opcion == 4:
                    limpiar_carrito(carrito)
                elif opcion == 5:
                    print("¡Hasta luego!")
                    return
                else:
                    print("Opción no válida. Por favor, ingrese un número válido.")
            except ValueError:
                print("Error: ingrese un número válido.")

        continuar = input("¿Desea realizar otra operación? (S/N): ")
        if continuar.lower() != 's':
            print("¡Hasta luego!")
            break

def agregar_producto_al_carrito(conexion, carrito):
    nombre_producto = input("Ingrese el nombre del producto que desea agregar al carrito: ")
    try:
        producto_encontrado = buscar_producto(nombre_producto, conexion)
        if producto_encontrado:
            print("Producto encontrado:")
            print(producto_encontrado)
            carrito.agregar_producto(producto_encontrado)
        else:
            print("Producto no encontrado.")
    except Exception as e:
        print("Error al agregar el producto al carrito:", e)

def buscar_producto(nombre_producto, conexion):
    try:
        conexion.conectar()
        cursor = conexion.conexion.cursor()
        cursor.execute("SELECT * FROM productos WHERE nombre_producto = ?", nombre_producto)
        producto = cursor.fetchone()
        if producto:
            return Producto(producto[0], producto[1], producto[3], producto[2])
        else:
            return None
    except Exception as e:
        print("Error al buscar el producto:", e)
        return None
    finally:
        conexion.desconectar()

def ver_carrito(carrito):
    carrito.ver_carrito()

def comprar(conexion, carrito):
    try:
        # Realizar la compra
        conexion.conectar()
        cursor = conexion.conexion.cursor()

        # Calcular el valor total de la compra
        costo_total, descuento_aplicado = calcular_costo_total(carrito)

        # Insertar la compra en la base de datos
        cursor.execute("INSERT INTO Compra (fecha_compra, valor_compra) VALUES (GETDATE(), ?)", costo_total)
        conexion.conexion.commit()

        if descuento_aplicado:
            print("¡Transacción exitosa! Se aplicó un descuento del 10% en su compra.")
        else:
            print("¡Transacción exitosa! No se aplicó ningún descuento en su compra.")

        # Vaciar el carrito después de realizar la compra
        carrito.productos = []
    except Exception as e:
        print("Error al realizar la compra:", e)
    finally:
        conexion.desconectar()


def calcular_costo_total(carrito):
    cantidad_total = sum(producto.cantidad for producto in carrito.productos)
    costo_total = sum(producto.precio * producto.cantidad for producto in carrito.productos)
    descuento_aplicado = False

    if cantidad_total > 5:
        descuento = costo_total * 0.1  # 10% de descuento
        costo_total -= descuento
        descuento_aplicado = True

    return costo_total, descuento_aplicado


def limpiar_carrito(carrito):
    try:
        carrito.productos = []
        print("El carrito ha sido limpiado correctamente.")
    except Exception as e:
        print("Error al limpiar el carrito:", e)

if __name__ == "__main__":
    conexion = ConexionBD(servidor=r'MELISSA-LAPTOP\SQLEXPRESS01', base_datos='edutech_database')
    ejecutar_carrito_compras(conexion)
