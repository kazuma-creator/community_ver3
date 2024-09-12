from flask import Blueprint,request,jsonify
from app.models import Community,db,User
import json
from werkzeug.security import check_password_hash,generate_password_hash
from flask_login import login_user,current_user,logout_user


# Blueprint を インスタンス化
main = Blueprint('main',__name__)


# ユーザー登録
@main.route('/register',methods=['POST'])
def register():
  try:
    data = request.get_json()
    username = data.get('username')
    user_id = data.get('user_id')
    password = data.get('password')
    
    # 既存のユーザーを確認
    if User.query.filter_by(user_id=user_id).first() is not None:
      return jsonify({"message":"Username already exists"}),400
    
    # パスワードをハッシュ化して保存
    hashed_password = generate_password_hash(password,method='pbkdf2:sha256')
    
    # 新規ユーザーを作成
    new_user = User(username=username,user_id=user_id,password_hash=hashed_password)
    db.session.add(new_user)
    db.session.commit()
    
    return jsonify({"message":"Account created successfully"}),201
  
  except Exception as e:
    # エラーをログに出力
    print(f"Error:{e}")
    return jsonify({"message":"Internal server error"}),500

# ログイン
@main.route('/login',methods=['GET','POST'])
def login():
  print("ログインのルートにアクセスしました")
  data = request.get_json()
  user_id = data.get('user_id')
  password = data.get('password')
  print(f"ユーザーID：{user_id}パスワード：{password}")
  user = User.query.filter_by(user_id=user_id).first()
  
  if user and check_password_hash(user.password_hash,password):
    login_user(user,remember=True) # ログイン状態にする
    print(f"ユーザー{user.id}がログインしました")
    return jsonify({'message':'Login successful'}),200
  else:
    return jsonify({'message':'Invalid credentials'}),401


# コミュニティ作成のエンドポイント
@main.route('/api/create_communities',methods=['POST'])
def create_community():  
  print("リクエストを受け取りました")
  print(request.form)
  
  if not current_user.is_authenticated:# ログイン時：True　ログインしていない場合：False
    print(f"現在のユーザー:{current_user},認証状態:{current_user.is_authenticated}")
    return jsonify({'error':'ログインが必要です'}),401
  
  name = request.form.get('name')
  description = request.form.get('description')
  rules = request.form.get('rules')
  icon = request.files.get('icon')

  print(f"名前:{name},説明:{description},ルール:{rules}")
  if not name or not description  or not rules:
    return jsonify({'error':'記入されていない項目があります'}),400
  
  # ファイルが送信されなかった場合の処理
  if icon:
    print(f"アイコンが正常に送信されました。サイズ：{len(icon_data) if icon_data else '無し'}")
    icon_data = icon.read()
  else:
    icon_data = None
    
  try:
    # コミュニティを作成し、データベースに保存
    print("コミュニティ情報を追加する")
    new_community = Community(
      name = name,
      description = description,
      rules = rules,
      icon = icon_data,
      creator_id = current_user.id
    )
    db.session.add(new_community)
    db.session.commit()
    print("コミュニティが正常に作成されました")
    return jsonify({'message':'Community created successfully'}), 201
  
  except Exception as e:
    # エラーが発生した場合の処理
    db.session.rollback()
    print(f'エラー発生:{e}')
    return jsonify({'error':str(e)})
  
@main.route('/api/get_communities',methods=['GET'])
def get_communities():
  communities = Community.query.all() # データベースからすべてのコミュニティを取得
  
  # 各コミュニティのデータをJSON形式に変換
  community_list = [Community.to_dict() for Community in communities]
  return jsonify(community_list),200

# ログインしているか確認
@main.route('/check_login', methods=['GET','POST'])
def check_login():
    if current_user.is_authenticated:
        print(f"ユーザーID:{current_user.id}")
        return jsonify({'message': 'User is logged in', 'user': current_user.user_id}), 200
    else:
        return jsonify({'message': 'User is not logged in'}), 401
      
# ログアウトの処理
@main.route('/logout',methods=['POST'])
def logout():
  logout_user()
  return jsonify({'message':'Logout successful'}),200

