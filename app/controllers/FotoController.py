from quart import request, jsonify, abort
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from app.models.Foto import Foto
from app import async_session_factory
import base64
from datetime import datetime
import io

async def criar_foto():
    """Criar uma nova foto"""
    try:
        data = await request.get_json()
        
        required_fields = ['nome', 'tipo_mime', 'dados', 'usuario_id']
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'Campo {field} é obrigatório'}), 400
        
        async with async_session_factory() as session:
            if isinstance(data['dados'], str):
                try:
                    dados_binarios = base64.b64decode(data['dados'])
                except Exception:
                    return jsonify({'error': 'Dados da imagem inválidos'}), 400
            else:
                dados_binarios = data['dados']
            
            tamanho = data.get('tamanho', len(dados_binarios))
            
            nova_foto = Foto(
                nome=data['nome'],
                tipo_mime=data['tipo_mime'],
                tamanho=tamanho,
                dados=dados_binarios,
                usuario_id=data['usuario_id']
            )
            
            session.add(nova_foto)
            await session.commit()
            
            return jsonify({
                'message': 'Foto criada com sucesso',
                'id': nova_foto.id
            }), 201
            
    except SQLAlchemyError as e:
        await session.rollback()
        return jsonify({'error': f'Erro no banco de dados: {str(e)}'}), 500
    except Exception as e:
        return jsonify({'error': f'Erro interno: {str(e)}'}), 500

async def get_fotos():
    try:
        async with async_session_factory() as session:
            page = int(request.args.get('page', 1))
            per_page = int(request.args.get('per_page', 10))
            usuario_id = request.args.get('usuario_id')
            
            query = select(Foto)
            
            if usuario_id:
                query = query.filter(Foto.usuario_id == usuario_id)
            
            result = await session.execute(query)
            fotos = result.scalars().all()
            
            start = (page - 1) * per_page
            end = start + per_page
            fotos_paginated = fotos[start:end]
            
            fotos_list = [foto.to_dict() for foto in fotos_paginated]
            
            return jsonify({
                'fotos': fotos_list,
                'pagination': {
                    'page': page,
                    'per_page': per_page,
                    'total': len(fotos),
                    'pages': (len(fotos) + per_page - 1) // per_page
                }
            }), 200
            
    except Exception as e:
        return jsonify({'error': f'Erro interno: {str(e)}'}), 500

async def get_foto_by_id(foto_id):
    try:
        async with async_session_factory() as session:
            result = await session.execute(select(Foto).filter(Foto.id == foto_id))
            foto = result.scalar_one_or_none()
            
            if not foto:
                abort(404, "Foto não encontrada")
            
            return jsonify({'foto': foto.to_dict()}), 200
            
    except Exception as e:
        return jsonify({'error': f'Erro interno: {str(e)}'}), 500

async def download_foto(foto_id):
    """Download da imagem"""
    try:
        async with async_session_factory() as session:
            result = await session.execute(select(Foto).filter(Foto.id == foto_id))
            foto = result.scalar_one_or_none()
            
            if not foto:
                abort(404, "Foto não encontrada")
            
            # Retornar dados em base64 para download via API
            dados_base64 = base64.b64encode(foto.dados).decode('utf-8')
            
            return jsonify({
                'nome': foto.nome,
                'tipo_mime': foto.tipo_mime,
                'tamanho': foto.tamanho,
                'dados': dados_base64
            }), 200
            
    except Exception as e:
        return jsonify({'error': f'Erro interno: {str(e)}'}), 500

async def atualizar_foto(foto_id):
    """Atualizar foto"""
    try:
        async with async_session_factory() as session:
            result = await session.execute(select(Foto).filter(Foto.id == foto_id))
            foto = result.scalar_one_or_none()
            
            if not foto:
                abort(404, "Foto não encontrada")
            
            data = await request.get_json()
            
            if 'nome' in data:
                foto.nome = data['nome']
            
            if 'tipo_mime' in data:
                foto.tipo_mime = data['tipo_mime']
            
            if 'dados' in data:
                if isinstance(data['dados'], str):
                    try:
                        dados_binarios = base64.b64decode(data['dados'])
                    except Exception:
                        return jsonify({'error': 'Dados da imagem inválidos'}), 400
                else:
                    dados_binarios = data['dados']
                
                foto.dados = dados_binarios
                foto.tamanho = len(dados_binarios)
            
            foto.updated_at = datetime.utcnow()
            
            await session.commit()
            
            return jsonify({
                'message': 'Foto atualizada com sucesso',
                'foto': foto.to_dict()
            }), 200
            
    except SQLAlchemyError as e:
        await session.rollback()
        return jsonify({'error': f'Erro no banco de dados: {str(e)}'}), 500
    except Exception as e:
        return jsonify({'error': f'Erro interno: {str(e)}'}), 500

async def deletar_foto(foto_id):
    """Deletar foto"""
    try:
        async with async_session_factory() as session:
            result = await session.execute(select(Foto).filter(Foto.id == foto_id))
            foto = result.scalar_one_or_none()
            
            if not foto:
                abort(404, "Foto não encontrada")
            
            await session.delete(foto)
            await session.commit()
            
            return jsonify({'message': 'Foto deletada com sucesso'}), 200
            
    except SQLAlchemyError as e:
        await session.rollback()
        return jsonify({'error': f'Erro no banco de dados: {str(e)}'}), 500
    except Exception as e:
        return jsonify({'error': f'Erro interno: {str(e)}'}), 500

async def get_fotos_by_usuario(usuario_id):
    """Buscar todas as fotos de um usuário"""
    try:
        async with async_session_factory() as session:
            page = int(request.args.get('page', 1))
            per_page = int(request.args.get('per_page', 10))
            
            result = await session.execute(select(Foto).filter(Foto.usuario_id == usuario_id))
            fotos = result.scalars().all()
            
            # Aplicar paginação
            start = (page - 1) * per_page
            end = start + per_page
            fotos_paginated = fotos[start:end]
            
            fotos_list = [foto.to_dict() for foto in fotos_paginated]
            
            return jsonify({
                'fotos': fotos_list,
                'pagination': {
                    'page': page,
                    'per_page': per_page,
                    'total': len(fotos),
                    'pages': (len(fotos) + per_page - 1) // per_page
                }
            }), 200
            
    except Exception as e:
        return jsonify({'error': f'Erro interno: {str(e)}'}), 500

async def deletar_fotos_by_usuario(usuario_id):
    """Deletar todas as fotos de um usuário"""
    try:
        async with async_session_factory() as session:
            result = await session.execute(select(Foto).filter(Foto.usuario_id == usuario_id))
            fotos = result.scalars().all()
            
            if not fotos:
                return jsonify({'message': 'Nenhuma foto encontrada para este usuário'}), 404
            
            for foto in fotos:
                await session.delete(foto)
            
            await session.commit()
            
            return jsonify({
                'message': f'{len(fotos)} fotos do usuário deletadas com sucesso'
            }), 200
            
    except SQLAlchemyError as e:
        await session.rollback()
        return jsonify({'error': f'Erro no banco de dados: {str(e)}'}), 500
    except Exception as e:
        return jsonify({'error': f'Erro interno: {str(e)}'}), 500
