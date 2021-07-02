import functools
import re

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for, jsonify, Response
)

from werkzeug.security import check_password_hash, generate_password_hash

from .db import get_db

bp = Blueprint('auth', __name__, url_prefix='/auth')


@bp.route('/')
def index():
    db = get_db()
    posts = db.execute(
        'SELECT p.id, title, body, created'
        ' FROM post p'
        ' ORDER BY created DESC'
    ).fetchall()
    post_data_set = []
    for i in posts:
        post_data = {}
        post_data['title'] = i['title']
        post_data['body'] = i['body']
        post_data_set.append(post_data)
    
    print(post_data_set)
    
    return Response(f'{post_data_set}', 200, mimetype='application/json')

@bp.route('/create', methods=["GET", "POST"])
def create():
    if request.method == 'POST':
        request_data = request.get_json()
        title = request_data.get('title')
        body = request_data.get('body')

        if title and body:
            db = get_db()
            db.execute(
                'INSERT INTO post (title, body)'
                ' VALUES (?, ?)',
                (title, body)
            )

            db.commit()
            return Response(status=201, mimetype='application/json')


    return ""