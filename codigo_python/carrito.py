from datetime import datetime

class CarritoCompras:
    def __init__(self, conexion):
        self.productos = []
        self.conexion = conexion

    def agregar_producto(self, producto):
        self.productos.append(producto)
        print("Producto agregado al carrito.")

    def ver_carrito(self):
        print("Productos en el carrito:")
        for producto in self.productos:
            print(producto)

    def comprar(self):
        try:
            conexion_bd = self.conexion.conectar()
            cursor = conexion_bd.cursor()

            # Calcular el valor total de la compra
            valor_total = sum(producto.precio for producto in self.productos)

            # Insertar la compra en la base de datos
            fecha_compra = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            cursor.execute("INSERT INTO Compra (fecha_compra, valor_compra) VALUES (?, ?)", fecha_compra, valor_total)
            conexion_bd.commit()

            print("Compra realizada. Gracias por su compra!")
            self.productos = []  # Vaciar el carrito después de realizar la compra
        except Exception as e:
            print("Error al realizar la compra:", e)
