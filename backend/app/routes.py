from flask import Blueprint,request,jsonify
from app.models import Community,db,User
import json
from werkzeug.security import check_password_hash

# Blueprint を インスタンス化
main = Blueprint('main',__name__)

@main.route('/')
def index():
  return "やっほー"

# ログイン
@main.route('/login',methods=['POST'])
def login():
  data = request.get_json()
  user_id = data.get('user_id')
  password = data.get('password')
  
  user = User.query.filter_by(user_id=user_id).first()
  
  if user and check_password_hash(user.password_hash,password):
    return jsonify({'message':'Login successful'}),200
  else:
    return jsonify({'message':'Invalid credentials'}),401

@main.route('/api/communities',methods=['POST'])
def create_community():  
  name = request.form.get('name')
  description = request.form.get('description')
  rules = request.form.get('rules')
  icon = request.files.get('icon')

  
  if not name or not description  or not rules:
    return jsonify({'error':'記入されていない項目があります'}),400
  
  # ファイルが尊信されなかった場合の処理
  if icon:
    icon_data = icon.read()
  else:
    icon_data = None
    
  try:
    # コミュニティを作成し、データベースに保存
    new_community = Community(
      name = name,
      description = description,
      rules = rules,
      icon = icon_data
    )
    db.session.add(new_community)
    db.session.commit()
    return jsonify({'message':'Community created successfully'}), 201
  
  except Exception as e:
    # エラーが発生した場合の処理
    db.session.rollback()
    print(f'Error occurred:{e}')
    return jsonify({'error':str(e)})