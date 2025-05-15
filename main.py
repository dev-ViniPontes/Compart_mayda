from flask import Flask, request, jsonify # type: ignore
from flask_cors import CORS # type: ignore
import psycopg2


app = Flask(__name__)
CORS(app)

# Conexão com banco de dados
def connection():
    try:
        #conn = psycopg2.connect(
        #    host="dpg-d03pjjali9vc73ftp4pg-a.oregon-postgres.render.com",
        #    port=5432,
        #    database="postgresql_maydaqueiroz",
        #    user="postgresql_maydaqueiroz_user",
        #    password="rEkCawpETemawycDK1ml5Sn5ShRAMPxc"
        #)
        conn = psycopg2.connect(
            host="31.97.17.69",
            port=5432,
            database="postgresql_maydaqueiroz",
            user="postgres",
            password="hcac10"
        )
        print("Conectado com sucesso ao PostgreSQL!")
        return conn
    except Exception as e:
        print("Erro ao conectar:", e)
    
# Criar tabela admin
def create_table():
    conn = connection()
    if conn is None:
        return jsonify({"message": "Erro de conexão com o banco de dados"}), 500
    cursor = conn.cursor()

    # Admin
    cursor.execute(
        "CREATE TABLE IF NOT EXISTS admin (nome VARCHAR, crm VARCHAR, sobre VARCHAR, image_base64 VARCHAR, whats VARCHAR, whatsmsg VARCHAR, email VARCHAR)"
    )
    conn.commit()

    # Formação Admin
    cursor.execute(
        "CREATE TABLE IF NOT EXISTS formacaoadmin (id INTEGER, rqe VARCHAR, especialidade VARCHAR, instituto VARCHAR)"
    )
    conn.commit()

    # Title Infanto Juvenil
    cursor.execute("CREATE TABLE IF NOT EXISTS infatojuvenilTitle (titulo VARCHAR)")
    conn.commit()

    # Textos InfantoJuvenil
    cursor.execute(
        "CREATE TABLE IF NOT EXISTS infatojuvenil (id INTEGER, descricao VARCHAR)"
    )
    conn.commit()

    # Especialidades
    cursor.execute(
        "CREATE TABLE IF NOT EXISTS especialidades (id INTEGER, descricao VARCHAR)"
    )
    conn.commit()
    
    # Multidisciplinares
    cursor.execute(
        "CREATE TABLE IF NOT EXISTS multidisciplinares (id INTEGER, nome VARCHAR, crm VARCHAR, id_especialidade VARCHAR, especialidade VARCHAR, tempexperiencia VARCHAR, tipoconsulta VARCHAR, publicoatendido VARCHAR, formaatendimento VARCHAR, imagebase64 VARCHAR, telefone VARCHAR, textmsg VARCHAR)"
    )
    conn.commit()
    
    # Depoimentos
    cursor.execute(
        "CREATE TABLE IF NOT EXISTS depoimentos (id INTEGER, nome VARCHAR, descricao VARCHAR)"
    )
    conn.commit()

    # Localizações
    cursor.execute(
        "CREATE TABLE IF NOT EXISTS localizacoes (id INTEGER, nome VARCHAR, endereco VARCHAR, telefone VARCHAR, email VARCHAR, link_maps VARCHAR)"
    )
    conn.commit()

    # Diagnósticos
    cursor.execute(
        "CREATE TABLE IF NOT EXISTS diagnosticos (id INTEGER, nome VARCHAR, url VARCHAR)"
    )
    conn.commit()

    conn.close()


@app.route("/Teste", methods=["GET"]) # Get informações admin - OK
def Teste():
    return jsonify({"message": "Ativa"}), 200



@app.route("/login", methods=["POST"]) # Get informações admin - OK
def Login():
    if not request.json:
        return jsonify({"message": "No data provided"}), 400

    key = request.json.get("key")

    if key == "netd3zztk1heyly2g4tr" or key == "hcac10":
        return jsonify({"message": "Success"}), 200
    else:
        return jsonify({"message": "Chave incorreta"}), 400


################################################

