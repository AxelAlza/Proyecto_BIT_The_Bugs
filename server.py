from flask import Flask, render_template

app = Flask(__name__)


@app.route('/')
def Inicio():
    return render_template("/Inicio.html")


@app.route('/Mantenimiento/Clientes')
def MantClientes():
    return render_template("/MantClientes.html")


@app.route('/Mantenimiento/Empleados', methods=['GET'])
def MantEmpleados():
    return render_template("/MantEmpleados.html")


if __name__ == "__main__":
    app.jinja_env.auto_reload = True
    app.jinja_env.cache = {}
    app.jinja_env.auto_reload = True
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.run(debug=True)
