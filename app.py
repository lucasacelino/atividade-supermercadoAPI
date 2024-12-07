from helpers.application import app

from controller.produtos import produtos_bp
from controller.categorias import categorias_bp
from controller.setores import setores_bp
from controller.usuarios import usuarios_bp


app.register_blueprint(produtos_bp, url_prefix="/produtos")
app.register_blueprint(categorias_bp, url_prefix="/categorias")
app.register_blueprint(setores_bp, url_prefix="/setores")
app.register_blueprint(usuarios_bp, url_prefix="/usuarios")

if __name__ == "__main__":
    app.run(debug=True)