@app.route("/admin", methods=["GET"]) # Get informações admin - OK
def get_admin():
    conn = connection()

    print(conn)

    cursor = conn.cursor()

    cursor.execute("SELECT * FROM admin")
    row = cursor.fetchone()
    if row is None:
        informacao = None
    else:     
        informacao = {
            "nome": row[0],
            "crm": row[1],
            "sobre": row[2],
            "imagebase64": row[3],
            "telefone": row[4],
            "mensagem": row[5],
            "email": row[6],
        }

    cursor.execute("SELECT * FROM formacaoadmin")
    rows = cursor.fetchall()
    formacao = []
    for row in rows:
        formacao.append({
            "id": row[0],
            "codigo": row[1],
            "descricao": row[2],
            "instituicao": row[3],
        })

    cursor.close()
    conn.close()
    return jsonify({"informacao": informacao, "formacao": formacao}), 200

@app.route("/admin", methods=["POST"]) # Alterar informações admin - OK
def update_admin():
    conn = connection()
    cursor = conn.cursor()

    if not request.json:
        cursor.close()
        conn.close()
        return jsonify({"message": "No data provided"}), 400

    informacoes = request.json.get("informacoes")
    formacao = request.json.get("formacao")

    numcontato = ""
    if informacoes['telefone'] != "":
        numcontato = informacoes['telefone'].replace(" ","").replace("-","").replace("(","").replace(")","")
        if len(numcontato) != 14:
            cursor.close()
            conn.close()
            return jsonify({"message": "O número deve estar no formato '+55 92 9(numero)'"}), 400


    query = "delete from admin"
    cursor.execute(query)
    conn.commit()

    query = f"insert into admin (nome, crm, sobre, image_base64, whats, whatsmsg, email) values ('{informacoes['nome']}', '{informacoes['crm']}', '{informacoes['sobre']}', '{informacoes['imagebase64']}', '{numcontato}', '{informacoes['mensagem']}', '{informacoes['email']}')"
    cursor.execute(query)
    conn.commit()

    query = "delete from formacaoadmin"
    cursor.execute(query)
    conn.commit()

    cont = 0
    for x in formacao:
        query = f"insert into formacaoadmin (id, rqe, especialidade, instituto) values ('{cont}', '{x['codigo']}', '{x['descricao']}', '{x['instituicao']}')"
        cursor.execute(query)
        conn.commit()
        cont += 1

    cursor.close()
    conn.close()
    return jsonify({"message": "Admin updated successfully"}), 200

################################################

@app.route("/infatojuvenil", methods=["GET"]) # Get informações InfantoJuvenil - OK
def get_infatojuvenil():
    conn = connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM infatojuvenilTitle limit 1")
    Titleinfatojuvenil = cursor.fetchone()

    infatojuvenil = []
    cursor.execute("SELECT descricao FROM infatojuvenil")
    for x in cursor.fetchall():
        infatojuvenil.append(x[0])

    cursor.close()
    conn.close()
    return jsonify({"Titleinfatojuvenil": Titleinfatojuvenil, "infatojuvenil": infatojuvenil}), 200

@app.route("/infatojuvenil", methods=["POST"]) # Alterar Informações InfantoJuvenil - OK
def update_infatojuvenil():
    conn = connection()
    cursor = conn.cursor()

    if not request.json:
        cursor.close()
        conn.close()
        return jsonify({"message": "No data provided"}), 400

    Titulo = request.json.get("infantojuvenilTitulo")
    listDescricao = request.json.get("infantojuvenilDescricao")

    query = "delete from infatojuvenilTitle;"
    cursor.execute(query)
    conn.commit()

    query = "delete from infatojuvenil;"
    cursor.execute(query)
    conn.commit()

    query = f"insert into infatojuvenilTitle (titulo) values ('{str(Titulo)}')"
    cursor.execute(query)
    conn.commit()

    cont = 0
    for x in listDescricao:
        query = f"insert into infatojuvenil (id, descricao) values ({cont}, '{x}')"
        cursor.execute(query)
        conn.commit()
        cont += 1

    cursor.close()
    conn.close()
    return jsonify({"message": "Infatojuvenil updated successfully"}), 200

