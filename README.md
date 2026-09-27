<p align="center">
  <img src="https://github.com/n0rs4rt/ORS_VeilCrypt/blob/4e61f42c74cbb43abcce7026c029d6c3dcd9773f/assest/portada.png" alt="VeilCrypt">
</p>

# ORS4 VeilCrypt

Es una herramienta de seguridad desarrollada en Python que combina **cifrado y esteganografía** para proteger y ocultar información dentro de archivos aparentemente convencionales.

La herramienta permite trabajar con dos tipos principales de portadores: **imágenes PNG, BMP y archivos de audio WAV**. Antes de que cualquier archivo o información sea ocultada dentro del portador, el contenido es cifrado, de modo que la extracción del contenido oculto no implica necesariamente que la información pueda ser interpretada sin disponer de la clave correspondiente.

VeilCrypt también permite **cifrar y descifrar mensajes directamente**, sin necesidad de utilizar un archivo portador.

El proyecto fue diseñado con una interfaz gráfica orientada a facilitar el uso de estas técnicas sin necesidad de trabajar directamente desde una terminal.

---
## Versiones disponibles

- **Versión principal**  
  Para uso normal de la aplicación.
  [ Descargar Ors4VeilCrypt_V1.0.0](https://github.com/n0rs4rt/ORS4VeilCrypt/releases/download/v1.0.0/Ors4_VeilCrypt_v1.0.0.zip)

- **Versión debug**  
  La versión DEBUG está destinada principalmente a desarrolladores o usuarios que deseen reportar errores.
  La consola integrada muestra información adicional que facilita el diagnóstico de incidencias. Para un uso normal, se recomienda descargar la versión principal.
  [ Descargar Ors4VeilCrypt_Debug V1.0.0](https://github.com/n0rs4rt/ORS4VeilCrypt/releases/download/v1.0.0/Ors4_VeilCrypt_v1.0.0_debug.zip)

---
## Funcionamiento

El proceso de ocultación sigue una secuencia de protección y ocultación de la información:

<p align="center">
  <img src="https://github.com/n0rs4rt/ORS_VeilCrypt/blob/b2a6387a3d5a5aa65aacb26d0070b457d49a8db6/assest/1.png" alt="VeilCrypt">
</p>

VeilCrypt procesa la información en varias etapas. El contenido seleccionado se lee en formato binario, se cifra mediante Fernet y posteriormente se incorpora al archivo portador mediante técnicas de esteganografía LSB.
El resultado es una imagen o un archivo de audio que contiene el contenido cifrado oculto.

---
## ¿Cómo se oculta la información?

La esteganografía utilizada por VeilCrypt se basa en la técnica LSB (Least Significant Bit). Este método permite almacenar información dentro de un archivo portador modificando sus bits menos significativos.

Antes de realizar esta inserción, VeilCrypt cifra la información que se desea ocultar. El resultado es un conjunto de datos cifrados que posteriormente se incorpora al archivo portador mediante la técnica LSB.

En la versión 1.0.0, VeilCrypt utiliza 2 bits menos significativos para realizar la inserción.

De forma simplificada, si un valor del archivo portador está representado por:


```
10110110
```

y los datos cifrados que deben almacenarse son:

```
01
```

los dos últimos bits del valor del portador se sustituyen por esos bits:

<p align="center">
  <img src="https://github.com/n0rs4rt/ORS_VeilCrypt/blob/b317edda78bcdac3972874a749e49307b788d7a4/assest/2.png" alt="VeilCrypt">
</p>

---

## Características principales

### Cifrado de mensajes

Permite introducir un mensaje y generar su versión cifrada directamente desde la interfaz.

El resultado incluye la información necesaria para conservar la clave de recuperación, permitiendo posteriormente realizar el proceso de descifrado.

Las claves pueden copiarse directamente o exportarse mediante archivos `.vlkey`.

> **Importante:** la clave es necesaria para recuperar información cifrada. VeilCrypt no almacena las claves utilizadas en el historial de operaciones.

<p align="center">
  <img src="https://github.com/n0rs4rt/ORS_VeilCrypt/blob/02cd3dcf34edc3cedbadd4d79caf4316dd720f20/assest/Captura%20de%20ecr%C3%A3%202026-09-08%20171814~2.jpg" alt="VeilCrypt">
</p>

---

### Ocultación de archivos en imágenes

ermite utilizar una imagen PNG o BMP como archivo portador y ocultar dentro de ella un archivo previamente cifrado.

El archivo seleccionado se cifra antes de realizar la ocultación. Posteriormente, el contenido cifrado se incorpora a los datos de la imagen mediante la técnica LSB (Least Significant Bit).


Proceso:

<p align="center">
  <img src="https://github.com/n0rs4rt/ORS_VeilCrypt/blob/8d790e7a7a0fb709e7e87c9b8f221c57e832b227/assest/3.png" alt="VeilCrypt" width="700">
</p>



La imagen resultante sera en formato PNG

<p align="center">
  <img src="https://github.com/n0rs4rt/ORS_VeilCrypt/blob/02cd3dcf34edc3cedbadd4d79caf4316dd720f20/assest/Captura%20de%20ecr%C3%A3%202026-09-08%20170448~2.jpg" alt="VeilCrypt">
</p>


---

### Ocultación de archivos en audio

VeilCrypt permite utilizar archivos **WAV** como portadores para ocultar información cifrada.

El proceso sigue el mismo principio utilizado en las imágenes: la información se cifra primero y posteriormente se incorpora al archivo de audio mediante técnicas de LSB (Least Significant Bit).

Cuando el contenido a ocultar es un archivo, este se cifra directamente. Cuando se trata de texto, VeilCrypt crea primero un archivo temporal .txt con el contenido introducido por el usuario; este archivo se cifra y posteriormente se utiliza como contenido oculto.

El resultado de la operación se guarda como un nuevo archivo WAV.

<p align="center">
  <img src="https://github.com/n0rs4rt/ORS_VeilCrypt/blob/4474f1ee2f92273c07f62b112b9e2487c90e9cb4/assest/4.png" alt="VeilCrypt" width="700">
</p>


Actualmente, esta funcionalidad presenta una **limitación conocida**: dependiendo del contenido del audio y de la cantidad de información ocultada, puede producirse una ligera alteración perceptible o un ruido de fondo después del procesamiento.

Este comportamiento se encuentra identificado como una línea de mejora para futuras versiones.

<p align="center">
  <img src="https://github.com/n0rs4rt/ORS_VeilCrypt/blob/02cd3dcf34edc3cedbadd4d79caf4316dd720f20/assest/Captura%20de%20ecr%C3%A3%202026-09-08%20171020~2.jpg" alt="VeilCrypt">
</p>

---

## Extracción de información

VeilCrypt permite recuperar información previamente ocultada dentro de una imagen o archivo de audio.

<p align="center">
  <img src="https://github.com/n0rs4rt/ORS_VeilCrypt/blob/02cd3dcf34edc3cedbadd4d79caf4316dd720f20/assest/Captura%20de%20ecr%C3%A3%202026-09-08%20171715~2.jpg" alt="VeilCrypt">
</p>

Durante el proceso de extracción, la herramienta:

1. Analiza el archivo portador.
2. Recupera el contenido oculto.
3. Valida y procesa la información extraída.
4. Utiliza la clave correspondiente para descifrar el contenido.
5. Presenta el resultado al usuario.

En función del tipo de contenido ocultado, la herramienta muestra la información recuperada o proporciona la ubicación del archivo extraído junto con sus detalles.

<p align="center">
  <img src="https://github.com/n0rs4rt/ORS_VeilCrypt/blob/02cd3dcf34edc3cedbadd4d79caf4316dd720f20/assest/Captura%20de%20ecr%C3%A3%202026-09-08%20171515~2.jpg" alt="VeilCrypt">
</p>

---

## Gestión de claves

La seguridad del contenido cifrado depende de la conservación de la clave correspondiente.

VeilCrypt permite:

- Generar claves de cifrado.
- Copiar claves directamente desde la interfaz.
- Exportar claves en formato `.vlkey`.
- Utilizar posteriormente la clave para recuperar el contenido cifrado.

Por motivos de seguridad, **las claves no se almacenan en el historial de operaciones**.

El usuario es responsable de conservar sus claves de forma segura.

---

## Capacidad de ocultación

Un archivo portador debe disponer de suficiente capacidad para almacenar el contenido cifrado.

La capacidad disponible **no depende únicamente del tamaño del archivo**. En imágenes intervienen factores como:

- Resolución.
- Número de píxeles.
- Canales de color.
- Bits utilizados para la ocultación.
- Tamaño del contenido cifrado.

Por este motivo, una imagen con un tamaño de archivo aparentemente grande no necesariamente tendrá suficiente capacidad para almacenar un determinado archivo.

La misma consideración se aplica a los archivos de audio WAV, donde la capacidad depende principalmente de características como la cantidad de muestras, canales y profundidad de bits.

Si el contenido supera la capacidad disponible del portador, la operación no podrá completarse correctamente.

<p align="center">
  <img src="https://github.com/n0rs4rt/ORS_VeilCrypt/blob/4df3f687358fdc145f9a90c435a4a100bf493212/assest/Screenshot%202026-09-13%20222948.png" alt="VeilCrypt">
</p>

---

## Rendimiento

El tiempo necesario para procesar un archivo depende principalmente de sus dimensiones y del tamaño de la información que se está procesando.

Con imágenes de resolución inferior a 4K, las operaciones normalmente se completan rápidamente.

En imágenes de resolución 4K o superior, especialmente cuando contienen una gran cantidad de datos, el procesamiento puede requerir varios segundos.

La versión actual ejecuta estas operaciones en el **hilo principal de ejecución**, por lo que durante procesos intensivos la interfaz puede dejar de responder temporalmente mientras se completa el procesamiento.

Este comportamiento no implica necesariamente que la aplicación se haya detenido; el proceso puede continuar ejecutándose hasta finalizar.

La implementación de procesamiento concurrente o multiproceso puede considerarse para futuras versiones.

---

## Historial de operaciones

VeilCrypt incorpora un sistema de historial basado en una base de datos local.

El historial permite consultar información relacionada con las operaciones realizadas mediante la herramienta, facilitando el seguimiento de los procesos de ocultación y extracción.

Por razones de seguridad, **las claves de cifrado no se almacenan en el historial**.

El historial está orientado a registrar información operativa y no secretos criptográficos.

<p align="center">
  <img src="https://github.com/n0rs4rt/ORS_VeilCrypt/blob/02cd3dcf34edc3cedbadd4d79caf4316dd720f20/assest/Screenshot%202026-09-13%20221415.png" alt="VeilCrypt">
</p>

---

## Consideraciones sobre el envío de archivos

Los archivos generados contienen información oculta directamente en los datos del archivo portador. Por este motivo, el archivo resultante debe mantenerse intacto después de su generación.

Algunas aplicaciones y plataformas, como **WhatsApp, Telegram, Instagram, Messenger y otras**, pueden comprimir, recomprimir, redimensionar o recodificar automáticamente las imágenes y archivos de audio enviados. Estas modificaciones pueden alterar los datos utilizados para ocultar la información y provocar que el contenido oculto no pueda recuperarse correctamente.

**Para evitarlo, se recomienda:**

- Al enviar una **imagen o archivo de audio**, utilizar la opción **"Enviar como archivo"** o **"Documento"**, en lugar de enviarlo directamente como imagen o audio.
- Verificar que la plataforma **no modifique ni comprima el archivo** durante el envío.
- Como alternativa, incluir el archivo dentro de un **ZIP, RAR u otro contenedor** que preserve su contenido original.

**El objetivo es que el archivo recibido mantenga exactamente los mismos datos que el archivo generado por VeilCrypt.**

El mismo principio aplica tanto a imágenes PNG o BMP como a archivos de audio WAV.

---

## Interfaz

La aplicación utiliza una interfaz gráfica desarrollada con **CustomTkinter**, diseñada para proporcionar una experiencia de uso sencilla y mantener separadas las diferentes operaciones de protección, ocultación y extracción.

<p align="center">
  <img src="https://github.com/n0rs4rt/ORS_VeilCrypt/blob/02cd3dcf34edc3cedbadd4d79caf4316dd720f20/assest/Screenshot%202026-09-13%20222016.png" alt="VeilCrypt">
</p>

*Interfaz principal de ORS4 VeilCrypt.*

---

## Limitaciones conocidas

VeilCrypt se encuentra en desarrollo y presenta algunas limitaciones conocidas:

- Actualmente, los portadores de imagen compatibles son **PNG** y **BMP**.
- Actualmente, los portadores de audio compatibles son **WAV**.
- El procesamiento de archivos de gran resolución puede provocar lentitud temporal en la interfaz mientras se realiza la operacion.
- La ocultación en audio puede producir una ligera modificación perceptible de la señal en determinadas condiciones.
- El archivo portador debe disponer de capacidad suficiente para almacenar el contenido cifrado.
  
Estas limitaciones podrán ser abordadas progresivamente en futuras versiones.

---

## Manejo de errores

Cuando una operación no puede completarse, se recomienda comprobar:

- Que el archivo seleccionado sea compatible.
- Que el archivo portador tenga suficiente capacidad.
- Que el contenido no supere la capacidad disponible.
- Que el archivo no haya sido modificado o dañado.
- Que la clave utilizada corresponda al contenido cifrado.

Si se encuentra un comportamiento inesperado o un error que no pueda reproducirse mediante estas comprobaciones, se recomienda abrir un reporte del problema proporcionando la mayor cantidad de información técnica posible.

---

## Actualizaciones

VeilCrypt incorpora un sistema de notificación de nuevas versiones.

Cuando se encuentra disponible una actualización, la herramienta puede informar al usuario directamente desde la interfaz para facilitar el acceso a la nueva versión.

---

## Seguridad y uso responsable

VeilCrypt es una herramienta desarrollada con fines de **aprendizaje, investigación, privacidad y análisis de técnicas de cifrado y ocultación de información**.

El uso de la herramienta debe realizarse respetando las leyes y normativas aplicables.

El usuario es responsable del contenido procesado y del uso que realice del software.

---

## Licencia

VeilCrypt es un proyecto de código abierto desarrollado por Nelson Arteaga (@n0rs4rt) — ORS4Tech.

El proyecto puede ser utilizado, estudiado, modificado y adaptado libremente, siempre respetando los términos de la licencia MIT.

Si utilizas o modificas VeilCrypt para crear una versión derivada o integrarlo en otro proyecto, debes conservar los créditos y la referencia al proyecto original y a su autor.

El objetivo es permitir que el código pueda ser aprendido y reutilizado por la comunidad, manteniendo siempre el reconocimiento de su autoría original.

Copyright © 2026 Nelson Arteaga (@n0rs4rt) — ORS4Tech

Licencia: MIT

<p align="center">
  <img src="https://github.com/n0rs4rt/ORS_VeilCrypt/blob/4df3f687358fdc145f9a90c435a4a100bf493212/assest/Captura%20de%20ecr%C3%A3%202026-09-08%20173517~2.jpg" alt="VeilCrypt">
</p>
