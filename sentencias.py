import mysql.connector
    
def conexionDB():
    global cursor
    global cnx
    cnx = mysql.connector.connect(user='root', password='211099',
                                host='localhost',
                                database='planta2')
    cursor = cnx.cursor()

def obtener_lista_de_plantas_por_suelo(suelo):
    conexionDB()
    query = """
    SELECT 
        P.id_planta as 'ID de Planta'
    FROM
        plantas P
    LEFT JOIN planta_suelo PS ON P.id_planta = PS.id_planta
    LEFT JOIN suelos S ON PS.id_suelo = S.id_suelo
    WHERE 
        S.nombre = '{}'
    GROUP BY
        P.nombre, S.nombre;
    """.format(suelo)
    cursor.execute(query)
    results = cursor.fetchall()
    cursor.close()
    cnx.close()
    
    # Como cada resultado es una tupla de un solo valor (ID de Planta), simplemente obtenemos el primer elemento
    final_results = [result[0] for result in results]
    
    return final_results

def obtener_datos_por_nombre_planta(planta):
    conexionDB()
    query = """
        SELECT
        P.id_planta as 'ID de Planta', 
        P.nombre as 'Nombre de Planta',
        GROUP_CONCAT(DISTINCT S.nombre) as 'Nombres de Suelo',
        GROUP_CONCAT(DISTINCT TC.nombre) as 'Tipos de Cultivo',
        GROUP_CONCAT(DISTINCT C.nombre) as 'Climas Soportados',
        GROUP_CONCAT(DISTINCT R.nombre) as 'Riesgos de la Planta',
        P.ph as 'Rango de PH Planta',
        P.nitrogeno as 'Nitrogeno Planta',
        P.potacio as 'Potacio Planta',
        P.calcio as 'Calcio Planta',
        P.fosforo as 'Fosforo Planta',
        P.aux_ph as 'Aux_PH Planta',
        S.ph as 'Rango de PH Suelo',
        S.nitrogeno as 'Nitrogeno Suelo',
        S.potacio as 'Potacio Suelo',
        S.calcio as 'Calcio Suelo',
        S.fosforo as 'Fosforo Suelo',
        IP.ph as 'PH Incremento',
        IP.nitrogeno as 'Nitrogeno Incremento',
        IP.potacio as 'Potacio Incremento',
        IP.calcio as 'Calcio Incremento',
        IP.fosforo as 'Fosforo Incremento',
        GROUP_CONCAT(DISTINCT M.nombre) as 'Meses',
        GROUP_CONCAT(DISTINCT E1.nombre) as 'Efectos de la Planta',
        GROUP_CONCAT(DISTINCT E2.nombre) as 'Efectos que Afectan a la Planta'
    FROM
        plantas P
    LEFT JOIN planta_suelo PS ON P.id_planta = PS.id_planta
    LEFT JOIN suelos S ON PS.id_suelo = S.id_suelo
    LEFT JOIN planta_tipo_cultivos PTC ON P.id_planta = PTC.id_planta
    LEFT JOIN tipo_cultivos TC ON PTC.id_tipo_cultivo = TC.id_tipo_cultivo
    LEFT JOIN planta_climas PC ON P.id_planta = PC.id_planta
    LEFT JOIN climas C ON PC.id_clima = C.id_clima
    LEFT JOIN planta_riesgos PR ON P.id_planta = PR.id_planta
    LEFT JOIN riesgos R ON PR.id_riesgo = R.id_riesgo
    LEFT JOIN incremento_planta IP ON P.id_planta = IP.id_planta
    LEFT JOIN plantas_mes PM ON P.id_planta = PM.id_planta
    LEFT JOIN meses M ON PM.id_mes = M.id_mes
    LEFT JOIN planta_efectos PE ON P.id_planta = PE.id_planta
    LEFT JOIN efectos E1 ON PE.id_efecto = E1.id_efecto
    LEFT JOIN planta_afecta PA ON P.id_planta = PA.id_planta
    LEFT JOIN efectos E2 ON PA.id_efecto = E2.id_efecto
    WHERE 
        P.nombre = '{}'
    GROUP BY
        P.nombre;
    """.format(planta)
    cursor.execute(query)
    results = cursor.fetchall()
    cursor.close()
    cnx.close()
        # Convert each tuple to a list
    results_as_lists = [list(tup) for tup in results]
    
    # Create the final result list
    final_results = []
    
    for result in results_as_lists:
        # Split string into list where commas occur
        nombre_suelo = [result[2]] # wrap the soil name into a list
        tipos_cultivo = [result[3]] # wrap the crop type into a list
        climas_soportados = result[4].split(",")  
        riesgos_planta = result[5].split(",")
        valores_planta = [result[7], result[8], result[9], result[10], result[11]] 
        valores_suelo = [result[12], result[13], result[14], result[15], result[16]] 
        valores_incremento = [result[17], result[18], result[19], result[20], result[21]]
        meses = result[22].split(",") 
        efectos_planta = result[23].split(",")
        efectos_afectan_planta = result[24].split(",")
        
        # Create a new record
        new_record = result[:2] + [nombre_suelo] + [tipos_cultivo] + [climas_soportados, riesgos_planta, 
                               result[6], valores_planta, valores_suelo, valores_incremento, 
                               meses, efectos_planta, efectos_afectan_planta]
        final_results.append(new_record)
    
    return final_results


