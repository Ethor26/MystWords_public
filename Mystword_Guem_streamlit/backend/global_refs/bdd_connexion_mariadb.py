import os, re, json
from enum import Enum
import mariadb
import sqlparse
from dotenv import load_dotenv
import pandas as pd


# tuto_mysql: https://dev.mysql.com/doc/connector-python/en/

# ---------
# FONTION AUXILIAIRE A LA PRINCIPALE POUR PREPARER LES PARAMETRES DES REQUETES
def prepDico_paramsQueries(params=None):
    if params is None:
        params = [()]
    return {f"r{numReq + 1}": params[numReq] for numReq in range(len(params)) if params[numReq] != ()}


def get_table_name_from_query(sql_statement):
    match = re.search(r"(?i)(?:(?:UPDATE|INSERT INTO|REPLACE INTO|DELETE FROM)\s+|INTO\s+)([^\s]+)", sql_statement)
    if match:
        return match.group(1)
    return None


# - - - - CONNECTION - - - -
# Configuration de la base de données MySQL
def get_dict_db_config(name_var):
    load_dotenv()
    return json.loads(os.getenv(name_var))

db_config_API_main = get_dict_db_config("DB_INFOS")

def connexion_bdd(host, user, port, password, database):
    try:
        connect_bdd = mariadb.connect( # mysql.connector.connect(
            host=host,
            user=user,
            port=port,
            password=password,
            database=database
        )
        cur = connect_bdd.cursor()
        return connect_bdd, cur
    except Exception as e:  # mariadb.Error as e:
        print(f"Erreur de connexion à la base de données: {e}")
        return None, None

# Obtention de l'url avec sqlalchemy
def get_url_db_config(db_config, sqlalchemy=False):
    url_infos = f"{db_config['user']}:{db_config['password']}@{db_config['host']}:{db_config['port']}/{db_config['database']}"
    url_prefix = "mysql+mysqlconnector://" if sqlalchemy else "jbdc:mysql://"
    return f"{url_prefix}{url_infos}"


# - - - - EXECUTE - - - -
# Récupérer la clé de résultat d'une instruction SQL
def get_instr_key_result(number, type="", table_name=None):
    if type.upper() == "SELECT":
        return f"{type.lower()}_instr_{number}"
    return f"verif_instr_{number}: in {table_name}"

class Types_return_query(Enum):
    DATA = "data"
    SCHEMA = "schema"
    STATUS = "status"
    ERROR = "error"

def execute_sql_queries(sql_statements, database_config=None, connexion_script=False, **params):
    if database_config is None:
        database_config = db_config_API_main
    conn, cur = connexion_bdd(**database_config)
    results_queries = {Types_return_query.STATUS.value: False}
    if conn is None or cur is None:
        results_queries[Types_return_query.ERROR.value] = "Connection to database failed."
        return results_queries

    results_queries = {Types_return_query.STATUS.value: False}
    try:
        if connexion_script:
            conn.autocommit = True

        cpt = 1
        for sql_statement in sql_statements.split(";"):
            sql_statement = re.sub(r"/\*.*?\*/", "", sql_statement, flags=re.DOTALL)
            sql_statement = re.sub(r"--.*$", "", sql_statement, flags=re.MULTILINE)
            sql_statement = sql_statement.strip()
            if sql_statement:
                query_params = params.get(f"r{cpt}", ())
                print(f"Query {cpt}: {sql_statement} ; -- with params: {query_params}")

                cur.execute(sql_statement, query_params)
                sql_type = sqlparse.parse(sql_statement)[0].get_type()
                if sql_type == 'SELECT':
                    data = cur.fetchall()
                    schema = [column[0] for column in cur.description]
                    results_queries[get_instr_key_result(cpt, sql_type)] = {Types_return_query.DATA.value: data, Types_return_query.SCHEMA.value: schema}
                else:
                    table_name = get_table_name_from_query(sql_statement)
                    if table_name:
                        select_statement = f"SELECT * FROM {table_name}"
                        cur.execute(select_statement)
                        data = cur.fetchall()
                        schema = [column[0] for column in cur.description]
                        results_queries[get_instr_key_result(cpt, table_name=table_name)] = {Types_return_query.DATA.value: data, Types_return_query.SCHEMA.value: schema}
                    else:
                        results_queries[get_instr_key_result(cpt, table_name=table_name)] = [
                            f"Table name not found in query: {sql_statement}"]
                cpt += 1

        conn.commit()
        results_queries[Types_return_query.STATUS.value] = True
    except mariadb.Error as e:
        print("//////////////// L'erreur s'est produite lors de l'exécution des instructions SQL :", e)
        conn.rollback()
    finally:
        cur.close()
        conn.close()

    return results_queries

