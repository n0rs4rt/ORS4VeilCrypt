from pathlib import Path
import os 


BASE_DIR = Path(__file__).resolve().parents[1]

logs = BASE_DIR / 'LOGS'
logs.mkdir(exist_ok=True, parents=True)

ruta_db = BASE_DIR /"data_store"

ruta_tmp = Path( os.environ['TMP']) / "ORS4_VEILCRYPT"
ruta_tmp.mkdir(exist_ok=True, parents=True)

ruta_logo_ico = BASE_DIR / "assets" / "logo.ico"

#imagenes panel izquierdo op secciones
ruta_logo_png = BASE_DIR / "assets" / "logo.png"
ocultar = BASE_DIR / "assets" / "ocultar.png"
extraer = BASE_DIR / "assets" / "extraer.png"
texto_ocultar = BASE_DIR / "assets" / "texto_ocultar.png"
historial = BASE_DIR / "assets" / "historial.png"
acerca_de = BASE_DIR / "assets" / "acerca_de.png"
descargar = BASE_DIR / "assets" / "descargar.png"

#imagenes panel derecho op ocultar
imagen = BASE_DIR / "assets" / "imagen.png"
audio = BASE_DIR / "assets" / "audio.png"
carpeta = BASE_DIR / "assets" / "carpeta.png"
archivo = BASE_DIR / "assets" / "archivo.png"
texto = BASE_DIR / "assets" / "texto.png"

#imagenes panel derecho resultados
vista_previa = BASE_DIR / "assets" / "vista_previa.png"
alerta = BASE_DIR / "assets" / "alerta.png"

archivo_nombre = BASE_DIR / "assets" / "archivo_nombre.png"
formato = BASE_DIR / "assets" / "formato.png"
ruta_archivo_generado = BASE_DIR / "assets" / "ruta_archivo.png"
tamanio = BASE_DIR / "assets" / "tamanio.png"
key_recovery = BASE_DIR / "assets" / "key_recovery.png"
copiar = BASE_DIR / "assets" / "copiar.png"
exportar = BASE_DIR / "assets" / "exportar.png"

#imagen procesando
procesando = BASE_DIR / "assets" / "procesando.png"

#imagenes panel derecho op extraer
llave = BASE_DIR / "assets" / "llave.png"
desocultar = BASE_DIR / "assets" / "desocultar.png"

#imagenes del panel derecho vista_previa extraer
vista_previa_extraer = BASE_DIR / "assets" / "vista_previa_extraer.png"

#imagenes panel derecho resultado extraccion
archivo_extraido = BASE_DIR / "assets" / "archivo_extraido.png"
abrir_archivo = BASE_DIR / "assets" / "abrir_archivo.png"

#imagenes panel cifrart o decifrar en texto
candado = BASE_DIR / "assets" / "candado.png"
papelera = BASE_DIR / "assets" / "papelera.png"
cerrar = BASE_DIR / "assets" / "cerrar.png"

vista_previa_texto = BASE_DIR / "assets" / "vista_previa_texto.png"

#iamgenes acerca de
funciones = BASE_DIR /"assets" / "funciones.png"
msj = BASE_DIR /"assets" / "msj.png"
historial_op = BASE_DIR /"assets" / "historial_op.png"
recursos = BASE_DIR /"assets" / "recursos.png"

youtube = BASE_DIR /"assets" / "youtube.png"
instagram = BASE_DIR /"assets" / "instagram.png"
github = BASE_DIR /"assets" / "github.png"
documentacion = BASE_DIR /"assets" / "documentacion.png"