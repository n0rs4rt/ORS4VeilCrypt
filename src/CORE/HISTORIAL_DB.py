import sqlite3, logging

from CORE.RUTAS import *

logger = logging.getLogger("LOGS")

class HistorialDB():
    def __init__ (self):
        pass
    
    def crear_db (self):
        try:
            with sqlite3.connect(ruta_db) as conn:
                
                cursor = conn.cursor()
                cursor.execute("""
                            CREATE TABLE IF NOT EXISTS historial(
                                id INTEGER PRIMARY KEY AUTOINCREMENT,
                                nombre_portador TEXT,
                                tipo_portador TEXT,
                                nombre_contenido TEXT,
                                tipo_contenido TEXT,
                                archivo_resultado TEXT,
                                ruta_resultado TEXT,
                                tamanio_resultado,
                                fecha TEXT,
                                pista_key TEXT,
                                key_exportada TEXT,
                                UNIQUE (nombre_portador, tipo_portador, nombre_contenido, tipo_contenido, archivo_resultado, ruta_resultado)
                            )
                            """)
        except Exception as e:
            logger.error(f"Error al crear la base de datos: {e}")

    def insertar_historial (self,nombre_portador,tipo_portador,nombre_contenido,tipo_contenido,archivo_resultado,ruta_resultado,tamanio_resultado,fecha,pista_key,key_exportada):
        
        clave = pista_key
        
        clave = clave[0:10]
        
        try:
            with sqlite3.connect(ruta_db) as conn:
                cursor = conn.cursor()
                cursor.execute("INSERT OR REPLACE INTO historial (nombre_portador, tipo_portador, nombre_contenido, tipo_contenido, archivo_resultado, ruta_resultado, tamanio_resultado, fecha, pista_key, key_exportada) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", (nombre_portador, tipo_portador, nombre_contenido, tipo_contenido, archivo_resultado, ruta_resultado, tamanio_resultado, fecha, clave, key_exportada))
                
                id_insertado = cursor.lastrowid
                
                return id_insertado
        except Exception as e:
            logger.error(f"Error al guardar el historial del proceso: {e}")
            return False
            
    def actualizar_key_exportada (self,id_operacion):
        
        try:
            with sqlite3.connect(ruta_db) as conn:
                cursor = conn.cursor()
                cursor.execute("UPDATE historial SET key_exportada = ? WHERE id = ?", ("SI", id_operacion))

        except Exception as e:
            logger.error(f"Error al actualizar la llave exportada: {e}")
    
        return
    

    def leer_historial_db (self):

        if ruta_db.exists():
            
            try:
                with sqlite3.connect(ruta_db) as conn:
                    cursor = conn.cursor()
                    cursor.execute ("SELECT * FROM historial")
                    
                    historial = cursor.fetchall()
                    
                    columnas_datos = self.preparar_datos_tabla(historial)
                    
                    return columnas_datos
                    
            except Exception as e:
                logger.error(f"Error al leer el historial: {e}")
                return


    def preparar_datos_tabla (self, historico):
        """
        Prepara los datos para la tabla de la interfaz y retorna las columnas y los datos
        """

        columnas = [
                    {
                        "key": "id",
                        "title": "ID",
                        "type": "number",
                        "visible": False
                    },
                    {
                        "key": "portador",
                        "title": "PORTADOR",
                        "type": "text"
                    },
                    {
                        "key": "tipo_portador",
                        "title": "TIPO DE PORTADOR",
                        "type": "text",
                        "align": "center"
                    },
                    {
                        "key": "contenido_oculto",
                        "title": "CONTENIDO OCULTO",
                        "type": "text"
                    },
                    {
                        "key": "tipo_contenido",
                        "title": "TIPO DE CONTENIDO",
                        "type": "text",
                        "align": "center"
                    },
                    {
                        "key": "archivo_resultado",
                        "title": "ARCHIVO RESULTADO",
                        "type": "text"
                    },
                    {
                        "key": "ruta_resultado",
                        "title": "RUTA DEL ARCHIVO",
                        "type": "text"
                    },
                    {
                        "key": "tamano",
                        "title": "TAMAÑO",
                        "type": "text",
                        "anchor": "center"
                    },
                    {
                        "key": "fecha",
                        "title": "FECHA",
                        "type": "text"
                    },
                    {
                        "key": "pista_key",
                        "title": "PISTA DE CLAVE",
                        "type": "text"
                    },
                    {
                        "key": "key_exportada",
                        "title": "CLAVE EXPORTADA",
                        "type": "text",
                        "align": "center"
                    }
                ]
                
        datos = []
        
        for dato in historico:

            fila = {"id":dato[0],"portador":dato[1],"tipo_portador":dato[2],"contenido_oculto":dato[3],"tipo_contenido":dato[4],"archivo_resultado":dato[5],"ruta_resultado":dato[6],"tamano":dato[7],"fecha":dato[8],"pista_key":dato[9],"key_exportada":dato[10]}
            
            datos.append(fila)
        
        
        return columnas, datos



    def eliminar_filas_db(self, filas_seleccionadas = None):
        
        if not ruta_db.exists():
            return
        
        try:
            with sqlite3.connect(ruta_db) as conn:
                cursor = conn.cursor()
                
                if filas_seleccionadas:
                    cursor.executemany("DELETE FROM historial WHERE id = ?", filas_seleccionadas)
                    
                else:
                    cursor.execute("DELETE FROM historial")

                cursor.execute("SELECT * FROM historial")
                filas = cursor.fetchall()
                
                if not filas:
                    #REINICIAMOS EL CONTADOR ID
                    cursor.execute ("DELETE FROM sqlite_sequence WHERE name = 'historial'")
    
                return True
        except Exception as e:
            logger.error(f"Error al eliminar el historial: {e}")
            
            return False
                
            
        
# db = HistorialDB()
# db.leer_historial_db()