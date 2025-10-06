from flask import Flask, request, render_template, flash, redirect, url_for, session
from services.manipular_database import criar_usuario, verificar_login
from utils.validacoes import (
    validar_email,
    validar_senha,
    validar_username,
    validar_telefone,
)
from utils.manipular_forms import obter_dados_login, obter_dados_cadastro

app = Flask(__name__)
app.secret_key = "d2ccd1731dc1cca262d6c889e3352a921f973db9698cc4ba"


# Rota principal: Tela de login
# Rota principal: Tela de login
@app.route("/", methods=["GET", "POST"])
def tela_login():
    if request.method == "POST":
        dados_login = obter_dados_login()
        usuario_form, senha_form = dados_login

        dados_usuario_bd = verificar_login(usuario_form, senha_form)

        if dados_usuario_bd:
            # SUCESSO NO LOGIN
            id_usuario_bd, nome_bd, _ = dados_usuario_bd

            session.clear()
            session["user_id"] = id_usuario_bd
            session["username"] = nome_bd

            return redirect(url_for("dashboard"))
        else:
            # FALHA NO LOGIN
            flash("Usuário ou senha incorretos.")

    # Esta linha é executada para:
    # 1. Requisições GET (Acesso inicial à página)
    # 2. Falhas no POST (Para mostrar a mensagem de flash)
    return render_template("index.html")


@app.route("/cadastro", methods=["GET", "POST"])
def tela_cadastro():
    if request.method == "GET":
        return render_template("cadastro.html")

    elif request.method == "POST":
        # Processa o formulário de cadastro
        erro = False
        user = obter_dados_cadastro()

        c_usuario, c_email, c_telefone, c_senha = user

        if erro:
            dados_para_manter = (c_usuario, c_email, c_telefone)
            return render_template("cadastro.html", user_data=dados_para_manter)
        else:
            criar_usuario(user)
            flash("Conta criada com sucesso! Faça login abaixo.", "sucesso")
            return redirect(url_for("tela_login"))

    # Este retorno é redundante se você tiver um GET ou POST que cobre todos os caminhos
    return redirect(url_for("tela_login"))


@app.route("/unauthorized")
def unauthorized():
    return render_template("unauthorized.html")


if __name__ == "__main__":
    app.run(debug=True)  # debug=True para recarregamento automático
