from flask import Blueprint, request, jsonify
import sqlite3

from helpers.database import getConnect
from models.Setor import Setor

setores_bp = Blueprint("setores", __name__)

def getSetorPorId(idSetor):
    try:
        connection = getConnect()
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM setores WHERE id = ?", (idSetor, ))
        resultSet = cursor.fetchone()
    except sqlite3.Error as e:
        return jsonify({'erro': 'Não foi possível conectar ao banco'})
    return resultSet


@setores_bp.route("/<int:idSetor>", methods=["GET"])
def dadosSetorPorId(idSetor):
    try:
        connection = getConnect()
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM setores WHERE id = ?", (idSetor, ))
        resultSet = cursor.fetchone()
        if(resultSet is not None):
            setor = {'id': resultSet[0], 'nome': resultSet[1]}
        else:
            return jsonify({'mensagem': 'O setor informada não existe'})
    except sqlite3.Error as e:
        return jsonify({'erro': str(e)})
    return setor


@setores_bp.route("/", methods=["GET"])
def listarTodosSetores():
    try:
        connection = getConnect()
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM setores")
        resultSet = cursor.fetchall()
        setores = []
        for props in resultSet:
            id = props[0]
            nome = props[1]
            setor = Setor(id=id, nome=nome)
            setores.append(setor.model_dump())
    except sqlite3.Error as e:
        return jsonify({'error': str(e)}), 500
    return jsonify(setores), 200


@setores_bp.route("/", methods=["POST"])
def criarSetor():
    try:
        novoSetor = request.json
        connection = getConnect()
        cursor = connection.cursor()
        cursor.execute("INSERT INTO setores(nome) VALUES(?)", (novoSetor['nome'], ))
        connection.commit()
        id = cursor.lastrowid
        novoSetor['id'] = id
    except sqlite3.Error as e:
        return jsonify({'er': str(e)}), 500
    return jsonify(novoSetor), 201


@setores_bp.route("/<int:idSetor>", methods=["DELETE"])
def deletarSetor(idSetor):
    try:
        connection = getConnect()
        cursor = connection.cursor()
        resultSet = getSetorPorId(idSetor)
        if(resultSet is None):
            return jsonify({'mensagem': 'Não é possível deletar um setor que não existe'})
        cursor.execute("DELETE FROM setores WHERE id = ?", (idSetor, ))
        connection.commit()
        return jsonify({'Mensagem': 'setor deletado com sucesso'})
    except sqlite3.Error as e:
        return jsonify({'erro': str(e)})


@setores_bp.route("/<int:idSetor>", methods=["PUT"])
def atualizarSetor(idSetor):
    try:
        dadosSetorAtualizado = request.json
        connection = getConnect()
        cursor = connection.cursor()
        resultSet = getSetorPorId(idSetor)
        if(resultSet is None):
            return jsonify({'mensagem': 'Não é possível atualizar os dados de um setor que não existe'})
        cursor.execute("UPDATE setores SET nome = ? WHERE id = ?", (dadosSetorAtualizado['nome'], idSetor))
        connection.commit()
        return jsonify({'mensagem': 'Os dados do setor foram atualizado'})
    except sqlite3.Error as e:
        return jsonify({'erro': str(e)})
