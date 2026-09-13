# ORS4 VeilCrypt

**VeilCrypt — Herramienta para cifrar mensajes y ocultar información y archivos cifrados dentro de imágenes y archivos de audio mediante técnicas de esteganografía y cifrado.**

![VeilCrypt Banner](./docs/images/veilcrypt-banner.png)

## Descripción

**ORS4 VeilCrypt** es una herramienta de seguridad desarrollada en Python que combina **cifrado y esteganografía** para proteger y ocultar información dentro de archivos aparentemente convencionales.

La herramienta permite trabajar con dos tipos principales de portadores: **imágenes PNG, BMP y archivos de audio WAV**. Antes de que cualquier archivo o información sea ocultada dentro del portador, el contenido es cifrado, de modo que la extracción del contenido oculto no implica necesariamente que la información pueda ser interpretada sin disponer de la clave correspondiente.

VeilCrypt también permite **cifrar y descifrar mensajes directamente**, sin necesidad de utilizar un archivo portador.

El proyecto fue diseñado con una interfaz gráfica orientada a facilitar el uso de estas técnicas sin necesidad de trabajar directamente desde una terminal.

---

## Funcionamiento

El proceso de ocultación sigue una secuencia de protección y ocultación de la información:

```text
Información original
        │
        ▼
     CIFRADO
        │
        ▼
Contenido cifrado
        │
        ▼
   ESTEGANOGRAFÍA
        │
        ▼
Imagen PNG / Audio WAV
con información oculta
```

La idea fundamental es separar dos conceptos:

**Cifrar la información** protege su contenido.

**Ocultar la información** reduce la evidencia de que dicha información existe dentro del archivo portador.

De esta forma, incluso si un tercero identifica y extrae el contenido oculto mediante técnicas externas, encontrará información cifrada que requiere la clave correspondiente para poder ser descifrada.

---

## Características principales

### Cifrado de mensajes

Permite introducir un mensaje y generar su versión cifrada directamente desde la interfaz.

El resultado incluye la información necesaria para conservar la clave de recuperación, permitiendo posteriormente realizar el proceso de descifrado.

Las claves pueden copiarse directamente o exportarse mediante archivos `.vlkey`.

> **Importante:** la clave es necesaria para recuperar información cifrada. VeilCrypt no almacena las claves utilizadas en el historial de operaciones.

---

### Ocultación de archivos en imágenes

Permite utilizar una imagen **PNG** o **BMP** como archivo portador y ocultar dentro de ella información previamente cifrada.

Proceso:

```text
Archivo
   │
   ▼
Cifrado
   │
   ▼
Payload cifrado
   │
   ▼
Imagen PNG o BMP
   │
   ▼
Imagen resultante
```

La información se incorpora mediante técnicas de **LSB (Least Significant Bit)**, modificando bits de menor significancia de los datos de imagen.

La imagen resultante sera en formato PNG

![Proceso de ocultación en imagen](./docs/images/image-steganography.png)

---

### Ocultación de archivos en audio

VeilCrypt permite utilizar archivos **WAV** como portadores para ocultar información cifrada.

El proceso sigue el mismo principio:

```text
Archivo
   │
   ▼
Cifrado
   │
   ▼
Payload cifrado
   │
   ▼
Audio WAV
   │
   ▼
Audio resultante
```

La información se incorpora en bits de menor significancia de las muestras de audio para minimizar el impacto sobre la señal original.

Actualmente, esta funcionalidad presenta una **limitación conocida**: dependiendo del contenido del audio y de la cantidad de información ocultada, puede producirse una ligera alteración perceptible o un ruido de fondo después del procesamiento.

Este comportamiento se encuentra identificado como una línea de mejora para futuras versiones.

![Proceso de ocultación en audio](./docs/images/audio-steganography.png)

---

## Extracción de información

VeilCrypt permite recuperar información previamente ocultada dentro de una imagen o archivo de audio.

Durante el proceso de extracción, la herramienta:

1. Analiza el archivo portador.
2. Recupera el contenido oculto.
3. Valida y procesa la información extraída.
4. Utiliza la clave correspondiente para descifrar el contenido.
5. Presenta el resultado al usuario.

En función del tipo de contenido ocultado, la herramienta muestra la información recuperada o proporciona la ubicación del archivo extraído junto con sus detalles.

![Proceso de extracción](./docs/images/extraction-process.png)

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

![Gestión de claves](./docs/images/key-management.png)

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

![Historial de operaciones](./docs/images/history.png)

---

## Consideraciones sobre el envío de archivos

Los archivos generados contienen información oculta directamente en los datos del archivo portador. Por este motivo, el archivo resultante debe mantenerse intacto después de su generación.

Algunas aplicaciones y plataformas pueden comprimir, recomprimir, redimensionar o recodificar automáticamente las imágenes y archivos de audio enviados.
Estas modificaciones pueden alterar los datos utilizados para ocultar la información y provocar que el contenido oculto no pueda recuperarse correctamente.

Por ello:

Evita enviar directamente imágenes o audios con información oculta mediante aplicaciones que puedan modificar o recomprimir el archivo.

Para conservar el archivo exactamente como fue generado, es recomendable enviarlo como archivo/documento, evitando funciones que procesen la imagen o el audio.

Otra alternativa es incluir el archivo dentro de un ZIP, RAR u otro contenedor que preserve sus bytes originales.

El mismo principio aplica tanto a imágenes PNG o BMP como a archivos de audio WAV.

En resumen: el archivo portador debe llegar al destinatario sin modificaciones respecto al archivo generado por VeilCrypt.

---

## Interfaz

La aplicación utiliza una interfaz gráfica desarrollada con **CustomTkinter**, diseñada para proporcionar una experiencia de uso sencilla y mantener separadas las diferentes operaciones de protección, ocultación y extracción.

![Interfaz principal](./docs/images/interface-main.png)

*Interfaz principal de ORS4 VeilCrypt.*

---

## Arquitectura conceptual

La herramienta combina diferentes capas de procesamiento:

```text
┌───────────────────────────────┐
│           Usuario             │
└───────────────┬───────────────┘
                │
                ▼
┌───────────────────────────────┐
│       Interfaz gráfica        │
│        CustomTkinter          │
└───────────────┬───────────────┘
                │
        ┌───────┴────────┐
        ▼                ▼
    Cifrado        Esteganografía
        │                │
        ▼                ▼
    Fernet         Imagen / Audio
        │                │
        └───────┬────────┘
                ▼
        Archivo resultante
```

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
