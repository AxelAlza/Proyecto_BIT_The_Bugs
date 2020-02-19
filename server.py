from flask import Flask, render_template

app = Flask(__name__,
            static_url_path='',
            static_folder='/static',
            template_folder='/templates')


@app.route('/')
def Inicio():
    return render_template("Inicio.html")


@app.route('/Mantenimiento/Clientes')
def MantClientes():
    return render_template("MantClientes.html")


@app.route('/Mantenimiento/Empleados')
def MantEmpleados():
    return render_template("MantEmpleados.html")


if __name__ == "__main__":
    app.run()