################################################

@app.route("/multidisciplinar", methods=["POST"]) # Cadastrar Funcionário
def insert_multidisciplinar():
    conn = connection()
    cursor = conn.cursor()

    if not request.json:
        cursor.close()
        conn.close()
        return jsonify({"message": "No data provided"}), 400

    dados = request.json.get("funcionario")

    if not dados:
        cursor.close()
        conn.close()
        return jsonify({"message": "No data provided"}), 400
    
    if dados['nome'] == "" :
        cursor.close()
        conn.close()
        return jsonify({"message": "Informe o nome"}), 400
    elif dados['id_especialidade'] == "":
        cursor.close()
        conn.close()
        return jsonify({"message": "Informe o CRP/CFP"}), 400
    elif dados['especialidade'] == "":
        cursor.close()
        conn.close()
        return jsonify({"message": "Informe a descrição da especialidade"}), 400
    elif dados['tempo_experiencia'] == "":
        cursor.close()
        conn.close()
        return jsonify({"message": "Informe o tempo de experiência"}), 400

    numcontato = ""
    if dados['telefone'] != "":
        numcontato = dados['telefone'].replace(" ","").replace("-","").replace("(","").replace(")","")
        if len(numcontato) != 14:
            cursor.close()
            conn.close()
            return jsonify({"message": "O número deve estar no formato '+55 92 9(numero)'"}), 400

    query = "select id from multidisciplinares order by id desc limit 1"
    cursor.execute(query)
    id = cursor.fetchone()
    if id == None:
        id = 0
    else:
        id = id[0] + 1

    query = f"""
        insert into multidisciplinares (id, nome, crm, id_especialidade, especialidade, tempexperiencia, tipoconsulta, publicoatendido, formaatendimento, imagebase64, telefone, textmsg) 
        values ('{id}', '{dados['nome']}', '{dados['crm']}', '{dados['id_especialidade']}', '{dados['especialidade']}', '{dados['tempo_experiencia']}', '{dados['tipo_consulta']}', '{dados['publico_atendido']}', '{dados['forma_atendimento']}', '{dados['imagebase64']}', '{numcontato}', '{dados['mensagem']}')
    """
    cursor.execute(query)
    conn.commit()
    
    cursor.close()
    conn.close()
    return jsonify({"message": "Funcionário cadastrado com sucesso"}), 200

@app.route("/multidisciplinar", methods=["GET"]) # Listar Funcionários
def select_multidisciplinar():
    conn = connection()

    cursor = conn.cursor()

    cursor.execute("SELECT * FROM multidisciplinares order by nome")
    rows = cursor.fetchall()
    funcionarios = []
    for row in rows:
        funcionarios.append({
            "id": row[0],
            "nome": row[1],
            "crm": row[2],
            "id_especialidade": row[3],
            "especialidade": row[4],
            "tempo_experiencia": row[5],
            "tipo_consulta": row[6],
            "publico_atendido": row[7],
            "forma_atendimento": row[8],
            "imagebase64": row[9],
            "telefone": row[10],
            "textmsg": row[11],
        })

    newList = []
    query = "select descricao from especialidades order by id"
    cursor.execute(query)
    rows = cursor.fetchall()
    for x in rows:
        especialidade = x[0]
        for y in funcionarios:
            if especialidade in y['especialidade']:
                if y not in newList:
                    newList.append(y)
            
    funcionarios = newList
    

    cursor.close()
    conn.close()
    return jsonify({"funcionarios": funcionarios}), 200

