
# BACKEND, Prototipo de analisis de sentimientos en visión por computadora en las aulas de clase de la Universidad del Valle sede Tuluá en FAST API

## Description

Este repositorio contiene el codigo fuente del **API** para el projecto analisis de sentimientos por visión de computadora en las aulas de clase de la universidad del valle sede Tuluá, este projecto pretender ser un apoyo para que los docentes puedan tener una mejor metodologia de enseñanza mejorando así significativamente la calidad de la ensañanza y el nivel actual de la educación pues mediante esta app logramos ver en que momentos las clases pasan de ser entrenenidas a algo totalmente diferente brindando un punto de inflexion para que el docente pueda cambiar su metodologia.

### Caracteristicas claves del **API**

- **Autenticación de usuarios**: Esta aplicación permite facilmente la autenticación de usuarios mediante un correo y una contraseña.
- **Registro de usuarios**: Para el registro de usuarios se recogen datos basicos como los nombres, los apellidos, el correo y la contraseña.
- **Analisis de sentimientos**: Mediante un algoritmo basado en inteligencia artificial la apliación es capaz de detectar rostros y emociones de los estudiantes.
- **Resumen semanal**: La apliación brinda un resumen semanal de las emociones que se han registrado durante todas las clases.
- **Resumen de emociones**: La aplicación facilita al usuario poder ver los videos de las emociones negativas en tiempo real así como poder analizar despues de las clases en que momentos las emociones cambiaron.

Esta **API** fue desarrollada en *Python* y el framework *FastAPI* y sigue las mejores practicas de la industria para garantizar la escalabilidad, el rendimiento y la seguridad. Permitiendo un funcionamiento fluido para evitar retrasos en la aplicacion.

***Nota*** : Esta aplicación se encuentra en fase de prototipo, por lo que puede contar con demoras de ejecución o pequeños errores que seran solucionados en trabajos posteriores.

### Primeros pasos

Para iniciar el projecto se deben seguir los siguientes pasos y recomendaciones:

1. Versión de python:

    `
    para poder ejecutar la aplicación se debe contar con una versión de python 3.10 o superior.
    `

2. Clonar el repositorio:

    Clonar el repositorio [FastAPI-TG](https://github.com/JaimeLopez04/FastAPI-TG.git)

    ```shell
    git clone https://github.com/JaimeLopez04/FastAPI-TG.git
    ```

3. Navegar hasta el repositorio:

    ```shell
    cd FastAPI-TG
    ```

4. Crear y activar el entorno virtual:

     ``` shell
     python -m venv .env

     .\.env\Scripts\activate
     ```

5. Instalar las dependencias necesarias para ejecutar el projecto:

    ```shell
    pip install -r requirements.txt
    ```

    Para esto de debe contar con *Python* y *pip* instalados en el sistema. El archivo *requirements.txt* contiene las dependencias necesarias y sus versiones.

6. Iniciar el servidor de *FastAPI* con *uvicorn*:

    ```shell
    uvicorn app.app:app --reload
    ```

Con estos comandos ya se cuenta con el API ejecutandose.
