import sqlite3
from prueba import key
from datetime import date
from flask import Flask, render_template, request, jsonify
from werkzeug.utils import redirect
import googlemaps

env_var = key()
dbconnect = sqlite3.connect('The_Bugs.db', check_same_thread=False)
database = dbconnect.cursor()
database2 = dbconnect.cursor()
keyscli = ['"clici":', '"clinom":', '"cliape":', '"cliage":', '"clihid":']
keysemp = ['"empci":', '"empnom":', '"empape":', '"empage":', '"emptel":', '"empdir":', '"empmail":', '"emphde":',
           '"emphha":']
skeysemp = ['"empci":', '"empnom":', '"empape":', '"empage":', '"emptel":', '"empbarrio":', '"empcalle":', '"empnro":',
            '"empmail":', '"emphde":', '"emphha":']
keyshos = ['"hosid":', '"hosdir":', '"hosnom":']
keystur = ['"turfch":', '"clici":', '"clihid":', '"empci":', '"turhde":', '"turhha":']
keysminemp = ['"empci":', '"empbarrio":', '"empcalle":', '"empnro":', '"emptel":']
speckeys = ['"empci":', '"empbarrio":', '"empcalle":', '"empnro":', '"emptel":', '"distext":', '"distvalue":',
            '"duration":']


def crearturnos():
    database.execute("select CliCi from Cliente")
    lista = database.fetchall()
    fechadehoy = date.today()
    valores = []
    for tupla in lista:
        for columna in tupla:
            valores.append((columna, fechadehoy))
    database.executemany("INSERT or IGNORE INTO Turno (CliCi,TurFch) Values(?,?) ", valores)
    dbconnect.commit()


def htmlfy(query, keys):
    database.execute(query)
    lista = database.fetchall()
    itemj = ''
    i = 0
    for num, tupla in enumerate(lista):
        agr2 = ','
        json = "{"
        agr = ','
        for columna in tupla:
            if i == len(keys):
                i = 0
            if i == len(keys) - 1:
                agr = ''
            column = keys[i] + '"' + str(columna) + '"' + agr
            json = json + column
            i = i + 1
        if num == len(lista) - 1:
            agr2 = ''
        itemj = itemj + json + '}' + agr2 + "\n"
    itemj = "[" + itemj + "]"
    return itemj


app = Flask(__name__)


@app.route('/')
def Inicio():
    return render_template("/inicio.html")


@app.route('/getoptemp')
def getoptemp():
    destino = request.args.get('Destino')
    emphde = request.args.get('EmpHde')
    emphha = request.args.get('EmpHha')
    database.execute("SELECT (EmpCi || ' - '|| EmpNom || ' - ' ||EmpApe) As Emp , EmpBarrio, EmpCalle, Empnro, "
                     "EmpTel FROM Empleado ORDER BY ABS(time(" + "'" + emphde + "'" + ") - time (EmpHde) and time(" +
                     "'" + emphha + "'" + ")-time(EmpHha))limit 20"
                     )
    lista = database.fetchall()
    gmap = googlemaps.Client(key=key())
    itemj = ''
    i = 0
    newlist = []
    for tupla in lista:
        distancia = \
            gmap.distance_matrix(tupla[1] + " " + tupla[2] + " " + tupla[3], destino, mode="transit", language="es-ES",
                                 units="metric", transit_mode="bus")['rows'][0]['elements'][0]
        leest = list(tupla)
        list.append(leest, distancia["distance"]["text"])
        list.append(leest, distancia["distance"]["value"])
        list.append(leest, distancia["duration"]["text"])
        emple = tuple(leest)
        list.append(newlist, emple)
    newlist = sorted(newlist, key=lambda x: x[6])
    for num, tupla2 in enumerate(newlist):
        agr2 = ','
        json = "{"
        agr = ','
        for columna in tupla2:
            if i == len(speckeys):
                i = 0
            if i == len(speckeys) - 1:
                agr = ''
            column = speckeys[i] + '"' + str(columna) + '"' + agr
            json = json + column
            i = i + 1
        if num == len(newlist) - 1:
            agr2 = ''
        itemj = itemj + json + '}' + agr2 + "\n"
    itemj = "[" + itemj + "]"
    return itemj