@app.route("/multidisciplinar", methods=["PUT"]) # Atualizar Funcionário
def update_multidisciplinar():
    conn = connection()
    cursor = conn.cursor()

    if not request.json:
        cursor.close()
        conn.close()
        return jsonify({"message": "No data provided"}), 400

    dados = request.json.get("funcionario")

    if dados['id'] == None:
        cursor.close()
        conn.close()
        return jsonify({"message": "No id provided"}), 400
    
    numcontato = ""
    if dados['telefone'] != "":
        numcontato = dados['telefone'].replace(" ","").replace("-","").replace("(","").replace(")","")
        if len(numcontato) != 14:
            cursor.close()
            conn.close()
            return jsonify({"message": "O número deve estar no formato '+55 92 9(numero)'"}), 400

    query = f"""
        update multidisciplinares set
        nome = '{dados['nome']}',
        crm = '{dados['crm']}',
        id_especialidade = '{dados['id_especialidade']}',
        especialidade = '{dados['especialidade']}',
        tempexperiencia = '{dados['tempo_experiencia']}',
        tipoconsulta = '{dados['tipo_consulta']}',
        publicoatendido = '{dados['publico_atendido']}',
        formaatendimento = '{dados['forma_atendimento']}',
        imagebase64 = '{dados['imagebase64']}',
        telefone = '{numcontato}',
        textmsg = '{dados['mensagem']}'
        where id = {dados['id']}
    """
    cursor.execute(query)
    conn.commit()

    cursor.close()
    conn.close()
    return jsonify({"message": "Funcionario atualizado com sucesso"}), 200

@app.route("/multidisciplinar/<int:id>", methods=["DELETE"])  # Deletar Funcionário
def delete_multidisciplinar(id):
    conn = connection()
    cursor = conn.cursor()

    if id is None:
        cursor.close()
        conn.close()
        return jsonify({"message": "No id provided"}), 400

    query = f"DELETE FROM multidisciplinares WHERE id = '{id}'"
    cursor.execute(query)
    conn.commit()

    cursor.close()
    conn.close()
    return jsonify({"message": "Funcionario deletado com sucesso"}), 200

@app.route("/multidisciplinar/especialidades", methods=["GET"]) # Listar Especialidades
def select_multidisciplinar_especialidades():
    conn = connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM especialidades order by id")
    rows = cursor.fetchall()
    list = []
    for row in rows:
        list.append({
            "id": row[0],
            "especialidade": row[1],
        })

    cursor.close()
    conn.close()
    return jsonify({"especialidades": list}), 200

@app.route("/multidisciplinar/especialidades", methods=["POST"]) # Atualizar
def insert_multidisciplinar_especialidade():
    conn = connection()
    cursor = conn.cursor()

    if not request.json:
        cursor.close()
        conn.close()
        return jsonify({"message": "No data provided"}), 400

    dados = request.json.get("especialidades")
    
    query = "delete from especialidades;"
    cursor.execute(query)
    conn.commit()   

    if dados:
        for x in dados:
            id, especialidade = x['id'], x['especialidade']
            
            query = f"insert into especialidades (id, descricao) values ({id}, '{especialidade}')"
            cursor.execute(query)
            conn.commit()
    
    cursor.close()
    conn.close()
    return jsonify({"message": "Especialidade cadastrada com sucesso"}), 200

@app.route("/multidisciplinar/especialidades/<int:id>", methods=["DELETE"])  # Deletar Especialidade
def delete_multidisciplinar_especialidade(id):
    conn = connection()
    cursor = conn.cursor()

    if id is None:
        cursor.close()
        conn.close()
        return jsonify({"message": "No id provided"}), 400

    query = f"DELETE FROM especialidade WHERE id = '{id}'"
    cursor.execute(query)
    conn.commit()

    # Adjust IDs after deletion
    cursor.execute("SELECT id FROM especialidade ORDER BY id")
    rows = cursor.fetchall()

    for index, row in enumerate(rows):
        new_id = index + 1
        if row[0] != new_id:
            cursor.execute(f"UPDATE especialidade SET id = {new_id} WHERE id = {row[0]}")
            conn.commit()


    cursor.close()
    conn.close()
    return jsonify({"message": "Funcionario deletado com sucesso"}), 200


################################################

@app.route("/depoimentos", methods=["POST"]) # Alterar Depoimentos
def update_depoimentos():
    conn = connection()
    cursor = conn.cursor()

    if not request.json:
        cursor.close()
        conn.close()
        return jsonify({"message": "No data provided"}), 400

    list = request.json.get("depoimentos")

    query = "delete from depoimentos"
    cursor.execute(query)
    conn.commit()

    cont = 0
    for x in list:
        query = f"insert into depoimentos (id, nome, descricao) values ({int(cont)}, '{x['autor']}', '{x['depoimento']}')"
        cursor.execute(query)
        conn.commit()
        cont += 1

    cursor.close()
    conn.close()
    return jsonify({"message": "Depoimentos updated successfully"}), 200

