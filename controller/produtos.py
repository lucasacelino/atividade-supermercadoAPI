from flask import Blueprint, request, jsonify
import sqlite3

from helpers.database import getConnect
from models.Produto import Produto

produtos_bp = Blueprint("produtos", __name__)

def getProdutoPorId(idPropriedade):
    try:
        connection = getConnect()
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM produtos WHERE id = ?", (idPropriedade, ))
        resultSet = cursor.fetchone()
    except sqlite3.Error as e:
        return jsonify({'erro': 'Não foi possível conectar ao banco'})
    return resultSet


@produtos_bp.route("/<int:idPropriedade>", methods=["GET"])
def dadosProdutosPorId(idPropriedade):
    try:
        connection = getConnect()
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM produtos WHERE id = ?", (idPropriedade, ))
        resultSet = cursor.fetchone()
        if(resultSet is not None):
            produto = {'id': resultSet[0], 'nome': resultSet[1]}
        else:
            return jsonify({'mensagem': 'O produto não existe'})
    except sqlite3.Error as e:
        return jsonify({'erro': str(e)})
    return produto


@produtos_bp.route("/", methods=["GET"])
def listarTodosProdutos():
    try:
        connection = getConnect()
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM produtos")
        resultSet = cursor.fetchall()
        produtos = []
        for props in resultSet:
            id = props[0]
            nome = props[1]
            produto = Produto(id=id, nome=nome)
            produtos.append(produto.model_dump())
    except sqlite3.Error as e:
        return jsonify({'error': str(e)}), 500
    return jsonify(produtos), 200


@produtos_bp.route("/", methods=["POST"])
def criarProduto():
    try:
        produtoNovo = request.json
        connection = getConnect()
        cursor = connection.cursor()
        cursor.execute("INSERT INTO produtos(nome) VALUES(?)", (produtoNovo['nome'], ))
        connection.commit()
        id = cursor.lastrowid
        produtoNovo['id'] = id
    except sqlite3.Error as e:
        return jsonify({'er': str(e)}), 500
    return jsonify(produtoNovo), 201


@produtos_bp.route("/<int:idPropriedade>", methods=["DELETE"])
def deletarProduto(idPropriedade):
    try:
        connection = getConnect()
        cursor = connection.cursor()
        resultSet = getProdutoPorId(idPropriedade)
        if(resultSet is None):
            return jsonify({'mensagem': 'Não é possível deletar uma propriedade que não existe'})
        cursor.execute("DELETE FROM produtos WHERE id = ?", (idPropriedade, ))
        connection.commit()
        return jsonify({'Mensagem': 'propriedade deletada com sucesso'})
    except sqlite3.Error as e:
        return jsonify({'erro': str(e)})


@produtos_bp.route("/<int:idPropriedade>", methods=["PUT"])
def atualizarProduto(idPropriedade):
    try:
        dadosProdutoUpdate = request.json
        connection = getConnect()
        cursor = connection.cursor()
        resultSet = getProdutoPorId(idPropriedade)
        if(resultSet is None):
            return jsonify({'mensagem': 'Não é possível atualizar uma propriedade que não existe'})
        cursor.execute("UPDATE produtos SET nome = ? WHERE id = ?", (dadosProdutoUpdate['nome'], idPropriedade))
        connection.commit()
        return jsonify({'Propriedade': 'Propriedade atualizada'})
    except sqlite3.Error as e:
        return jsonify({'erro': str(e)})
