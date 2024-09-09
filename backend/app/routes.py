from flask import Blueprint,request,jsonify
from app.models import Community,db
import json

# Blueprint を インスタンス化
main = Blueprint('main',__name__)

@main.route('/')
def index():
  return "やっほー"

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
    return jsonify({'error':str(e)})