@app.route("/depoimentos", methods=["GET"]) # Get informações Depoimentos
def get_depoimentos():
    conn = connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM depoimentos")
    depoimentos = cursor.fetchall()

    cursor.close()
    conn.close()
    return jsonify({"depoimentos": depoimentos}), 200

################################################

@app.route("/localizacoes", methods=["POST"]) # Alterar localizacoes
def update_localizacoes():
    conn = connection()
    cursor = conn.cursor()

    if not request.json:
        cursor.close()
        conn.close()
        return jsonify({"message": "No data provided"}), 400

    list = request.json.get("localizacoes")

    query = "delete from localizacoes"
    cursor.execute(query)
    conn.commit()

    cont = 0
    for x in list:
        if (x['Nome'] != '' and x['Endereco'] != '' and x['Telefone'] != '' and x['Email'] != '' and x['LinkMaps'] != ''):
            cont += 1
    
    if cont == 0:
        cursor.close()
        conn.close()
        return jsonify({"message": "Preencha TODOS os campos de pelo menos uma localização"}), 404


    for x in list:
        if (x['Nome'] != '' and x['Endereco'] != '' and x['Telefone'] != '' and x['Email'] != '' and x['LinkMaps'] != ''):
            maps = x['LinkMaps']

            if "<iframe" in x['LinkMaps'] and "https://" in x['LinkMaps']:
                link = x['LinkMaps'].split("https://")[1]
                link = link.split("width")[0]
                url = "https://" + link
                url = url.strip()
                url = url[:len(url)-1]
                maps = url

            query = f"insert into localizacoes (nome, endereco, telefone, email, link_maps) values ('{x['Nome']}', '{x['Endereco']}', '{x['Telefone']}', '{x['Email']}', '{maps}')"
            cursor.execute(query)
            conn.commit()

    cursor.close()
    conn.close()
    return jsonify({"message": "Localizacoes updated successfully"}), 200

@app.route("/localizacoes", methods=["GET"]) # Get localizacoes
def get_localizacoes():
    conn = connection()
    cursor = conn.cursor()

    locs = []
    cursor.execute("SELECT * FROM localizacoes")
    rows = cursor.fetchall()
    
    for row in rows:
        id, Nome, Endereco, Telefone, Email, Maps = row
        locs.append({
            "Id": id,
            "Nome": Nome,
            "Endereco": Endereco,
            "Telefone": Telefone,
            "Email": Email,
            "Maps": Maps,
        })

    cursor.close()
    conn.close()
    return jsonify({"localizacoes": locs}), 200

################################################

@app.route("/diagnostico", methods=["POST"]) # Criar Diagnostico
def create_diagnostico():
    conn = connection()
    cursor = conn.cursor()

    if not request.json:
        cursor.close()
        conn.close()
        return jsonify({"message": "No data provided"}), 400

    ListaSites = request.json.get("ListaSites")
    
    cursor.execute("delete from diagnosticos")
    conn.commit()

    for x in ListaSites:
        query = f"insert into diagnosticos (id, nome, url) values ('{x['id']}','{x['descricao']}', '{x['link']}')"
        cursor.execute(query)
        conn.commit()

    cursor.close()
    conn.close()
    return jsonify({"message": "Diagnostico updated successfully"}), 200

@app.route("/diagnostico", methods=["GET"]) # Read informações Diagnostico
def get_diagnostico():
    conn = connection()
    cursor = conn.cursor()

    listaSites = []
    cursor.execute("SELECT * FROM diagnosticos")
    rows = cursor.fetchall()

    for row in rows:
        listaSites.append({
            "id": row[0],
            "descricao": row[1],
            "link": row[2],
        })

    cursor.close()
    conn.close()
    return jsonify({"listaSites": listaSites}), 200

################################################

