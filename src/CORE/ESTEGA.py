import logging
from stego_lsb import LSBSteg #biblioteca para ocultar y desocultar archivos en imagenes
from stego_lsb.LSBSteg import hide_message_in_image #biblioteca para ocultar texto en imagenes
from stego_lsb import WavSteg #biblioteca para ocultar archivos en audios
from stego_lsb.LSBSteg import recover_message_from_image #biblioteca para desocultar texto en imagenes
from PIL import Image
from cryptography.fernet import Fernet
from CORE.RUTAS import *
from datetime import datetime

logger = logging.getLogger("LOGS")

class Esteganografia:
    def __init__(self):
        
        self.clave_recuperacion = None #clave de cifrado
        self.fecha = None #fecha del proceso
        self.archivo_portador = None #nombre del archivo portador
        self.nombre_contenido = None #nombre del archivo oculto
        self.archivo_contenido = None #formato del archivo oculto
        
        self.archivo_generado = None #nombre del archivo generado o extraido
        self.ruta_archivo_generado = None #ruta del archivo generado o extraido
        self.tamano_archivo_generado = None #tamaño del archivo generado o extraido
        self.formato_archivo = None #formato del archivo generado o extraido
        self.texto_extraido = None #texto extraido de la imagen o audio
        
    
    ############ CIFRADO Y OCULTAMIENTO DE ARCHIVOS ############
    
    def _generar_clave(self):
        """
        Genera la clave de cifrado y descifrado
        """
        
        self.clave_recuperacion = Fernet.generate_key().decode("utf-8") #generamos la clave de decifrado
        

    def _guardar_recover_key(self, ruta_destino):
        """
        Guarda la clave de cifrado y descifrado
        """
        try:
            with open(ruta_destino, "wb") as clave:
                clave.write(self.clave_recuperacion)
            self.key_exportada = "SI"
            return True
        
        except Exception as e:
            logger.error(f"Error al guardar la llave: {e}")
            self.key_exportada = "ERROR"
            return False
            

    def _cifrar_archivo (self, archivo_oculto):
        """
        Cifra el archivo oculto, lo guarda en una carpeta temporal y retorna la ruta de ese archivo
        """

        fernet = Fernet(self.clave_recuperacion.encode())

        with open(archivo_oculto, "rb" ) as archivo:
            contenido_archivo = archivo.read()

        contenido_cifrado = fernet.encrypt(contenido_archivo)

        self.fecha = datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
        ruta_archivo_cifrado =  ruta_tmp / f"cifrado{self.fecha}.vlkey"

        try:
            with open(ruta_archivo_cifrado, "wb") as archivo:
                archivo.write(contenido_cifrado)
            return ruta_archivo_cifrado #retorna la ruta del archivo cifrado
        
        except Exception as e:
            logger.error(f"Error de cifrado: {e}")
            return False


    def _desencriptar_archivo (self, archivo_cifrado,clave,destino,nombre,formato):
        """
        Desencripta el archivo oculto
        """

        fernet = Fernet(clave.encode())

        #LEEMOS EL CONTENIDO CIFRADO DEL ARCHIVO
        with open(archivo_cifrado, "rb") as archivo:
            contenido_cifrado = archivo.read()

        #DESCIFRAMOS EL CONTENIDO
        archivo_desifrado = fernet.decrypt(contenido_cifrado)

        archivo_destino = Path(destino) / f"{nombre}{formato}" #NOMBRE DEL ARCHIVO DESCIFRADO CON SU FORMATO

        #GUARDAMOS EL ARCHIVO DESCIFRADO
        with open(archivo_destino, "wb") as archivo:
            archivo.write(archivo_desifrado)

        self.ruta_archivo_generado = archivo_destino
        self.archivo_generado = Path(self.ruta_archivo_generado).name
        self.tamano_archivo_generado = Path(self.ruta_archivo_generado).stat().st_size


        if self.tamano_archivo_generado > 1024 and self.tamano_archivo_generado < 1048576:
            self.tamano_archivo_generado = f"{round(self.tamano_archivo_generado/1024,2)} KB"

        elif self.tamano_archivo_generado > 1048576 and self.tamano_archivo_generado < 1073741824:
            self.tamano_archivo_generado = f"{round(self.tamano_archivo_generado/1048576,2)} MB"

        elif self.tamano_archivo_generado > 1073741824:
            self.tamano_archivo_generado = f"{round(self.tamano_archivo_generado/1073741824,2)} GB"

        self.formato_archivo = self.ruta_archivo_generado.suffix

        return True

    def _cifrar_texto (self,texto):
        """CIFRA EL TEXTO Y LO DEVUELVE EN BYTES"""
        self.clave_recuperacion = Fernet.generate_key().decode("utf-8")
        
        fernet = Fernet(self.clave_recuperacion.encode())
        
        contenido_cifrado = fernet.encrypt(texto.encode("utf-8"))
        
        return contenido_cifrado #devuelve el texto cifrado en bytes

    ##########IMAGEN
    def archivo_imagen (self,archivo_portador, archivo_oculto, archivo_destino):
        """
        Oculta el archivo en la imagen
        """
        self._generar_clave ()
        
        archivo_cifrado =self._cifrar_archivo(archivo_oculto) #ARCHIVO A OCULTAR CIFRADO
        
        if not archivo_cifrado:
            return False
        
        try:
            LSBSteg.hide_data(input_image_path = archivo_portador, input_file_path = archivo_cifrado, steg_image_path= archivo_destino, num_lsb=2, compression_level=1)
            
            self.archivo_portador = Path(archivo_portador).name
            
            self.nombre_contenido = Path(archivo_oculto).name
            self.archivo_contenido = Path(archivo_oculto).suffix
            self.clave_recuperacion = f"{self.clave_recuperacion}|{self.archivo_contenido}"
            
            self.ruta_archivo_generado = archivo_destino
            self.tamano_archivo_generado = Path(self.ruta_archivo_generado).stat().st_size
            
            if self.tamano_archivo_generado > 1024 and self.tamano_archivo_generado < 1048576:
                self.tamano_archivo_generado = f"{round(self.tamano_archivo_generado/1024,2)} KB"
                
            elif self.tamano_archivo_generado > 1048576 and self.tamano_archivo_generado < 1073741824:
                self.tamano_archivo_generado = f"{round(self.tamano_archivo_generado/1048576,2)} MB"
            elif self.tamano_archivo_generado > 1073741824:
                self.tamano_archivo_generado = f"{round(self.tamano_archivo_generado/1073741824,2)} GB"
                
                
            self.archivo_generado = Path(self.ruta_archivo_generado).name
            self.formato_archivo = Path(self.ruta_archivo_generado).suffix
            
            return True
        
        except Exception as e:
            logger.error(f"Error al ocutar el archivo: {e}")
            return False

    #OCULTA TEXTO EN IMAGEN
    def archivo_texto (self,archivo_portador, texto, archivo_destino):
        """Oculta el texto en la imagen"""
        texto_bytes_cifrado = self._cifrar_texto(texto)

        try:
            with Image.open(archivo_portador) as imag_portador:
                imag_portador_RGB = imag_portador.convert("RGB")
                
                imagen_resultado = hide_message_in_image(input_image = imag_portador_RGB, message = texto_bytes_cifrado, num_lsb=2)
                
                imagen_resultado.save(archivo_destino,format="PNG",compression_level=1)
                
                
                
                self.archivo_portador = Path(archivo_portador).name
                self.formato_archivo_portador = Path(archivo_portador).suffix
                
                self.nombre_contenido = "Texto"
                self.archivo_contenido = "String (Texto)"
                
                self.clave_recuperacion = f"{self.clave_recuperacion}|SrRTeXt"
                
                self.ruta_archivo_generado = archivo_destino
                self.tamano_archivo_generado = Path(self.ruta_archivo_generado).stat().st_size
                
                if self.tamano_archivo_generado > 1024 and self.tamano_archivo_generado < 1048576:
                    self.tamano_archivo_generado = f"{round(self.tamano_archivo_generado/1024,2)} KB"
                
                elif self.tamano_archivo_generado > 1048576 and self.tamano_archivo_generado < 1073741824:
                    self.tamano_archivo_generado = f"{round(self.tamano_archivo_generado/1048576,2)} MB"

                elif self.tamano_archivo_generado > 1073741824:
                    self.tamano_archivo_generado = f"{round(self.tamano_archivo_generado/1073741824,2)} GB"

                self.archivo_generado = Path(self.ruta_archivo_generado).name
                self.formato_archivo = Path(self.ruta_archivo_generado).suffix
                self.fecha = datetime.now().strftime("%Y_%m_%d_%H_%M_%S")

                
                return True
        
        except Exception as e:
            logger.error(f"Error al ocutar el texto: {e}")
            return False
    

    ############ CIFRADO Y DESOCULTAMIENTO DE ARCHIVOS ############

    #Extrae los datos de la imagen
    def extraer_data_de_imagen (self, archivo_portador,archivo_key,carpeta_destino = None):
        try:

            data_key = archivo_key.split("|")
            
            clave = data_key[0]
            formato = data_key[1]

            if formato == "SrRTeXt": #SI ES UNA CADENA DE TEXTO OCULTA
                texto_extraido = self.extraer_texto_de_imagen(archivo_portador,clave) #extraermos y desiframos el texto
                if texto_extraido:
                    return True
                
                return False
            
            else:
                archivo_extraido = self.extraer_archivo_de_imagen(archivo_portador,carpeta_destino,clave,formato)
            
                if archivo_extraido:
                    return True
                
                return False
        except Exception as e:
            logger.error(f"Error formato clave: {e}")
            return False
        
    #EXTRAER ARCHIVO DE IMAGEN
    def extraer_archivo_de_imagen (self, archivo_portador,carpeta_destino,clave, formato):
        fecha = datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
        nombre_tmp = f"cifrado_{fecha}_extract.vlkey"
        destino_tmp = ruta_tmp / nombre_tmp

        try: #DESOCULTAMOS EL ARCHIVO CIFRADO
            LSBSteg.recover_data(steg_image_path=(archivo_portador),output_file_path=destino_tmp, num_lsb=2)

            try:
                nombre = f"Recuperado_{fecha}"
                self._desencriptar_archivo(destino_tmp,clave,carpeta_destino,nombre,formato) #INICIAMOS EL PROCESO DE DESCIFRADO
                return True

            except Exception as e:
                logger.error(f"Error al desencriptar el archivo oculto: {e}")
                return False

        except Exception as e:
            logger.error(f"Error al extraer el archivo oculto de la imagen: {e}")
            return False

    #EXTRAER TEXTO DE IMAGEN
    def extraer_texto_de_imagen (self, archivo_portador,clave):
        
        try:
            with Image.open(archivo_portador) as imagen:
                
                texto_recuperado = recover_message_from_image(input_image=imagen, num_lsb=2) 
                
                self.texto_extraido = self._desencriptar_texto(texto_recuperado,clave)
                
                if self.texto_extraido:
                    return True
                else:
                    return False
        except Exception as e:
            logger.error(f"Error al extraer el texto de la imagen: {e}")
            return False
            
    def _desencriptar_texto (self,contenido_cifrado,clave):
        """
        Desencripta el texto cifrado
        """

        try:
            fernet = Fernet(clave.encode("utf-8"))
            texto_decifrado = fernet.decrypt(contenido_cifrado).decode("utf-8")
            return texto_decifrado
        except Exception as e:
            logger.error(f"Error al desencriptar el texto: {e}")
            return False


    ################### AUDIO ######
    def archivo_audio (self,archivo_portador, archivo_oculto, archivo_destino):
        """
        Oculta el archivo en el audio
        """
        
        self._generar_clave()
        archivo_cifrado = self._cifrar_archivo(archivo_oculto)
        
        if not archivo_cifrado:
            return False
        
        bytes_ocultos = Path(archivo_cifrado).stat().st_size #obtenemos el tamaño del archivo (la cantidad de bytes que sera ocultados)

        try:
            WavSteg.hide_data(sound_path =str(archivo_portador), file_path =str(archivo_cifrado), output_path=str(archivo_destino), num_lsb=2)

            self.archivo_portador = Path(archivo_portador).name
    
            self.nombre_contenido = Path(archivo_oculto).name
            self.archivo_contenido = Path(archivo_oculto).suffix
            
            self.ruta_archivo_generado = archivo_destino
            self.tamano_archivo_generado = Path(self.ruta_archivo_generado).stat().st_size
            
            if self.tamano_archivo_generado > 1024 and self.tamano_archivo_generado < 1048576:
                self.tamano_archivo_generado = f"{round(self.tamano_archivo_generado/1024,2)} KB"
            
            elif self.tamano_archivo_generado > 1048576 and self.tamano_archivo_generado < 1073741824:
                self.tamano_archivo_generado = f"{round(self.tamano_archivo_generado/1048576,2)} MB"

            elif self.tamano_archivo_generado > 1073741824:
                self.tamano_archivo_generado = f"{round(self.tamano_archivo_generado/1073741824,2)} GB"
            
            self.archivo_generado = Path(self.ruta_archivo_generado).name
            self.formato_archivo = Path(self.ruta_archivo_generado).suffix
            self.fecha = datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
            
            #mezclamos la clave + el formato del archivo + la cantidad de bytes ocultos (informacion necesaria para desencriptar)
            self.clave_recuperacion = f"{self.clave_recuperacion}|{self.archivo_contenido}|{bytes_ocultos}" 
            
            return True

        except Exception as e:
            logger.error(f"Error al ocutar el audio: {e}")
            return False
            
    def texto_audio (self,archivo_portador,archivo_texto,archivo_destino):
        """
        Oculta el texto en el audio
        """

        self.fecha = datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
        archivo_text_destino = ruta_tmp / f"vlkey{self.fecha}"

        self._generar_clave()

        try:
            with open (archivo_text_destino, "w", encoding="utf-8") as archivo_text:
                archivo_text.write(archivo_texto)

            archivo_cifrado = self._cifrar_archivo(archivo_text_destino)

            if not archivo_cifrado:
                return False

            bytes_ocultos = Path(archivo_cifrado).stat().st_size

            try:
                WavSteg.hide_data(sound_path =str(archivo_portador), file_path =str(archivo_cifrado), output_path=str(archivo_destino), num_lsb=2)
                
                self.clave_recuperacion = f"{self.clave_recuperacion}|SrRTeXt|{bytes_ocultos}"
                
                self.archivo_portador = Path(archivo_portador).name
                
                self.nombre_contenido = Path(archivo_text_destino).name
                self.archivo_contenido = Path(archivo_text_destino).suffix
                
                self.ruta_archivo_generado = archivo_destino
                self.tamano_archivo_generado = Path(self.ruta_archivo_generado).stat().st_size
                
                if self.tamano_archivo_generado > 1024 and self.tamano_archivo_generado < 1048576:
                    self.tamano_archivo_generado = f"{round(self.tamano_archivo_generado/1024,2)} KB"
                
                elif self.tamano_archivo_generado > 1048576 and self.tamano_archivo_generado < 1073741824:
                    self.tamano_archivo_generado = f"{round(self.tamano_archivo_generado/1048576,2)} MB"

                elif self.tamano_archivo_generado > 1073741824:
                    self.tamano_archivo_generado = f"{round(self.tamano_archivo_generado/1073741824,2)} GB"
                
                self.archivo_generado = Path(self.ruta_archivo_generado).name
                self.formato_archivo = Path(self.ruta_archivo_generado).suffix
                return True
            
            except Exception as e:
                logger.error(f"Error al ocutar el audio: {e}")
                return False

        except Exception as e:
            logger.error(f"Error al guardar el texto: {e}")
            return False

    def extraer_data_de_audio (self, archivo_portador,archivo_key,carpeta_destino = None):

        try:

            data_key = archivo_key.split("|")
            
            clave = data_key[0]
            formato = data_key[1]
            bytes_ocultos = int(data_key[2])
            
            if formato == "SrRTeXt": #SI ES UNA CADENA DE TEXTO OCULTA
                texto_extraido = self.extraer_texto_de_audio(archivo_portador,clave,bytes_ocultos) #extraermos y desiframos el texto
                if texto_extraido:
                    return True
                
                return False
            
            else:
                archivo_extraido = self.extraer_archivo_de_audio(archivo_portador,carpeta_destino,clave,bytes_ocultos,formato)
            
                if archivo_extraido:
                    return True
                
                return False

        except Exception as e:
            logger.error(f"Error formato clave: {e}")
            return False

    def extraer_archivo_de_audio(self,archivo_portador,carpeta_destino,clave,bytes_ocultos,formato):

        fecha = datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
        nombre_tmp = f"cifrado_{fecha}_extract.vlkey"
        destino_tmp = ruta_tmp / nombre_tmp

        try:
            #EXTRAERMOS EL ARCHIVO CIFRADO OCULTO EN EL AUDIO
            WavSteg.recover_data(sound_path=str(archivo_portador),output_path=str(destino_tmp),num_lsb=2,
            bytes_to_recover=bytes_ocultos)
            
            try:
                nombre = f"recuperado_{fecha}"
                self._desencriptar_archivo(destino_tmp,clave,carpeta_destino,nombre,formato) #INICIAMOS EL PROCESO DE DESCIFRADO
                return True

            except Exception as e:
                logger.error(f"Error al desencriptar el archivo oculto: {e}")
                return False
            
        except Exception as e:
            logger.error(f"Error al extraer el archivo oculto: {e}")
            return False

    def extraer_texto_de_audio(self,archivo_portador,clave,bytes_ocultos): #extraemos el texto de un audio
        """
        Extrae el texto de un audio (UN ARCHIVO TXT CIFRADO CON EL TEXTO DENTRO)
        """
        fecha = datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
        nombre_tmp = f"cifrado_{fecha}_extract.vlkey"
        destino_tmp = ruta_tmp / nombre_tmp
        
        try:
            WavSteg.recover_data(sound_path=str(archivo_portador),output_path=str(destino_tmp),num_lsb=2,
            bytes_to_recover=bytes_ocultos)
            
            arhivo_extraido = self._desencriptar_archivo(destino_tmp,clave,ruta_tmp,nombre_tmp,".txt")
            
            if arhivo_extraido: #SI EL ARCHIVO SE DESCIFRO CORRECTAMENTE LO LEEMOS Y RETORNAMOS EL TEXTO
                with open(f"{destino_tmp}.txt", "r", encoding="utf-8") as archivo:
                    self.texto_extraido = archivo.read()
                return True
            
            return False
        except Exception as e:
            logger.error(f"Error al extraer el texto de un audio: {e}")
            return False

    def exportar_clave (self, ruta_destino, clave):
        """
        Guarda la clave de descifrado
        """
        
        ruta_destino = Path(ruta_destino)
        
        if ruta_destino.suffix != ".vlkey":
            ruta_destino = f"{ruta_destino}.vlkey"
        
        try:
            with open (ruta_destino, "w", encoding="utf-8") as archivo:
                archivo.write(clave)
            return True
        except Exception as e:
            logger.error(f"Error al exportar la clave: {e}")
            return False
        
