import sqlite3
import os

# Determinar la ruta a kiosco.db de forma robusta
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_NAME = "kiosco.db"
if not os.path.exists(DB_NAME):
    posible_local = os.path.join(BASE_DIR, "kiosco.db")
    posible_padre = os.path.join(BASE_DIR, "..", "kiosco.db")
    if os.path.exists(posible_local):
        DB_NAME = posible_local
    elif os.path.exists(posible_padre):
        DB_NAME = posible_padre


def insertar_producto(nombre: str, precio: float, stock_actual: int, stock_minimo: int):
    """
    Inserta un nuevo producto en la tabla Producto.
    Maneja excepciones en caso de error y asegura el cierre de la conexión con with.
    """
    try:
        with sqlite3.connect(DB_NAME) as conexion:
            cursor = conexion.cursor()
            query = """
                INSERT INTO Producto (Nombre_Descripcion, Precio_Venta, Stock_Actual, Stock_Minimo)
                VALUES (?, ?, ?, ?)
            """
            cursor.execute(query, (nombre, precio, stock_actual, stock_minimo))
            nuevo_id = cursor.lastrowid
            print(f"[+] Producto '{nombre}' insertado exitosamente con ID {nuevo_id}.")
            return nuevo_id
    except sqlite3.Error as e:
        print(f"[!] Error al insertar el producto '{nombre}': {e}")
        return None


def buscar_producto(nombre_parcial: str) -> list:
    """
    Ejecuta una consulta con LIKE para buscar productos que contengan nombre_parcial
    en su descripción y devuelve una lista de tuplas con los resultados:
    (ID, Nombre, Precio, Stock).
    """
    try:
        with sqlite3.connect(DB_NAME) as conexion:
            cursor = conexion.cursor()
            query = """
                SELECT ID_Producto, Nombre_Descripcion, Precio_Venta, Stock_Actual
                FROM Producto
                WHERE Nombre_Descripcion LIKE ?
            """
            cursor.execute(query, (f"%{nombre_parcial}%",))
            resultados = cursor.fetchall()
            return resultados
    except sqlite3.Error as e:
        print(f"[!] Error al buscar productos con el término '{nombre_parcial}': {e}")
        return []


def actualizar_precio(id_producto: int, nuevo_precio: float) -> bool:
    """
    Actualiza el Precio_Venta del producto que coincida con el ID.
    Maneja excepciones y asegura la confirmación/cierre de la conexión con with.
    """
    try:
        with sqlite3.connect(DB_NAME) as conexion:
            cursor = conexion.cursor()
            query = """
                UPDATE Producto
                SET Precio_Venta = ?
                WHERE ID_Producto = ?
            """
            cursor.execute(query, (nuevo_precio, id_producto))
            if cursor.rowcount > 0:
                print(f"[+] Precio del producto ID {id_producto} actualizado a ${nuevo_precio:.2f}.")
                return True
            else:
                print(f"[-] No se encontró ningún producto con el ID {id_producto}.")
                return False
    except sqlite3.Error as e:
        print(f"[!] Error al actualizar el precio del producto ID {id_producto}: {e}")
        return False


if __name__ == "__main__":
    print(f"Conectado a la base de datos: {DB_NAME}\n")

    # Demostración / pruebas
    print("--- 1. Insertando productos ---")
    id1 = insertar_producto("Alfajor Havanna Chocolate", 1200.0, 50, 10)
    id2 = insertar_producto("Gaseosa Coca-Cola 500ml", 1500.0, 30, 5)
    id3 = insertar_producto("Alfajor Jorgito Blanco", 600.0, 40, 10)

    print("\n--- 2. Buscando productos con 'Alfajor' ---")
    encontrados = buscar_producto("Alfajor")
    for prod in encontrados:
        print(f"ID: {prod[0]} | Nombre: {prod[1]} | Precio: ${prod[2]} | Stock: {prod[3]}")

    print("\n--- 3. Actualizando precio ---")
    if id1:
        actualizar_precio(id1, 1350.0)

    print("\n--- 4. Verificando producto actualizado ---")
    encontrados = buscar_producto("Havanna")
    for prod in encontrados:
        print(f"ID: {prod[0]} | Nombre: {prod[1]} | Precio: ${prod[2]} | Stock: {prod[3]}")
