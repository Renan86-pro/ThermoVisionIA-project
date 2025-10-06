from flask import request


def obter_dados_cadastro():
    c_usuario = request.form.get("c_usuario").strip()
    c_email = request.form.get("c_usuario").strip()
    c_telefone = request.form.get("c_telefone").strip()
    c_senha = request.form.get("c_senha").strip()

    return [c_usuario, c_email, c_telefone, c_senha]


def obter_dados_login():
    usuario = request.form.get("usuario").strip()
    senha = request.form.get("senha").strip()

    return [usuario, senha]
