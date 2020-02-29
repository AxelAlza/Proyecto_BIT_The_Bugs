import sqlite3

from flask import Flask, render_template, request, jsonify

dbconnect = sqlite3.connect('The_Bugs.db', check_same_thread=False)
database = dbconnect.cursor()


def htmlfy(tabla, keys):
    database.execute("Select * From " + tabla)
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
        itemj = itemj + json + '}' + agr2
    itemj = "[" + itemj + "]"
    return itemj


app = Flask(__name__)


@app.route('/')
def Inicio():
    return render_template("/Inicio.html")


@app.route('/Mantenimiento/getpagesemp', methods=['GET'])
def getpagesemp():
    keys = ['"empci":', '"empnom":', '"empape":', '"empage":', '"emptel":', '"empdir":', '"empmail":', '"emphde":',
            '"emphha":']
    htmlpages = htmlfy("Empleado", keys)
    return htmlpages


@app.route('/Mantenimiento/getpagescli', methods=['GET'])
def getpagescli():
    keys = ['"clici":', '"clinom":', '"cliape":', '"cliage":', '"clitel":', '"clidir":', '"clihid']
    htmlpages = htmlfy("Cliente", keys)
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
    database.execute('Delete from empleado where EmpCi = ?', (cedula,))
    dbconnect.commit()
    return jsonify({'reply': "success"})


@app.route('/EliminarCliente', methods=['POST'])
def EliminarCliente():
    cedula = request.args.get('cedula')
    database.execute('Delete from Cliente where EmpCi = ?', (cedula,))
    dbconnect.commit()
    return jsonify({'reply': "success"})


@app.route('/CedulaDisponibleEmp', methods=['GET', 'POST'])
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


@app.route('/Mantenimiento/Empleados/AgregarEmpleado', methods=['GET', 'POST'])
def AgregarEmpleado():
    if request.method == "POST":
        EmpCi = request.form['EmpCi']
        EmpNom = request.form['EmpNom']
        EmpApe = request.form['EmpApe']
        EmpAge = request.form['EmpAge']
        EmpTel = request.form['EmpTel']
        EmpDir = request.form['EmpDir']
        EmpMail = request.form['EmpMail']
        EmpHde = request.form['EmpHde']
        EmpHha = request.form['EmpHha']
        database.execute(
            "INSERT INTO Empleado VALUES (? , ? , ? , ? , ?, ? ,? ,? , ?)", (EmpCi, EmpNom, EmpApe, EmpAge, EmpTel
                                                                             , EmpDir, EmpMail, EmpHde, EmpHha))
        dbconnect.commit()
    return render_template("/AgregarEmpleado.html")


if __name__ == "__main__":
    app.jinja_env.cache = {}
    app.jinja_env.auto_reload = True
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.run(debug=True)
