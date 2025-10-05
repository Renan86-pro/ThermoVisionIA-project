from flask import Flask, request, render_template, redirect, url_for

app = Flask(__name__)


# Rota principal: Tela de login
@app.route("/", methods=["GET", "POST"])
def tela_login():
    # Renderiza a página de login
    return render_template("index.html")


@app.route("/cadastro", methods=["GET", "POST"])
def tela_cadastro():
    if request.method == "GET":
        return render_template("cadastro.html")

    elif request.method == "POST":
        # Processa o formulário de cadastro
        erro = False
        if erro:
            return render_template("cadastro.html")
        else:
            return redirect(url_for("tela_login"))

    return redirect(url_for("tela_login"))


@app.route("/unauthorized")
def unauthorized():
    return render_template("unauthorized.html")


if __name__ == "__main__":
    app.run(debug=True)  # debug=True para recarregamento automático