@app.route('/Mantenimiento/getpagestur', methods=['GET'])
def getpagestur():
    htmlpages = htmlfy("Select TurFch, (Turno.CliCi|| ' - ' ||CliNom|| ' - '|| CliApe) As Cliente, HosNom, "
                       "(Turno.EmpCi || '   - '||EmpNom|| ' - "
                       "'||EmpApe) As Empleado ,TurHde , TurHha from Turno inner join Cliente on Cliente.Clici = "
                       "Turno.CliCi inner join Hospital on Cliente.CliHid = Hospital.HosId left join Empleado on "
                       "Turno.EmpCi = Empleado.EmpCi", keystur)
    return htmlpages


@app.route('/Mantenimiento/getpagesemp', methods=['GET'])
def getpagesemp():
    htmlpages = htmlfy('Select EmpCi,EmpNom,EmpApe,EmpAge,EmpTel,(EmpBarrio || " "|| EmpCalle|| "  " || Empnro) As '
                       'Dirección,EmpMail,EmpHde,EmpHha from Empleado', keysemp)
    return htmlpages


@app.route('/Mantenimiento/getpagescli', methods=['GET'])
def getpagescli():
    htmlpages = htmlfy("Select clici,clinom,cliape,cliage,hosnom From Cliente inner join hospital on cliente.clihid = "
                       "hospital.hosid", keyscli)
    return htmlpages


@app.route('/Mantenimiento/gethospitales', methods=['GET'])
def gethospitales():
    htmlpages = htmlfy("Select * From Hospital", keyshos)
    return htmlpages


@app.route('/Mantenimiento/Clientes', methods=['GET'])
def MantClientes():
    return render_template("/MantClientes.html")


@app.route('/Mantenimiento/Empleados')
def MantEmpleados():
    return render_template("/MantEmpleados.html")


@app.route('/EliminarEmpleado', methods=['POST'])
def EliminarEmpleado():
    cedula = request.args.get('cedula')
    try:
        database.execute('Delete from empleado where EmpCi = ?', (cedula,))
        dbconnect.commit()
        return jsonify({'reply': "success"})
    except sqlite3.Error:
        return jsonify({'reply': "fail"})


@app.route('/EliminarCliente', methods=['POST'])
def EliminarCliente():
    cedula = request.args.get('cedula')
    try:
        database.execute('Delete from Cliente where CliCi = ?', (cedula,))
        dbconnect.commit()
        return jsonify({'reply': "success"})
    except sqlite3.Error:
        return jsonify({'reply': "fail"})


@app.route('/CedulaDisponible', methods=['GET', 'POST'])
def CedulaDisponibleEmp():
    cedula = request.args.get('cedula')
    modo = request.args.get('modo')
    if modo == "emp":
        database.execute('Select EmpCi  from Empleado where EmpCi = ?', (cedula,))
    else:
        database.execute('Select CliCi  from Cliente where CliCi = ?', (cedula,))
    ci = database.fetchone()

    if ci is None:
        return jsonify({'reply': "success"})
    else:
        return jsonify({'reply': "fail"})


@app.route('/getdata', methods=['GET', 'POST'])
def GetDataEmp():
    cedula = request.args.get('ced')
    modo = request.args.get('modo')
    fch = request.args.get('fch')
    if modo == "emp":
        json = htmlfy("select * from Empleado where EmpCi =" + cedula, skeysemp)
    elif modo == "cli":
        json = htmlfy("select * from Cliente where CliCi =" + cedula, keyscli)
    else:
        json = htmlfy("Select TurFch, (Turno.CliCi|| ' - ' ||CliNom|| ' - '|| CliApe) As Cliente, HosNom, "
                      "(Turno.EmpCi || ' - '||EmpNom|| ' - "
                      "'||EmpApe) As Empleado ,TurHde , TurHha from Turno inner join Cliente on Cliente.Clici = "
                      "Turno.CliCi inner join Hospital on Cliente.CliHid = Hospital.HosId left join Empleado on "
                      "Turno.EmpCi = Empleado.EmpCi where Turno.CliCi =" + cedula + " and TurFch =" + "'" + fch + "'",
                      keystur)

    return json


