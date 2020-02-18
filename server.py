from flask import Flask, render_template

app = Flask(__name__)


@app.route('/')
def Inicio():
    return render_template("Inicio.html")


@app.route('/Mantenimiento/Empleados')
def MantEmpleados():
    return render_template("MantEmpleados.html")


if __name__ == "__main__":
    app.run()
