import psycopg2
from dotenv import load_dotenv
import os
from hl7apy.core import Message

load_dotenv()

# Function to execute the SQL query and fetch results
def execute_sql_query(sql_query):
    conn = psycopg2.connect(
        host        =os.getenv("HOST"),
        database    =os.getenv("DATABASE"),
        user        =os.getenv("USER"),
        password    =os.getenv("PASSWORD"),
    )
    cursor = conn.cursor()
    cursor.execute(sql_query)
    results = cursor.fetchall()
    cursor.close()
    conn.close()
    return results

# SQL Query for the header information
header_query = """
    SELECT
        paciente.paciente_id,
        CONCAT(paciente.APELLIDO1, ' ', paciente.NOMBRES) AS apellido1_pl2,
        paciente.numero_documento AS numero_documento,
        for_informe.informe_id,
        for_informe.nro_informe,
        for_informe.fecha_informe,        
        paciente.sexo,
        paciente.fecha_nacimiento,
        for_informe.fecha_carga,
        for_informe.fecha_final,        
        for_informe.nro_informe,        
        for_informe.per_servicio_id,
        for_informe.formulario_id,
        for_informe.for_estado_id,
        for_estado.for_nombre,
        for_tipo.nombre_tipo,
        for_informe.hclinica
    FROM
        for_informe
        LEFT JOIN for_tipo ON for_informe.for_tipo_id = for_tipo.for_tipo_id
        LEFT JOIN for_estado ON for_informe.for_estado_id = for_estado.for_estado_id
        LEFT JOIN paciente ON for_informe.paciente_id = paciente.paciente_id;
"""

# SQL Query for the body information
body_query = """
    SELECT
        for_resultado_detalle.respuesta_info AS nombre_determinacion,
        for_resultado_detalle.codigo_opcion AS codigo_determinacion       
    FROM
        for_resultado_detalle
    WHERE
        for_resultado_detalle.resultado_detalle_id IS NOT NULL;
"""


# Function to build the HL7 ORU^R01 message from the query results
def build_hl7_message(result_header, result_body):
    # Create the ORU^R01 message
    message = Message("ADT_A01", version="2.5")

    # MSH Segment
    msh_segment = message.add_segment("MSH")
    msh_segment.MSH_3 = os.getenv("SENDING_APP")           # Sending application name
    msh_segment.MSH_4 = os.getenv("SENDING_FACILITY")      # Sending facility name
    msh_segment.MSH_5 = os.getenv("RECEIVING_APP")         # Receiving application name
    msh_segment.MSH_6 = os.getenv("RECEIVING_FACILITY")    # Receiving facility name

    # PID Segment (Patient Information)
    pid_segment = message.add_segment("PID")
    pid_segment.PID_3 = str(result_header[0])  # Patient ID
    pid_segment.PID_5 = result_header[1]  # Patient's full name (Last Name and First Name)
    pid_segment.PID_7 = str(result_header[7]).replace("-", "")  # Patient Sex
    pid_segment.PID_8 = str(result_header[6])  # Patient Birth Date
    pid_segment.PID_18 = str(result_header[2])  # Patient's ID number (DNI)

    # Add other segments and fields according to the type of HL7 message you want to generate
    # ...

    # OBX Segment (Observation/Result)
    obx_segment = message.add_segment("OBX")
    obx_segment.OBX_2 = str(result_body[1])  # Value Code (ST: String)
    obx_segment.OBX_3 = "LABORATORY REQUEST"  # Result Description
    obx_segment.OBX_5 = result_body[0]  # Value of the result obtained

    # Add other results from the second query in additional OBX segments
    # ...

    return message.to_er7()


# Execute the queries and fetch the results
results_header = execute_sql_query(header_query)
results_body = execute_sql_query(body_query)

# Combine the results into a list of tuples
combined_results = list(zip(results_header, results_body))

# Generate unique txt files for each pair of records
for i, (result_header, result_body) in enumerate(combined_results, 1):
    with open(f"exports/resultado_{str(result_header[2])}.txt", "w") as file:
        
        # file.write(str(result_header) + "\n")
        # file.write(str(result_body) + "\n")

        hl7_message = build_hl7_message(result_header, result_body)

    # Save the HL7 message to a file
    with open(f"exports/resultado_{str(result_header[2])}.hl7", "w") as file:
        file.write(hl7_message)

print("Txt files with the query results have been generated.")
