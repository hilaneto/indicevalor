import os
from datetime import datetime
from dotenv import load_dotenv
from flask import Flask

from routes.home import home_bp
from routes.auth import auth_bp
from routes.upload import upload_bp
from routes.api_cpf import cpf_bp
from routes.api_cnpj import cnpj_bp
from routes.api_usuario import api_usuario_bp
from routes.contato import contato_bp
from routes.downloads import download_bp

load_dotenv()

app = Flask(__name__)

app.secret_key = os.environ["SECRET_KEY"]
app.config["MAX_CONTENT_LENGTH"] = 50 * 1024 * 1024

app.register_blueprint(home_bp)
app.register_blueprint(auth_bp)
app.register_blueprint(api_usuario_bp, url_prefix="/cdusuario")
app.register_blueprint(contato_bp)
app.register_blueprint(upload_bp)
app.register_blueprint(download_bp)
app.register_blueprint(cpf_bp, url_prefix="/cpf")
app.register_blueprint(cnpj_bp, url_prefix="/cnpj")

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5154, debug=True, use_reloader=False)
