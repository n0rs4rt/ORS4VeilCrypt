import customtkinter as ctk, threading , os, webbrowser
import tkinter as tk
from CORE.LIMPIAR_TMP import limpiar_tmp
from tkinter import filedialog
from PIL import Image
from CTkDataTable import CTkDataTable, TableStyle

from CORE.CONFIG_LOGS import config_log
logger = config_log()

from CORE.ESTEGA import Esteganografia
from CORE.RUTAS import *
from CORE.HISTORIAL_DB import HistorialDB
from CORE.CHECK_UPDATE import consultar_update

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class Interfaz (ctk.CTk):
    def __init__ (self):
        super().__init__()

        limpiar_tmp()
        self.title("ORS4 VeilCrypt")
        ancho =1360
        alto = 750
        
        self.iconbitmap(str(ruta_logo_ico))
        
        x = (self.winfo_screenwidth() // 2) - (ancho // 2)
        y = (self.winfo_screenheight() // 2) - (alto // 2)

        self.geometry(f"{ancho}x{alto}+{x}+{y}")
        self.minsize(ancho, alto)
        
        self.protocol("WM_DELETE_WINDOW", self.al_cerrar_app)
        
        self.secciones =[] #CONTIENE LOS WIDGET BOTONES DE LAS SECCIONES PARA MARCAR LA SELECCION
        
        self.contenedor_app()
        self.contenedores_principales()
        self._interfaz_op_secciones()
        self._interfaz_ocultar()
        

    def contenedor_app(self):
        """
        Contenedor BASE VENTANA
        """
        
        self.contenedor_ventana = ctk.CTkFrame(self, fg_color="#0d1826")
        self.contenedor_ventana.pack(fill="both", expand=True)
        self.contenedor_ventana.grid_rowconfigure(0, weight=1)
        self.contenedor_ventana.grid_columnconfigure(1, weight=1)
        
    
    def contenedores_principales (self):
        """
        Contenedores principales
        """

        #CONTENEDOR IZQUIEDO CON LAS SECCIONES
        self.contenedor_op_principales = ctk.CTkFrame (self.contenedor_ventana, fg_color="transparent") 
        self.contenedor_op_principales.grid(row=0, column=0, padx=(5,2), sticky="ns")
        self.contenedor_op_principales.grid_columnconfigure(0, weight=1)
        self.contenedor_op_principales.grid_rowconfigure(7, weight=1)

        #CONTENEDOR DERECHO CENTRAL TENDRA LOS CONTENEDORES OCULTAR, EXTRAER, HISTORIAL, ACERCA DE
        self.contenedor_central = ctk.CTkFrame (self.contenedor_ventana, fg_color="transparent") 
        self.contenedor_central.grid(row=0, column=1,  sticky="nsew")
        self.contenedor_central.grid_columnconfigure(0, weight=1)
        self.contenedor_central.grid_rowconfigure(0, weight=1)

    #INTERFAZ DE LAS OPCIONES DEL PANEL IZQUIERDO (OCULTAR, EXTRAR, TEXTO, HISOTRAL, ACERCA DE)
    def _interfaz_op_secciones (self):
        """Widgets PANEL IZQUIERDO"""
        #LOGO
        logo = ctk.CTkImage(light_image=Image.open(ruta_logo_png), size=(120, 180))
        label_logo = ctk.CTkLabel(self.contenedor_op_principales, image=logo, text="")
        label_logo.grid(row=0, column=0, padx=5, pady=(10,0))

        version = ctk.CTkLabel(self.contenedor_op_principales, text="v1.0.0", font=("Bahnschrift", 13, "bold"), text_color="#8b93a1")
        version.grid(row=1, column=0, padx=5, pady=(0,10))

        #FRAME BOTON OCULTAR
        self.frame_boton_ocultar = ctk.CTkFrame(self.contenedor_op_principales,fg_color="#6b65f7", corner_radius=5,cursor="hand2")
        self.frame_boton_ocultar.grid (row=2, column=0, padx=5, pady=(10,0), sticky="ew")
        self.frame_boton_ocultar.bind("<Button-1>", self._interfaz_ocultar)

        logo_ocultar = ctk.CTkImage(light_image=Image.open(ocultar), size=(22, 26))
        self.boton_ocultar = ctk.CTkButton(self.frame_boton_ocultar, text=" Ocultar", font=("segoe ui", 15, "bold"), text_color="white", image=logo_ocultar, compound="left", anchor="w", width=210,height=35 , fg_color="#19204a", hover_color="#19204a",corner_radius=0, border_spacing=14,cursor="hand2",command=lambda: self._interfaz_ocultar(self.boton_ocultar))
        self.boton_ocultar.grid(row=0, column=0, padx=(6,0), sticky="nsew")

        #FRAME BOTON EXTRAER
        self.frame_boton_extraer = ctk.CTkFrame(self.contenedor_op_principales,fg_color="#0d1826", corner_radius=5,cursor="hand2")
        self.frame_boton_extraer.grid (row=3, column=0, padx=5, pady=1, sticky="ew")
        self.frame_boton_extraer.bind("<Button-1>", self._interfaz_extraer)

        logo_extraer = ctk.CTkImage(light_image=Image.open(extraer), size=(21, 24))
        self.boton_extraer = ctk.CTkButton(self.frame_boton_extraer, text=" Extraer", font=("segoe ui", 15, "bold"), text_color="#8b93a1", image=logo_extraer, compound="left", anchor="w", width=210,height=35 , fg_color="#0d1826", hover_color="#0d1826",corner_radius=0, border_spacing=14,cursor="hand2",command=lambda: self._interfaz_extraer(self.boton_extraer))
        self.boton_extraer.grid(row=0, column=0, padx=(6,0), sticky="ew")

        #FRAME CIFRAR MENSAJE
        self.frame_texto_ocultar = ctk.CTkFrame(self.contenedor_op_principales,fg_color="#0d1826", corner_radius=5,cursor="hand2")
        self.frame_texto_ocultar.grid (row=4, column=0, padx=5, pady=1, sticky="ew")
        self.frame_texto_ocultar.bind("<Button-1>",)
        
        logo_texto = ctk.CTkImage(light_image=Image.open(texto_ocultar), size=(19, 24)) 
        self.boton_texto_ocultar = ctk.CTkButton(self.frame_texto_ocultar, text="Cifrado de mensaje", font=("segoe ui", 15, "bold"), text_color="#8b93a1",image=logo_texto,compound="left",anchor="w",width=210,height=35,fg_color="#0d1826",hover_color="#0d1826",corner_radius=0,border_spacing=14,cursor="hand2",command=lambda: self._interfaz_ocultar_texto(self.boton_texto_ocultar))
        self.boton_texto_ocultar.grid(row=0, column=0, padx=(6,0), sticky="ew")
        
        #FRAME HISTORIAL
        self.frame_historial = ctk.CTkFrame(self.contenedor_op_principales,fg_color="#0d1826", corner_radius=5,cursor="hand2")
        self.frame_historial.grid (row=5, column=0, padx=5, pady=1, sticky="ew")
        self.frame_historial.bind("<Button-1>", self._interfaz_historial)
        
        logo_historial = ctk.CTkImage(light_image=Image.open(historial), size=(19, 24))
        self.boton_historial = ctk.CTkButton(self.frame_historial,text=" Historial", font=("segoe ui", 15, "bold"), text_color="#8b93a1",image=logo_historial, compound="left", anchor="w", width=210,height=35 , fg_color="#0d1826", hover_color="#0d1826",corner_radius=0, border_spacing=14,cursor="hand2",command=lambda: self._interfaz_historial(self.boton_historial))
        self.boton_historial.grid(row=0, column=0, padx=(6,0), sticky="ew")

        #FRAME ACERCA DE
        self.frame_acerca_de = ctk.CTkFrame(self.contenedor_op_principales,fg_color="#0d1826", corner_radius=5,cursor="hand2")
        self.frame_acerca_de.grid (row=6, column=0, padx=5, pady=1, sticky="ew")
        self.frame_acerca_de.bind("<Button-1>", self._interfaz_acerca_de)

        logo_acerca_de = ctk.CTkImage(light_image=Image.open(acerca_de), size=(23, 24))
        self.boton_acerca_de = ctk.CTkButton(self.frame_acerca_de, text=" Acerca de", font=("segoe ui", 15, "bold"), text_color="#8b93a1",image=logo_acerca_de, compound="left", anchor="w", width=210,height=35, fg_color="#0d1826", hover_color="#0d1826",corner_radius=0, border_spacing=11,cursor="hand2",command=lambda: self._interfaz_acerca_de(self.boton_acerca_de))
        self.boton_acerca_de.grid(row=0, column=0, padx=(6,0), sticky="ew")

        self.secciones = [(self.frame_boton_ocultar, self.boton_ocultar),(self.frame_boton_extraer, self.boton_extraer),(self.frame_texto_ocultar, self.boton_texto_ocultar),(self.frame_historial, self.boton_historial),(self.frame_acerca_de, self.boton_acerca_de)] #PASAMOS TODOS LOS WIDGETS DE LAS SECCIONES PARA CAMBIAR LOS COLORES EN SELECCION

        #VERIFICAMOS NUEVAS VERSIONES
        
        nueva_version = consultar_update()
        if nueva_version:
            logo_descargar = ctk.CTkImage(light_image=Image.open(descargar), size=(21, 22))
            boton_new_version = ctk.CTkButton(self.contenedor_op_principales,image=logo_descargar,compound="left",text="Nueva versión disponible",font=("segoe ui", 13, "bold"), text_color="#f3f3f3",anchor="s",fg_color="#8a2121",hover_color="#8a2121",corner_radius=5,border_spacing=11,cursor="hand2",command=lambda:webbrowser.open("https://github.com/n0rs4rt/ORS4SysInfo"))
            boton_new_version.grid(row=7, column=0, padx=(6,10), pady=(10), sticky="ews")
        
        frame_linea = ctk.CTkFrame(self.contenedor_op_principales,fg_color="#1b2431",border_width=1,width=2)
        frame_linea.grid(row=0, column=1, rowspan=8, sticky="ns")

    #CAMBIA EL COLOR DE LOS BOTONES DE LAS SECCIONES (OCULTAR EXTRAER HISTORIAL ACERCA DE)
    def activar_desact_seleccion (self, widget):
        """
        Activa y desactiva los colores de seleccion de todos los widget que no sean el widget actual
        """
        for frame_boton in self.secciones:
            if widget in frame_boton:
                frame_boton[0].configure(fg_color="#6b65f7")
                frame_boton[1].configure(fg_color="#19204a", hover_color="#19204a",text_color="white")

            else:
                frame_boton[0].configure(fg_color="#0d1826")
                frame_boton[1].configure(fg_color="#0d1826", hover_color="#0d1826",text_color="#8b93a1")

    #INTERFAZ DE LA SECCION OCULTAR - TIENE LOS CONTENEDORES BASE DE OCULTAR Y RESULTADO
    def _interfaz_ocultar (self,widget=None):
        """
        CONTENEDOR TOTAL DE LA SECCION OCULTAR (CONTENEDORES OPCIONES DE SELECCION Y RESULTADO)
        """
        #SI LA INTERFAZ DE OCULTAR YA ESTA ACTIVA MOSTRANDOSE NO LO VUELVE A CREAR CUANDO SE HACE CLICK NUEVAMENTE
        if hasattr(self, "contenedor_ocultar") and self.contenedor_ocultar.winfo_exists():
            return
        
        #PROPIEDADES DEL BOTON OCULTAR DE LA _interfaz_op_secciones
        self.frame_boton_ocultar.configure(fg_color="#6b65f7")
        self.boton_ocultar.configure(fg_color="#19204a", hover_color="#19204a",text_color="white")

        if widget is not None: #SI LA INTERFAZ ES LLAMANDA DESDE LOS BOTONES DEL MENU IZQUIERDO ACTIVAMOS LA SELECCION Y ELIMINAMOS LOS CONTENEDORES ACTIVOS
            self.activar_desact_seleccion(widget)
            
            if hasattr(self, "contenedor_extraer") and self.contenedor_extraer.winfo_exists():
                self.contenedor_extraer.destroy()
            
            if hasattr(self,"contenedor_historial") and self.contenedor_historial.winfo_exists():
                self.contenedor_historial.destroy()

            if hasattr(self, "contenedor_cifrar_msj") and self.contenedor_cifrar_msj.winfo_exists():
                        self.contenedor_cifrar_msj.destroy()

        #CONTENEDOR DE TODOS LOS CONTENEDORES DE OCULTAR INFORMACION. ES EL CONTENEDOR QUE SE ELIMINAR AL CAMBIAR DE SECCION
        self.contenedor_ocultar = ctk.CTkFrame(self.contenedor_central,fg_color="transparent")
        self.contenedor_ocultar.grid(row=0, column=0, padx=10, pady=5, sticky="nsew")
        self.contenedor_ocultar.grid_rowconfigure(2, weight=1)
        self.contenedor_ocultar.grid_columnconfigure(1, weight=1)

        label_titulo = ctk.CTkLabel(self.contenedor_ocultar, text="Ocultar Informacion", font=("segoe ui", 28, ), text_color="white")
        label_titulo.grid(row=0, column=0, padx=10, pady=(2,0), sticky="w")

        label_detalles = ctk.CTkLabel(self.contenedor_ocultar, text="Oculta texto o arhivos dentro de imagenes o audio. Todo el contenido se cifra automaticamente para proteger tu informacion", font=("segoe ui", 13, ), text_color="#8b93a1",wraplength=600,justify="left")
        label_detalles.grid(row=1, column=0, padx=10, pady=2, sticky="w")
        
        #contenedor de resultados errores y vista previa
        self.contenedor_resultado = ctk.CTkFrame(self.contenedor_ocultar,fg_color="transparent")
        self.contenedor_resultado.grid(row=2, column=1, padx=(5,0), pady=(10,5), sticky="snew")
        self.contenedor_resultado.grid_columnconfigure(0, weight=1)
        self.contenedor_resultado.grid_rowconfigure(0, weight=1)

        self.op_contenedor_ocultar()
        self.contenedor_vista_estado()


    def op_contenedor_ocultar (self):
        """
        CONTENEDOR BASE DE LAS OPCIONES DE PORTADOR Y DESTINO
        """
        
        #contenedor izquierdo con todas las opciones y widget de ocultar
        
        frame_contenedor_OP = ctk.CTkFrame(self.contenedor_ocultar,fg_color="#132033",border_color="#2b3542", border_width=1,corner_radius=10)
        frame_contenedor_OP.grid(row=2, column=0, pady=(10,5), sticky="snew")
        frame_contenedor_OP.grid_rowconfigure(4, weight=1)

        self.contenedor_tipo_portador(frame_contenedor_OP)
        self.contenedor_a_ocultar(frame_contenedor_OP)
        self.contenedor_destino_ocultar(frame_contenedor_OP)
        
    #CONTENEDOR DE SELECCION RADIO - TIPO DE PORTADOR IMAGEN O AUDIO
    def contenedor_tipo_portador (self,frame_contenedor_OP):
        """
        CONTENEDOR CON LA OPCIONES DEL TIPO DE PORTADOR QUE TENDRA LOS DATOS OCULTOS
        """
        #FRAME TIPO DE PORTADOR
        frame_tipo_portador = ctk.CTkFrame(frame_contenedor_OP, fg_color="transparent")
        frame_tipo_portador.grid(row=0, column=0, columnspan=2, padx=5,pady=(2,5), sticky="we")
        
        label_portador = ctk.CTkLabel(frame_tipo_portador, text="Tipo de portador", font=("segoe ui", 13,"bold" ), text_color="#f3f3f3", anchor="s")
        label_portador.grid(row=0, column=0, padx=10, pady=(2,0), sticky="w")

        #FRAME CONETENDOR DE SELECCION TIPO IMAGEN
        self.contenedor_portador_imagen = ctk.CTkFrame(frame_tipo_portador,fg_color="transparent", border_width=1,width=1,corner_radius=8, border_color="#6770f9",cursor="hand2")
        self.contenedor_portador_imagen.grid(row=1, column=0, padx=10, sticky="we")

        #check radio selector Imagen
        self.op_tipo_portador = tk.StringVar(value="imagen")
        self.selector_imag = ctk.CTkRadioButton(self.contenedor_portador_imagen, text="", variable=self.op_tipo_portador, value="imagen",radiobutton_height=12, radiobutton_width=12, border_width_checked=3, border_width_unchecked=1,  width=8, fg_color="#6770f9", hover=False,border_color="#6770f9",command = self.activar_portador_imag)
        self.selector_imag.grid(row=0, column=0, rowspan=2,padx=(10,0), pady=5)
        
        logo_imag = ctk.CTkImage(light_image=Image.open(imagen), size=(40,40))
        label_imag = ctk.CTkLabel(self.contenedor_portador_imagen, text="", image=logo_imag, compound="left", text_color="#f3f3f3", font=("segoe ui", 13,), anchor="w")
        label_imag.grid(row=0, column=1, rowspan=2,padx=2, pady=5, sticky="w")
        
        label_titulo = ctk.CTkLabel(self.contenedor_portador_imagen, text="Imagen", font=("segoe ui", 13,"bold"), text_color="#f3f3f3",anchor="s",cursor="hand2")
        label_titulo.grid(row=0, column=3, padx=(5,10), pady=2, sticky="sw")

        label_descrip_imag = ctk.CTkLabel(self.contenedor_portador_imagen, text="Usar una imagen como archivo portador", font=("segoe ui", 13,), text_color="#8b93a1",anchor="n",cursor="hand2")
        label_descrip_imag.grid(row=1, column=3, padx=(5,10), pady=(0,5), sticky="en")

        #EVENTOS
        self.contenedor_portador_imagen.bind("<Button-1>", self.activar_portador_imag)
        label_imag.bind("<Button-1>", self.activar_portador_imag)
        label_titulo.bind("<Button-1>", self.activar_portador_imag)
        label_descrip_imag.bind("<Button-1>", self.activar_portador_imag)

        #FRAME CONETENDOR DE SELECCION AUDIO
        self.contenedor_portador_audio = ctk.CTkFrame(frame_tipo_portador,fg_color="transparent", border_width=2,width=1,corner_radius=8, border_color="#2b3542",cursor="hand2")
        self.contenedor_portador_audio.grid(row=1, column=1, padx=(0,10), pady=5, sticky="w")

        #check radio selector audio
        self.selector_audio= ctk.CTkRadioButton(self.contenedor_portador_audio,text="", variable=self.op_tipo_portador, value="audio",radiobutton_height=12, radiobutton_width=12, border_width_checked=3, border_width_unchecked=1,  width=8, fg_color="#6770f9", hover=False,border_color="#6770f9", cursor="hand2", command = self.activar_portador_audio)
        self.selector_audio.grid(row=0, column=0, rowspan=2,padx=(10,0), pady=5)

        logo_audio = ctk.CTkImage(light_image=Image.open(audio), size=(40,40))
        label_audio = ctk.CTkLabel(self.contenedor_portador_audio, text="", image=logo_audio, compound="left", text_color="#f3f3f3", font=("segoe ui", 13,), anchor="w",cursor="hand2")
        label_audio.grid(row=0, column=1, rowspan=2,padx=2, pady=5, sticky="w")

        label_titulo_audio = ctk.CTkLabel(self.contenedor_portador_audio, text="Audio", font=("segoe ui", 13,"bold"), text_color="#f3f3f3",anchor="s",cursor="hand2")
        label_titulo_audio.grid(row=0, column=3, padx=(5,10), pady=2, sticky="sw")

        label_descrip_audio = ctk.CTkLabel(self.contenedor_portador_audio, text="Usar un audio como archivo portador", font=("segoe ui", 13,), text_color="#8b93a1",anchor="n",cursor="hand2")
        label_descrip_audio.grid(row=1, column=3, padx=(5,10), pady=(0,5), sticky="en")

        label_archivo_portador = ctk.CTkLabel(frame_tipo_portador, text="Archivo Portador", font=("segoe ui", 13,"bold" ), text_color="#f3f3f3",anchor="s")
        label_archivo_portador.grid(row=2, column=0, padx=10, pady=(5,0), sticky="w")
        
        #EVENTOS
        self.contenedor_portador_audio.bind("<Button-1>", self.activar_portador_audio)
        label_audio.bind("<Button-1>", self.activar_portador_audio)
        label_titulo_audio.bind("<Button-1>", self.activar_portador_audio)
        label_descrip_audio.bind("<Button-1>", self.activar_portador_audio)
        
        #contenedor_ruta y boton seleccionar
        frame_seleccion = ctk.CTkFrame(frame_tipo_portador, fg_color= "transparent")
        frame_seleccion.grid(row=3, column=0, columnspan=2,padx=(5,10), sticky="we")
        frame_seleccion.grid_columnconfigure(0, weight=1)
        
        self.entry_ruta_portador = ctk.CTkEntry(frame_seleccion, width=500,fg_color="transparent", text_color="#8b93a1",border_color="#2b3542",border_width=1,corner_radius=8, height=35,state="readonly")
        self.entry_ruta_portador.grid(row=0, column=0, padx=(5,2), sticky="we")
    
        logo_carpeta = ctk.CTkImage(light_image=Image.open(carpeta), size=(20,18))
        boton_seleccionar = ctk.CTkButton(frame_seleccion, image=logo_carpeta, compound="left",text="Seleccionar",fg_color="#132033",hover_color="#19204a", border_width=1, text_color="#f3f3f3", border_color="#2b3542",width=120,height=35, corner_radius=8, cursor="hand2",command=self.boton_selec_portador)
        boton_seleccionar.grid(row=0, column=1, padx=(5,2), pady=5, sticky="we")
        
    #COLORES LA SELECCION DEL TIPO DE PORTADOR IMAGEN Y LIMPIA EL CAMPO DE RUTA AL SELECCIONAR
    def activar_portador_imag (self,event= None):
        """activa las opciones y colores al seleccionar el portador imagen"""
        
        self.contenedor_portador_audio.configure(border_color="#2b3542",border_width=2)
        self.contenedor_portador_imagen.configure(border_color="#6770f9",border_width=1)
        self.op_tipo_portador.set("imagen")
        
        ruta_portador = self.entry_ruta_portador.get().lower()
        
        if ruta_portador:
            #SI HAY UNA RUTA QUE FUE CARGADA ANTES POR LA OPCION DE AUDIO LA LIMPIAMOS
            if not Path(ruta_portador).suffix == ".png" and not Path(ruta_portador).suffix.lower() == ".bmp":
                self.entry_ruta_portador.configure(state="normal")
                self.entry_ruta_portador.delete(0, "end")
                self.entry_ruta_portador.configure(state="readonly",border_color="#2b3542")

    
    #COLORES LA SELECCION DEL TIPO DE PORTADOR AUDIO Y LIMPIA EL CAMPO DE RUTA AL SELECCIONAR
    def activar_portador_audio (self,event= None):
        """activa las opciones y colores al seleccionar el portador audio"""
        
        self.contenedor_portador_imagen.configure(border_color="#2b3542",border_width=2)
        self.contenedor_portador_audio.configure(border_color="#6770f9",border_width=1)
        self.op_tipo_portador.set("audio")
        
        ruta_portador = self.entry_ruta_portador.get().lower()
                
        if ruta_portador:
            #SI HAY UNA RUTA QUE FUE CARGADA ANTES POR LA OPCION DE IMAGEN LA LIMPIAMOS
            if not Path(ruta_portador).suffix == ".wav":
                self.entry_ruta_portador.configure(state="normal")
                self.entry_ruta_portador.delete(0, "end")
                self.entry_ruta_portador.configure(state="readonly",border_color="#2b3542")
    
    #BOTON DE SELECCIONAR RUTA DEL PORTADOR
    def boton_selec_portador (self):
        """
        PERMITE SELECCIONAR EL ARCHIVO PORTADOR Y COLOCA LA RUTA EN EL ENTRY
        """
        
        opcion_elegida = self.op_tipo_portador.get()

        if opcion_elegida == "imagen":
            ruta_imagen= filedialog.askopenfilename(filetypes=[("PNG", "*.png"), ("bmp","*.bmp")])
            
            if ruta_imagen:
                self.entry_ruta_portador.configure(state="normal")
                self.entry_ruta_portador.delete(0, "end")
                self.entry_ruta_portador.insert(0, ruta_imagen)
                self.entry_ruta_portador.configure(state="readonly",border_color="#2b3542")

        elif opcion_elegida == "audio":
            ruta_audio = filedialog.askopenfilename(filetypes=[("Archivos de audio", "*.wav")])
            
            if ruta_audio:
                self.entry_ruta_portador.configure(state="normal")
                self.entry_ruta_portador.delete(0, "end")
                self.entry_ruta_portador.insert(0, ruta_audio)
                self.entry_ruta_portador.configure(state="readonly",border_color="#2b3542")
                
    #INTERFAZ DE LA PARTE DE SELECCIONAR EL CONTENIDO A OCULTAR (TIPO DE ARCHIVO O CAJA TEXTO)
    def contenedor_a_ocultar (self, frame_contenedor_OP):
        """
        CONTENEDOR DE LAS OPCIONES DEL TIPO DE ARCHIVOS O CAJA TEXTO A OCULTAR
        """
        #FRAME CONTENEDOR BASE ARCHIVO TEXTO
        contenedor_tipo_contenido = ctk.CTkFrame(frame_contenedor_OP, fg_color="transparent")
        contenedor_tipo_contenido.grid(row=4, column=0, columnspan=2,padx=5, sticky="wens")
        contenedor_tipo_contenido.grid_rowconfigure(5, weight=1)

        label_tipo_contenido = ctk.CTkLabel(contenedor_tipo_contenido, text="Contenido a ocultar", font=("segoe ui", 13,"bold" ), text_color="#f3f3f3",anchor="s")
        label_tipo_contenido.grid(row=0, column=0, padx=10, pady=(0,5), sticky="w")

        #FRAME CONTENEDOR SELECCION ARCHIVO
        self.contenedor_select_archivo = ctk.CTkFrame(contenedor_tipo_contenido, fg_color="transparent",border_width=1,width=1,corner_radius=8, border_color="#6770f9",cursor="hand2")
        self.contenedor_select_archivo.grid(row=1, column=0, padx=10, pady=5, sticky="we")

        #check radio selector archivo
        self.opcion_tipo_contenido = ctk.StringVar(value="archivo")
        
        selector_archivo= ctk.CTkRadioButton(self.contenedor_select_archivo, text="", variable=self.opcion_tipo_contenido, value="archivo",radiobutton_height=12, radiobutton_width=12, border_width_checked=3, border_width_unchecked=1,  width=8, fg_color="#6770f9", hover=False,border_color="#6770f9",command=self.activar_selector_archivo)
        selector_archivo.grid(row=0, column=0, rowspan=2,padx=(10,0), pady=5)

        logo_archivo = ctk.CTkImage(light_image=Image.open(archivo), size=(28,35))
        label_logo_archivo = ctk.CTkLabel(self.contenedor_select_archivo, text="", image=logo_archivo, cursor="hand2")
        label_logo_archivo.grid(row=0, column=1, rowspan=2,padx=2, pady=5, sticky="w")

        label_titulo_archivo = ctk.CTkLabel(self.contenedor_select_archivo, text="Archivo", font=("segoe ui", 13,"bold"),text_color="#f3f3f3",anchor="s",cursor="hand2")
        label_titulo_archivo.grid(row=0, column=2, padx=(5,10), pady=2, sticky="ws")

        label_descrip_archivo = ctk.CTkLabel(self.contenedor_select_archivo, text="Selecciona el archivo deseas ocultar", font=("segoe ui", 13), text_color="#8b93a1",anchor="n",cursor="hand2")
        label_descrip_archivo.grid(row=1, column=2, padx=5, pady=(0,5), sticky="nw")

        #EVENTOS
        self.contenedor_select_archivo.bind("<Button-1>", self.activar_selector_archivo)
        label_logo_archivo.bind("<Button-1>", self.activar_selector_archivo)
        label_titulo_archivo.bind("<Button-1>", self.activar_selector_archivo)
        label_descrip_archivo.bind("<Button-1>", self.activar_selector_archivo)

        #FRAME_SELECCION TIPO TEXTO
        self.contenedor_select_texto = ctk.CTkFrame(contenedor_tipo_contenido, fg_color="transparent",border_width=1,width=1,corner_radius=8, border_color="#2b3542",cursor="hand2")
        self.contenedor_select_texto.grid(row=1, column=1, padx=(0,4), pady=5, sticky="we")

        selector_texto = ctk.CTkRadioButton (self.contenedor_select_texto,text="", variable=self.opcion_tipo_contenido, value="texto",radiobutton_height=12, radiobutton_width=12, border_width_checked=3, border_width_unchecked=1,  width=8, fg_color="#6770f9", hover=False,border_color="#6770f9",command=self.activar_selector_texto)
        selector_texto.grid(row=0, column=0, rowspan=2,padx=(10,0), pady=5)

        logo_texto = ctk.CTkImage(light_image=Image.open(texto), size=(25,19))
        label_logo_texto = ctk.CTkLabel(self.contenedor_select_texto, text="", image=logo_texto, cursor="hand2")
        label_logo_texto.grid(row=0, column=1, rowspan=2,padx=2, pady=5, sticky="w")

        label_titulo_texto = ctk.CTkLabel(self.contenedor_select_texto, text="Texto", font=("segoe ui", 13,"bold"), text_color="#f3f3f3",anchor="s",cursor="hand2")
        label_titulo_texto.grid(row=0, column=2, padx=(5,10), pady=(5,0), sticky="ws")

        label_descrip_texto = ctk.CTkLabel(self.contenedor_select_texto, text="Ingresa un texto deseas ocultar", font=("segoe ui", 13), text_color="#8b93a1",anchor="n",cursor="hand2")
        label_descrip_texto.grid(row=1, column=2, padx=(5,10), pady=(0,5), sticky="nw")

        #EVENTOS
        self.contenedor_select_texto.bind("<Button-1>", self.activar_selector_texto)
        label_logo_texto.bind("<Button-1>", self.activar_selector_texto)
        label_titulo_texto.bind("<Button-1>", self.activar_selector_texto)
        label_descrip_texto.bind("<Button-1>", self.activar_selector_texto)

        self.label_archivo_ocultar = ctk.CTkLabel(contenedor_tipo_contenido, text="Archivo a ocultar", font=("segoe ui", 13,"bold"), text_color="#f3f3f3",anchor="w")
        self.label_archivo_ocultar.grid(row=2, column=0, padx=10, pady=(5,0), sticky="w")

        #CONTENEDOR DE LA RUTA DEL ARCHIVO SELECCIONADO Y BOTON
        contenedor_archivo_seleccion = ctk.CTkFrame(contenedor_tipo_contenido,fg_color= "transparent" )
        contenedor_archivo_seleccion.grid(row=3, column=0, columnspan=2, padx=5, pady=(0,5), sticky="we")
        
        self.entry_ruta_a_ocultar = ctk.CTkEntry(contenedor_archivo_seleccion, width=500,fg_color="transparent",text_color="#8b93a1",border_color="#2b3542",border_width=1,corner_radius=8, height=35,state="readonly")
        self.entry_ruta_a_ocultar.grid(row=0, column=0, padx=10, pady=5, sticky="we")

        logo_carpeta = ctk.CTkImage(light_image=Image.open(carpeta), size=(20,18))
        self.boton_seleccionar = ctk.CTkButton(contenedor_archivo_seleccion, image=logo_carpeta, compound="left",text="Seleccionar",fg_color="#132033",hover_color="#19204a", border_width=1, text_color="#f3f3f3", border_color="#2b3542",width=120,height=35, corner_radius=8, cursor="hand2", command=self.boton_select_a_ocultar)
        self.boton_seleccionar.grid(row=0, column=1, padx=(0,5), pady=5, sticky="we")

        #CAJA DE TEXTO A OCULTAR
        self.texto = ctk.CTkLabel(contenedor_tipo_contenido, text="Texto a ocultar", font=("segoe ui", 13,"bold"), text_color="#8b93a1",anchor="w")
        self.texto.grid(row=4, column=0, padx=10, sticky="w")

        self.caja_texto = ctk.CTkTextbox(contenedor_tipo_contenido, width=500, height=100, fg_color="#132033",text_color="#f3f3f3",border_color="#2b3542",border_width=1,corner_radius=8, state="disabled",font=("segoe ui", 12),wrap="word",undo=True,autoseparators=True,maxundo=-1)
        self.caja_texto.grid(row=5, column=0, columnspan=2, padx=(10,5), pady=(0,5), sticky="wens")
        self.caja_texto.bind("<Button-3>",self.menu_contextual)

    
    #INTERFAZ DE LA PARTE DE SELECCIONAR EL DESTINO DE SALIDA GUARDAR HISTORIAL Y BOTON OCULTAR
    def contenedor_destino_ocultar (self,frame_contenedor_OP):
        """
        CONTENEDOR CON LAS OPCIONES DE DESTINO Y DE PROCESAR
        """

        #CONTENEDOR DE DESTINO
        contenedor_destino = ctk.CTkFrame(frame_contenedor_OP, fg_color="transparent")
        contenedor_destino.grid(row=5, column=0, columnspan=2,padx=5, sticky="snew")
        
        label_destino = ctk.CTkLabel(contenedor_destino, text="Destino de salida", font=("segoe ui", 13,"bold"), text_color="#f3f3f3",anchor="w")
        label_destino.grid(row=0, column=0, padx=10, pady=(5,0), sticky="w")
        
        #CONTENEDOR RUTA DESTINO Y BOTON
        contenedor_ruta_destino = ctk.CTkFrame(contenedor_destino,fg_color= "transparent" )
        contenedor_ruta_destino.grid(row=1, column=0, columnspan=2, padx=5, pady=(0,5), sticky="we")
        
        self.entry_destino = ctk.CTkEntry(contenedor_ruta_destino, width=500,fg_color="transparent",text_color="#8b93a1",border_color="#2b3542",border_width=1,corner_radius=8, height=35,state="readonly")
        self.entry_destino.grid(row=0, column=0, padx=10, pady=5, sticky="we")
        
        logo_carpeta = ctk.CTkImage(light_image=Image.open(carpeta), size=(20,18))
        boton_destino = ctk.CTkButton(contenedor_ruta_destino, image=logo_carpeta, compound="left",text="Seleccionar",fg_color="#132033",hover_color="#19204a", border_width=1, text_color="#f3f3f3", border_color="#2b3542",width=120,height=35, corner_radius=8, cursor="hand2", command=self.boton_destino_ocultar)
        boton_destino.grid(row=0, column=1, padx=(0,5), pady=5, sticky="we")
        
        self.caja_check = ctk.CTkCheckBox(contenedor_destino, text="Guardar esta operacion en el historial",fg_color="#6770f9",text_color="#f3f3f3",border_color="#6770f9",hover_color="#525ace",border_width=2,corner_radius=4, checkbox_height=18, checkbox_width=18,cursor="hand2")
        self.caja_check.select()
        self.caja_check.grid(row=2, column=0, padx=10, sticky="w")

        logo_ocultar = ctk.CTkImage(light_image=Image.open(ocultar), size=(25,28))
        self.boton_ocultar_informacion = ctk.CTkButton(contenedor_destino, image=logo_ocultar, compound="left", text="Ocultar informacion", font=("segoe ui", 16,"bold"),fg_color="#525ace",text_color="#f3f3f3",border_color="#6770f9",hover_color="#5d66ee",border_width=2,corner_radius=8, height=50,cursor="hand2", command=self.ocultar_informacion)
        self.boton_ocultar_informacion.grid(row=3, column=0, padx=10, columnspan=2, pady=(5,10), sticky="we")


    def activar_selector_archivo (self,event=None):
        """
        Activa el selector de archivos
        """

        self.contenedor_select_archivo.configure(border_color="#6770f9")
        self.contenedor_select_texto.configure(border_color="#2b3542")
        self.opcion_tipo_contenido.set("archivo")
        self.label_archivo_ocultar.configure(text_color="#f3f3f3")
        self.boton_seleccionar.configure(state="normal")
        
        self.texto.configure(text_color="#8b93a1")
        self.caja_texto.delete("1.0", "end")
        self.caja_texto.configure(state="disabled",fg_color="#132033",border_color="#2b3542")

    def activar_selector_texto (self,event=None):
        """
        Activa el selector de texto
        """
        
        self.contenedor_select_archivo.configure(border_color="#2b3542")
        self.contenedor_select_texto.configure(border_color="#6770f9")
        self.opcion_tipo_contenido.set("texto")
        self.boton_seleccionar.configure(state="disabled")
        
        self.label_archivo_ocultar.configure(text_color="#8b93a1")
        self.entry_ruta_a_ocultar.configure(state="normal",border_color="#2b3542")
        self.entry_ruta_a_ocultar.delete(0, "end")
        self.entry_ruta_a_ocultar.configure(state="readonly")
        
        self.texto.configure(text_color="#f3f3f3")
        self.caja_texto.configure(state="normal",fg_color="#0e1925")

    def boton_select_a_ocultar (self):
        """
        BOTON SELECCIONAR RUTA ARCHIVO OCULTAR
        """
        self.ruta_achivo_ocultar = filedialog.askopenfilename(filetypes=[("Archivos", "*.*")])
        
        if not self.ruta_achivo_ocultar:
            return
        
        self.entry_ruta_a_ocultar.configure(state="normal")
        self.entry_ruta_a_ocultar.delete(0, "end")
        self.entry_ruta_a_ocultar.insert(0, self.ruta_achivo_ocultar)
        self.entry_ruta_a_ocultar.configure(state="readonly",border_color="#2b3542")

    #BOTON SELECCIONAR RUTA DESTINO PNG O WAV
    def boton_destino_ocultar (self):
        """
        BOTON SELECCIONAR RUTA DESTINO OCULTAR
        """        
        if self.op_tipo_portador.get() == "imagen":
            ruta_destino_ocultar = filedialog.asksaveasfilename(defaultextension=".png",filetypes=[("PNG", "*.png")])
        
        elif self.op_tipo_portador.get() == "audio":
            ruta_destino_ocultar = filedialog.asksaveasfilename(defaultextension=".wav",filetypes=[("Archivos de audio", "*.wav")])
            
        if not ruta_destino_ocultar:
            return
        
        self.entry_destino.configure(state="normal")
        self.entry_destino.delete(0, "end")
        self.entry_destino.insert(0, ruta_destino_ocultar)
        self.entry_destino.configure(state="readonly",border_color="#2b3542")

    #INICIA EL PROCESO DE OCULTAR
    def ocultar_informacion (self):
        """INICIA EL PROCESO DE OCULTAR INFORMACION"""
        
        #obtenemos los valores
        tipo_portador = self.op_tipo_portador.get()
        archivo_portador = self.entry_ruta_portador.get().lower()#convierto en minusculas para evitar problemas con las extensiones

        tipo_contenido_ocultar = self.opcion_tipo_contenido.get()
        archivo_ocultar = self.entry_ruta_a_ocultar.get()
        contenido_caja_texto = self.caja_texto.get("1.0", "end").strip()
        
        archivo_destino = self.entry_destino.get().lower().strip()#convierto en minusculas para evitar problemas con las extensiones
        
        #si alguno de los campos esta vacio lo resaltamos en rojo
        if not archivo_portador:
            self.entry_ruta_portador.configure(border_color="#8a2121")
            return
        
        if tipo_contenido_ocultar == "archivo":
            
            if not archivo_ocultar:
                self.entry_ruta_a_ocultar.configure(border_color="#8a2121")
                return
        
        if tipo_contenido_ocultar == "texto":
            if not contenido_caja_texto:
                self.caja_texto.configure(border_color="#8a2121")
                return

        
        if not archivo_destino:
            self.entry_destino.configure(border_color="#8a2121")
            return
        

        ##si no hay ningun error, iniciamos el proceso dentro de un hilo para que la interfaz no se bloquee
        #desactivo el boton para evitar click duplicados rapidamente
        self.boton_ocultar_informacion.configure(state="disabled")
        self.procesando(self.contenedor_resultado)

        guardar_historial = self.caja_check.get()#obtenemos el valor de la caja de check
        
        threading.Thread(target=self.iniciar_proceso_ocultar, args=(archivo_portador,tipo_portador,tipo_contenido_ocultar,archivo_ocultar,contenido_caja_texto,archivo_destino,guardar_historial)).start()
        

    def iniciar_proceso_ocultar (self,archivo_portador,tipo_portador,tipo_contenido_ocultar,archivo_ocultar,contenido_caja_texto,archivo_destino,guardar_historial):
        """INICIA EL PROCESO DE OCULTAR INFORMACION EN IMAGEN O AUDIO"""
        
        esteganografia = Esteganografia()
        historial = HistorialDB()
        historial.crear_db()
                
        #OCUTAR EN IMAGEN
        if Path(archivo_portador).suffix == ".png" or Path(archivo_portador).suffix ==".bmp":
            
            #SI EL PORTADOR ES UNA IMAGEN
            if tipo_portador == "imagen":
                #verificamos que el destino sea un archivo imagen
                if Path(archivo_destino).suffix != ".png":
                    self.after(0,self.contenedor_error,self.contenedor_resultado,self.boton_ocultar_informacion)
                    self.after(0,self.boton_destino_ocultar())
                    return
                    
                    
                if tipo_contenido_ocultar == "archivo":
                    ocultado = esteganografia.archivo_imagen(archivo_portador,archivo_ocultar,archivo_destino)
                    
                    if not ocultado:
                        self.after(0,self.contenedor_error,self.contenedor_resultado,self.boton_ocultar_informacion)
                        return
                    
                    nombre_portador = esteganografia.archivo_portador
                    tipo_portador = "Imagen"
                    nombre_contenido = esteganografia.nombre_contenido
                    archivo_contenido = esteganografia.archivo_contenido
                    
                    archivo_resultante = esteganografia.archivo_generado
                    ruta_archivo_resultante = esteganografia.ruta_archivo_generado
                    tamanio_archivo_resultante = esteganografia.tamano_archivo_generado
                    formato_archivo_resultante = esteganografia.formato_archivo
                    clave_recuperacion = esteganografia.clave_recuperacion
                    fecha = esteganografia.fecha

                    
                elif tipo_contenido_ocultar == "texto":
                    ocultado = esteganografia.archivo_texto(archivo_portador,contenido_caja_texto,archivo_destino)
                    
                    if not ocultado:
                        self.after(0,self.contenedor_error,self.contenedor_resultado,self.boton_ocultar_informacion)
                        return
                    
                    nombre_portador = esteganografia.archivo_portador
                    tipo_portador = "Imagen"
                    nombre_contenido = esteganografia.nombre_contenido
                    archivo_contenido = esteganografia.archivo_contenido
                    archivo_resultante = esteganografia.archivo_generado
                    ruta_archivo_resultante = esteganografia.ruta_archivo_generado
                    tamanio_archivo_resultante = esteganografia.tamano_archivo_generado
                    formato_archivo_resultante = esteganografia.formato_archivo
                    clave_recuperacion = esteganografia.clave_recuperacion
                    fecha = esteganografia.fecha

            
            id_operacion = False
            if  guardar_historial:

                id_operacion =historial.insertar_historial(nombre_portador,tipo_portador,nombre_contenido,archivo_contenido,archivo_resultante,ruta_archivo_resultante,tamanio_archivo_resultante,fecha,clave_recuperacion, "NO")

            #CUANDO EL HILO TERMINE LLAMAMOS A LA FUNCION QUE CONTIENE LA INTERFAZ DEL RESULTADO TERMINADO
            self.after(0,self.contenedor_proceso_terminado, archivo_resultante,ruta_archivo_resultante,tamanio_archivo_resultante,formato_archivo_resultante,clave_recuperacion,guardar_historial,id_operacion,esteganografia,historial)

                        
        #OCULTAR EN AUDIO
        elif Path(archivo_portador).suffix == ".wav":
            #SI EL PORTADOR ES UN AUDIO
            if tipo_portador == "audio":
                #confirmamos que el destino sea un formato audio
                if Path(archivo_destino).suffix != ".wav":
                    self.after(0,self.contenedor_error,self.contenedor_resultado,self.boton_ocultar_informacion)
                    self.after(0,self.boton_destino_ocultar())
                    return
                if tipo_contenido_ocultar == "archivo":
                    ocultado = esteganografia.archivo_audio(archivo_portador,archivo_ocultar,archivo_destino)

                    if not ocultado:
                        self.after(0,self.contenedor_error,self.contenedor_resultado,self.boton_ocultar_informacion)
                        return

                    nombre_portador = esteganografia.archivo_portador
                    tipo_portador = "Audio"
                    nombre_contenido = esteganografia.nombre_contenido
                    archivo_contenido = esteganografia.archivo_contenido
                    archivo_resultante = esteganografia.archivo_generado
                    ruta_archivo_resultante = esteganografia.ruta_archivo_generado
                    tamanio_archivo_resultante = esteganografia.tamano_archivo_generado
                    formato_archivo_resultante = esteganografia.formato_archivo
                    clave_recuperacion = esteganografia.clave_recuperacion
                    fecha = esteganografia.fecha
                    
                elif tipo_contenido_ocultar == "texto":
                    
                    ocultado = esteganografia.texto_audio(archivo_portador,contenido_caja_texto,archivo_destino)
                    
                    if not ocultado:
                        self.after(0,self.contenedor_error,self.contenedor_resultado,self.boton_ocultar_informacion)
                        return
                    
                    nombre_portador = esteganografia.archivo_portador
                    tipo_portador = "Audio"
                    nombre_contenido = esteganografia.nombre_contenido
                    archivo_contenido = esteganografia.archivo_contenido
                    archivo_resultante = esteganografia.archivo_generado
                    ruta_archivo_resultante = esteganografia.ruta_archivo_generado
                    tamanio_archivo_resultante = esteganografia.tamano_archivo_generado
                    formato_archivo_resultante = esteganografia.formato_archivo
                    clave_recuperacion = esteganografia.clave_recuperacion
                    fecha = esteganografia.fecha

                
                id_operacion = False

                if  guardar_historial:

                    id_operacion = historial.insertar_historial(nombre_portador,tipo_portador,nombre_contenido,archivo_contenido,archivo_resultante,ruta_archivo_resultante,tamanio_archivo_resultante,fecha,clave_recuperacion, "NO")
                
            #CUANDO EL HILO TERMINE LLAMAMOS A LA FUNCION QUE CONTIENE LA INTERFAZ DEL RESULTADO TERMINADO
            self.after(0,self.contenedor_proceso_terminado, archivo_resultante,ruta_archivo_resultante,tamanio_archivo_resultante,formato_archivo_resultante,clave_recuperacion,guardar_historial,id_operacion,esteganografia,historial)

    #INTERFAZ CONTENEDOR VISTA PREVIA RESULTADO POR DEFECTO
    def contenedor_vista_estado (self):
        """
        CONTENEDOR VISTA DE RESULTADOS PREDETERMINADA (VISTRA PREVIA Y ESTADO)
        """
        
        self.contenedor_vista_previa = ctk.CTkFrame(self.contenedor_resultado,fg_color="#132033",border_color="#2b3542", border_width=1,corner_radius=10)
        self.contenedor_vista_previa.grid(row=0, column=0, sticky="wesn")
        self.contenedor_vista_previa.grid_columnconfigure(0, weight=1)
        
        label_titulo = ctk.CTkLabel(self.contenedor_vista_previa, text="Vista previa y estado", font=("segoe ui", 13, "bold" ), text_color="#f3f3f3",anchor="w")
        label_titulo.grid(row=0, column=0, padx= 10, pady=(10,70), sticky="w")
        
        imagen_previa = ctk.CTkImage(light_image=Image.open(vista_previa), size=(215,165))
        label_vista_previa = ctk.CTkLabel(self.contenedor_vista_previa, image=imagen_previa, text="")
        label_vista_previa.grid(row=1, column=0, padx=80, pady=(40,30), sticky="wesn")
        
        label1 = ctk.CTkLabel(self.contenedor_vista_previa, text="Aun no se ha procesado ninguna operacion", font=("segoe ui", 18), text_color="#f3f3f3",)
        label1.grid(row=2, column=0, padx=5, pady=(0,15), sticky="we")
        
        label2 = ctk.CTkLabel(self.contenedor_vista_previa, text="Completa los datos necesarios y pulsa 'Ocultar informacion' para iniciar el proceso.", font=("segoe ui", 13), text_color="#8b93a1", wraplength=380)
        label2.grid(row=3, column=0, padx=5, pady=(0,10), sticky="we")
        
    #INTERFAZ QUE MUESTRA EL CONTENEDOR DE QUE LA INFORMACION SE ESTA PROCESANDO
    def procesando (self, contenedor):
        """
        MUESTRA EL CONTENEDOR DE PROCESANDO CON LA BARRA DE PROGRESO
        RECIBE UN CONTENEDOR DONDE SERA COLOCADA (self.contenedor_resultado (ocultar) o self.contenedor_resultado_extraccion(extraer))
        """
        self.destruir_contenedores_resultados()

        self.contenedor_proceando = ctk.CTkFrame(contenedor,fg_color="#132033",border_color="#2b3542", border_width=1,corner_radius=10)
        self.contenedor_proceando.grid(row=0, column=0, sticky="wesn")
        self.contenedor_proceando.grid_columnconfigure(0, weight=1)

        label_titulo = ctk.CTkLabel(self.contenedor_proceando, text="Procesando informacion", font=("segoe ui", 17, "bold" ), text_color="#f3f3f3",)
        label_titulo.grid(row=0, column=0, padx= 10, pady=(85,0), sticky="we")

        label1 = ctk.CTkLabel(self.contenedor_proceando, text="Por favor espera mientras se procesa la información", font=("segoe ui", 13), text_color="#8b93a1",)
        label1.grid(row=1, column=0, padx=5, pady=(0,15), sticky="we")

        logo_procesando = ctk.CTkImage(light_image=Image.open(procesando), size=(190,180))
        label_logo_procesando = ctk.CTkLabel(self.contenedor_proceando, image=logo_procesando, text="")
        label_logo_procesando.grid(row=2, column=0, padx=5, pady=10, sticky="we")

        #BARRA DE PROGRESO
        self.barra_progreso = ctk.CTkProgressBar(self.contenedor_proceando, orientation="horizontal", fg_color="#2b3542", progress_color="#6b65f7", mode = "indeterminate", indeterminate_speed=2)
        self.barra_progreso.grid(row=3, column=0, padx=15, pady=(0,10), sticky="we")

        label_info = ctk.CTkLabel(self.contenedor_proceando, text="Ejecutando procesamiento criptográfico...", font=("segoe ui", 14, "bold"), text_color="#f3f3f3",)
        label_info.grid(row=4, column=0, padx=5, sticky="we")

        label_info1 = ctk.CTkLabel(self.contenedor_proceando, text="El proceso puede tardar varios segundos según el tamaño del archivo", font=("segoe ui", 13), text_color="#8b93a1",)
        label_info1.grid(row=5, column=0, padx=5, pady=(0,10), sticky="we")

        self.barra_progreso.start()

    #INTERFAZ QUE SE MUESTRA AL TERMINAR EL PROCESO CON EXITO (EL CONTENEDOR DE RESULTADO CON LA VISTA PREVIA DE LA INFORMACION)
    def contenedor_proceso_terminado (self, nombre_archivo,ruta_archivo,tamanio_archivo,formato_archivo,clave_recuperacion,guardar_historial,id_operacion,esteganografia,historial):
        """
        CONTENEDOR QUE MUESTRA EL RESULTADO EXITOSO DE LA OPERACION
        """
        self.destruir_contenedores_resultados()
        
        self.boton_ocultar_informacion.configure(state="normal") #activo nuevamente el boton una vez finalizado el proceso
        
        self.contenedor_de_resultado = ctk.CTkScrollableFrame(self.contenedor_resultado,fg_color="#132033",border_color="#2b3542", border_width=1,corner_radius=10,scrollbar_button_color="#2b3542", scrollbar_button_hover_color="#2b3542")
        self.contenedor_de_resultado.grid(row=0, column=0, sticky="wesn")
        self.contenedor_de_resultado._scrollbar.grid_configure(padx=(0, 2))#separacion de la barra scroll
        
        self.contenedor_de_resultado.grid_columnconfigure(0, weight=1)

        label_titulo = ctk.CTkLabel(self.contenedor_de_resultado, text="Resultado generado", font=("segoe ui", 13, "bold" ), text_color="#f3f3f3",anchor="w")
        label_titulo.grid(row=0, column=0, sticky="w")

        #contenedor de la imagen vista previa
        contenedor_imagen = ctk.CTkFrame(self.contenedor_de_resultado,fg_color="#101B2C",border_color="#6770f9", border_width=1,corner_radius=10)
        contenedor_imagen.grid(row=1, column=0, padx=5, pady=5, sticky="wesn")
        contenedor_imagen.grid_columnconfigure(0, weight=1)
        
        if Path(ruta_archivo).suffix == ".png":
            imagen_previa = Image.open(ruta_archivo)
            imagen_previa.thumbnail((400,350),Image.Resampling.LANCZOS)
            imagen_resultado = ctk.CTkImage(light_image=imagen_previa, size=(imagen_previa.size))
        
        elif Path(ruta_archivo).suffix == ".wav":
            imagen_resultado = ctk.CTkImage(light_image=Image.open(audio), size=(280,180))
            

        label_vista_previa = ctk.CTkLabel(contenedor_imagen, image=imagen_resultado, text="",)
        label_vista_previa.grid(row=0, column=0, padx=5, pady=5, sticky="wesn")

        #Contenedor datos imagen
        contenedor_datos_imagen = ctk.CTkFrame(self.contenedor_de_resultado,fg_color="#101B2C",border_color="#6770f9", border_width=1,corner_radius=10)
        contenedor_datos_imagen.grid(row=2, column=0, pady=5, sticky="wesn")
        contenedor_datos_imagen.grid_columnconfigure(0, weight=0)
        contenedor_datos_imagen.grid_columnconfigure(1, weight=1)
        contenedor_datos_imagen.grid_columnconfigure(2, weight=0)

        logo_archivo = ctk.CTkImage(light_image=Image.open(archivo_nombre), size=(14,16))
        label_archivo = ctk.CTkLabel(contenedor_datos_imagen, text="   Nombre del archivo", font=("segoe ui", 13), text_color="#8b93a1",image=logo_archivo, compound="left", )
        label_archivo.grid(row=0, column=0, padx=(15,25), pady=(5,10), sticky="w")
        
        label_nombre_archivo = ctk.CTkLabel(contenedor_datos_imagen, text=nombre_archivo , font=("segoe ui", 13), text_color="#f3f3f3",anchor="w")
        label_nombre_archivo.grid(row=0, column=1, padx=5, pady=(5,10), sticky="w")                                                                                                                                                                                         
        logo_formato = ctk.CTkImage(light_image=Image.open(formato), size=(14,16))
        label_formato = ctk.CTkLabel(contenedor_datos_imagen, text="   Formato", font=("segoe ui", 13), text_color="#8b93a1",image=logo_formato, compound="left", )
        label_formato.grid(row=1, column=0, padx=(15,25), pady=2, sticky="w")
        
        label_formato_archivo = ctk.CTkLabel(contenedor_datos_imagen, text=formato_archivo , font=("segoe ui", 13), text_color="#f3f3f3",anchor="w")
        label_formato_archivo.grid(row=1, column=1, padx=5, sticky="w")
        
        logo_tamano = ctk.CTkImage(light_image=Image.open(tamanio), size=(14,16))
        label_tamano = ctk.CTkLabel(contenedor_datos_imagen, text="   Tamano", font=("segoe ui", 13), text_color="#8b93a1",image=logo_tamano, compound="left", )
        label_tamano.grid(row=2, column=0, padx=(15,25), pady=5, sticky="w")
        
        label_tamano_archivo = ctk.CTkLabel(contenedor_datos_imagen, text=tamanio_archivo , font=("segoe ui", 13), text_color="#f3f3f3",anchor="w")
        label_tamano_archivo.grid(row=2, column=1, padx=5, sticky="w")
        
        logo_ruta = ctk.CTkImage(light_image=Image.open(ruta_archivo_generado), size=(14,14))
        label_ruta = ctk.CTkLabel(contenedor_datos_imagen, text="   Ruta", font=("segoe ui", 13), text_color="#8b93a1",image=logo_ruta, compound="left", )
        label_ruta.grid(row=3, column=0, padx=(15,25), sticky="w")
        
        label_ruta_archivo = ctk.CTkEntry(contenedor_datos_imagen, font=("segoe ui", 13), width=300,text_color="#f3f3f3",state="normal",fg_color="#101B2C")
        label_ruta_archivo.grid(row=3, column=1, padx=5, pady=5, sticky="we")
        
        label_ruta_archivo.insert(0, ruta_archivo)
        label_ruta_archivo.configure(state="readonly",border_color="#2b3542")

        #contenedor de la llave de recuperacion
        contenedor_key_recovery = ctk.CTkFrame(self.contenedor_de_resultado,fg_color="#101B2C",border_color="#6770f9", border_width=1,corner_radius=10)
        contenedor_key_recovery.grid(row=3, column=0, pady=2, sticky="wesn")
        contenedor_key_recovery.grid_columnconfigure(1, weight=1)

        logo_key = ctk.CTkImage(light_image=Image.open(key_recovery), size=(20,20))
        label_clave = ctk.CTkLabel(contenedor_key_recovery, text="", image=logo_key, compound="left", anchor="s")
        label_clave.grid(row=0, column=0, padx=15, pady=(5,10), rowspan=2, sticky="w")

        label_titulo_key = ctk.CTkLabel(contenedor_key_recovery, text="Clave de recuperacion", font=("segoe ui", 17, "bold"), text_color="#f3f3f3",anchor="s")
        label_titulo_key.grid(row=0, column=1, padx=(0,5),pady=2, sticky="w")

        label_descrip_key = ctk.CTkLabel(contenedor_key_recovery, text="La clave es necesaria para extraer el contenido oculto ", font=("segoe ui", 13), text_color="#8b93a1",anchor="w")
        label_descrip_key.grid(row=1, column=1, padx=(0,5), sticky="w")

        entry_key = ctk.CTkEntry(contenedor_key_recovery, font=("segoe ui", 16), width=300,text_color="#d14641",state="normal",fg_color="#101B2C")
        entry_key.grid(row=2, column=0, columnspan=2, padx=15, pady=(10,5), sticky="we")

        entry_key.insert(0, clave_recuperacion)
        entry_key.configure(state="readonly")

        #contenedor de botones centrado
        contenedor_botones = ctk.CTkFrame(contenedor_key_recovery,fg_color="#101B2C")
        contenedor_botones.grid(row=3, column=0, columnspan=2, padx=5, pady=2, sticky="wesn")
        contenedor_botones.grid_columnconfigure(0, weight=1)
        contenedor_botones.grid_columnconfigure(1, weight=1)

        logo_copiar = ctk.CTkImage(light_image=Image.open(copiar), size=(16,16))
        boton_copiar = ctk.CTkButton(contenedor_botones, image=logo_copiar, compound="left", border_spacing=15,text="  Copiar", font=("segoe ui", 14), text_color="#f3f3f3",fg_color="#101B2C", hover_color="#2b3542", border_width=1, border_color="#2b3542",height=40,command=lambda: self.copiar(clave_recuperacion),cursor="hand2")
        boton_copiar.grid(row=0, column=0, padx=15, pady=(5,8), sticky="we")
        
        logo_exportar = ctk.CTkImage(light_image=Image.open(exportar), size=(16,15))
        boton_guardar =ctk.CTkButton(contenedor_botones, image=logo_exportar, compound="left", border_spacing=15,text="  Exportar clave .vlkey", font=("segoe ui", 14), text_color="#f3f3f3",fg_color="#101B2C", hover_color="#2b3542", border_width=1,border_color="#2b3542", height=40,command=lambda: self.exportar_clave(clave_recuperacion,guardar_historial,id_operacion,esteganografia,historial),cursor="hand2")
        boton_guardar.grid(row=0, column=1, padx=(0,5), pady=(5,10), sticky="we")

    #CONTENEDOR DE ERROR PARA LOS RESULTADOS DE OCULTAR Y EXTRAER
    def contenedor_error (self,contenedor,boton):
        """
        CONTENEDOR DE RESULTADOS DE ERRORES 
        RECIBE UN CONTENEDOR DONDE SERA COLOCADA (EN OCULTAR O EXTRAER)
        RECIBE UN BOTON (OCULTAR O DESOCULTAR) PARA ACTIVARLO
        """
        
        self.destruir_contenedores_resultados()
        
        #Activamos el boton una vez termine el proceso (self.boton_ocultar_informacion o self.boton_desocultar_informacion)
        boton.configure(state="normal") 
        
        self.contenedor_de_error = ctk.CTkFrame(contenedor,fg_color="#132033",border_color="#2b3542", border_width=1,corner_radius=10)
        self.contenedor_de_error.grid(row=0, column=0, sticky="wesn")
        self.contenedor_de_error.grid_columnconfigure(0, weight=1)
        
        label_titulo = ctk.CTkLabel(self.contenedor_de_error, text="Estado de la operacion", font=("segoe ui", 13, "bold" ), text_color="#f3f3f3",anchor="w")
        label_titulo.grid(row=0, column=0, padx= 10, pady=(10,40), sticky="w")
        
        logo_alerta = ctk.CTkImage(light_image=Image.open(alerta), size=(175,165))
        label_alerta = ctk.CTkLabel(self.contenedor_de_error, image=logo_alerta, text="")
        label_alerta.grid(row=1, column=0, padx=80, pady=(40,10), sticky="wesn")
        
        
        label1 = ctk.CTkLabel(self.contenedor_de_error, text="No se pudo completar la operación", font=("segoe ui", 18, "bold"), text_color="#d14641",)
        label1.grid(row=2, column=0, padx=5, pady=(0,10), sticky="we")
        
        label2 = ctk.CTkLabel(self.contenedor_de_error, text="La operación no pudo completarse. Revisa los archivos seleccionados, los datos introducidos y vuelve a intentarlo", font=("segoe ui", 13), text_color="#8b93a1", wraplength=380)
        label2.grid(row=3, column=0, padx=5, pady=(0,10), sticky="we")
        
        #CONTENEDOR DE FRAME CAUSAS (PARA CENTRARLO MEDIANTE COLUMNAS)
        contenedor_causa = ctk.CTkFrame(self.contenedor_de_error, fg_color= "transparent")
        contenedor_causa.grid(row=4, column=0, padx=5, pady=20, sticky="wsne")
        contenedor_causa.grid_columnconfigure(0, weight=1)
        contenedor_causa.grid_columnconfigure(1, weight=0)
        contenedor_causa.grid_columnconfigure(2, weight=1)
        
        frame_causas = ctk.CTkFrame(contenedor_causa,fg_color="transparent",border_color="#d14641", border_width=1,corner_radius=10)
        frame_causas.grid(row=0, column=1, padx=5, pady=20, sticky="wsne")
        frame_causas.grid_columnconfigure(0, weight=1)
        
        label_causas = ctk.CTkLabel(frame_causas, text="Posibles causas: ", font=("segoe ui", 13, "bold"), text_color="#d14641",anchor="w")
        label_causas.grid(row=0, column=0, padx= 10, pady=5, sticky="we")
        
        label_causa1 = ctk.CTkLabel(frame_causas, text="• El contenido supera la capacidad disponible del portador.", font=("segoe ui", 13), text_color="#8b93a1",anchor="w")
        label_causa1.grid(row=1, column=0, padx= 10, sticky="we")
        
        label_causa2 = ctk.CTkLabel(frame_causas, text="• El archivo portador está dañado o no pudo procesarse correctamente.", font=("segoe ui", 13), text_color="#8b93a1",anchor="w",wraplength=380, justify="left")
        label_causa2.grid(row=2, column=0, padx= 10, pady=5,  sticky="we")
        
        label_causa3 = ctk.CTkLabel(frame_causas, text="• No fue posible crear o guardar el archivo en la ubicación de destino", font=("segoe ui", 13), text_color="#8b93a1",anchor="w",wraplength=360, justify="left")
        label_causa3.grid(row=3, column=0, padx= 10, pady=5, sticky="we")
        
        label_causa4 = ctk.CTkLabel(frame_causas, text="• Clave de recuperacion o archivo .vlkey invalido", font=("segoe ui", 13), text_color="#8b93a1",anchor="w",wraplength=380, justify="left")
        label_causa4.grid(row=4, column=0, padx= 10, pady=5, sticky="we")
        
    #DESTRUYE LOS CONTENEDORES DE RESULTADOS
    def destruir_contenedores_resultados (self):
        
        """DESTRUYE LOS CONTENEDORES DE RESULTADOS PARA QUE NO SE SOBREESCRIBAN EN CASO DE QUE EXISTAN """

        if hasattr(self, "contenedor_proceando") and self.contenedor_proceando.winfo_exists():
            self.contenedor_proceando.destroy()
        
        elif hasattr(self, "contenedor_de_resultado") and self.contenedor_de_resultado.winfo_exists():
            self.contenedor_de_resultado.destroy()
            
        elif hasattr(self, "contenedor_vista_previa") and self.contenedor_vista_previa.winfo_exists():
            self.contenedor_vista_previa.destroy()
            
        elif hasattr(self, "contenedor_de_error") and self.contenedor_de_error.winfo_exists():
            self.contenedor_de_error.destroy()
        
        elif hasattr(self,"contenedor_vista_previa_extraer") and self.contenedor_vista_previa_extraer.winfo_exists():
            self.contenedor_vista_previa_extraer.destroy()
        
        elif hasattr(self,"contenedor_extraccion_archivo") and self.contenedor_extraccion_archivo.winfo_exists():
            self.contenedor_extraccion_archivo.destroy()

    #EXPORTA LA CLAVE DE RECUPERACION Y ACTUALIZA EL REGISTRO EN LA BASE DE DATOS (EN EL CASO DE LA SECCION OCULTAR)
    def exportar_clave (self,clave_recuperacion,guardar_historial=None,id_operacion=None,esteganografia=None,historial=None):
        """
        Exporta la clave de recuperacion y actualiza el registro en la base de datos caso que sea necesario
        """
        
        ruta_destino = filedialog.asksaveasfilename(defaultextension=".vlkey",filetypes=[("Archivos de encriptación", "*.vlkey")])
        
        if not ruta_destino:
            return
        
        key_guardada = esteganografia.exportar_clave(ruta_destino,clave_recuperacion)
        
        #SI LA OPCION DE GUARDAR OPERACION ESTABA MARCADA AL MOMENTO DE PROCESAR SE ACTUALIZA EL REGISTRO SI LA CLAVE ES EXPORTADA
        if key_guardada:

            if guardar_historial:
                historial.actualizar_key_exportada(id_operacion)

    #MENU CLICK DERECHO PARA LA CAJA DE TEXTO
    def menu_contextual (self,event):
        menu = tk.Menu(self, tearoff=0, bg="#132033", fg="#8b93a1")
        menu.add_command(label="Copiar", command=self.copiar)
        menu.add_command(label="Pegar", command=self.pegar)
        menu.tk_popup(event.x_root, event.y_root)

    #COPIA LA INFORMACION (CAJA DE TEXTO, CLAVE DE CIFRADO O MSJ OCULTO) AL PORTAPAPELES DE WINDOWS
    def copiar (self, texto = None):
        """COPIA LA INFORMACION AL PORTAPAPELES DE WINDOWS"""
        if texto:
            self.clipboard_clear()
            self.clipboard_append(texto)
            self.update()
        
        else:
            try:
                texto = self.caja_texto.selection_get()
            except:
                texto = self.caja_texto.get("1.0", "end-1c")
                
            self.clipboard_clear()
            self.clipboard_append(texto)
            self.update()
            
    def pegar (self):
        """PEGA LA INFORMACION DEL PORTAPAPELES DE WINDOWS EN LA CAJA DE TEXTO"""
        
        texto = self.clipboard_get()
        self.caja_texto.insert("insert", texto)

    ##############################################EXTRAER
    
    #CONTENEDOR TOTAL DE LA SECCION EXTRAER Y TITULO
    def _interfaz_extraer (self,widget):

        self.activar_desact_seleccion(widget)
        if hasattr(self,"contenedor_ocultar") and self.contenedor_ocultar.winfo_exists():
            self.contenedor_ocultar.destroy()
        
        if hasattr(self,"contenedor_historial") and self.contenedor_historial.winfo_exists():
            self.contenedor_historial.destroy()
        """
        CONTENEDOR TOTAL DE LA SECCION EXTRAER (CONTENEDORES OPCIONES DE SELECCION Y RESULTADO)
        """
        
        if hasattr(self, "contenedor_cifrar_msj") and self.contenedor_cifrar_msj.winfo_exists():
            self.contenedor_cifrar_msj.destroy()
            
        ##SI LA INTERFAZ DE OCULTAR YA ESTA ACTIVA MOSTRANDOSE NO LO VUELVE A CREAR CUANDO SE HACE CLICK NUEVAMENTE
        if hasattr(self, "contenedor_extraer") and self.contenedor_extraer.winfo_exists():
            return


        #CONTENEDOR DE TODOS LOS CONTENEDORES DE EXTRAER INFORMACION. ES EL CONTENEDOR QUE SE ELIMINA AL CAMBIAR DE SECCION
        self.contenedor_extraer = ctk.CTkFrame(self.contenedor_central,fg_color="transparent")
        self.contenedor_extraer.grid(row=0, column=0, padx=10, pady=5, sticky="nsew")
        self.contenedor_extraer.grid_rowconfigure(2, weight=1)
        self.contenedor_extraer.grid_columnconfigure(1, weight=1)

        label_titulo = ctk.CTkLabel(self.contenedor_extraer, text="Extraer Informacion", font=("segoe ui", 28, ), text_color="white")
        label_titulo.grid(row=0, column=0, padx=10, pady=(2,0), sticky="w")

        label_detalles = ctk.CTkLabel(self.contenedor_extraer, text="Recupera texto o archivos ocultos dentro de imagenes o audios", font=("segoe ui", 13, ), text_color="#8b93a1",wraplength=600,justify="left")
        label_detalles.grid(row=1, column=0, padx=10, pady=2, sticky="w")

        #contenedor de opciones y vista previa
        self.contenedor_resultado_extraccion = ctk.CTkFrame(self.contenedor_extraer,fg_color="transparent")
        self.contenedor_resultado_extraccion.grid(row=2, column=1, padx=(5,0), pady=(10,5), sticky="snew")
        self.contenedor_resultado_extraccion.grid_columnconfigure(0, weight=1)
        self.contenedor_resultado_extraccion.grid_rowconfigure(0, weight=1)

        self.op_contenedor_extraer()
        self.contenedor_vista_estado_extraer()
        # self.contenedor_resultado_extraccion_texto()

    def op_contenedor_extraer (self):
        """
        CONTENEDOR BASE DE LAS OPCIONES DE EXTRAER Y DESTINO
        """
        
        #contenedor izquierdo con todas las opciones y widget de extraer
        
        frame_contenedor_OP = ctk.CTkFrame(self.contenedor_extraer,fg_color="#132033",border_color="#2b3542", border_width=1,corner_radius=10)
        frame_contenedor_OP.grid(row=2, column=0, pady=(10,5), sticky="snew")
        frame_contenedor_OP.grid_rowconfigure(4, weight=1)

        self.contenedor_tipo_portador(frame_contenedor_OP)
        self.contenedor_desencriptar(frame_contenedor_OP)
        # self.contenedor_destino_ocultar(frame_contenedor_OP)

    #INTERFAZ CONTENEDOR CON TODAS LAS OPCIONES PARA DESENCRIPTAR (TIPO PORTADOR, METODO DE DESENCRIPCION, BOTON DESOCULTAR)
    def contenedor_desencriptar (self, frame_contenedor_OP):
        """
        CONTENEDOR DE LAS OPCIONES DE DESENCRIPCION
        """
        #FRAME CONTENEDOR BASE METODO DE DESENCRIPCION (OPCIONES Y RUTAS)
        contenedor_tipo_desencriptar = ctk.CTkFrame(frame_contenedor_OP, fg_color="transparent")
        contenedor_tipo_desencriptar.grid(row=4, column=0, columnspan=2,padx=5, sticky="wens")
        contenedor_tipo_desencriptar.grid_rowconfigure(5, weight=1)
        contenedor_tipo_desencriptar.grid_columnconfigure(0, weight=1)
        contenedor_tipo_desencriptar.grid_columnconfigure(1, weight=1)

        label_tipo_contenido = ctk.CTkLabel(contenedor_tipo_desencriptar, text="Metodo de desencriptacion", font=("segoe ui", 13,"bold" ), text_color="#f3f3f3",anchor="s")
        label_tipo_contenido.grid(row=0, column=0, padx=10, pady=(0,5), sticky="w")

        #FRAME CONTENEDOR DESENCRIPCION POR CLAVE
        self.contenedor_clave = ctk.CTkFrame(contenedor_tipo_desencriptar, fg_color="transparent",border_width=1,width=1,corner_radius=8, border_color="#6770f9",cursor="hand2")
        self.contenedor_clave.grid(row=1, column=0, padx=10, pady=5, sticky="we")

        #CHECK RADIO SELECTOR CLAVE
        self.opcion_tipo_desencriptar = ctk.StringVar(value="clave")
        
        selector_clave= ctk.CTkRadioButton(self.contenedor_clave, text="", variable=self.opcion_tipo_desencriptar, value="clave",radiobutton_height=12, radiobutton_width=12, border_width_checked=3, border_width_unchecked=1,  width=8, fg_color="#6770f9", hover=False,border_color="#6770f9",command=self.activar_metodo_clave)
        selector_clave.grid(row=0, column=0, rowspan=2,padx=(10,0), pady=5)

        logo_llave = ctk.CTkImage(light_image=Image.open(llave), size=(32,32))
        label_logo_llave = ctk.CTkLabel(self.contenedor_clave, text="", image=logo_llave, cursor="hand2")
        label_logo_llave.grid(row=0, column=1, rowspan=2,padx=2, pady=5, sticky="w")

        label_titulo_llave = ctk.CTkLabel(self.contenedor_clave, text="Ingresar clave", font=("segoe ui", 13,"bold"),text_color="#f3f3f3",anchor="s",cursor="hand2")
        label_titulo_llave.grid(row=0, column=2, padx=(5,10), pady=2, sticky="ws")

        label_descrip_llave = ctk.CTkLabel(self.contenedor_clave, text="Escribe tu clave de recuperacion", font=("segoe ui", 13),text_color="#8b93a1",anchor="n",cursor="hand2")
        label_descrip_llave.grid(row=1, column=2, padx=5, pady=(0,5), sticky="nw")

        #EVENTOS
        self.contenedor_clave.bind("<Button-1>",command=self.activar_metodo_clave )
        label_logo_llave.bind("<Button-1>",command=self.activar_metodo_clave )
        label_titulo_llave.bind("<Button-1>", command=self.activar_metodo_clave )
        label_descrip_llave.bind("<Button-1>",command=self.activar_metodo_clave )

        #FRAME CONTENEDOR DESENCRIPCION POR ARCHIVO CLAVE
        self.contenedor_archivo_vlkey = ctk.CTkFrame(contenedor_tipo_desencriptar, fg_color="transparent",border_width=2,width=1,corner_radius=8, border_color="#2b3542",cursor="hand2")
        self.contenedor_archivo_vlkey.grid(row=1, column=1, padx=(0,4), pady=5, sticky="we")

        #CHECK RADIO SELECTOR ARCHIVO CLAVE
        selector_archivo_vlkey = ctk.CTkRadioButton (self.contenedor_archivo_vlkey,text="", variable=self.opcion_tipo_desencriptar, value="archivo",radiobutton_height=12, radiobutton_width=12, border_width_checked=3, border_width_unchecked=1,  width=8, fg_color="#6770f9", hover=False,border_color="#6770f9",command=self.activar_metodo_archivo_clave)
        selector_archivo_vlkey.grid(row=0, column=0, rowspan=2,padx=(10,0), pady=5)

        logo_archivo = ctk.CTkImage(light_image=Image.open(archivo), size=(28,35))
        label_logo_archivo = ctk.CTkLabel(self.contenedor_archivo_vlkey, text="", image=logo_archivo, cursor="hand2")
        label_logo_archivo.grid(row=0, column=1, rowspan=2,padx=2, pady=5, sticky="w")

        label_titulo_archivo = ctk.CTkLabel(self.contenedor_archivo_vlkey, text="Cargar archivo .vlkey", font=("segoe ui", 13,"bold"), text_color="#f3f3f3",anchor="s",cursor="hand2")
        label_titulo_archivo.grid(row=0, column=2, padx=(5,10), pady=(5,0), sticky="ws")

        label_descrip_archivo = ctk.CTkLabel(self.contenedor_archivo_vlkey, text="Usar un archivo de clave", font=("segoe ui", 13), text_color="#8b93a1",anchor="n",cursor="hand2")
        label_descrip_archivo.grid(row=1, column=2, padx=(5,10), pady=(0,5), sticky="nw")

        #EVENTOS
        self.contenedor_archivo_vlkey.bind("<Button-1>",command=self.activar_metodo_archivo_clave)
        label_logo_archivo.bind("<Button-1>",command=self.activar_metodo_archivo_clave)
        label_titulo_archivo.bind("<Button-1>", command=self.activar_metodo_archivo_clave)
        label_descrip_archivo.bind("<Button-1>",command=self.activar_metodo_archivo_clave)

        self.label_titulo_clave = ctk.CTkLabel(contenedor_tipo_desencriptar, text="Clave de recuperacion", font=("segoe ui", 13,"bold"), text_color="#f3f3f3",anchor="w")
        self.label_titulo_clave.grid(row=2, column=0, padx=10, pady=(5,0), sticky="w")
        
        #ENTRADA DE CLAVE RECUPERACION
        self.entry_clave = ctk.CTkEntry(contenedor_tipo_desencriptar, fg_color="transparent",text_color="#f3f3f3",border_color="#2b3542",border_width=1,corner_radius=8, height=35,state="normal",)
        self.entry_clave.grid(row=3, column=0, columnspan=2, padx=(10,5), pady=5, sticky="we")
        self.entry_clave.bind("<Button-3>",self.menu_contextual_llave)

        
        #CONTENEDOR DE LA RUTA DEL ARCHIVO CLAVE Y DESTINO
        contenedor_archivo_clave = ctk.CTkFrame(contenedor_tipo_desencriptar,fg_color= "transparent" )
        contenedor_archivo_clave.grid(row=4, column=0, columnspan=2, padx=5, pady=(0,5), sticky="we")
        contenedor_archivo_clave.grid_columnconfigure(0, weight=1)
        
        self.label_archivo_clave = ctk.CTkLabel(contenedor_archivo_clave, text="Archivo de clave (*.vlkey) (opcional)", font=("segoe ui", 13,"bold"), text_color="#8b93a1",anchor="w")
        self.label_archivo_clave.grid(row=0, column=0, padx=10, pady=(5,0), sticky="w")
        
        #RUTA DE ARCHIVO CLAVE
        self.entry_archivo_clave = ctk.CTkEntry(contenedor_archivo_clave,fg_color="transparent",text_color="#8b93a1",border_color="#2b3542",border_width=1,corner_radius=8, height=35,state="readonly")
        self.entry_archivo_clave.grid(row=1, column=0, padx=(5,2), pady=5, sticky="we")
        logo_carpeta = ctk.CTkImage(light_image=Image.open(carpeta), size=(20,18))
        
        #BOTON SELECCION ARCHIVO CLAVE
        self.boton_archivo_clave = ctk.CTkButton(contenedor_archivo_clave, image=logo_carpeta, compound="left",text="Seleccionar",fg_color="#132033",hover_color="#19204a", border_width=1, text_color="#f3f3f3", border_color="#2b3542",width=120,height=35, corner_radius=8, state="disabled", cursor="hand2", command=lambda:self.boton_seleccionar_archivo_clave(self.entry_archivo_clave))
        self.boton_archivo_clave.grid(row=1, column=1, padx=(2,0), pady=5, sticky="we")

        label_destino = ctk.CTkLabel(contenedor_archivo_clave, text="Destino de extraccion (opcional)", font=("segoe ui", 13,"bold"), text_color="#f3f3f3",anchor="w")
        label_destino.grid(row=2, column=0, padx=10, pady=(5,0), sticky="w")
        self.entry_ruta_destino = ctk.CTkEntry(contenedor_archivo_clave,fg_color="transparent",text_color="#8b93a1",border_color="#2b3542",border_width=1,corner_radius=8, height=35,state="readonly")
        self.entry_ruta_destino.grid(row=3, column=0, padx=(5,2), pady=5, sticky="we")
        
        self.boton_destino = ctk.CTkButton(contenedor_archivo_clave, image=logo_carpeta, compound="left",text="Seleccionar",fg_color="#132033",hover_color="#19204a", border_width=1, text_color="#f3f3f3", border_color="#2b3542",width=120,height=35, corner_radius=8, cursor="hand2",command=self.boton_destino_extraccion)
        self.boton_destino.grid(row=3, column=1, padx=(5,0), pady=5, sticky="we")

        logo_desocultar = ctk.CTkImage(light_image=Image.open(desocultar), size=(19,24))
        
        #BOTON DESOCULTAR INFORMACION
        self.boton_desocultar_informacion = ctk.CTkButton(contenedor_archivo_clave, image=logo_desocultar, compound="left", text="Desocultar informacion", font=("segoe ui", 16,"bold"),fg_color="#525ace",text_color="#f3f3f3",border_color="#6770f9",hover_color="#5d66ee",border_width=2,corner_radius=8, height=50,cursor="hand2",command=self.boton_inciar_desocultar)
        self.boton_desocultar_informacion.grid(row=4, column=0, padx=10, columnspan=2, pady=(5,10), sticky="we")

    #ACTIVA LAS OPCIONES Y COLORES AL SELECCIONAR EL TIPO DE METODO DE DESCRIPTACION
    def activar_metodo_clave (self,event= None):
        """activa las opciones y colores al seleccionar el metodo desencritacion via clave"""
        
        self.contenedor_archivo_vlkey.configure(border_color="#2b3542",border_width=2)
        self.contenedor_clave.configure(border_color="#6770f9",border_width=1)
        self.opcion_tipo_desencriptar.set("clave")
        
        self.label_titulo_clave.configure(text_color="#f3f3f3")
        self.entry_clave.configure(state="normal")
        
        self.entry_archivo_clave.configure(state="normal",border_color="#2b3542")
        self.entry_archivo_clave.delete(0, "end")
        self.entry_archivo_clave.configure(state="readonly")
        
        self.label_archivo_clave.configure(text_color="#8b93a1")
        self.boton_archivo_clave.configure(state="disabled")
        

    #ACTIVA LAS OPCIONES Y COLORES AL SELECCIONAR EL TIPO DE METODO DE DESCRIPTACIO
    def activar_metodo_archivo_clave (self,event= None):
        """activa las opciones y colores al seleccionar el  metodo desencritacion via archivo clave"""
        self.contenedor_clave.configure(border_color="#2b3542",border_width=2)
        self.contenedor_archivo_vlkey.configure(border_color="#6770f9",border_width=1)
        self.opcion_tipo_desencriptar.set("archivo")
        self.label_archivo_clave.configure(text_color="#f3f3f3")
        
        
        self.entry_clave.delete(0, "end")
        self.entry_clave.configure(border_color="#2b3542",state="disabled")
        self.label_titulo_clave.configure(text_color="#8b93a1")
            
        self.boton_archivo_clave.configure(state="normal")

    #SELECCIONA EL ARCHIVO CLAVE
    def boton_seleccionar_archivo_clave (self,widget):
        """selecciona el archivo clave"""
        
        ruta = filedialog.askopenfilename(filetypes=[("Archivos de clave","*.vlkey")])
        
        if not ruta:
            return
        
        if hasattr(self, "boton_vlkey") and self.boton_vlkey.winfo_exists():#SI ES LLAMADO DESDE EL BOTON VLKEY DE DESCIFRAR MENSAJE CAMBIAMOS EL COLOR Y EXTRAERMOS LA CLAVE
            self.boton_vlkey.configure(fg_color= "#1e245a",hover_color="#1e245a",border_color="#353e90")
            self.boton_clave.configure(fg_color= "#132033",hover_color="#132033",border_color="#2b3542")
            try:
                with open(ruta,"r",encoding="utf-8") as f:
                    ruta = f.read().strip()
            except Exception as e:
                logger.error(f"Error al abrir el archivo .vlkey: {e}")
                
            
        widget.configure(state="normal",border_color="#2b3542")
        widget.delete(0, "end")
        widget.insert(0, ruta)
        widget.configure(state="readonly")

    def boton_destino_extraccion (self):
        
        ruta = filedialog.askdirectory()
        
        if not ruta:
            return
    
        self.entry_ruta_destino.configure(state="normal",border_color="#2b3542")
        self.entry_ruta_destino.delete(0, "end")
        self.entry_ruta_destino.insert(0, ruta)
        self.entry_ruta_destino.configure(state="readonly")
    
    #COMPRUEBA E INCIA EL PROCESO DE DESOCULT
    def boton_inciar_desocultar(self):
        """
        INICIA EL PROCESO DE VERIFICACION PARA INICIAR EL PROCESO DE DESOCULTAR
        """
        
        archivo_portador = self.entry_ruta_portador.get()

        if not archivo_portador:
            self.entry_ruta_portador.configure(border_color="#8a2121")
            return

        metodo_seleccionado = self.opcion_tipo_desencriptar.get()

        if metodo_seleccionado == "clave":
            clave =self.entry_clave.get().strip()
            
            if not clave:
                self.entry_clave.configure(border_color="#8a2121")
                self.entry_archivo_clave.configure(border_color="#2b3542")
                return
            
            try:
                formato_archivo_oculto = clave.split("|")[1]
            except Exception as e:
                
                self.contenedor_error(self.contenedor_resultado_extraccion,self.boton_desocultar_informacion)#si la clave esta un un formato errado muestra error
                return
                
            if formato_archivo_oculto != "SrRTeXt": #SI NO ES UN TEXTO OCULTO ENTONCES ES UN ARCHIVO VERIFICAMOS QUE EXISTA UN DESTINO DE EXTRACCION
                carpeta_destino = self.entry_ruta_destino.get()
                
                if not carpeta_destino:#SI NO EXISTE UN DESTINO LO PEDIMOS
            
                    self.entry_ruta_destino.configure(border_color = "#8a2121")
                    self.boton_destino_extraccion()
                    return

                self.boton_desocultar_informacion.configure(state="disabled") #desactivamos el boton para evitar que se pulse varias veces al iniciar le proceso
                self.procesando(self.contenedor_resultado_extraccion)
                threading.Thread(target=self.iniciar_proceso_extraccion, args=(archivo_portador,clave,carpeta_destino),daemon=True).start()
            
            else:
                self.boton_desocultar_informacion.configure(state="disabled")
                #desactivamos el boton para evitar que se pulse varias veces al iniciar le proceso
                self.procesando(self.contenedor_resultado_extraccion)
                threading.Thread(target=self.iniciar_proceso_extraccion, args=(archivo_portador,clave),daemon=True).start() #se
                
                
        elif metodo_seleccionado == "archivo": #ARCHIVO .vlkey
            archivo_clave = self.entry_archivo_clave.get()
            
            if not archivo_clave:
                self.entry_archivo_clave.configure(border_color="#8a2121")
                self.entry_clave.configure(border_color="#2b3542")
                return
            
            try:
                with open(archivo_clave, "r") as archivo:#LEEMOS EL ARCHIVO CLAVE
                    clave = archivo.read()
                try:
                    formato_archivo_oculto = clave.split("|")[1]
                except Exception as e:

                    self.contenedor_error(self.contenedor_resultado_extraccion,self.boton_desocultar_informacion)#si la clave esta un un formato errado muestra error
                    return

                #SI NO ES UN TEXTO OCULTO ENTONCES ES UN ARCHIVO VERIFICAMOS QUE EXISTA UN DESTINO DE EXTRACCION
                if formato_archivo_oculto != "SrRTeXt":
                    
                    carpeta_destino = self.entry_ruta_destino.get()
                    
                    if not carpeta_destino:#SI NO EXISTE UN DESTINO LO PEDIMOS
                        self.entry_ruta_destino.configure(border_color = "#8a2121")
                        self.boton_destino_extraccion()
                        return

                    self.boton_desocultar_informacion.configure(state="disabled") #desactivamos el boton para evitar que se pulse varias veces al iniciar le proceso
                    self.procesando(self.contenedor_resultado_extraccion)
                    threading.Thread(target=self.iniciar_proceso_extraccion, args=(archivo_portador,clave,carpeta_destino),daemon=True).start()

                else:
                    self.boton_desocultar_informacion.configure(state="disabled") #desactivamos el boton para evitar que se pulse varias veces al iniciar le proceso
                    self.procesando(self.contenedor_resultado_extraccion)
                    threading.Thread(target=self.iniciar_proceso_extraccion, args=(archivo_portador,clave),daemon=True).start()

            except Exception as e:
                logger.error(f"Error al leer el archivo de clave en interfaz: {e}") 
                self.contenedor_error(self.contenedor_resultado_extraccion,self.boton_desocultar_informacion)           
                return

    #PROCESO EN HILO PARA DESOCULTAR 
    def iniciar_proceso_extraccion(self,archivo_portador,archivo_key,carpeta_destino = None):
        esteganografia = Esteganografia()
        if carpeta_destino: #SI HAY CARPETA DESTINO ES PORQUE LO QUE ESTA OCULTO DEBERIA SER UN ARCHIVO (SEGUN LA LLAVE KEY)

            if Path(archivo_portador).suffix.lower() == ".png":
                extraer_archivo_imagen =esteganografia.extraer_data_de_imagen(archivo_portador,archivo_key,carpeta_destino)
                if extraer_archivo_imagen: #SI LA EXTRACCION FUE EXITOSA
                    nombre_archivo = esteganografia.archivo_generado
                    formato_archivo = esteganografia.formato_archivo
                    tamano_archivo = esteganografia.tamano_archivo_generado
                    ruta_archivo = esteganografia.ruta_archivo_generado
                
                    self.after(0,self.contenedor_resultado_extraccion_archivo, nombre_archivo,formato_archivo, tamano_archivo,ruta_archivo, archivo_portador)

                else:
                    self.after(0,self.contenedor_error,self.contenedor_resultado_extraccion,self.boton_desocultar_informacion)
                    return

            #EXTRACCION DE AUDIO
            elif Path(archivo_portador).suffix.lower() == ".wav":
                extraer_archivo_audio = esteganografia.extraer_data_de_audio(archivo_portador,archivo_key,carpeta_destino)
                
                if extraer_archivo_audio: #SI LA EXTRACCION FUE EXITOSA
                    nombre_archivo = esteganografia.archivo_generado
                    formato_archivo = esteganografia.formato_archivo
                    tamano_archivo = esteganografia.tamano_archivo_generado
                    ruta_archivo = esteganografia.ruta_archivo_generado
                
                    self.after(0,self.contenedor_resultado_extraccion_archivo, nombre_archivo,formato_archivo, tamano_archivo,ruta_archivo, archivo_portador)

                else:
                    self.after(0,self.contenedor_error,self.contenedor_resultado_extraccion,self.boton_desocultar_informacion)
                    return
            
            
            else:
                self.after(0,self.contenedor_error,self.contenedor_resultado_extraccion,self.boton_desocultar_informacion)
                return

        else: #SI ES UN TEXTO OCULTO  

            if Path(archivo_portador).suffix.lower() == ".png":

                extraer_texto_imagen = esteganografia.extraer_data_de_imagen(archivo_portador,archivo_key)

                if extraer_texto_imagen:
                    texto_extraido = esteganografia.texto_extraido

                    self.after(0,self.contenedor_resultado_extraccion_texto,archivo_portador,texto_extraido)
                else:
                    self.after(0,self.contenedor_error,self.contenedor_resultado_extraccion,self.boton_desocultar_informacion)
                    return

            elif Path(archivo_portador).suffix.lower() == ".wav":

                extraer_texto_audio = esteganografia.extraer_data_de_audio(archivo_portador,archivo_key)

                if extraer_texto_audio:
                    texto_extraido = esteganografia.texto_extraido
                    self.after(0,self.contenedor_resultado_extraccion_texto,archivo_portador,texto_extraido)
                else:
                    self.after(0,self.contenedor_error,self.contenedor_resultado_extraccion,self.boton_desocultar_informacion)
                    return

            else:
                self.after(0,self.contenedor_error,self.contenedor_resultado_extraccion,self.boton_desocultar_informacion)
                return
    
    #CONTENEDOR POR DEFECTO VISTA PREVIA Y ESTADO EXTRAER 
    def contenedor_vista_estado_extraer (self):
        """
        CONTENEDOR VISTA DE RESULTADOS PREDETERMINADA (VISTRA PREVIA Y ESTADO)
        """
        
        self.contenedor_vista_previa_extraer = ctk.CTkFrame(self.contenedor_resultado_extraccion,fg_color="#132033",border_color="#2b3542", border_width=1,corner_radius=10)
        self.contenedor_vista_previa_extraer.grid(row=0, column=0, sticky="wesn")
        self.contenedor_vista_previa_extraer.grid_columnconfigure(0, weight=1)
        
        label_titulo = ctk.CTkLabel(self.contenedor_vista_previa_extraer, text="Vista previa y estado", font=("segoe ui", 13, "bold" ), text_color="#f3f3f3",anchor="w")
        label_titulo.grid(row=0, column=0, padx= 10, pady=(10,70), sticky="w")
        
        imagen_previa = ctk.CTkImage(light_image=Image.open(vista_previa_extraer), size=(255,195))
        label_vista_previa = ctk.CTkLabel(self.contenedor_vista_previa_extraer, image=imagen_previa, text="")
        label_vista_previa.grid(row=1, column=0, padx=80, pady=(40,30), sticky="wesn")
        
        label1 = ctk.CTkLabel(self.contenedor_vista_previa_extraer, text="Aun no se ha realizado ninguna extraccion", font=("segoe ui", 18), text_color="#f3f3f3",)
        label1.grid(row=2, column=0, padx=5, pady=(0,15), sticky="we")
        
        label2 = ctk.CTkLabel(self.contenedor_vista_previa_extraer, text="Selecciona un archivo portador, ingresa la clave o carga tu archivo .vlkey y pulsa 'Desocultar informacion'.", font=("segoe ui", 13), text_color="#8b93a1", wraplength=380)
        label2.grid(row=3, column=0, padx=5, pady=(0,10), sticky="we")

    ##INTERFAZ CONTENEDOR RESULTADO DE EXTRACCION DE ARCHIVO 
    def contenedor_resultado_extraccion_archivo(self,nombre_archivo,formato_archivo, tamano_archivo,ruta_archivo,archivo_portador):
        """
        CONTENEDOR RESULTADO DE EXTRACCION DE ARCHIVO
        """
        self.destruir_contenedores_resultados()
        self.boton_desocultar_informacion.configure(state="normal")
        
        self.contenedor_extraccion_archivo = ctk.CTkFrame(self.contenedor_resultado_extraccion,fg_color="#132033",border_color="#2b3542", border_width=1,corner_radius=10)
        self.contenedor_extraccion_archivo.grid(row=0, column=0, sticky="wesn")
        self.contenedor_extraccion_archivo.grid_columnconfigure(0, weight=1)
        self.contenedor_extraccion_archivo.grid_columnconfigure(1, weight=1)
        self.contenedor_extraccion_archivo.grid_columnconfigure(2, weight=1)

        label_titulo = ctk.CTkLabel(self.contenedor_extraccion_archivo, text="Resultado de la extraccion", font=("segoe ui", 13, "bold" ), text_color="#f3f3f3",anchor="w")
        label_titulo.grid(row=0, column=0,columnspan=2, padx= 10, pady=5, sticky="w")

        #contenedor de datos del archivo extraido
        contenedor_datos_archivo = ctk.CTkFrame(self.contenedor_extraccion_archivo,fg_color="#132033",border_color="#6770f9", border_width=1,corner_radius=10)
        contenedor_datos_archivo.grid(row=1, column=1, padx=10, sticky="wesn")
        contenedor_datos_archivo.grid_columnconfigure(0, weight=0)
        contenedor_datos_archivo.grid_columnconfigure(1, weight=1)
        contenedor_datos_archivo.grid_columnconfigure(2, weight=0)

        label_detalle_contenido = ctk.CTkLabel(contenedor_datos_archivo, text="Detalles del contenido extraido ", font=("segoe ui", 13, "bold" ), text_color="#f3f3f3",anchor="w")
        label_detalle_contenido.grid(row=0, column=0, columnspan=2,padx= 10, pady=10, sticky="w")

        logo_archivo = ctk.CTkImage(light_image=Image.open(archivo_nombre), size=(14,16))
        label_archivo = ctk.CTkLabel(contenedor_datos_archivo, text="   Nombre", font=("segoe ui", 13), text_color="#8b93a1",image=logo_archivo, compound="left", )
        label_archivo.grid(row=1, column=0, padx=(15,25), sticky="w")

        label_nombre_archivo = ctk.CTkLabel(contenedor_datos_archivo, text=nombre_archivo , font=("segoe ui", 13), text_color="#f3f3f3",anchor="w")
        label_nombre_archivo.grid(row=1, column=1, padx=5, pady=(5,0), sticky="w")                                                                                                                                                                                         
        logo_formato = ctk.CTkImage(light_image=Image.open(formato), size=(14,16))
        label_formato = ctk.CTkLabel(contenedor_datos_archivo, text="   Formato", font=("segoe ui", 13), text_color="#8b93a1",image=logo_formato, compound="left", )
        label_formato.grid(row=2, column=0, padx=(15,25),  sticky="w")

        label_formato_archivo = ctk.CTkLabel(contenedor_datos_archivo, text=formato_archivo , font=("segoe ui", 13), text_color="#f3f3f3",anchor="w")
        label_formato_archivo.grid(row=2, column=1, padx=5, sticky="w")

        logo_tamano = ctk.CTkImage(light_image=Image.open(tamanio), size=(14,16))
        label_tamano = ctk.CTkLabel(contenedor_datos_archivo, text="   Tamano", font=("segoe ui", 13), text_color="#8b93a1",image=logo_tamano, compound="left", )
        label_tamano.grid(row=3, column=0, padx=(15,25), sticky="w")

        label_tamano_archivo = ctk.CTkLabel(contenedor_datos_archivo, text=tamano_archivo , font=("segoe ui", 13), text_color="#f3f3f3",anchor="w")
        label_tamano_archivo.grid(row=3, column=1, padx=5, sticky="w")

        logo_ruta = ctk.CTkImage(light_image=Image.open(ruta_archivo_generado), size=(14,14))
        label_ruta = ctk.CTkLabel(contenedor_datos_archivo, text="   Ruta", font=("segoe ui", 13), text_color="#8b93a1",image=logo_ruta, compound="left", )
        label_ruta.grid(row=4, column=0, padx=(15,25),pady=(0,5), sticky="w")

        label_ruta_archivo = ctk.CTkEntry(contenedor_datos_archivo, font=("segoe ui", 13), width=300,text_color="#f3f3f3",state="normal",fg_color="#101B2C")
        label_ruta_archivo.grid(row=4, column=1, padx=5, pady=(0,5), sticky="we")

        label_ruta_archivo.insert(0, ruta_archivo)
        label_ruta_archivo.configure(state="readonly",border_color="#2b3542")

        #CONTENEDOR DE LA VISTA PREVIA DEL ARCHIVO EXTRAIDO Y BOTONES
        contenedor_vista_archivo = ctk.CTkFrame(self.contenedor_extraccion_archivo,fg_color="#132033",border_color="#6770f9", border_width=1,corner_radius=10)
        contenedor_vista_archivo.grid(row=2, column=1, padx=10, pady=10, sticky="wesn")
        contenedor_vista_archivo.grid_columnconfigure(0, weight=1)
        contenedor_vista_archivo.grid_columnconfigure(1, weight=1)

        label_titulo = ctk.CTkLabel(contenedor_vista_archivo, text="Archivo recuperado", font=("segoe ui", 13, "bold" ), text_color="#f3f3f3",anchor="w")
        label_titulo.grid(row=0, column=0,padx=10, pady=5, sticky="w")

        logo_archivo_extraido = ctk.CTkImage(light_image=Image.open(archivo_extraido), size=(110,110))
        label_archivo_extraido = ctk.CTkLabel(contenedor_vista_archivo,image=logo_archivo_extraido, text = "", compound="left", )
        label_archivo_extraido.grid(row=1, column=0, columnspan=2, padx=5, pady=5, sticky="we")

        logo_abrir_archivo= ctk.CTkImage(light_image=Image.open(abrir_archivo), size=(14,16))
        boton_abrir_archivo = ctk.CTkButton(contenedor_vista_archivo, image=logo_abrir_archivo, compound="left", border_spacing=15,text="  Abrir archivo", font=("segoe ui", 14), text_color="#f3f3f3",fg_color="#101B2C", hover_color="#2b3542", anchor="w", border_width=1, border_color="#2b3542",cursor="hand2",command=lambda:self.abrir_archivo(ruta_archivo))
        boton_abrir_archivo.grid(row=2, column=0, padx=15, pady=(5,8), sticky="we")

        logo_abrir_carpeta = ctk.CTkImage(light_image=Image.open(exportar), size=(16,16))
        boton_abrir_ubicacion =ctk.CTkButton(contenedor_vista_archivo, image=logo_abrir_carpeta, compound="left", border_spacing=15,text="  Abrir ubicacion", font=("segoe ui", 14), text_color="#f3f3f3",fg_color="#101B2C", hover_color="#2b3542",anchor="w", border_width=1,border_color="#2b3542", cursor="hand2",command=lambda:self.abrir_ubicacion(ruta_archivo))
        boton_abrir_ubicacion.grid(row=2, column=1, padx=(0,5), pady=5, sticky="we")

        #CONTENEDOR DE LA VISTA PREVIA DEL ARCHIVO PORTADOR
        contenedor_vista_portador = ctk.CTkFrame(self.contenedor_extraccion_archivo,fg_color="#132033",border_color="#6770f9", border_width=1,corner_radius=10)
        contenedor_vista_portador.grid(row=3, column=1, padx=10, sticky="wesn")
        contenedor_vista_portador.grid_columnconfigure(1, weight=1)

        label_titulo = ctk.CTkLabel(contenedor_vista_portador, text="Archivo portador", font=("segoe ui", 13, "bold" ), text_color="#f3f3f3",anchor="w")
        label_titulo.grid(row=0, column=0,columnspan=2,padx=10, pady=5, sticky="w")

        contenedor_imag_portador = ctk.CTkFrame(contenedor_vista_portador,fg_color="#132033",border_color="#2b3542", border_width=1,corner_radius=10)
        contenedor_imag_portador.grid(row=1, column=0, padx=5, pady=(0,2), sticky="wesn")
        contenedor_imag_portador.grid_columnconfigure(0, weight=1)

        #ruta del portador en Path
        archivo_portador = Path(archivo_portador)

        if archivo_portador.suffix == ".wav": #si el portador es un audio
            portador = ctk.CTkImage(light_image=Image.open(audio), size=(145,110))
        
        elif archivo_portador.suffix == ".png":
            imagen_portador = Image.open(archivo_portador)
            imagen_portador.thumbnail((145,145),Image.Resampling.LANCZOS)
            portador = ctk.CTkImage(light_image=imagen_portador, size=imagen_portador.size)

        label_imagen = ctk.CTkLabel(contenedor_imag_portador,image=portador, text = "", compound="left", )
        label_imagen.grid(row=0, column=0,  padx=5, pady=5, sticky="we")

        #contenedor de los datos del portador
        contenedor_datos_portador = ctk.CTkFrame(contenedor_vista_portador,fg_color="#132033",border_color="#2b3542", border_width=1,corner_radius=10)
        contenedor_datos_portador.grid(row=1, column=1, padx=(2,5), pady=(0,2), sticky="wesn")
        contenedor_datos_portador.grid_columnconfigure(1, weight=1)

        label_nombre_portador = ctk.CTkLabel(contenedor_datos_portador, text="  Nombre", font=("segoe ui", 13), text_color="#8b93a1",image=logo_archivo, compound="left", )
        label_nombre_portador.grid(row=0, column=0, padx=5,pady=2, sticky="w")

        label_nombre = ctk.CTkLabel(contenedor_datos_portador, text=archivo_portador.name, font=("segoe ui", 13), text_color="#f3f3f3",anchor="w")
        label_nombre.grid(row=0, column=1, pady=2,padx=5, sticky="w") 

        label_formato_portador = ctk.CTkLabel(contenedor_datos_portador, text="  Formato", font=("segoe ui", 13), text_color="#8b93a1",image=logo_formato, compound="left", )
        label_formato_portador.grid(row=1, column=0, padx=5,pady=2, sticky="w")

        formato_portador = ctk.CTkLabel(contenedor_datos_portador, text=archivo_portador.suffix , font=("segoe ui", 13), text_color="#f3f3f3",anchor="w")
        formato_portador.grid(row=1, column=1, pady=2,padx=5, sticky="w")

        label_ruta_portador = ctk.CTkLabel(contenedor_datos_portador, text="  Ruta", font=("segoe ui", 13), text_color="#8b93a1",image=logo_ruta, compound="left", )
        label_ruta_portador.grid(row=2, column=0, padx=5,pady=2, sticky="w")

        entry_ruta_portador = ctk.CTkEntry(contenedor_datos_portador, font=("segoe ui", 13), text_color="#f3f3f3",state="normal",fg_color="#101B2C")
        entry_ruta_portador.grid(row=2, column=1, padx=5, pady=2, sticky="we")

        entry_ruta_portador.insert(0,archivo_portador)
        entry_ruta_portador.configure(state="readonly",border_color="#2b3542")

    def abrir_archivo (self,archivo):
        """ABRE EL ARCHIVO EXTRAIDO"""
        archivo = Path(archivo)
        if archivo.exists():
            os.startfile(archivo)
        else:
            logger.error(f"El archivo {archivo} no existe")
            
    def abrir_ubicacion (self,ubicacion):
        """ABRE LA UBICACION DEL ARCHIVO EXTRAIDO"""
        ubicacion = Path(ubicacion).parent
        if ubicacion.exists():
            os.startfile(ubicacion)
        else:
            logger.error(f"La ubicacion {ubicacion} no existe")

    #INTERFAZ CONTENEDOR DE RESULTADOS TEXTO EXTRAÍDO AUDIO
    def contenedor_resultado_extraccion_texto (self,archivo_portador,texto_extraido):
        """
        CONTENEDOR QUE MUESTRA EL RESULTADO EXITOSO DE LA OPERACION
        """
        self.destruir_contenedores_resultados()
        
        self.boton_desocultar_informacion.configure(state="normal") #activo nuevamente el boton una vez finalizado el proceso
        
        self.contenedor_de_resultado = ctk.CTkScrollableFrame(self.contenedor_resultado_extraccion,fg_color="#132033",border_color="#2b3542", border_width=1,corner_radius=10,scrollbar_button_color="#2b3542", scrollbar_button_hover_color="#2b3542")
        self.contenedor_de_resultado.grid(row=0, column=0, sticky="wesn")
        self.contenedor_de_resultado._scrollbar.grid_configure(padx=(0, 2))#separacion de la barra scroll
        
        self.contenedor_de_resultado.grid_columnconfigure(0, weight=1)

        label_titulo = ctk.CTkLabel(self.contenedor_de_resultado, text="Resultado generado", font=("segoe ui", 13, "bold" ), text_color="#f3f3f3",anchor="w")
        label_titulo.grid(row=0, column=0, sticky="w")

        #contenedor de la imagen vista previa
        contenedor_imagen = ctk.CTkFrame(self.contenedor_de_resultado,fg_color="#101B2C",border_color="#6770f9", border_width=1,corner_radius=10)
        contenedor_imagen.grid(row=1, column=0, padx=5, pady=5, sticky="wesn")
        contenedor_imagen.grid_columnconfigure(0, weight=1)
        
        ruta_archivo = Path(archivo_portador)
        
        if Path(ruta_archivo).suffix == ".png":
            imagen_previa = Image.open(ruta_archivo)
            imagen_previa.thumbnail((400,350),Image.Resampling.LANCZOS)
            imagen_resultado = ctk.CTkImage(light_image=imagen_previa, size=(imagen_previa.size))
        
        elif Path(ruta_archivo).suffix == ".wav":
            imagen_resultado = ctk.CTkImage(light_image=Image.open(audio), size=(280,180))

        label_vista_previa = ctk.CTkLabel(contenedor_imagen, image=imagen_resultado, text="",)
        label_vista_previa.grid(row=0, column=0, padx=5, pady=5, sticky="wesn")

        #Contenedor datos imagen
        contenedor_datos_imagen = ctk.CTkFrame(self.contenedor_de_resultado,fg_color="#101B2C",border_color="#6770f9", border_width=1,corner_radius=10)
        contenedor_datos_imagen.grid(row=2, column=0, pady=5, sticky="wesn")
        contenedor_datos_imagen.grid_columnconfigure(0, weight=0)
        contenedor_datos_imagen.grid_columnconfigure(1, weight=1)
        contenedor_datos_imagen.grid_columnconfigure(2, weight=0)

        logo_archivo = ctk.CTkImage(light_image=Image.open(archivo_nombre), size=(14,16))
        label_archivo = ctk.CTkLabel(contenedor_datos_imagen, text="   Nombre del archivo", font=("segoe ui", 13), text_color="#8b93a1",image=logo_archivo, compound="left", )
        label_archivo.grid(row=0, column=0, padx=(15,25), pady=(5,0), sticky="w")

        label_nombre_archivo = ctk.CTkLabel(contenedor_datos_imagen, text=ruta_archivo.name , font=("segoe ui", 13), text_color="#f3f3f3",anchor="w")
        label_nombre_archivo.grid(row=0, column=1, padx=5, sticky="w")
    
        logo_formato = ctk.CTkImage(light_image=Image.open(formato), size=(14,16))
        label_formato = ctk.CTkLabel(contenedor_datos_imagen, text="   Formato", font=("segoe ui", 13), text_color="#8b93a1",image=logo_formato, compound="left", )
        label_formato.grid(row=1, column=0, padx=(15,25), sticky="w")
        
        label_formato_archivo = ctk.CTkLabel(contenedor_datos_imagen, text=ruta_archivo.suffix , font=("segoe ui", 13), text_color="#f3f3f3",anchor="w")
        label_formato_archivo.grid(row=1, column=1, padx=5, sticky="w")
        
        logo_tamano = ctk.CTkImage(light_image=Image.open(tamanio), size=(14,16))
        label_tamano = ctk.CTkLabel(contenedor_datos_imagen, text="   Tamano", font=("segoe ui", 13), text_color="#8b93a1",image=logo_tamano, compound="left", )
        label_tamano.grid(row=2, column=0, padx=(15,25), sticky="w")
        
        tamano = ruta_archivo.stat().st_size
        
        if tamano > 1024 and tamano < 1048576:
            tamano = f"{round(tamano/1024,2)} KB"
        
        elif tamano > 1048576 and tamano < 1073741824:
            tamano = f"{round(tamano/1048576,2)} MB"

        elif tamano > 1073741824:
            tamano = f"{round(tamano/1073741824,2)} GB"

        label_tamano_archivo = ctk.CTkLabel(contenedor_datos_imagen, text=tamano , font=("segoe ui", 13), text_color="#f3f3f3",anchor="w")
        label_tamano_archivo.grid(row=2, column=1, padx=5, sticky="w")
        
        logo_ruta = ctk.CTkImage(light_image=Image.open(ruta_archivo_generado), size=(14,14))
        label_ruta = ctk.CTkLabel(contenedor_datos_imagen, text="   Ruta", font=("segoe ui", 13), text_color="#8b93a1",image=logo_ruta, compound="left", )
        label_ruta.grid(row=3, column=0, padx=(15,25), sticky="w")
        
        label_ruta_archivo = ctk.CTkEntry(contenedor_datos_imagen, font=("segoe ui", 13), width=300,text_color="#f3f3f3",state="normal",fg_color="#101B2C")
        label_ruta_archivo.grid(row=3, column=1, padx=5, pady=(0,5), sticky="we")
        
        label_ruta_archivo.insert(0,str(ruta_archivo_generado))
        label_ruta_archivo.configure(state="readonly")

        #CONTENEDOR VISTA PREVIA DEL TEXTO OCULTO
        contenedor_texto = ctk.CTkFrame(self.contenedor_de_resultado,fg_color="#101B2C",border_color="#6770f9", border_width=1,corner_radius=10)
        contenedor_texto.grid(row=3, column=0, pady=5, sticky="wesn")
        contenedor_texto.grid_columnconfigure(0, weight=1)

        label_texto = ctk.CTkLabel(contenedor_texto, text="Mensaje oculto:", font=("segoe ui", 13,"bold"), text_color="#f3f3f3",anchor="w")
        label_texto.grid(row=0, column=0, padx=10, pady=5, sticky="w")
        
        caja_texto_oculto = ctk.CTkTextbox(contenedor_texto, font=("segoe ui", 13),text_color="#8b93a1",state="normal",fg_color="#101B2C",border_color="#2b3542", border_width=1,corner_radius=10,wrap="word")
        caja_texto_oculto.grid(row=1, column=0, padx=10, pady=5, sticky="wesn")

        caja_texto_oculto.insert("0.0",texto_extraido)
        caja_texto_oculto.configure(state="disabled")
        
        #contenedor de botones centrado
        contenedor_botones = ctk.CTkFrame(self.contenedor_de_resultado,fg_color="transparent")
        contenedor_botones.grid(row=4, column=0,padx=5, pady=2, sticky="wesn")
        contenedor_botones.grid_columnconfigure(0, weight=1)
        contenedor_botones.grid_columnconfigure(1, weight=1)

        logo_copiar = ctk.CTkImage(light_image=Image.open(copiar), size=(16,16))
        boton_copiar = ctk.CTkButton(contenedor_botones, image=logo_copiar, compound="left", border_spacing=15,text="  Copiar mensaje", font=("segoe ui", 14), text_color="#f3f3f3",fg_color="#101B2C", hover_color="#2b3542", border_width=1, border_color="#2b3542",height=30,cursor="hand2", command=lambda:self.copiar(texto_extraido))
        boton_copiar.grid(row=0, column=0, padx=15, pady=(5,8), sticky="we")
        
        logo_exportar = ctk.CTkImage(light_image=Image.open(exportar), size=(16,15))
        boton_guardar =ctk.CTkButton(contenedor_botones, image=logo_exportar, compound="left", border_spacing=15,text="  Guardar como archivo", font=("segoe ui", 14), text_color="#f3f3f3",fg_color="#101B2C", hover_color="#2b3542", border_width=1,border_color="#2b3542", height=30,cursor="hand2",command=lambda:self.guardar_texto_extraido(texto_extraido))
        boton_guardar.grid(row=0, column=1, padx=(0,5), pady=(5,10), sticky="we")

    #GUARDA EL TEXTO EXTRAIDO
    def guardar_texto_extraido(self,texto_extraido):
        """
        GUARDA EL TEXTO EXTRAIDO
        """
        ruta = filedialog.asksaveasfilename(defaultextension=".txt",filetypes=[("Archivos de texto", "*.txt"),("Todos los archivos", "*.*")])
        if not ruta:
            return
        
        try:
            with open(ruta, "w") as f:
                f.write(texto_extraido)
        except Exception as e:
            logger.error(f"Error al guardar el archivo: {e} ")

    def menu_contextual_llave (self,event):
        """
        MENU CONTEXTUAL QUE APARECE EN EL CAMPO DE LA LLAVE
        """
        #CAMPO DE LLAVE EN EXTRAER (ESTEGANOGRAFIA)
        if hasattr(self, "entry_clave") and event.widget == self.entry_clave.focus_get() and self.opcion_tipo_desencriptar.get() == "clave" and self.entry_clave.winfo_exists():
            menu = tk.Menu(self, tearoff=0,bg="#132033", fg="#8b93a1")
            menu.add_command(label="Pegar", command=lambda:self.pegar_clave(self.entry_clave))
            menu.tk_popup(event.x_root, event.y_root)

        #CAMPO DE LLAVE EN CIFRAR
        elif hasattr(self, "entry_clave_vlkey") and event.widget == self.entry_clave_vlkey.focus_get() and self.entry_clave_vlkey.winfo_exists():
            menu = tk.Menu(self, tearoff=0,bg="#132033", fg="#8b93a1")
            menu.add_command(label="Pegar", command=lambda:self.pegar_clave(self.entry_clave_vlkey))
            menu.tk_popup(event.x_root, event.y_root)


    def pegar_clave (self,widget):
        """
        PEGA LA LLAVE EN EL CAMPO DE LA LLAVE
        """
        try:
            clave = self.clipboard_get().strip()
            widget.delete(0, "end")
            widget.insert(0,clave)
        except Exception as e:
            logger.error(f"Error al pegar la llave: {e}")
            

    
    ########################################### CIFRAR  MENSAJE ####################################################
    def _interfaz_ocultar_texto (self,widget):

        """
        CONTENEDOR TOTAL DE LA SECCION EXTRAER (CONTENEDORES OPCIONES DE SELECCION Y RESULTADO)
        """

        self.msj = None # VARIABLE QUE ALMACENA EL MSJ DE LA CAJA DE TEXTO CIFRAR Y DESCIFRAR CON EL OBJETIVO DE CONTROLAR EL MAXIMO DE CARACTERES (METODO pegar_msj_caja_cifrar_desifrar)
        
        self.activar_desact_seleccion(widget)

        if hasattr(self,"contenedor_ocultar") and self.contenedor_ocultar.winfo_exists():
            self.contenedor_ocultar.destroy()

        if hasattr(self, "contenedor_extraer") and self.contenedor_extraer.winfo_exists():
            self.contenedor_extraer.destroy()

        if hasattr(self,"contenedor_historial") and self.contenedor_historial.winfo_exists():
            self.contenedor_historial.destroy()

        ####### SI LA INTERFAZ DE OCULTAR YA ESTA ACTIVA MOSTRANDOSE NO LO VUELVE A CREAR CUANDO SE HACE CLICK NUEVAMENTE
        if hasattr(self, "contenedor_cifrar_msj") and self.contenedor_cifrar_msj.winfo_exists():
            return

        #CONTENEDOR DE TODOS LOS CONTENEDORES DE LA SECCION CIFRAR EN MSJ. ES EL CONTENEDOR QUE SE ELIMINA AL CAMBIAR DE SECCION
        self.contenedor_cifrar_msj = ctk.CTkFrame(self.contenedor_central,fg_color="transparent")
        self.contenedor_cifrar_msj.grid(row=0, column=0, padx=10, pady=5, sticky="nsew")
        self.contenedor_cifrar_msj.grid_rowconfigure(3, weight=1)
        self.contenedor_cifrar_msj.grid_columnconfigure(1, weight=1)

        label_titulo = ctk.CTkLabel(self.contenedor_cifrar_msj, text="Cifrar mensajes", font=("segoe ui", 28, ), text_color="white")
        label_titulo.grid(row=0, column=0,columnspan=2, padx=10, pady=(2,0), sticky="w")

        label_detalles = ctk.CTkLabel(self.contenedor_cifrar_msj, text="Protege tus mensajes mediante cifrado seguro y genera una clave para poder recuperarlos", font=("segoe ui", 13, ), text_color="#8b93a1",wraplength=600,justify="left")
        label_detalles.grid(row=1, column=0, columnspan=2, padx=10, pady=2, sticky="w")

        #BOTON CIFRAR
        logo_candado = ctk.CTkImage(light_image=Image.open(candado), size=(16,20))
        self.boton_cifrar_msj = ctk.CTkButton(self.contenedor_cifrar_msj, image=logo_candado, compound="left",text="Cifrar mensaje", font=("segoe ui", 16, ),fg_color= "#1e245a",hover_color="#1e245a",text_color="white",width=300,height=45,cursor="hand2",border_width=2,corner_radius=8, border_color="#353e90",command=self.contenedor_op_cifrar_msj)
        self.boton_cifrar_msj.grid(row=2, column=0, padx=5, pady=10, sticky="w")

        #BOTON EXTRAER
        logo_extraer = ctk.CTkImage(light_image=Image.open(desocultar), size=(16,20))
        self.boton_descifrar_msj = ctk.CTkButton(self.contenedor_cifrar_msj, image=logo_extraer, compound="left", text="Decifrar mensaje", font=("segoe ui", 16, ),fg_color= "#132033",hover_color="#132033",text_color="white",width=300,height=45,cursor="hand2",border_width=2,corner_radius=8, border_color="#2b3542",command=self.contenedor_op_descifrar_msj)
        self.boton_descifrar_msj.grid(row=2, column=1, padx=5, pady=10, sticky="w")

        self.contenedor_op_cifrar_msj()

    def contenedor_op_cifrar_msj (self):

        """
        CONTENEDOR BASE DE LA SECCION CIFRAR MSJ
        ES EL CONTENEDOR QUE SE ELIMINA AL CAMBIAR LAS OPCIONES DE CIFRAR MSJ y DESIFRAR MSJ
        """

        self.boton_descifrar_msj.configure(border_color="#2b3542", fg_color="#132033", hover_color="#132033")
        self.boton_cifrar_msj.configure(border_color="#353e90", fg_color="#1e245a", hover_color="#1e245a")

        if hasattr(self,"contenedor_cifrar_resultados") and self.contenedor_cifrar_resultados.winfo_exists():
            return
        
        if hasattr(self,"contenedor_descifrar_resultados") and self.contenedor_descifrar_resultados.winfo_exists():
            self.contenedor_descifrar_resultados.destroy()


        #CONTENEDOR QUE TIENE LOS CONTENEDORES DE TEXTO PORTADOR Y RESULTADO) ES EL CONTENEDOR QUE SE DESTRUYE AL CAMBIAR LA OPCION A DECIFRAR MENSAJE
        self.contenedor_cifrar_resultados = ctk.CTkFrame(self.contenedor_cifrar_msj,fg_color="transparent")
        self.contenedor_cifrar_resultados.grid(row=3, column=0, columnspan=2, pady=5, sticky="nsew")
        self.contenedor_cifrar_resultados.grid_rowconfigure(0, weight=1)
        self.contenedor_cifrar_resultados.grid_columnconfigure(1, weight=1)

        #CONTENEDOR DE TEXTO PORTADOR
        self.contenedor_op_texto = ctk.CTkFrame(self.contenedor_cifrar_resultados,fg_color="#132033",border_color="#2b3542", border_width=1,corner_radius=10)
        self.contenedor_op_texto.grid(row=0, column=0, padx=(2,5), sticky="nsew")
        self.contenedor_op_texto.grid_rowconfigure(2, weight=1)


        label_portador = ctk.CTkLabel(self.contenedor_op_texto, text="Mensaje a cifrar", font=("segoe ui", 13,"bold" ), text_color="#f3f3f3")
        label_portador.grid(row=0, column=0, padx=10, pady=(10,0), sticky="w")

        label_descrip_portador = ctk.CTkLabel(self.contenedor_op_texto, text="Escribe o pega (Ctrl + V) el mensaje que deseas cifrar.", font=("segoe ui", 13, ), text_color="#8b93a1",wraplength=600,justify="left")
        label_descrip_portador.grid(row=1, column=0, padx=10, pady=(0,2), sticky="w")

        #CAJA DE TEXTO
        self.caja_portador = ctk.CTkTextbox(self.contenedor_op_texto, width=600, height=450, fg_color="#132033",text_color="#8b93a1",border_color="#2b3542",border_width=1,corner_radius=8,font=("segoe ui", 13),wrap="word",undo=True,autoseparators=True,maxundo=-1)
        self.caja_portador.grid(row=2, column=0, padx=10, pady=(0,10), sticky="nsew")
        self.caja_portador.bind("<Control-v>", self.pegar_msj_caja_cifrar_desifrar)

        logo_ocultar = ctk.CTkImage(light_image=Image.open(ocultar), size=(25,28))
        self.boton_cifrar = ctk.CTkButton(self.contenedor_op_texto, image=logo_ocultar, compound="left", text="Cifrar mensaje", font=("segoe ui", 16,"bold"),fg_color="#525ace",text_color="#f3f3f3",border_color="#6770f9",hover_color="#5d66ee",border_width=2,corner_radius=8, height=50,cursor="hand2",command=self.inciar_cifrar_msj)
        self.boton_cifrar.grid(row=3, column=0, padx=10, columnspan=2, pady=(5,10), sticky="we")

        self.contenedor_resultado_texto() #CONTENEDOR DE TEXTO RESULTADO

    #INICIA LA VERIFICACION DEL CONTENIDO Y EL PROCESO PARA OCULTAR EL MSJ
    def inciar_cifrar_msj(self):
        """
        VERIFICA QUE EXISTA CONTENIDO PARA OCULTAR
        E INICIA EL PROCESO PARA OCULTA EL MSJ
        """

        msj_portador = self.caja_portador.get("1.0","end-1c").strip()
    
        if not msj_portador:
            self.caja_portador.configure(border_color = "#8a2121")
            return
        
        if len(msj_portador) >= 30000:

            # Si supera los 30.000 caracteres, usamos el mensaje completo
            # almacenado en memoria, que debería existir porque probablemente
            # fue pegado en lugar de escrito manualmente.

            msj_portador = self.msj
        
        self.cifrar_msj(msj_portador)
    
    #CIFRA EL MSJ     
    def cifrar_msj(self,msj):
        """
        CIFRA EL CONTENIDO DEL MSJ
        """
        #RESTABLECEMOS EL BORDE DE LAS CAJAS CASO QUE ESTEN EN ROJO
        self.caja_portador.configure(border_color="#2b3542")

        esteganografia =Esteganografia()
        
        msj_cifrado = esteganografia._cifrar_texto(msj)
        llave_desencriptar = esteganografia.clave_recuperacion
        
        if msj_cifrado and llave_desencriptar:
            self.contenedor_resultado_texto(msj_cifrado,llave_desencriptar,esteganografia)
        
        else:
            self.contenedor_error_cifrado_descifrado()
            return
        self.msj = None #BORRAMOS EL MSJ DE LA MEMORIA REINICIAMOS VARIABLE


    def contenedor_resultado_texto (self,msj_cifrado = None, llave_desencriptar= None, estegano = None):
        
        if hasattr(self,"contenedor_msj_resultado") and self.contenedor_msj_resultado.winfo_exists():
            self.contenedor_msj_resultado.destroy()
            
        self.contenedor_msj_resultado = ctk.CTkFrame(self.contenedor_cifrar_resultados,fg_color="#132033",border_color="#2b3542", border_width=1,corner_radius=10)
        self.contenedor_msj_resultado.grid(row=0, column=1, sticky="wesn")
        self.contenedor_msj_resultado.grid_rowconfigure(2, weight=1)
        self.contenedor_msj_resultado.grid_columnconfigure(0, weight=1)
        
        label_titulo = ctk.CTkLabel(self.contenedor_msj_resultado, text="Resultado", font=("segoe ui", 13, "bold" ), text_color="#f3f3f3",anchor="w")
        label_titulo.grid(row=0, column=0, padx= 10, pady=(10,0), sticky="w")
        
        label_descripcion = ctk.CTkLabel(self.contenedor_msj_resultado, text="El mensaje resultante aparecera aqui despues de cifrar la informacion.", font=("segoe ui", 13, ), text_color="#8b93a1",wraplength=600,justify="left")
        label_descripcion.grid(row=1, column=0, padx= 10, sticky="w")
        
        if not msj_cifrado and not llave_desencriptar: #si no hay ningun msj ni llave mostramos la vista previa       
        #CONTENEDOR DE VISTA PREVIA
            frame_vista_previa = ctk.CTkFrame(self.contenedor_msj_resultado,fg_color="#132033",border_color="#2b3542", border_width=1,corner_radius=10)
            frame_vista_previa.grid(row=2, column=0, padx=20, pady=(15,15), sticky="wesn")
            frame_vista_previa.grid_columnconfigure(0, weight=1)
            frame_vista_previa.grid_rowconfigure(0, weight=1)
            frame_vista_previa.grid_rowconfigure(4, weight=1)
            
            imagen_previa = ctk.CTkImage(light_image=Image.open(vista_previa_texto), size=(215,165))
            label_vista_previa = ctk.CTkLabel(frame_vista_previa, image=imagen_previa, text="")
            label_vista_previa.grid(row=1, column=0, padx=80, pady=(40,30), sticky="wesn")
            
            label1 = ctk.CTkLabel(frame_vista_previa, text="Aun no hay resultados", font=("segoe ui", 18), text_color="#f3f3f3",)
            label1.grid(row=2, column=0, padx=5, pady=(0,15), sticky="we")
            
            label2 = ctk.CTkLabel(frame_vista_previa, text="Introduce el texto portador y el mensaje que deseas ocultar. Luego pulsa «Ocultar mensaje» para generar el resultado.", font=("segoe ui", 13), text_color="#8b93a1", wraplength=380)
            label2.grid(row=3, column=0, padx=5, pady=(0,20), sticky="we")
                    
        else:
            caja_msj_oculto = ctk.CTkTextbox(self.contenedor_msj_resultado,font=("segoe ui", 13), text_color="#f3f3f3",fg_color="#2b3542",border_color="#2b3542",border_width=1,height=310)
            caja_msj_oculto.grid(row=2, column=0, padx=15, pady=5, sticky="wens")
            msj_cifrado = msj_cifrado.decode("utf-8")
            
            caja_msj_oculto.insert("1.0",msj_cifrado[:30000])
            caja_msj_oculto.tag_config("vista_previa",foreground="#fcf82f")
            if len(msj_cifrado) > 30000:
                texto_vista_previa = "\n\n[Se muestran los primeros 30.000 caracteres. El mensaje cifrado completo está disponible para copiar.]"
                caja_msj_oculto.insert("end",texto_vista_previa,"vista_previa") 
            
            
            caja_msj_oculto.configure(state="disabled")
            
            boton_copiar_msj = ctk.CTkButton(self.contenedor_msj_resultado, text="Copiar mensaje cifrado", font=("segoe ui", 13), text_color="#f3f3f3",fg_color="#101B2C",border_color="#2b3542",border_width=1,cursor = "hand2", height=45,command=lambda:self.copiar(msj_cifrado))
            boton_copiar_msj.grid(row=3, column=0, padx=15, pady=2, sticky="we")
        
        label_clave = ctk.CTkLabel(self.contenedor_msj_resultado, text="Clave de recuperacion ", font=("segoe ui", 13, "bold"), text_color="#f3f3f3")
        label_clave.grid(row=4, column=0, padx=10, sticky="w")
        
        label_clave_descrip = ctk.CTkLabel(self.contenedor_msj_resultado, text="Guarda esta clave en un lugar seguro. La necesitaras para desencriptar el msj", font=("segoe ui", 13), text_color="#8b93a1",justify="left")
        label_clave_descrip.grid(row=5,column=0, padx=10, sticky="w")

        self.entry_clave_texto = ctk.CTkEntry(self.contenedor_msj_resultado,font=("segoe ui", 13), text_color="#f3f3f3",fg_color="#2b3542",border_color="#2b3542",border_width=1,state="disabled")
        self.entry_clave_texto.grid(row=6, column=0, padx=15, pady=5, sticky="we")
        
        contenedor_botones = ctk.CTkFrame(self.contenedor_msj_resultado,fg_color="transparent")
        contenedor_botones.grid(row=7, column=0, columnspan=1, padx=5, pady=5, sticky="wesn")
        contenedor_botones.grid_columnconfigure(0, weight=1)
        contenedor_botones.grid_columnconfigure(1, weight=1)

        logo_copiar = ctk.CTkImage(light_image=Image.open(copiar), size=(16,16))
        boton_copiar = ctk.CTkButton(contenedor_botones, image=logo_copiar, compound="left", border_spacing=15,text="  Copiar", font=("segoe ui", 14), text_color="#f3f3f3",fg_color="#101B2C", hover_color="#2b3542", border_width=1, border_color="#2b3542",height=40,state="disabled",command=lambda:self.copiar(llave_desencriptar))
        boton_copiar.grid(row=0, column=0, padx=15, pady=5, sticky="we")
        
        logo_exportar = ctk.CTkImage(light_image=Image.open(exportar), size=(16,15))
        boton_guardar =ctk.CTkButton(contenedor_botones, image=logo_exportar, compound="left", border_spacing=15,text="  Exportar clave .vlkey", font=("segoe ui", 14), text_color="#f3f3f3",fg_color="#101B2C", hover_color="#2b3542", border_width=1,border_color="#2b3542", height=40,state="disabled",command=lambda:self.exportar_clave(llave_desencriptar,esteganografia=estegano))
        boton_guardar.grid(row=0, column=1, padx=(0,5), pady=5, sticky="we")

        if msj_cifrado and llave_desencriptar:
            self.entry_clave_texto.configure(state="normal")
            self.entry_clave_texto.insert(0,llave_desencriptar)
            self.entry_clave_texto.configure(state="readonly")
            boton_copiar.configure(state="normal",cursor="hand2")
            boton_guardar.configure(state="normal",cursor="hand2")

    def pegar_msj_caja_cifrar_desifrar (self, event):
        """
        PEGA EL MSJ DEL PORTAPAPELES EN LA CAJA DE TEXTO PARA EVITAR QUE COLAPSE SI SON MAS DE 30.000 CARACTERES
        """


        event.widget.delete("1.0", "end")
        
        event.widget.tag_config("vista_previa",foreground="#fcf82f")
        
        try:
        
            self.msj = self.clipboard_get()
            event.widget.insert("1.0",self.msj[:30000])

        except Exception as e:
            logger.error(f"Error al obtener el msj de la portapapeles: {e}")

        if len(self.msj) > 30000:

            texto_vista_previa = "\n\n[Vista previa limitada a 30.000 caracteres. El contenido completo se ha cargado correctamente.]"
            event.widget.insert("end",texto_vista_previa,"vista_previa") 
        
        return "break"
        

    ########################################## DESCIFRAR MENSAJE #########################################################

    def contenedor_op_descifrar_msj (self):

        """
        CONTENEDOR TOTAL DE LA SECCION DESCIFRAR (CONTENEDORES OPCIONES DE SELECCION Y RESULTADO)
        ES EL CONTENEDOR QUE SE DESTRUYE AL CAMBIAR DE OPCION A CIFRAR MENSAJE
        """

        if hasattr(self,"contenedor_cifrar_resultados") and self.contenedor_cifrar_resultados.winfo_exists():
            self.contenedor_cifrar_resultados.destroy()
        
        if hasattr(self,"contenedor_descifrar_resultados") and self.contenedor_descifrar_resultados.winfo_exists():
            return
        
        self.boton_descifrar_msj.configure(border_color="#353e90", fg_color="#1e245a", hover_color="#1e245a")
        self.boton_cifrar_msj.configure(border_color="#2b3542", fg_color="#132033", hover_color="#132033")
        
        #CONTENEDOR DE TODOS LOS CONTENEDORES DE DESCIFRAR. ES EL CONTENEDOR QUE SE ELIMINA AL CAMBIAR DE SECCION
        self.contenedor_descifrar_resultados = ctk.CTkFrame(self.contenedor_cifrar_msj,fg_color="transparent")
        self.contenedor_descifrar_resultados.grid(row=3, column=0, columnspan=2, pady=5, sticky="nsew")
        self.contenedor_descifrar_resultados.grid_rowconfigure(0, weight=1)
        self.contenedor_descifrar_resultados.grid_columnconfigure(1, weight=1)

        #CONTENEDOR DE MSJ A DECIFRAR
        self.contenedor_msj_cifrado = ctk.CTkFrame(self.contenedor_descifrar_resultados,fg_color="#132033",border_color="#2b3542", border_width=1,corner_radius=10)
        self.contenedor_msj_cifrado.grid(row=0, column=0, padx=(2,5), sticky="nsew")
        self.contenedor_msj_cifrado.grid_rowconfigure(2, weight=1)

        label_msj_cifrado = ctk.CTkLabel(self.contenedor_msj_cifrado, text="Mensaje cifrado:", font=("segoe ui", 13,"bold" ), text_color="#f3f3f3")
        label_msj_cifrado.grid(row=0, column=0, padx=10, pady=(10,0), sticky="w")
        
        label_descrip_msj_cifrado = ctk.CTkLabel(self.contenedor_msj_cifrado, text="Pega (Ctrl + V) el mensaje que deseas descifrar.", font=("segoe ui", 13, ), text_color="#8b93a1",wraplength=600,justify="left")
        label_descrip_msj_cifrado.grid(row=1, column=0, padx=10, pady=(0,2), sticky="w")
        
        #CAJA DE TEXTO
        self.caja_msj_cifrado = ctk.CTkTextbox(self.contenedor_msj_cifrado, width=600, fg_color="#132033",text_color="#8b93a1",border_color="#2b3542",border_width=1,corner_radius=8,font=("segoe ui", 13),wrap="word",undo=True,autoseparators=True,maxundo=-1)
        self.caja_msj_cifrado.grid(row=2, column=0, padx=10, pady=(0,10), sticky="nsew")
        self.caja_msj_cifrado.bind("<Control-v>", self.pegar_msj_caja_cifrar_desifrar)

        label_clave_desifrar = ctk.CTkLabel(self.contenedor_msj_cifrado, text="Clave de cifrado", font=("segoe ui", 13,"bold" ), text_color="#f3f3f3")
        label_clave_desifrar.grid(row=3, column=0, padx=10, pady=(10,0), sticky="w")
        
        label_clave_descrip = ctk.CTkLabel (self.contenedor_msj_cifrado, text="Introduce la clave de cifrado o carga un archivo. vlkey.", font=("segoe ui", 13, ), text_color="#8b93a1",wraplength=600,justify="left")
        label_clave_descrip.grid(row=4, column=0, padx=10, pady=(0,2), sticky="w")

        #CONTENEDOR DE BOTONES
        contenedor_botones_llave = ctk.CTkFrame(self.contenedor_msj_cifrado,fg_color="transparent")
        contenedor_botones_llave.grid(row=5, column=0, padx=10, pady=(0,10), sticky="nsew")

        logo_llave = ctk.CTkImage(light_image=Image.open(key_recovery),size=(20,20))
        self.boton_clave = ctk.CTkButton(contenedor_botones_llave, image=logo_llave, compound="left", text="Introducir clave", font=("segoe ui", 14, ),fg_color= "#1e245a",hover_color="#1e245a",text_color="white",width=280,height=40,cursor="hand2",border_width=2,corner_radius=8, border_color="#353e90",command= self.boton_introducir_clave)
        self.boton_clave.grid(row=0, column=0, padx=(0,5), pady=5, sticky="nsew")

        logo_archivo = ctk.CTkImage(light_image=Image.open(archivo_nombre),size=(17,20))
        self.boton_vlkey = ctk.CTkButton(contenedor_botones_llave, image=logo_archivo, compound="left", text="Cargar .vlkey", font=("segoe ui", 14, ),fg_color= "#132033",hover_color="#132033",text_color="white",width=300,height=45,cursor="hand2",border_width=2,corner_radius=8, border_color="#2b3542",command=lambda:self.boton_seleccionar_archivo_clave(self.entry_clave_vlkey))
        self.boton_vlkey.grid(row=0, column=1,  pady=5, sticky="nsew")

        self.entry_clave_vlkey = ctk.CTkEntry(self.contenedor_msj_cifrado,fg_color="#132033",text_color="#8b93a1",border_color="#2b3542",border_width=1,corner_radius=8,font=("segoe ui", 13),height=30)
        self.entry_clave_vlkey.grid(row=6, column=0, padx=10, pady=(0,10), sticky="nsew")
        self.entry_clave_vlkey.bind("<Button-3>", self.menu_contextual_llave)

        logo_desocultar = ctk.CTkImage(light_image=Image.open(desocultar), size=(22,26))
        self.boton_descifrar = ctk.CTkButton(self.contenedor_msj_cifrado, image=logo_desocultar, compound="left", text="Descifrar mensaje", font=("segoe ui", 16,"bold"),fg_color="#525ace",text_color="#f3f3f3",border_color="#6770f9",hover_color="#5d66ee",border_width=2,corner_radius=8, height=50,cursor="hand2",command=self.iniciar_desencriptar)
        self.boton_descifrar.grid(row=7, column=0, padx=10, pady=(5,10), sticky="we")

        self.cont_resultado_msj_descifrado()

    def cont_resultado_msj_descifrado (self,msj_descifrado = None):

        self.destruir_contenedor_cifrado_descifrado_result()

        self.contenedor_resultado_descifrado = ctk.CTkFrame(self.contenedor_descifrar_resultados,fg_color="#132033",border_color="#2b3542", border_width=1,corner_radius=10)
        self.contenedor_resultado_descifrado.grid(row=0, column=1, sticky="wesn")
        self.contenedor_resultado_descifrado.grid_rowconfigure(2, weight=1)
        self.contenedor_resultado_descifrado.grid_columnconfigure(0, weight=1)
        
        label_titulo = ctk.CTkLabel(self.contenedor_resultado_descifrado, text="Mensaje descifrado", font=("segoe ui", 13, "bold" ), text_color="#f3f3f3",anchor="w")
        label_titulo.grid(row=0, column=0, padx= 10, pady=(10,0), sticky="w")

        label_descripcion = ctk.CTkLabel(self.contenedor_resultado_descifrado, text="El mensaje original aparecera aqui despues de decifrarlo.", font=("segoe ui", 13, ), text_color="#8b93a1",wraplength=600,justify="left")
        label_descripcion.grid(row=1, column=0, padx= 10, sticky="w")

        if not msj_descifrado: #si no hay ningun msj mostramos el aviso de vista previa

        #CONTENEDOR DE VISTA PREVIA
            frame_vista_previa = ctk.CTkFrame(self.contenedor_resultado_descifrado,fg_color="#132033",border_color="#2b3542", border_width=1,corner_radius=10)
            frame_vista_previa.grid(row=2, column=0, padx=20, pady=(15,15), sticky="wesn")
            frame_vista_previa.grid_columnconfigure(0, weight=1)
            frame_vista_previa.grid_rowconfigure(0, weight=1)
            frame_vista_previa.grid_rowconfigure(4, weight=1)

            imagen_previa = ctk.CTkImage(light_image=Image.open(vista_previa_texto), size=(215,165))
            label_vista_previa = ctk.CTkLabel(frame_vista_previa, image=imagen_previa, text="")
            label_vista_previa.grid(row=1, column=0, padx=80, pady=(40,30), sticky="wesn")

            label1 = ctk.CTkLabel(frame_vista_previa, text="Aun no hay resultados", font=("segoe ui", 18), text_color="#f3f3f3",)
            label1.grid(row=2, column=0, padx=5, pady=(0,15), sticky="we")

            label2 = ctk.CTkLabel(frame_vista_previa, text="Introduce el mensaje cifrado y su clave, luego pulsa 'Descifrar mensaje' par ver el contenido", font=("segoe ui", 13), text_color="#8b93a1", wraplength=380)
            label2.grid(row=3, column=0, padx=5, pady=(0,20), sticky="we")

        else:
            caja_msj_descifrado = ctk.CTkTextbox(self.contenedor_resultado_descifrado,font=("segoe ui", 13), text_color="#f3f3f3",fg_color="#2b3542",border_color="#2b3542",border_width=1,height=310)
            caja_msj_descifrado.grid(row=2, column=0, padx=15, pady=5, sticky="wens")
            msj_descifrado = msj_descifrado

            caja_msj_descifrado.insert("1.0",msj_descifrado[:30000])
            caja_msj_descifrado.tag_config("vista_previa",foreground="#fcf82f")
            if len(msj_descifrado) > 30000:
                texto_vista_previa = "\n\n[Se muestran los primeros 30.000 caracteres. El mensaje descifrado completo está disponible para copiar.]"
                caja_msj_descifrado.insert("end",texto_vista_previa,"vista_previa") 

            caja_msj_descifrado.configure(state="disabled")

            boton_copiar_msj = ctk.CTkButton(self.contenedor_resultado_descifrado, text="Copiar mensaje descifrado", font=("segoe ui", 13), text_color="#f3f3f3",fg_color="#101B2C",border_color="#2b3542",border_width=1,cursor = "hand2", height=45,command=lambda:self.copiar(msj_descifrado))
            boton_copiar_msj.grid(row=3, column=0, padx=15, pady=10, sticky="we")


    #CAMBIA EL COLOR DE LA SELECCION DE LA CLAVE
    def boton_introducir_clave (self):
        """
        CAMBIA EL COLOR DEL BOTON CLAVE Y DEL BOTON VLKEY
        """

        self.boton_clave.configure(fg_color= "#1e245a",hover_color="#1e245a",border_color="#353e90")
        self.boton_vlkey.configure(fg_color= "#132033",hover_color="#132033",border_color="#2b3542")
        self.entry_clave_vlkey.configure(state="normal")
        self.entry_clave_vlkey.delete(0, "end")

    def iniciar_desencriptar(self):

        """
        INICIA EL PROCESO DE DESCIFRADO
        """
        
        self.caja_msj_cifrado.configure(border_color="#2b3542")
        self.entry_clave_vlkey.configure(border_color="#2b3542")
        #obtenemos los datos para verificar que los campos no esten vacios
        msj_cifrado = self.caja_msj_cifrado.get("1.0", "end-1c")
        clave_vlkey = self.entry_clave_vlkey.get().strip()

        if not msj_cifrado:
            self.caja_msj_cifrado.configure(border_color="#8a2121")
            return

        if not clave_vlkey:
            self.entry_clave_vlkey.configure(border_color="#8a2121")
            return

        if len(msj_cifrado) >= 30000:
            # Si supera los 30.000 caracteres, usamos el mensaje completo
            # almacenado en memoria, que debería existir porque probablemente
            # fue pegado en lugar de escrito manualmente.            
            msj_cifrado = self.msj
        
        
        esteganografia = Esteganografia()
        msj_descifrado =esteganografia._desencriptar_texto(msj_cifrado,clave_vlkey) #enviamos el msj completo en memoria y la clave
        
        self.msj = None #limpiamos la variable
        
        if not msj_descifrado:
            self.contenedor_error_cifrado_descifrado()
            return

        self.cont_resultado_msj_descifrado(msj_descifrado)

    #CONTENEDOR DE ERROR EN RESULTADOS
    def contenedor_error_cifrado_descifrado (self):
        """
        CONTENEDOR DE RESULTADOS DE ERRORES 
        RECIBE UN CONTENEDOR DONDE SERA COLOCADA (EN OCULTAR O EXTRAER)
        RECIBE UN BOTON (OCULTAR O DESOCULTAR) PARA ACTIVARLO
        """
        
        self.destruir_contenedor_cifrado_descifrado_result()

        self.contenedor_de_error_texto = ctk.CTkFrame(self.contenedor_resultado_descifrado,fg_color="#132033",border_color="#2b3542", border_width=1,corner_radius=10)
        self.contenedor_de_error_texto.grid(row=0, column=0, sticky="wesn")
        self.contenedor_de_error_texto.grid_columnconfigure(0, weight=1)
        
        label_titulo = ctk.CTkLabel(self.contenedor_de_error_texto, text="Estado de la operacion", font=("segoe ui", 13, "bold" ), text_color="#f3f3f3",anchor="w")
        label_titulo.grid(row=0, column=0, padx= 10, pady=(10,40), sticky="w")
        
        logo_alerta = ctk.CTkImage(light_image=Image.open(alerta), size=(175,165))
        label_alerta = ctk.CTkLabel(self.contenedor_de_error_texto, image=logo_alerta, text="")
        label_alerta.grid(row=1, column=0, padx=80, pady=(40,10), sticky="wesn")
        
        
        label1 = ctk.CTkLabel(self.contenedor_de_error_texto, text="No se pudo completar la operación", font=("segoe ui", 18, "bold"), text_color="#d14641",)
        label1.grid(row=2, column=0, padx=5, pady=(0,10), sticky="we")
        
        label2 = ctk.CTkLabel(self.contenedor_de_error_texto, text="La operación no pudo completarse. Verifica los datos introducidos e inténtalo nuevamente", font=("segoe ui", 13), text_color="#8b93a1", wraplength=380)
        label2.grid(row=3, column=0, padx=5, pady=(0,10), sticky="we")
        
        #CONTENEDOR DE FRAME CAUSAS (PARA CENTRARLO MEDIANTE COLUMNAS)
        contenedor_causa = ctk.CTkFrame(self.contenedor_de_error_texto, fg_color= "transparent")
        contenedor_causa.grid(row=4, column=0, padx=5, pady=20, sticky="wsne")
        contenedor_causa.grid_columnconfigure(0, weight=1)
        contenedor_causa.grid_columnconfigure(1, weight=0)
        contenedor_causa.grid_columnconfigure(2, weight=1)

        frame_causas = ctk.CTkFrame(contenedor_causa,fg_color="transparent",border_color="#d14641", border_width=1,corner_radius=10)
        frame_causas.grid(row=0, column=1, padx=5, pady=20, sticky="wsne")
        frame_causas.grid_columnconfigure(0, weight=1)

        label_causas = ctk.CTkLabel(frame_causas, text="Posibles causas: ", font=("segoe ui", 13, "bold"), text_color="#d14641",anchor="w")
        label_causas.grid(row=0, column=0, padx= 10, pady=5, sticky="we")

        label_causa1 = ctk.CTkLabel(frame_causas, text="• Error interno al procesar la operación.", font=("segoe ui", 13), text_color="#8b93a1",anchor="w")
        label_causa1.grid(row=1, column=0, padx= 10, sticky="we")

        label_causa2 = ctk.CTkLabel(frame_causas, text="• El mensaje cifrado fue modificado o está incompleto.", font=("segoe ui", 13), text_color="#8b93a1",anchor="w",wraplength=380, justify="left")
        label_causa2.grid(row=2, column=0, padx= 10, pady=5,  sticky="we")

        label_causa3 = ctk.CTkLabel(frame_causas, text="• La clave proporcionada no es correcta.", font=("segoe ui", 13), text_color="#8b93a1",anchor="w",wraplength=360, justify="left")
        label_causa3.grid(row=3, column=0, padx= 10, pady=5, sticky="we")

    #DESTRUYE EL CONTENEDOR DE RESULTADOS
    def destruir_contenedor_cifrado_descifrado_result (self):
        """
        DESTRUYE EL CONTENEDOR DE RESULTADOS DE CIFRADO Y DESCIFRADO
        """
        
        #CONTENEDOR DE RESULTADO EN DESCIFRADO
        if hasattr(self, "contenedor_resultado_descifrado") and self.contenedor_resultado_descifrado.winfo_exists():
            self.contenedor_resultado_descifrado.destroy()
        
        #CONTENEDOR DE RESULTADO EN CIFRADO
        if hasattr(self, "contenedor_msj_resultado") and self.contenedor_msj_resultado.winfo_exists():
            self.contenedor_msj_resultado.destroy()

        #CONTENEDOR DE RESULTADO DE ERROR
        if hasattr(self, "contenedor_resultado_descifrado") and self.contenedor_resultado_descifrado.winfo_exists():
            self.contenedor_resultado_descifrado.destroy()
            
            
    ######################################### INTERFAZ DE HISTORIAL ##############################
    def _interfaz_historial (self,widget):

        """
        CONTENEDOR TOTAL DE HISTORIAL
        """
        self.activar_desact_seleccion(widget)
        
        if hasattr(self, "contenedor_ocultar") and self.contenedor_ocultar.winfo_exists():
            self.contenedor_ocultar.destroy()
        
        if hasattr(self, "contenedor_extraer") and self.contenedor_extraer.winfo_exists():
            self.contenedor_extraer.destroy()

        if hasattr(self,"contenedor_cifrar_msj") and self.contenedor_cifrar_msj.winfo_exists():
            self.contenedor_cifrar_msj.destroy()
            
        if hasattr(self,"contenedor_historial") and self.contenedor_historial.winfo_exists():
            return
        
        ##CONTENEDOR DE TODOS LOS CONTENEDORES DE HISTORIAL. ES EL CONTENEDOR QUE SE ELIMINA AL CAMBIAR DE SECCION
        self.contenedor_historial = ctk.CTkFrame(self.contenedor_central,fg_color="transparent")
        self.contenedor_historial.grid(row=0, column=0, padx=10, pady=5, sticky="nsew")
        self.contenedor_historial.grid_rowconfigure(2, weight=1)
        self.contenedor_historial.grid_columnconfigure(0, weight=1)
        
        label_titulo = ctk.CTkLabel(self.contenedor_historial, text="Historial", font=("segoe ui", 28, ), text_color="white")
        label_titulo.grid(row=0, column=0, padx=10, pady=(2,0), sticky="w")

        label_detalles = ctk.CTkLabel(self.contenedor_historial, text="Listado de todas las operaciones de protección mediante cifrado y esteganografía", font=("segoe ui", 13, ), text_color="#8b93a1",wraplength=600,justify="left")
        label_detalles.grid(row=1, column=0, padx=10, pady=2, sticky="w")
        
        logo_eliminar = ctk.CTkImage(light_image=Image.open(papelera), size=(16,15))
        
        boton_eliminar = ctk.CTkButton(self.contenedor_historial, image=logo_eliminar, compound="left",text="Eliminar seleccionado",fg_color="#132033",hover_color="#19204a", border_width=1, text_color="#f3f3f3", border_color="#2b3542",width=120,height=35,font=("segoe ui", 13), corner_radius=8, cursor="hand2",command=lambda:self._interfaz_eliminar("seleccionados"))
        boton_eliminar.grid(row=1, column=1, padx=10, pady=2, sticky="e")
        
        boton_eliminar_todo = ctk.CTkButton(self.contenedor_historial,  image=logo_eliminar,compound="left",text="Eliminar todos los registros",fg_color="#132033",hover_color="#19204a", border_width=1, text_color="#f3f3f3", border_color="#2b3542",width=120,height=35,font=("segoe ui", 13), corner_radius=8, cursor="hand2",command=lambda:self._interfaz_eliminar("todos"))
        boton_eliminar_todo.grid(row=1, column=2, padx=(5,45), pady=2, sticky="e")

        #contenedor de la tabla de registro
        self.contenedor_tabla= ctk.CTkFrame(self.contenedor_historial,fg_color="transparent")
        self.contenedor_tabla.grid(row=2, column=0,columnspan=3, padx=2, pady=(10,5), sticky="snew")
        self.contenedor_tabla.grid_rowconfigure(0, weight=1)
        self.contenedor_tabla.grid_columnconfigure(0, weight=1)
        
        self.tabla_historial()

    #CREA LA TABLA DE HISTORIAL
    def tabla_historial (self):
        """
        CREA LA TABLA DE HISTORIAL
        """
        
        db_historial = HistorialDB()
        historial =db_historial.leer_historial_db()
        columnas = historial[0]
        datos = historial[1]
        
        estilo = TableStyle(surface_bg="#132033",row_bg="#2b3542",row_alt_bg="#34404F",corner_radius=10, border_width=2,cell_padding_x=5)
        
        self.tabla = CTkDataTable(self.contenedor_tabla, columns=columnas,column_width_mode="fill",resizable_columns=True,data=datos,style=estilo, multi_select=True, empty_message="No hay registros")
        self.tabla.grid(row=0, column=0, padx=5, pady=2, sticky="nsew")

    #INTERFAZ DEL MSJ DE ELIMINAR VENTANA EMERGENTE
    def _interfaz_eliminar (self, registros):
        """
        INTERFAZ DEL MSJ DE ELIMINAR VENTANA EMERGENTE
        """
        
        if registros == "seleccionados":
            msj = "Estas seguro que deseas eliminar los registros seleccionados?"
            msj_boton = "Eliminar"
            ancho = 494
        elif registros == "todos":
            msj = "Estas seguro que deseas eliminar TODOS los registros seleccionados?"
            msj_boton = "Eliminar todo"
            ancho = 540

        self.ventana_eliminar = ctk.CTkToplevel(self)
        self.ventana_eliminar.withdraw() #oculta la ventana 
        alto = 136
        self.ventana_eliminar.resizable(False, False)

        x = app.winfo_rootx() + (app.winfo_width() // 2) - (ancho // 2)
        y = app.winfo_rooty() + (app.winfo_height() // 2) - (alto // 2)

        color_transparente = self.ventana_eliminar._apply_appearance_mode(self.ventana_eliminar._fg_color)
        self.ventana_eliminar.attributes("-transparentcolor", color_transparente) #color transparente para la ventana

        self.ventana_eliminar.after(100,lambda: self.ventana_eliminar.overrideredirect(True)) #elimina la barra de titulo

        self.ventana_eliminar.geometry(f"{ancho}x{alto}+{x}+{y}")
        self.ventana_eliminar.lift()
        self.ventana_eliminar.grab_set()
        self.ventana_eliminar.focus_set()
        self.ventana_eliminar.bind("<Escape>", lambda event: self.ventana_eliminar.destroy())

        self.ventana_eliminar.after(120,lambda: self.ventana_eliminar.deiconify())

        #contenedor
        frame_contenedor = ctk.CTkFrame(self.ventana_eliminar,fg_color="#132033",border_color="#18406D", border_width=2,corner_radius=8)
        frame_contenedor.grid(row=0, column=0, sticky="wesn")
        #imagen papelera
        frame_papelera = ctk.CTkFrame(frame_contenedor,fg_color="#34404F",border_color="#1f2733", border_width=1,corner_radius=10)
        frame_papelera.grid(row=0, column=0, padx=(20,8), pady=20, sticky="wesn")

        logo_papelera = ctk.CTkImage(light_image=Image.open(papelera), size=(20,20))
        label_imagen = ctk.CTkLabel(frame_papelera, image=logo_papelera, text="", font=("segoe ui", 18, "bold"), text_color="#f3f3f3")
        label_imagen.grid(row=0, column=0, padx=15, pady=12, sticky="w")

        #texto
        frame_texto = ctk.CTkFrame(frame_contenedor,fg_color="transparent")
        frame_texto.grid(row=0, column=1, pady=(20,10), sticky="wesn")

        titulo = ctk.CTkLabel(frame_texto, text="Eliminar registros", font=("segoe ui", 18, "bold"), text_color="#f3f3f3")
        titulo.grid(row=0, column=0, sticky="w")

        label_texto = ctk.CTkLabel(frame_texto, text=msj, font=("segoe ui", 13), text_color="#f3f3f3")
        label_texto.grid(row=1, column=0, sticky="w")

        #botones
        logo_cerrrar = ctk.CTkImage(light_image=Image.open(cerrar), size=(15,15))
        boton_cerrar = ctk.CTkButton(frame_contenedor, image=logo_cerrrar, text="", fg_color="#132033", hover_color="#8a2121",cursor="hand2",width=15, height=15,command=lambda:self.ventana_eliminar.destroy())
        boton_cerrar.grid(row=0, column=2, padx=10, pady=10, sticky="n")

        boton_eliminar = ctk.CTkButton(frame_contenedor, text=msj_boton, fg_color="#8a2121", font=("segoe ui", 13, "bold"),hover_color="#9b2c2c",border_width=1, text_color="#f3f3f3", border_color="#2b3542",width=120,height=35, corner_radius=8, cursor="hand2",command=lambda: self.eliminar_registro(msj_boton))
        boton_eliminar.grid(row=1, column=1, columnspan=2, padx=10, pady=(0,10), sticky="e")

    #ELIMINAR REGISTROS
    def eliminar_registro (self,cantidad):
        """ELIMINA LOS REGISTROS DE LA TABLA Y BASE DE DATOS
        
        """
        
        self.ventana_eliminar.destroy()
        
        id_filas = []
        db_historial = HistorialDB()
        
        if cantidad == "Eliminar todo":
            filas_eliminadas = db_historial.eliminar_filas_db()
            if filas_eliminadas:
                self.tabla.set_data([])
            return


        filas = self.tabla.get_selected_rows()

        
        if not filas:
            return

        for fila in filas: #hacemos una lista de tuplas que sqlite pueda recibir para eliminar en cantidad
            id_fila = (fila["id"],)
            id_filas.append(id_fila)
        
        filas_eliminadas = db_historial.eliminar_filas_db(id_filas)
        
        if filas_eliminadas: 
            
            for fila_num in id_filas:
                fila=fila_num[0]
                self.tabla.delete_row_by_key("id",fila) #eliminamos las filas de la interfaz


    def _interfaz_acerca_de (self,widget):

        self.activar_desact_seleccion(widget)

        if hasattr(self, "contenedor_ocultar") and self.contenedor_ocultar.winfo_exists():
            self.contenedor_ocultar.destroy()

        if hasattr(self, "contenedor_extraer") and self.contenedor_extraer.winfo_exists():
            self.contenedor_extraer.destroy()

        if hasattr(self,"contenedor_cifrar_msj") and self.contenedor_cifrar_msj.winfo_exists():
            self.contenedor_cifrar_msj.destroy()
        
        if hasattr(self,"contenedor_historial") and self.contenedor_historial.winfo_exists():
            self.contenedor_historial.destroy()
            
        if hasattr(self,"contenedor_acerca_de") and self.contenedor_acerca_de.winfo_exists():
            return
        
        #CONTENEDOR BASE DE LA SECCION ES EL QUE SE DESTRUYE AL CAMBIAR LA SECCION
        self.contenedor_acerca_de = ctk.CTkFrame(self.contenedor_central,fg_color="transparent")
        self.contenedor_acerca_de.grid(row=0, column=0, padx=10, pady=5, sticky="nsew")
        self.contenedor_acerca_de.grid_columnconfigure(0, weight=1)
        self.contenedor_acerca_de.grid_columnconfigure(1, weight=0)
        self.contenedor_acerca_de.grid_columnconfigure(2, weight=1)
        
        # self.contenedor_acerca_de.grid_rowconfigure(2, weight=1)
        
        label_titulo = ctk.CTkLabel(self.contenedor_acerca_de, text="Acerca de VeilCrypt", font=("segoe ui", 28, ), text_color="white")
        label_titulo.grid(row=0, column=0, columnspan=3, padx=10, pady=(10,0), sticky="w")

        label_descripcion = ctk.CTkLabel(self.contenedor_acerca_de, text="Informacion sobre la aplicacion, sus funciones y el proyecto", font=("segoe ui", 13, ), text_color="#8b93a1")
        label_descripcion.grid(row=1, column=0, columnspan=3, padx=10,  sticky="w")

        #CONTENEDOR HEADER LOGO

        contenedor_logo =ctk.CTkFrame(self.contenedor_acerca_de,fg_color="#132033",border_color="#2b3542", border_width=1,corner_radius=10)
        contenedor_logo.grid(row=2, column=0, columnspan=3, padx=10, pady=10,sticky="nsew")
        contenedor_logo.grid_rowconfigure(0, weight=1)
        contenedor_logo.grid_columnconfigure(0, weight=1)
        

        logo = ctk.CTkImage(light_image=Image.open(ruta_logo_png), size=(130, 190))
        label_logo = ctk.CTkLabel(contenedor_logo, image=logo,text="")
        label_logo.grid(row=0, column=0, padx=10, pady=(10,0), sticky="nsew")

        version = ctk.CTkLabel(contenedor_logo, text="v1.0.0", font=("Bahnschrift", 13, "bold"), text_color="#8b93a1")
        version.grid(row=1, column=0, padx=5, pady=(0,10))

        #CONTENEDOR SOBRE:
        contenedor_sobre = ctk.CTkFrame(self.contenedor_acerca_de,fg_color="#132033",border_color="#2b3542", border_width=1,corner_radius=10)
        contenedor_sobre.grid(row=3, column=0, padx=(10,5), pady=5, sticky="nsew")
        contenedor_sobre.grid_columnconfigure(0, weight=1)
        contenedor_sobre.grid_columnconfigure(2, weight=1)


        logo_sobre = ctk.CTkImage(light_image=Image.open(archivo),size=(20,24))
        label_sobre = ctk.CTkLabel(contenedor_sobre, image=logo_sobre, compound="left", text="   Sobre VeiltCrypt", font=("segoe ui", 16, "bold"), text_color="#f3f3f3", anchor="w")
        label_sobre.grid(row=0, column=1, padx=20, pady=(10,0), sticky="w")
        
        label_descripcion_sobre = ctk.CTkLabel(contenedor_sobre,text="VeilCrypt es una herramienta de código abierto diseñada para proteger información mediante cifrado y esteganografía. Permite cifrar y descifrar mensajes, así como ocultar información cifrada dentro de imágenes y archivos de audio. Además, mantiene un historial de las operaciones realizadas.", font=("segoe ui", 16, ),anchor="w", text_color="#8b93a1", justify="left",wraplength=600)
        label_descripcion_sobre.grid(row=1, column=1, padx=10, pady=(10,20), sticky="we")

        #contenedor_funciones
        contenedor_funciones = ctk.CTkFrame(self.contenedor_acerca_de,fg_color="#132033",border_color="#2b3542", border_width=1,corner_radius=10)
        contenedor_funciones.grid(row=3, column=2, padx=(5,10), pady=5, sticky="nsew")
        
        logo_funciones = ctk.CTkImage(light_image=Image.open(funciones),size=(22,24))
        label_funciones = ctk.CTkLabel(contenedor_funciones, image=logo_funciones, compound="left",text="   Funciones principales", font=("segoe ui", 16, "bold"), text_color="#f3f3f3" )
        label_funciones.grid(row=0, column=0, padx=10, pady=(10,0), sticky="w")
        
        logo_imagen = ctk.CTkImage(light_image=Image.open(imagen),size=(22,22))
        label_imagen = ctk.CTkLabel(contenedor_funciones, image=logo_imagen, compound="left",text="   Ocultación de información cifrada en imágenes", font=("segoe ui", 16, "bold"), text_color="#f3f3f3" )
        label_imagen.grid(row=1, column=0, padx=10, pady=(10,0), sticky="w")

        logo_audio = ctk.CTkImage(light_image=Image.open(audio),size=(26,28))
        label_audio = ctk.CTkLabel(contenedor_funciones, image=logo_audio, compound="left",text="   Ocultación de información cifrada en archivos de audio", font=("segoe ui", 16, "bold"), text_color="#f3f3f3" )
        label_audio.grid(row=2, column=0, padx=10, pady=(10,0), sticky="w")

        logo_mensaje = ctk.CTkImage(light_image=Image.open(msj),size=(25,25))
        label_mensaje = ctk.CTkLabel(contenedor_funciones, image=logo_mensaje, compound="left",text="   Cifrado de mensajes", font=("segoe ui", 16, "bold"), text_color="#f3f3f3" )
        label_mensaje.grid(row=3, column=0, padx=10, pady=(10,0), sticky="w")

        logo_historial = ctk.CTkImage(light_image=Image.open(historial_op),size=(25,25))
        label_historial = ctk.CTkLabel(contenedor_funciones, image=logo_historial, compound="left",text="   Historial de operaciones", font=("segoe ui", 16, "bold"), text_color="#f3f3f3" )
        label_historial.grid(row=4, column=0, padx=10, pady=10, sticky="w")

        #CONTENEDOR RECURSOS
        contenedor_recursos = ctk.CTkFrame(self.contenedor_acerca_de,fg_color="#132033",border_color="#2b3542", border_width=1,corner_radius=10)
        contenedor_recursos.grid(row=4, column=0, columnspan=3, padx=(5,10), pady=(5,0), sticky="nsew")
        contenedor_recursos.grid_columnconfigure(1, weight=1)
        
        logo_recursos = ctk.CTkImage(light_image=Image.open(recursos),size=(24,24))
        label_logo = ctk.CTkLabel(contenedor_recursos, image=logo_recursos, compound="left",text="")
        label_logo.grid(row=0, column=0, rowspan=2, padx=10, pady=(10,0), sticky="w")
        
        label_recursos = ctk.CTkLabel(contenedor_recursos, text="Recursos y comunidad", font=("segoe ui", 16, "bold"), text_color="#f3f3f3", anchor="s")
        label_recursos.grid(row=0, column=1, padx=10, pady=(10,0), sticky="w")
        
        label_recursos_descrip = ctk.CTkLabel(contenedor_recursos, text="Descubre novedades, proyectos, recursos y contenido de interes", font=("segoe ui", 14), text_color="#8b93a1",anchor="n")
        label_recursos_descrip.grid(row=1, column=1, padx=10, sticky="w")

        #REDES CONTENERDOR
        frame_redes = ctk.CTkFrame(contenedor_recursos,fg_color="transparent")
        frame_redes.grid(row=2, column=0,columnspan=2, padx=10, pady=10, sticky="ew")
        frame_redes.grid_columnconfigure(0, weight=1)
        frame_redes.grid_columnconfigure(1, weight=1)
        frame_redes.grid_columnconfigure(2, weight=1)
        frame_redes.grid_columnconfigure(3, weight=1)
        frame_redes.grid_columnconfigure(4, weight=1)
        frame_redes.grid_columnconfigure(5, weight=1)
        
        logo_github = ctk.CTkImage(light_image=Image.open(github),size=(24,24))
        boton_github = ctk.CTkButton(frame_redes, image=logo_github, compound="left",text="  GitHub", font=("segoe ui", 16, "bold"), text_color="#f3f3f3",fg_color="#132033",hover_color="#132033", border_color="#2b3542", border_width=1,anchor="center",height=45, cursor="hand2",command=lambda: webbrowser.open("https://github.com/n0rs4rt"))
        boton_github.grid(row=0, column=1, padx=10, pady=10, sticky="ew") 

        logo_youtube = ctk.CTkImage(light_image=Image.open(youtube),size=(35,23))
        boton_youtube = ctk.CTkButton(frame_redes, image=logo_youtube,compound="left",text="  YouTube", font=("segoe ui", 16, "bold"), text_color="#f3f3f3",fg_color="#132033",hover_color="#132033", border_color="#2b3542", border_width=1,anchor="center", height=45,cursor="hand2",command=lambda: webbrowser.open("https://www.youtube.com/@Ors4tech"))
        boton_youtube.grid(row=0, column=2, padx=10, pady=10, sticky="ew")

        logo_instagram = ctk.CTkImage(light_image=Image.open(instagram),size=(24,24))
        boton_instagram = ctk.CTkButton(frame_redes,image=logo_instagram, compound="left",text="  Instagram", font=("segoe ui", 16, "bold"), text_color="#f3f3f3",fg_color="#132033",hover_color="#132033", border_color="#2b3542", border_width=1,anchor="center", height=45,cursor="hand2",command=lambda: webbrowser.open("https://www.instagram.com/ors4tech"))
        boton_instagram.grid(row=0, column=3, padx=10, pady=10, sticky="ew")

        logo_documentacion = ctk.CTkImage(light_image=Image.open(documentacion),size=(24,24))
        boton_documentacion = ctk.CTkButton(frame_redes, image=logo_documentacion, compound="left",text="  Documentación", font=("segoe ui", 16, "bold"), text_color="#f3f3f3",fg_color="#132033",hover_color="#132033", border_color="#2b3542", border_width=1,anchor="center", height=45,cursor="hand2",command=lambda: webbrowser.open("https://github.com/n0rs4rt/VeilCrypt/"))
        boton_documentacion.grid(row=0, column=4, padx=10, pady=10, sticky="ew")

        #Desarrollado por
        label_desarrollado = ctk.CTkLabel(self.contenedor_acerca_de, text="© 2026 ORS4Tech  |  VeilCrypt  |  Desarrollado por Nelson Arteaga · @n0rs4rt  |  MIT License", font=("segoe ui", 13, ), text_color="#8b93a1",anchor="s")
        label_desarrollado.grid(row=5, column=0, columnspan=3, padx=10, pady=(0,5), sticky="ew")
        
        
    def al_cerrar_app(self):
        self.withdraw()#OCULTAMOS LA VENTANA PARA SIMULAR EL CIERRE
        limpiar_tmp() #BORRAMOS CUALQUIER DATO GENERADO POR LA APP
        self.destroy() #CERRAMOS LA APP
        
app = Interfaz()
app.mainloop()