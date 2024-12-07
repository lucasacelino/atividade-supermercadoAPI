from flask import Blueprint, request, jsonify
import sqlite3

from helpers.database import getConnect
from models.Usuario import Usuario

usuarios_bp = Blueprint("usuarios", __name__)

def getUsuarioPorId(idUsuario):
    try:
        connection = getConnect()
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM usuarios WHERE id = ?", (idUsuario, ))
        resultSet = cursor.fetchone()
    except sqlite3.Error as e:
        return jsonify({'erro': 'Não foi possível conectar ao banco'})
    return resultSet


@usuarios_bp.route("/<int:idUsuario>", methods=["GET"])
def dadosUsuarioPorId(idUsuario):
    try:
        connection = getConnect()
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM usuarios WHERE id = ?", (idUsuario, ))
        resultSet = cursor.fetchone()
        if(resultSet is not None):
            setor = {'id': resultSet[0], 'nome': resultSet[1]}
        else:
            return jsonify({'mensagem': 'O usuario informado não existe'})
    except sqlite3.Error as e:
        return jsonify({'erro': str(e)})
    return setor


@usuarios_bp.route("/", methods=["GET"])
def listarTodosUsuarios():
    try:
        connection = getConnect()
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM usuarios")
        resultSet = cursor.fetchall()
        usuarios = []
        for props in resultSet:
            id = props[0]
            nome = props[1]
            usuario = Usuario(id=id, nome=nome)
            usuarios.append(usuario.model_dump())
    except sqlite3.Error as e:
        return jsonify({'error': str(e)}), 500
    return jsonify(usuarios), 200


@usuarios_bp.route("/", methods=["POST"])
def criarUsuario():
    try:
        novoUsuario = request.json
        connection = getConnect()
        cursor = connection.cursor()
        cursor.execute("INSERT INTO usuarios(nome) VALUES(?)", (novoUsuario['nome'], ))
        connection.commit()
        id = cursor.lastrowid
        novoUsuario['id'] = id
    except sqlite3.Error as e:
        return jsonify({'er': str(e)}), 500
    return jsonify(novoUsuario), 201


@usuarios_bp.route("/<int:idUsuario>", methods=["DELETE"])
def deletarUsuario(idUsuario):
    try:
        connection = getConnect()
        cursor = connection.cursor()
        resultSet = getUsuarioPorId(idUsuario)
        if(resultSet is None):
            return jsonify({'mensagem': 'Não é possível deletar um usuário que não existe'})
        cursor.execute("DELETE FROM usuarios WHERE id = ?", (idUsuario, ))
        connection.commit()
        return jsonify({'Mensagem': 'usuario deletado com sucesso'})
    except sqlite3.Error as e:
        return jsonify({'erro': str(e)})


@usuarios_bp.route("/<int:idUsuario>", methods=["PUT"])
def atualizarProduto(idUsuario):
    try:
        dadosUsuarioAtualizado = request.json
        connection = getConnect()
        cursor = connection.cursor()
        resultSet = getUsuarioPorId(idUsuario)
        if(resultSet is None):
            return jsonify({'mensagem': 'Não é possível atualizar os dados de um usuário que não existe'})
        cursor.execute("UPDATE usuarios SET nome = ? WHERE id = ?", (dadosUsuarioAtualizado['nome'], idUsuario))
        connection.commit()
        return jsonify({'mensagem': 'Os dados do usuário foram atualizados com sucesso'})
    except sqlite3.Error as e:
        return jsonify({'erro': str(e)})