def obtener_datos_por_ids_planta(lista_ids):
    conexionDB()
    ids = ', '.join(map(str, lista_ids))
    query = """
            SELECT
        P.id_planta as 'ID de Planta', 
        P.nombre as 'Nombre de Planta',
        GROUP_CONCAT(DISTINCT S.nombre) as 'Nombres de Suelo',
        GROUP_CONCAT(DISTINCT TC.nombre) as 'Tipos de Cultivo',
        GROUP_CONCAT(DISTINCT C.nombre) as 'Climas Soportados',
        GROUP_CONCAT(DISTINCT R.nombre) as 'Riesgos de la Planta',
        P.ph as 'Rango de PH Planta',
        P.nitrogeno as 'Nitrogeno Planta',
        P.potacio as 'Potacio Planta',
        P.calcio as 'Calcio Planta',
        P.fosforo as 'Fosforo Planta',
        P.aux_ph as 'Aux_PH Planta',
        S.ph as 'Rango de PH Suelo',
        S.nitrogeno as 'Nitrogeno Suelo',
        S.potacio as 'Potacio Suelo',
        S.calcio as 'Calcio Suelo',
        S.fosforo as 'Fosforo Suelo',
        IP.ph as 'PH Incremento',
        IP.nitrogeno as 'Nitrogeno Incremento',
        IP.potacio as 'Potacio Incremento',
        IP.calcio as 'Calcio Incremento',
        IP.fosforo as 'Fosforo Incremento',
        GROUP_CONCAT(DISTINCT M.nombre) as 'Meses',
        GROUP_CONCAT(DISTINCT E1.nombre) as 'Efectos de la Planta',
        GROUP_CONCAT(DISTINCT E2.nombre) as 'Efectos que Afectan a la Planta',
        GROUP_CONCAT(DISTINCT PC2.id_planta2) as 'Plantas Compatibles'
    FROM
        plantas P
    LEFT JOIN planta_suelo PS ON P.id_planta = PS.id_planta
    LEFT JOIN suelos S ON PS.id_suelo = S.id_suelo
    LEFT JOIN planta_tipo_cultivos PTC ON P.id_planta = PTC.id_planta
    LEFT JOIN tipo_cultivos TC ON PTC.id_tipo_cultivo = TC.id_tipo_cultivo
    LEFT JOIN planta_climas PC ON P.id_planta = PC.id_planta
    LEFT JOIN climas C ON PC.id_clima = C.id_clima
    LEFT JOIN planta_riesgos PR ON P.id_planta = PR.id_planta
    LEFT JOIN riesgos R ON PR.id_riesgo = R.id_riesgo
    LEFT JOIN incremento_planta IP ON P.id_planta = IP.id_planta
    LEFT JOIN plantas_mes PM ON P.id_planta = PM.id_planta
    LEFT JOIN meses M ON PM.id_mes = M.id_mes
    LEFT JOIN planta_efectos PE ON P.id_planta = PE.id_planta
    LEFT JOIN efectos E1 ON PE.id_efecto = E1.id_efecto
    LEFT JOIN planta_afecta PA ON P.id_planta = PA.id_planta
    LEFT JOIN efectos E2 ON PA.id_efecto = E2.id_efecto
    LEFT JOIN plantas_compatibles PC2 ON P.id_planta = PC2.id_planta1
    WHERE 
        P.id_planta IN ({})
    GROUP BY
        P.nombre;
    """.format(ids)
    cursor.execute(query)
    results = cursor.fetchall()
    cursor.close()
    cnx.close()

    final_results = {}
    
    for result in results:
        # Split strings into lists where commas occur
        nombre_suelo = result[2].split(",")  
        tipos_cultivo = result[3].split(",")
        climas_soportados = result[4].split(",")  
        riesgos_planta = result[5].split(",")
        valores_planta = [result[7], result[8], result[9], result[10], result[11]] 
        valores_suelo = [result[12], result[13], result[14], result[15], result[16]] 
        valores_incremento = [result[17], result[18], result[19], result[20], result[21]]
        meses = result[22].split(",") 
        efectos_planta = result[23].split(",")
        efectos_afectan_planta = result[24].split(",")
        plantas_compatibles = list(map(int, result[25].split(",")))
        
        # Create a new record
        new_record = [result[1]] + [nombre_suelo] + [tipos_cultivo] + [climas_soportados, riesgos_planta, 
                               result[6], valores_planta, valores_suelo, valores_incremento, 
                               meses, efectos_planta, efectos_afectan_planta,plantas_compatibles]
        
        # Append the new record to the dictionary with the plant ID as the key
        final_results[result[0]] = new_record
    
    return final_results

    
    


