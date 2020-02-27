from flask import Flask, render_template, request
import sqlite3

from werkzeug.utils import redirect

dbconnect = sqlite3.connect('The_Bugs.db', check_same_thread=False)
database = dbconnect.cursor()


def htmlfy(tabla):
    html = ""
    database.execute("Select * From " + tabla)
    lista = database.fetchall()
    for tupla in lista:
        tup = "<tr>"
        for columna in tupla:
            td = "<td>" + str(columna) + "</td>"
            tup = tup + td
        tup = tup + "</tr>"
        html = html + tup
    return html


app = Flask(__name__)


@app.route('/')
def Inicio():
    return render_template("/Inicio.html")


@app.route('/Mantenimiento/Clientes')
def MantClientes():
    html = htmlfy("Cliente")
    return render_template("/MantClientes.html", html=html)


@app.route('/Mantenimiento/Empleados')
def MantEmpleados():
    html = htmlfy("Empleado")
    return render_template("/MantEmpleados.html", html=html)


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
        return redirect("/Mantenimiento/Empleados")
    return render_template('/AgregarEmpleado.html')


if __name__ == "__main__":
    app.jinja_env.cache = {}
    app.jinja_env.auto_reload = True
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.run(debug=True)
