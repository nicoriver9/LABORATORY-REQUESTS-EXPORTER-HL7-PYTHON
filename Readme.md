# Exportación de Pedidos de Laboratorio  - Script de Python
### Este script de Python está diseñado para realizar dos consultas SQL a una base de datos PostgreSQL y luego exportar los resultados a archivos de texto y mensajes HL7.

## Requisitos
Antes de ejecutar el script, asegúrate de tener instaladas las siguientes bibliotecas:

1. psycopg2: Para interactuar con la base de datos PostgreSQL.
2. dotenv: Para cargar las variables de entorno desde un archivo .env.
3. hl7apy: Para generar mensajes HL7.
## Instala estas bibliotecas usando el siguiente comando:
    pip install psycopg2 dotenv hl7apy

## Configuración de las variables de entorno
El script utiliza un archivo .env para almacenar las variables de conexión a la base de datos y otros parámetros necesarios para la generación de mensajes HL7. Asegúrate de crear un archivo .env en el mismo directorio que el script y define las siguientes variables:

    HOST=nombre_de_host
    DATABASE=nombre_de_la_base_de_datos
    USER=nombre_de_usuario
    PASSWORD=contraseña_del_usuario
    SENDING_APP=aplicacion_emisora
    SENDING_FACILITY=instalacion_emisora
    RECEIVING_APP=aplicacion_receptora
    RECEIVING_FACILITY=instalacion_receptora

## Funciones principales
execute_sql_query(sql_query)
Esta función se encarga de ejecutar la consulta SQL en la base de datos y devuelve los resultados. Recibe la consulta SQL como parámetro y utiliza las variables de entorno para la conexión a la base de datos.

build_hl7_message(result1, result2)
Esta función construye un mensaje HL7 ORU^R01 a partir de los resultados de las consultas SQL. Recibe dos tuplas con los resultados de las consultas y utiliza los datos para completar los campos del mensaje MSH y PID, así como para agregar segmentos OBX con los resultados obtenidos.

## Consultas SQL
El script contiene dos consultas SQL:

**query1:** Esta consulta recupera información relacionada con el paciente y la solicitud de laboratorio desde las tablas for_informe, for_tipo, for_estado, y paciente.

**query2:** Esta consulta recupera los detalles del resultado del laboratorio desde la tabla for_resultado_detalle.

##  Generación de archivos
El script combina los resultados de ambas consultas en una lista de tuplas y luego genera archivos de texto y mensajes HL7 únicos para cada par de registros.

Los archivos de texto se generan en la carpeta "exports" y contienen los resultados de las consultas en formato de texto plano.

Los mensajes HL7 se generan en la misma carpeta y siguen el estándar HL7 v2.5. Cada mensaje contiene información relacionada con el paciente y un conjunto de resultados de laboratorio obtenidos de la segunda consulta.

## Ejecución
Para ejecutar el script, simplemente ejecute el archivo index.py. Los archivos de texto y mensajes HL7 se generarán automáticamente en la carpeta "exports".

    Nota: Asegúrate de haber configurado correctamente las variables de entorno en el archivo .env antes de ejecutar el script.
    
    python index.py

## Créditos
Este script fue creado por Gabriel Alias y es parte del proyecto LAB_RESULTS_EXPORTER_APP. Si tienes alguna pregunta o comentario, por favor ponte en contacto con Gabriel Alias a través de montoto.

Esperamos que este script te sea útil. ¡Gracias por usar nuestro Laboratorio de Exportación de HL7!