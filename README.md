
# BACKEND, Prototipo de analisis de sentimientos en visión por computadora en las aulas de clase de la Universidad del Valle sede Tuluá en FAST API

## Description

Este repositorio contiene el Código fuente del **API** para el proyecto análisis de sentimientos por visión de computadora en las aulas de clase de la universidad del valle sede Tuluá, este proyecto pretender ser un apoyo para que los docentes puedan tener una mejor metodología de enseñanza mejorando así significativamente la calidad de la enseñanza y el nivel actual de la educación pues mediante esta app logramos ver en qué momentos las clases pasan de ser entretenidas a algo totalmente diferente brindando un punto de inflexión para que el docente pueda cambiar su metodología.

### Características claves del **API**

- **Autenticación de usuarios**: Esta aplicación permite fácilmente la autenticación de usuarios mediante un correo y una contraseña.
- **Registro de usuarios**: Para el registro de usuarios se recogen datos básicos como los nombres, los apellidos, el correo y la contraseña.
- **Análisis de sentimientos**: Mediante un algoritmo basado en inteligencia artificial la aplicación es capaz de detectar rostros y emociones de los estudiantes.
- **Resumen semanal**: La aplicación brinda un resumen semanal de las emociones que se han registrado durante todas las clases.
- **Resumen de emociones**: La aplicación facilita al usuario poder ver los videos de las emociones negativas en tiempo real, así como poder verlos después de las clases para saber en qué momentos las emociones cambiaron.

Esta **API** fue desarrollada en *Python* y el framework *FastAPI* y sigue las mejores prácticas de la industria para garantizar la escalabilidad, el rendimiento y la seguridad. Permitiendo un funcionamiento fluido para evitar retrasos en la aplicación.

***Nota***: Esta aplicación se encuentra en fase de prototipo, por lo que puede contar con demoras de ejecución o pequeños errores que serán solucionados en trabajos posteriores.

### Primeros pasos

Para iniciar el proyecto se deben seguir los siguientes pasos y recomendaciones:

1. Requisitos para poder ejecutar el proyecto:

    - Contar con una versión de *Python* 3.10 o superior.
    - Tener instalado *MySQL* (En caso de no contar con este instalado revisar [Instalación de MySQL en docker](#instalación-de-mysql-en-docker))
    - En *MySQL* debemos crear una base de datos llamada *feelings_app*
    - *Opcional*, contar con *docker* instalado

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

5. Instalar las dependencias necesarias para ejecutar el proyecto:

    ```shell
    pip install -r requirements.txt
    ```

    Para esto se debe contar con *Python* y *pip* instalados en el sistema. El archivo *requirements.txt* contiene las dependencias necesarias y sus versiones por lo que debes verificar que cuentas con este archivo.

6. Iniciar el servidor de *FastAPI* con *uvicorn*:

    ```shell
    uvicorn app.app:app --reload
    ```

Con estos comandos ya se cuenta con el API ejecutándose.

### Versiones de las dependencias

Este proyecto fue realizado en *Python 3.12.3, pip 24.0* y las dependencias utilizadas son las siguientes:

- fastapi : 0.110.1
- pydantic : 2.7.0
- uvicorn : 0.29.0
- SQLAlchemy : 2.0.29
- PyMySQL : 1.1.0
- cryptography : 42.0.5
- numpy : 1.26.4
- keras : 3.2.1
- tensorflow : 2.16.1
- tensorflow-intel : 2.16.1
- opencv-python : 4.9.0.80
- python-multipart : 0.0.9

### Instalación de MySQL en docker

Para poder realizar esto necesitaremos las siguientes herramientas:

- Docker
- WSL (Esto aplica en el caso de Windows)

Para instalar MySQL en docker se debe ejecutar el siguiente comando:

1. Desplegar el *docker-compose*:

    ```shell
    docker compose up
    ```

Luego debemos por linea de comandos o algún gestor de base de datos como puede ser *DBeaver* conectarnos a *MySQL* para esto usamos los siguientes datos:

1. Host: localhost
2. Puerto: 3306
3. Usuario: root
4. Contraseña: root

debemos crear una nueva base de datos con el nombre *feelings_app*

Para que el *API* pueda hacer uso de esto debemos modificar el archivo *constants.py* que se encuentra en una carpeta con el mismo nombre dentro de app.
