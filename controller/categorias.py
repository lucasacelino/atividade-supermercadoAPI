from flask import Blueprint, request, jsonify
import sqlite3

from helpers.database import getConnect
from models.Categoria import Categoria

categorias_bp = Blueprint("categorias", __name__)

def getCategoriaPorId(idCategoria):
    try:
        connection = getConnect()
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM categorias WHERE id = ?", (idCategoria, ))
        resultSet = cursor.fetchone()
    except sqlite3.Error as e:
        return jsonify({'erro': 'Não foi possível conectar ao banco'})
    return resultSet


@categorias_bp.route("/<int:idCategoria>", methods=["GET"])
def dadosCategoriaPorId(idCategoria):
    try:
        connection = getConnect()
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM categorias WHERE id = ?", (idCategoria, ))
        resultSet = cursor.fetchone()
        if(resultSet is not None):
            produto = {'id': resultSet[0], 'nome': resultSet[1]}
        else:
            return jsonify({'mensagem': 'A categoria informada não existe'})
    except sqlite3.Error as e:
        return jsonify({'erro': str(e)})
    return produto


@categorias_bp.route("/", methods=["GET"])
def listarTodasCategorias():
    try:
        connection = getConnect()
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM categorias")
        resultSet = cursor.fetchall()
        categorias = []
        for props in resultSet:
            id = props[0]
            nome = props[1]
            categoria = Categoria(id=id, nome=nome)
            categorias.append(categoria.model_dump())
    except sqlite3.Error as e:
        return jsonify({'error': str(e)}), 500
    return jsonify(categorias), 200


@categorias_bp.route("/", methods=["POST"])
def criarCategoria():
    try:
        categoriaNova = request.json
        connection = getConnect()
        cursor = connection.cursor()
        cursor.execute("INSERT INTO categorias(nome) VALUES(?)", (categoriaNova['nome'], ))
        connection.commit()
        id = cursor.lastrowid
        categoriaNova['id'] = id
    except sqlite3.Error as e:
        return jsonify({'er': str(e)}), 500
    return jsonify(categoriaNova), 201


@categorias_bp.route("/<int:idCategoria>", methods=["DELETE"])
def deletarCategoria(idCategoria):
    try:
        connection = getConnect()
        cursor = connection.cursor()
        resultSet = getCategoriaPorId(idCategoria)
        if(resultSet is None):
            return jsonify({'mensagem': 'Não é possível deletar uma categoria que não existe'})
        cursor.execute("DELETE FROM categorias WHERE id = ?", (idCategoria, ))
        connection.commit()
        return jsonify({'Mensagem': 'categoria deletada com sucesso'})
    except sqlite3.Error as e:
        return jsonify({'erro': str(e)})


@categorias_bp.route("/<int:idCategoria>", methods=["PUT"])
def atualizarProduto(idCategoria):
    try:
        dadosCategoriaAtualizada = request.json
        connection = getConnect()
        cursor = connection.cursor()
        resultSet = getCategoriaPorId(idCategoria)
        if(resultSet is None):
            return jsonify({'mensagem': 'Não é possível atualizar uma categoria que não existe'})
        cursor.execute("UPDATE categorias SET nome = ? WHERE id = ?", (dadosCategoriaAtualizada['nome'], idCategoria))
        connection.commit()
        return jsonify({'mensagem': 'categoria atualizada'})
    except sqlite3.Error as e:
        return jsonify({'erro': str(e)})
