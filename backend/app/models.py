from datetime import datetime, timezone
from app import db
from flask_login import UserMixin

class User(UserMixin,db.Model):
  __tablename__ = 'users'
  
  id =db.Column(db.Integer,primary_key=True)
  username = db.Column(db.String(100),nullable=False,unique=True)
  user_id = db.Column(db.String(100),unique=True,nullable=True)
  password_hash = db.Column(db.String(128),nullable=False)
  created_at = db.Column(db.DateTime,default=lambda: datetime.now(timezone.utc))
  
  # リレーション: ユーザーが作成したコミュニティ
  communities = db.relationship('Community',backref='creator',lazy=True)
  memberships = db.relationship('Membership',backref='user',lazy=True)
  
  def __repr__(self):
    return f'<User {self.username}>'


class Community(db.Model):
  __tablename__ = 'communities'
  
  id = db.Column(db.Integer,primary_key=True)
  name = db.Column(db.String(150),nullable=False,unique=True)
  description = db.Column(db.Text,nullable=False)
  icon = db.Column(db.LargeBinary,nullable=True)
  rules = db.Column(db.Text,nullable=False)
  created_at = db.Column(db.DateTime,default=lambda:datetime.now(timezone.utc))
  
  def to_dict(self):
    return{
      'id':self.id,# コミュニティのID
      'name':self.name,# コミュニティの名前
      'description':self.description,# コミュニティの説明
      'icon':self.icon,# コミュニティのアイコン
      'rules':self.rules,# コミュニティのルール
      'created_at':self.created_at.isoformat()# コミュニティの作成日時
    }
  
  # リレーション: コミュニティを作成したユーザー
  creator_id = db.Column(db.Integer,db.ForeignKey('users.id'),nullable=False)
  
  # リレーション: コミュニティに参加しているメンバー
  memberships = db.relationship('Membership',backref='community',lazy=True)
  
  def __repr__(self):
    return f'<Community {self.name}>'
  
  
class Membership(db.Model):
  __tablename__ = 'memberships'
  
  id = db.Column(db.Integer,primary_key=True)
  user_id = db.Column(db.Integer,db.ForeignKey('users.id'),nullable=False)
  community_id = db.Column(db.Integer,db.ForeignKey('communities.id'),nullable=False)
  joined_at = db.Column(db.DateTime,default=lambda:datetime.now(timezone.utc))
  
  def __repr__(self):
    return f'<Membership User {self.user_id} Community {self.community_id}>'