def get_resQueries_in_df(query, database_config=None):
    return pd.read_sql(query, get_url_db_config(database_config, sqlalchemy=True))

# - - - - - - RESULTS
def display_results(results, rows_on_one_line=False):
    if not results:
        print("No results.")
    if type(results) != dict:
        print("- - - - Result query:\n", results)
    else:
        for key, value in results.items():
            if key == Types_return_query.STATUS.value:
                print(f"{Types_return_query.STATUS.name}: ", value)
            else:
                print(f"Query: {key}")
                if isinstance(value, dict):
                    if Types_return_query.SCHEMA.value in value and Types_return_query.DATA.value in value:
                        schema = value[Types_return_query.SCHEMA.value]
                        data = value[Types_return_query.DATA.value]
                        print("Schema:", schema)
                        if data:
                            print("Result:\n" + ('\n' if not rows_on_one_line else '; ').join(str(row) for row in data))
                        else:
                            print("No results.")
                    else:
                        print("Invalid result format.")
                elif isinstance(value, list):
                    if value:
                        print("Result:\n" + ('\n' if not rows_on_one_line else '; ').join(str(row) for row in value))
                    else:
                        print("No results.")
                else:
                    print(value)
                print()

# - - - - - TEST
if __name__ == '__main__':

    # Autres parties du script restent inchangées
    sql_statements = """
      -- Commentaire de test d'exécution sur une ligne
    SELECT * FROM Word LIMIT 20;/* Commentaire de test d'exécution 
    sur plusieurs lignes */ 
    SELECT (SELECT WordText FROM Word LIMIT 1),
       (SELECT ModeName FROM Mode WHERE IsTerminal = FALSE LIMIT 1),
       (SELECT ModeName FROM Mode WHERE IsTerminal = True LIMIT 1),
       CalculateGematria_funct(
    (SELECT WordText FROM Word LIMIT 1),
    (SELECT ModeName FROM Mode WHERE IsTerminal = FALSE LIMIT 1),
    (SELECT ModeName FROM Mode WHERE IsTerminal = True LIMIT 1));
    
    SELECT CONCAT('[', group_concat(JSON_QUOTE(Word.WordText) SEPARATOR ','  LIMIT 3), ']') FROM Word LIMIT 3; -- substring_index(group_concat(JSON_QUOTE(Word.WordText) SEPARATOR ','  LIMIT 3), ',', 3)
    -- JSON_UNQUOTE(JSON_ARRAYAGG(CONVERT(Word.WordText USING utf8mb4) LIMIT 3)) FROM Word;
    SELECT CONCAT((SELECT GROUP_CONCAT(ModeName LIMIT 2 OFFSET 1) FROM Mode WHERE IsTerminal = False ORDER BY ModeName LIMIT 2),',', (SELECT ModeName FROM Mode WHERE IsTerminal = True LIMIT 1));
    SELECT CalculateGematriaArray(
                   (SELECT CONCAT('[', group_concat(JSON_QUOTE(Word.WordText) SEPARATOR ','  LIMIT 3), ']') FROM Word LIMIT 3),-- JSON_ARRAY('אֲשֶׁר-שַׂמְתִּי','אֲשֶׁר-נָטְעָה'),
                   (SELECT ModeName FROM Mode WHERE IsTerminal = FALSE LIMIT 1),
                   (SELECT CONCAT((SELECT GROUP_CONCAT(ModeName LIMIT 3 OFFSET 1) FROM Mode WHERE IsTerminal = False ORDER BY ModeName LIMIT 3),',',(SELECT ModeName FROM Mode WHERE IsTerminal = True LIMIT 1)))
                   );
    """
    args = prepDico_paramsQueries()
    results = execute_sql_queries(sql_statements, database_config=db_config_API_main, **args)
    print("\n===================== RESULTS TESTS =====================")
    display_results(results, rows_on_one_line=True)