@app.route("/website", methods=["GET"]) # Read informações Diagnostico
def get_website():
    conn = connection()
    if conn is None:
        return jsonify({"message": "Erro de conexão com o banco de dados"}), 500
    
    cursor = conn.cursor()

    query_1 = "select nome, crm, sobre, image_base64, whats, whatsmsg, email from admin limit 1"
    cursor.execute(query_1)
    informacoes_ADM = cursor.fetchone()
    
    query_2 = "select rqe, especialidade, instituto from formacaoadmin"
    cursor.execute(query_2)
    formacoes_ADM = cursor.fetchall()

    Adm = {
        "nome": informacoes_ADM[0],
        "especialidadesText": informacoes_ADM[1],
        "sobre": informacoes_ADM[2],
        "image_base64": informacoes_ADM[3],
        "whats": informacoes_ADM[4],
        "whatsmsg": informacoes_ADM[5],
        "email": informacoes_ADM[6],
        "formacoes": formacoes_ADM
    }

    query_3 = "select * from infatojuvenilTitle limit 1"
    cursor.execute(query_3)
    Titleinfatojuvenil = cursor.fetchone()

    query_4 = "select descricao from infatojuvenil"
    cursor.execute(query_4)
    infatojuvenil = cursor.fetchall()
    
    if Titleinfatojuvenil and infatojuvenil:
        Infanto_juvenil = {
            "Title": Titleinfatojuvenil[0],
            "Topicos": infatojuvenil
        }
    else:
        Infanto_juvenil = {}
    

    Testes_Diagnosticos = []
    query_5 = "select nome, url from diagnosticos"
    cursor.execute(query_5)
    for x in cursor.fetchall():
        Testes_Diagnosticos.append({
            "descricao": x[0],
            "url": x[1]
        })

    Depoimentos = []
    query_6 = "select * from depoimentos where nome <>'' and descricao <>''"
    cursor.execute(query_6)
    for x in cursor.fetchall():
        Depoimentos.append({
            "autor": x[1],
            "depoimento": x[2]
        })

    
    cursor.execute("SELECT * FROM multidisciplinares order by nome")
    rows = cursor.fetchall()
    funcionarios = []
    if len(rows) > 0:
        for row in rows:
            funcionarios.append({
                "id": row[0],
                "nome": row[1],
                "crp": row[2],
                "id_especialidade": row[3],
                "especialidade": row[4],
                "tempexperiencia": row[5],
                "tipoconsulta": row[6],
                "publicoatendido": row[7],
                "formaatendimento": row[8],
                "imagebase64": row[9],
                "telefone": row[10],
                "textmsg": row[11],
            })

        newList = []
        query = "select descricao from especialidades order by id"
        cursor.execute(query)
        rows = cursor.fetchall()
        for x in rows:
            especialidade = x[0]
            for y in funcionarios:
                if especialidade in y['especialidade']:
                    if y not in newList:
                        newList.append(y)
                
        funcionarios = newList

    query = "select id, descricao from especialidades order by id"
    cursor.execute(query)
    rows = cursor.fetchall()
    lista_especialidades = []
    if len(rows) > 0:
        for row in rows:
            lista_especialidades.append({
                "id": row[0],
                "descricao": row[1]
            })


    query_7 = "select id, nome, endereco, telefone, email, link_maps from localizacoes"
    cursor.execute(query_7)
    rows = cursor.fetchall()
    localizacoes = []
    for row in rows:
        id, nome, endereco, telefone, email, maps = row
        localizacoes.append({
            "id": id,
            "nome": nome,
            "endereco": endereco,
            "telefone": telefone,
            "email": email,
            "maps": maps,
        })
    
    cursor.close()
    conn.close()
    return jsonify({"Adm": Adm, "Infanto_juvenil": Infanto_juvenil, "Testes_Diagnosticos": Testes_Diagnosticos,"Depoimentos":Depoimentos, "list_funcionarios": funcionarios, "localizacoes": localizacoes, "lista_especialidades": lista_especialidades}), 200


if __name__ == "__main__":
    create_table()
    app.run(debug=True, port=5000, host="127.0.0.1")

