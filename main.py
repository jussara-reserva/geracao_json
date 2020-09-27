import cx_Oracle # Biblioteca responsável por conectar o Python ao Oracle DB
import json # Bibilioteca responsável por formatar arquivos json

# Setar a instância do cliente Oracle 32-bits
cx_Oracle.init_oracle_client(lib_dir=r"C:\oracle\instantclient_19_6")

# Credenciais de acesso ao DB hr
user = "hr"
password = "hr"
db = "localhost/xepdb1"

connection = cx_Oracle.connect(user, password, db) # Criando a conexão com o DB
cursor = connection.cursor() # Setando um cursor

# print("Database version: ", connection.version) # Verificando se a conexão foi realizada

# Função responsável pela criação do dicionário
def criar_dicionario(cursor):
    '''Esta função é a responsável pela criação do dicionário com os dados extraídos do BD,
    que será posteriormente inserido no json'''

    # Busca no BD todos os países
    cursor.execute('SELECT country_id, country_name FROM countries')
    # Armazena o resultado da query em uma variável
    resPaises = cursor.fetchall()

    # Define as chaves que serão combinadas com os resultados da busca no BD para criar o dicionário
    chavesPaises = ['id', 'nome']
    paises = []

    # Varredura pelo resultado da busca para pegar cada país e armazenar na lista de paises, como um dicionário
    for rP in resPaises:
        paises.append(dict(zip(chavesPaises, rP)))

        # Busca as localizações de acordo com o id dos países
        cursor.prepare('SELECT location_id, street_address, city FROM locations WHERE country_id = :id')
        cursor.execute(None, {'id': rP[0]})
        resLocais = cursor.fetchall()

        # Verifica se os países possuem localizações cadastradas e atribui o valor None caso não possua
        if resLocais == []:
            paises[-1]['localizacoes'] = None

        else:
            chavesLocais = ['id', 'endereco', 'cidade']
            localizacoes = []

            # Varredura pelo resultado da busca para pegar cada localização e armazenar na lista de localizações, como um dicionário
            for rL in resLocais:
                localizacoes.append(dict(zip(chavesLocais, rL)))

                # Busca os departamentos de acordo com o id das localizações
                cursor.prepare('SELECT d.department_id, d.department_name, concat(e.first_name, concat(:espaco, e.last_name)) manager_name FROM departments d LEFT JOIN employees e ON d.manager_id = e.employee_id WHERE location_id = :id')
                cursor.execute(None, {'espaco': ' ', 'id': rL[0]})
                resDepartamentos = cursor.fetchall()

                # Verifica se as localizações possuem departamentos cadastrados e atribui o valor None caso não possua
                if resDepartamentos == []:
                    localizacoes[-1]['departamentos'] = None

                else:
                    chavesDepartamentos = ['id', 'nome', 'gerente']
                    departamentos = []

                    # Varredura pelo resultado da busca para pegar cada departamento e armazenar na lista de departamentos, como um dicionário
                    for rD in resDepartamentos:
                        departamentos.append(dict(zip(chavesDepartamentos, rD)))

                        # Verifica se o departamento possui um gerente e atribui o valor None caso não possua
                        if departamentos[-1]['gerente'] == ' ':
                            departamentos[-1]['gerente'] = None

                        # Busca os empregados de acordo com o id dos departamentos
                        cursor.prepare('SELECT e.employee_id, concat(e.first_name, concat(:espaco, e.last_name)) employee_name, j.job_title, e. salary '
                                       'FROM employees e JOIN jobs j ON e.job_id = j.job_id WHERE e.department_id = :id')
                        cursor.execute(None, {'espaco': ' ', 'id': rD[0]})
                        resEmpregados = cursor.fetchall()

                        # Verifica se os departamentos possuem empregados cadastrados e atribui o valor None caso não possua
                        if resEmpregados == []:
                            departamentos[-1]['empregados'] = None

                        else:
                            chavesEmpregados = ['id', 'nome', 'cargo', 'salario']
                            empregados = []

                            # Varredura pelo resultado da busca para pegar cada empregado e armazenar na lista de empregados, como um dicionário
                            for rE in resEmpregados:
                                empregados.append(dict(zip(chavesEmpregados, rE)))

                            # Armazena a lista de empregados no seu departamento correspondente, o último adicionado
                            departamentos[-1]['empregados'] = empregados

                    # Armazena a lista de departamentos na sua localização correspondente, a última adicionada
                    localizacoes[-1]['departamentos'] = departamentos

            # Armazena a lista de localizações no seu país correspondente, o último adicionado
            paises[-1]['localizacoes'] = localizacoes

    # Cria o dicionário dos países, com a chave 'paises' e a lista paises como o seu valor
    dicPaises = {'paises': paises}
    # Ao fim, retorna o dicionário de países criado
    return dicPaises

# Função responsável pela criação e escrita no arquivo
def escrever_arquivo(dicPaises):
    '''Esta função é a responsável pela criação do arquivo com os dados extraídos do BD,
    que são armazenados em um dicionário a partir da execução da função criar_dicionario()'''

    # Cria o arquivo (ou apenas abre, caso já exista) no modo de escrita 'w', que substitui os dados no arquivo caso já possua
    with open('dados.json', 'w') as arquivo:
        json.dump(dicPaises, arquivo, indent = 4)
        

dicPaises = criar_dicionario(cursor)
escrever_arquivo(dicPaises)

cursor.close()
connection.close()