@app.route('/Mantenimiento/Empleados/AgregarModificarEmpleado', methods=['GET', 'POST'])
def AgregarModificarEmpleado():
    mode = request.args.get('mode')
    cedula = request.args.get('cedula')
    if request.method == "POST":
        EmpCi = request.form['EmpCi']
        EmpNom = request.form['EmpNom'].strip()
        EmpApe = request.form['EmpApe'].strip()
        EmpAge = request.form['EmpAge']
        EmpTel = request.form['EmpTel']
        EmpBarrio = request.form['EmpBarrio'].strip()
        EmpCalle = request.form['EmpCalle'].strip()
        EmpNro = request.form['EmpNro'].strip()
        EmpMail = request.form['EmpMail'].strip()
        EmpHde = request.form['EmpHde']
        EmpHha = request.form['EmpHha']
        if mode == "INS":
            database.execute(
                "INSERT INTO Empleado VALUES (? , ? , ? , ? , ? , ? , ? , ? ,? , ?, ?)",
                (EmpCi, EmpNom, EmpApe, EmpAge, EmpTel
                 , EmpBarrio, EmpCalle, EmpNro, EmpMail,
                 EmpHde, EmpHha))
            dbconnect.commit()
            return redirect("/Mantenimiento/Empleados")
        else:
            database.execute(
                "UPDATE Empleado SET Empci = ?,EmpNom = ?, EmpApe = ? ,EmpAge =?, EmpTel = ? , EmpBarrio = ?,"
                "EmpCalle =?,EmpNro = ? ,EmpMail = ?, "
                "EmpHde = ? , EmpHha = ? where EmpCi = ?",
                (EmpCi, EmpNom, EmpApe, EmpAge, EmpTel, EmpBarrio, EmpCalle, EmpNro, EmpMail, EmpHde, EmpHha, cedula))
            dbconnect.commit()
            return redirect("/Mantenimiento/Empleados")
    return render_template("/AgregarModificarEmpleado.html")


@app.route('/getapikey')
def getkey():
    return env_var


@app.route('/gethos')
def gethos():
    cedula = request.args.get('ced')
    database2.execute("Select CliHid from cliente where CliCi = ?", (cedula,))
    idhos = database2.fetchone()
    database2.execute("Select HosDir from Hospital where HosId = ?", (idhos[0],))
    destino = database2.fetchone()
    return jsonify(destino)


@app.route('/Mantenimiento/Empleados/AgregarModificarCliente', methods=['GET', 'POST'])
def AgregarModificarCliente():
    mode = request.args.get('mode')
    cedula = request.args.get('cedula')
    if request.method == "POST":
        CliCi = request.form['CliCi']
        CliNom = request.form['CliNom'].strip()
        CliApe = request.form['CliApe'].strip()
        CliAge = request.form['CliAge']
        CliHid = request.form['CliHid']
        if mode == "INS":
            database.execute("INSERT INTO Cliente VALUES (? , ? , ? , ? , ?)", (CliCi, CliNom, CliApe, CliAge, CliHid))
            dbconnect.commit()
            return redirect("/Mantenimiento/Clientes")
        else:
            database.execute(
                "UPDATE Cliente SET CliCi = ? ,CliNom = ?, CliApe = ? ,CliAge =?, CliHid = ? where CliCi = ?",
                (CliCi, CliNom, CliApe, CliAge, CliHid, cedula))
            dbconnect.commit()
            return redirect("/Mantenimiento/Clientes")
    return render_template("/AgregarModificarCliente.html")


@app.route('/Asignar', methods=['GET', 'POST'])
def Asignar():
    if request.method == "POST":
        TurFch = request.form['TurFch'].strip()
        CliCi = request.form['CliCi'][0:8]
        EmpCi = request.form['EmpCi'].strip()
        TurHha = request.form['lmao2'].strip()
        TurHde = request.form['lmao'].strip()
        print(TurFch, CliCi, EmpCi, TurHha, TurHde)
        database.execute("Update Turno set EmpCi =?,TurHde = ?,TurHha = ? where CliCi = ? and TurFch = ?",
                         (EmpCi, TurHde, TurHha, CliCi, TurFch))
        dbconnect.commit()
        return redirect("/MantTurnos")
    return render_template("Asignar.html")


@app.route('/MantTurnos', methods=['GET', 'POST'])
def MantTurnos():
    return render_template("MantTurnos.html")


if __name__ == "__main__":
    crearturnos()
    app.jinja_env.cache = {}
    app.jinja_env.auto_reload = True
    app.config['autocomplete'] = 'off'
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.run(debug=True)