def obtener_id_por_nombre(id):
    conexionDB()
    query = """
    SELECT 
        P.id_planta as 'ID de Planta'
    FROM
        plantas P
    WHERE 
        P.nombre = '{}';

    """.format(id)
    cursor.execute(query)
    results = cursor.fetchall()
    # Check if the results are not empty
    if results:
        # Access the first element of the first tuple
        id_planta = results[0][0]
        print(id_planta)
        cursor.close()
        cnx.close()
        return id_planta
    else:
        print('No results found')
        cursor.close()
        cnx.close()
        return None

def obtener_atributos_suelo_por_nombre(nombre_suelo):
    conexionDB()
    query = """
        SELECT 
            nombre, 
            nitrogeno, 
            potacio, 
            calcio, 
            fosforo, 
            ph
        FROM
            suelos
        WHERE
            nombre = '{}';
    """.format(nombre_suelo)
    cursor.execute(query)
    resultado = cursor.fetchone()
    cursor.close()
    cnx.close()
    
    # Convert the tuple to a list
    resultado_lista = list(resultado)
    
    return resultado_lista

def obtener_nombres_de_plantas():
    conexionDB()
    query = "SELECT nombre FROM plantas"
    cursor.execute(query)
    results = cursor.fetchall()
    cursor.close()
    cnx.close()

    # Convertir los resultados en una lista de nombres de plantas.
    # Como cada resultado es una tupla, debemos obtener el primer elemento de cada tupla.
    nombres_de_plantas = [tup[0] for tup in results]

    return nombres_de_plantas

def obtener_tipos_de_cultivos():
    conexionDB()
    query = "SELECT nombre FROM tipo_cultivos"
    cursor.execute(query)
    results = cursor.fetchall()
    cursor.close()
    cnx.close()

    # Convertir los resultados en una lista de tipos de cultivos.
    # Como cada resultado es una tupla, debemos obtener el primer elemento de cada tupla.
    tipos_de_cultivos = [tup[0] for tup in results]

    return tipos_de_cultivos

def obtener_riesgos():
    conexionDB()
    query = "SELECT nombre FROM riesgos"
    cursor.execute(query)
    results = cursor.fetchall()
    cursor.close()
    cnx.close()

    # Convertir los resultados en una lista de riesgos.
    # Como cada resultado es una tupla, debemos obtener el primer elemento de cada tupla.
    riesgos = [tup[0] for tup in results]

    return riesgos

def obtener_suelos():
    conexionDB()
    query = "SELECT nombre FROM suelos"
    cursor.execute(query)
    results = cursor.fetchall()
    cursor.close()
    cnx.close()

    # Convertir los resultados en una lista de nombres de suelos.
    # Como cada resultado es una tupla, debemos obtener el primer elemento de cada tupla.
    suelos = [tup[0] for tup in results]

    return suelos


def obtener_climas():
    conexionDB()
    query = "SELECT nombre FROM climas"
    cursor.execute(query)
    results = cursor.fetchall()
    cursor.close()
    cnx.close()

    # Convertir los resultados en una lista de nombres de climas.
    # Como cada resultado es una tupla, debemos obtener el primer elemento de cada tupla.
    climas = [tup[0] for tup in results]

    return climas


def obtener_meses():
    conexionDB()
    query = "SELECT nombre FROM meses"
    cursor.execute(query)
    results = cursor.fetchall()
    cursor.close()
    cnx.close()

    # Convertir los resultados en una lista de nombres de meses.
    # Como cada resultado es una tupla, debemos obtener el primer elemento de cada tupla.
    meses = [tup[0] for tup in results]

    return meses
