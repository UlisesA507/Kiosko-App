import sqlite3
import os

DB_NAME = "kiosco.db"

TABLAS = {
    "Producto": """
        CREATE TABLE IF NOT EXISTS Producto (
            ID_Producto INTEGER PRIMARY KEY AUTOINCREMENT,
            Nombre_Descripcion TEXT NOT NULL,
            Precio_Venta REAL NOT NULL,
            Stock_Actual REAL DEFAULT 0,
            Stock_Minimo REAL DEFAULT 0,
            Es_Pesable INTEGER DEFAULT 0
        );
    """,
    "Cliente": """
        CREATE TABLE IF NOT EXISTS Cliente (
            ID_Cliente INTEGER PRIMARY KEY AUTOINCREMENT,
            Nombre TEXT NOT NULL,
            Telefono TEXT,
            Saldo_Deuda REAL DEFAULT 0
        );
    """,
    "Venta": """
        CREATE TABLE IF NOT EXISTS Venta (
            ID_Venta INTEGER PRIMARY KEY AUTOINCREMENT,
            Fecha_Hora DATETIME DEFAULT CURRENT_TIMESTAMP,
            Total_Venta REAL NOT NULL,
            ID_Cliente INTEGER,
            FOREIGN KEY (ID_Cliente) REFERENCES Cliente(ID_Cliente)
        );
    """,
    "Detalle_Venta": """
        CREATE TABLE IF NOT EXISTS Detalle_Venta (
            ID_Detalle INTEGER PRIMARY KEY AUTOINCREMENT,
            ID_Venta INTEGER NOT NULL,
            ID_Producto INTEGER NOT NULL,
            Cantidad REAL NOT NULL,
            Precio_Historico REAL NOT NULL,
            Subtotal REAL NOT NULL,
            FOREIGN KEY (ID_Venta) REFERENCES Venta(ID_Venta),
            FOREIGN KEY (ID_Producto) REFERENCES Producto(ID_Producto)
        );
    """
}


def tabla_existe(cursor, nombre_tabla: str) -> bool:
    """Verifica si una tabla ya existe en la base de datos."""
    cursor.execute(
        "SELECT 1 FROM sqlite_master WHERE type='table' AND name = ?",
        (nombre_tabla,)
    )
    return cursor.fetchone() is not None


def inicializar_bd(nombre_db: str = DB_NAME):
    """Crea la base de datos SQLite y sus tablas con las restricciones indicadas."""
    print(f"Conectando a la base de datos '{nombre_db}'...")
    conexion = sqlite3.connect(nombre_db)
    cursor = conexion.cursor()

    try:
        # Habilitar soporte para claves foráneas
        cursor.execute("PRAGMA foreign_keys = ON;")

        for nombre_tabla, ddl in TABLAS.items():
            ya_existia = tabla_existe(cursor, nombre_tabla)
            cursor.execute(ddl)

            if ya_existia:
                print(f"[-] La tabla '{nombre_tabla}' ya existía en la base de datos.")
            else:
                print(f"[+] Tabla '{nombre_tabla}' creada exitosamente.")

        conexion.commit()
        print("Operación completada con éxito.")

    except sqlite3.Error as e:
        print(f"[!] Error al procesar la base de datos: {e}")
        conexion.rollback()
    finally:
        conexion.close()


if __name__ == "__main__":
    inicializar_bd()
