# Emotion Recognition
Este proyecto de arquitectura software utiliza AWS Serverless para implementar un servicio de reconocimiento de emociones. Permite subir imágenes, detectar emociones en las imágenes y gestionar los registros de emociones almacenados.

## Tabla de contenidos
- [Requisitos previos](#requisitos-previos)
- [Despliegue](#despliegue)
- [Funcionalidades](#funcionalidades)
- [Recursos](#recursos)
- [Limpieza](#limpieza)

## Requisitos previos
Antes de comenzar, asegúrate de tener los siguientes requisitos previos configurados:

- Una cuenta de AWS con permisos para crear y administrar los servicios necesarios.
- AWS CLI (Command Line Interface) instalado y configurado en tu máquina local.
- Serverless Framework instalado en tu máquina local. Puedes instalarlo siguiendo las instrucciones en [este enlace](https://www.serverless.com/framework/docs/getting-started/).
- Node.js instalado en tu máquina local. Puedes descargarlo desde [el sitio oficial de Node.js](https://nodejs.org/es/) y seguir las instrucciones de instalación.
- Docker instalado en tu máquina local. Puedes descargar Docker desde [el sitio oficial de Docker](https://www.docker.com/get-started) y seguir las instrucciones de instalación.

## Despliegue

Sigue los pasos a continuación para desplegar el proyecto en tu cuenta de AWS:

1. Clona este repositorio en tu máquina local.
2. Configura tus credenciales de AWS utilizando AWS CLI si aún no lo has hecho:
```shell
aws configure
```
3. Abre una terminal y navega hasta el directorio raíz del proyecto.
4. Ejecuta el siguiente comando para instalar las dependencias del proyecto:
```shell
npm install
```
Esto instalará las dependencias necesarias para la ejecución del Lambda en Node.js.

5. Configura las variables de entorno en el archivo serverless.yml para adaptar el servicio a tus necesidades:
```yaml
custom:
  variables:
    AWS_REGION: us-west-1
    BUCKET_NAME: ucb-sis-image-bucket
    TABLE_NAME: emotion_recognition_records
```
Asegúrate de modificar los valores de estas variables según tus preferencias. Aquí tienes una breve descripción de cada una:
- AWS_REGION: Elige la región de AWS en la que deseas desplegar el servicio.
- BUCKET_NAME: Especifica el nombre del bucket de S3 donde se almacenarán las imágenes.
- TABLE_NAME: Indica el nombre de la tabla de DynamoDB donde se registrarán las emociones detectadas.

7.  Ejecuta el siguiente comando para desplegar la infraestructura y las funciones de AWS Lambda:
```shell
serverless deploy
```
8. Una vez completado el despliegue, obtendrás la URL de la API Gateway que se generó, así como una API Key para acceder a la API. Puedes encontrar esta información en la salida del comando sls deploy en la sección de la API Gateway. Utiliza esta URL y la API Key para acceder a la aplicación de reconocimiento de emociones.

## Funcionalidades
El proyecto ofrece las siguientes funcionalidades:
- Subida de imágenes: La función imageUploadHandler permite subir imágenes a un bucket de S3 especificado en la variable de entorno BUCKET.
- Reconocimiento de emociones: La función emotion-recognition-handler procesa imágenes para reconocer emociones. Utiliza el contenedor de Docker especificado en appimage y ejecuta el comando app.emotion_recognition_handler. Los resultados se almacenan en la tabla de DynamoDB especificada en la variable de entorno TABLE_NAME.
- Obtención de emociones: La función get-emotion-handler permite obtener las emociones registradas en la tabla de DynamoDB especificada en la variable de entorno TABLE_NAME.
- Eliminación de emociones: La función delete-emotion-handler permite eliminar las emociones registradas en la tabla de DynamoDB especificada en la variable de entorno TABLE_NAME.

![Emotion Recognition Diagram](https://github.com/Arquitectura-de-Software-01-2023/Emotion-Recognition/assets/102682441/8f8fff56-e6af-40bb-9c33-cc6f6d595475)

## Recursos
El proyecto utiliza los siguientes recursos de AWS:
- AWS Lambda: Se utilizan varias funciones Lambda para procesar las solicitudes y realizar el reconocimiento de emociones.
- Amazon API Gateway: Se configura una API Gateway para exponer los endpoints de las funciones Lambda.
- Amazon S3: Se crea un bucket de S3 para almacenar las imágenes subidas.
- Amazon DynamoDB: Se crea una tabla de DynamoDB para almacenar los registros de emociones.

## Limpieza

Si deseas eliminar todos los recursos creados por el proyecto, ejecuta el siguiente comando:
```shell
serverless remove
```
Esto eliminará todas las funciones y recursos creados en tu cuenta de AWS.

Recuerda que el uso de Docker y el Serverless Framework puede requerir recursos adicionales en tu máquina y puede implicar costos adicionales en AWS. Asegúrate de tener suficiente capacidad de almacenamiento y ancho de banda disponible, y monitorea tus costos de AWS regularmente.

¡Gracias por utilizar Emotion Recognition! Si tienes alguna pregunta o problema, no dudes en abrir un problema en este repositorio.