from flask import Flask, request, render_template_string
import re
import html

app = Flask(__name__)

with open("index.html", "r", encoding="utf-8") as f:
    form_html = f.read()

def validar_dados(nome, email, senha):
    nome = html.escape(nome.strip())
    email = html.escape(email.strip())
    senha = html.escape(senha.strip())

    if len(nome) < 3:
        return "Nome deve ter pelo menos 3 caracteres.", nome, email, senha
    
    email_regex = r"^[^@\s]+@[^@\s]+\.[^@\s]+$"
    if not re.match(email_regex, email):
        return "E-mail inválido.", nome, email, senha

    senha_regex = r"^(?=.*[A-Z])(?=.*\d).{8,}$"
    if not re.match(senha_regex, senha):
        return "Senha deve ter pelo menos 8 caracteres, incluindo uma letra maiúscula e um número.", nome, email, senha
    
    return None, nome, email, senha

@app.route("/", methods=["GET"])
def index():
    return form_html

@app.route("/submit", methods=["POST"])
def submit():
    nome = request.form.get("nome", "")
    email = request.form.get("email", "")
    senha = request.form.get("senha", "")

    erro, nome, email, senha = validar_dados(nome, email, senha)
    if erro:
        return f"<h3>Erro: {erro}</h3><a href='/'>Voltar</a>"

    return f"""
    <h3>Cadastro realizado com sucesso!</h3>
    <p><strong>Nome:</strong> {nome}<br>
    <strong>E-mail:</strong> {email}</p>
    """

if __name__ == "__main__":
    app.run(debug=True)
