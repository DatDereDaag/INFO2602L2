import click, sys
from models import db, User, Todo
from app import app
from sqlalchemy.exc import IntegrityError


@app.cli.command("init", help="Creates and initializes the database")
def initialize():
  db.drop_all()
  db.init_app(app)
  db.create_all()
  bob = User('bob', 'bob@mail.com', 'bobpass')
  bob.todos.append(Todo('wash car'))
  db.session.add(bob)
  db.session.commit()
  print(bob)
  print('database intialized')

@app.cli.command("get-user", help = "Retrives a user")
@click.argument('username', default = 'bob')
def get_user(username):
  bob = User.query.filter_by(username = username).first()
  if not bob:
    print(f'User {username} not found')
    return
  print(bob)

@app.cli.command('get-users')
def get_users():
  users = User.query.all()
  if not users:
    print('No users found')
    return
  for user in users:
    print(user)

@app.cli.command('change-email')
@click.argument('username', default = 'bob')
@click.argument('email', default = 'bob@mail.com')
def change_email(username, email):
  user = User.query.filter_by(username = username).first()
  if not user:
    print(f'User {username} not found')
    return
  user.email = email
  db.session.add(user)
  db.session.commit()
  print(user)

@app.cli.command('create-user')
@click.argument('username', default = 'babaoolal')
@click.argument('email', default = 'babaoolal@gmail.com')
@click.argument('password', default = 'babaoolalpass')
def create_user(username, email, password):
  newuser = User(username, email, password)
  try:
    db.session.add(newuser)
    db.session.commit()
  except IntegrityError as e:
    db.session.rollback()
    print(f'Error creating user: User already exists')
  else:
    print(f'User {newuser} created successfully')
                
@app.cli.command('delete-user')
@click.argument('username', default = 'bob')
def delete_user(username):
  user = User.query.filter_by(username = username).first()
  if not user:
    print(f'User {username} not found')
    return
  db.session.delete(user)
  db.session.commit()
  print(f'User {user} deleted successfully')

@app.cli.command('get-todos')
@click.argument('username', default='bob')
def get_user_todos(username):
  bob = User.query.filter_by(username=username).first()
  if not bob:
      print(f'{username} not found!')
      return
  print(bob.todos)