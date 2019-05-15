import pickle
import json, pprint
from flask import Flask, request, Response, render_template, jsonify

app = Flask(__name__)

def add_user(**kwargs):
    print(kwargs)
    id = kwargs['id']
    name = kwargs['name']
    age = kwargs['age']
    type = kwargs['type']
    parent = kwargs['parent']

    pickle_in = open('users_file.data', "rb")
    data_in = pickle.load(pickle_in)
    pickle_in.close()
    user_exists = False
    for user in data_in:
        if str(user['id']) == str(id):
            user_exists = True
    if not user_exists:
        data_out = {'id': id, 'name': name, 'age': age, 'type': type, 'parent':parent}
        data_in.append(data_out)
        pickle_out = open('users_file.data', "wb")
        pickle.dump(data_in,pickle_out)
        pickle_out.close()
    return Response('{"status": "ok"}', status=200, mimetype='application/json')

def update_user(**kwargs):
    print(kwargs)
    id = kwargs['id']
    name = kwargs['name']
    age = kwargs['age']
    type = kwargs['type']
    parent = kwargs['parent']
    pickle_in = open('users_file.data', "rb")
    data_in = pickle.load(pickle_in)
    pickle_in.close()
    user_exists = False
    for user in data_in:
        if str(user['id']) == str(id):
            user['id'] = id
            user['name'] = name
            user['age'] = age
            user['type'] = type
            user['parent'] = parent

        pickle_out = open('users_file.data', "wb")
        pickle.dump(data_in,pickle_out)
        pickle_out.close()
    return Response('{"status": "ok"}', status=200, mimetype='application/json')

def print_user(id):
    pickle_in = open('users_file.data', "rb")
    data_in = pickle.load(pickle_in)
    if id == 0:
        pprint.pprint(data_in)
    else:
        for user in data_in:
            if user['id'] == id:
                print(user)
    pickle_in.close()
    return Response('{"status": "ok"}', status=200, mimetype='application/json')

def del_user(**kwargs):
    idp = kwargs['id']
    pickle_in = open('users_file.data', "rb")
    data_in = pickle.load(pickle_in)
    data_out = data_in
    pickle_in.close()
    for user in data_in:
        print(user['id'])
        print(idp)
        if str(user['id']) == str(idp):
            print(user)
            print(idp)
            data_out.remove(user)

    pickle_out = open('users_file.data', "wb")
    pickle.dump(data_out,pickle_out)
    pickle_out.close()
    return Response('{"status": "ok"}', status=200, mimetype='application/json')

#add_user(1,'Group 1',0,'group',0)
#print_user(0)
#update_user(4,'Michael',40,'user',1)
#print_user(0)
#del_user(5)

@app.route('/')
def index():
    pickle_in = open('users_file.data', "rb")
    data_in = pickle.load(pickle_in)
    pickle_in.close()
    return render_template('index.html',
                           title = 'All Users',
                           user = 0)

@app.route('/users/', methods=['GET', 'POST', 'PATCH', 'DELETE'])
def users2(*args, **kwars):
    pickle_in = open('users_file.data', "rb")
    data_in = pickle.load(pickle_in)
    pickle_in.close()

    return '''
        <html>
          <head>
            <title>All user Info</title>
          </head>
          <body>
            <h1> All USers </h1>
            <h1> ''' + str(data_in) + '''</h1>
          </body>
        </html>
        '''

@app.route('/users/<id>', methods=['GET', 'POST', 'PATCH', 'DELETE'])
def users(*args, **kwars):
    pickle_in = open('users_file.data', "rb")
    data_in = pickle.load(pickle_in)
    pickle_in.close()
    post_user = 'user'
    for user in data_in:
        if user['id'] == int(kwars['id']):
            post_user = user['name']
            post_age = user['age']
            post_type = user['type']
            post_parent = user['parent']
            post_id = user['id']

    if request.method == 'GET':
        return '''
            <html>
              <head>
                <title>User Info</title>
              </head>
              <body>
                <h1> Name - , ''' + post_user + '''</h1>
                <h1> age - , ''' + str(post_age) + '''</h1>
                <h1> type - , ''' + post_type + '''</h1>
                <h1> parent - , ''' + str(post_parent) + '''</h1>
                <h1> id - , ''' + str(post_id) + '''</h1>
              </body>
            </html>
            '''
    elif request.method == 'POST':
        return add_user(id=request.args['id'],
                           name=request.args['name'],
                           age=request.args['age'],
                           type=request.args['type'],
                           parent=request.args['parent'])
    elif request.method == 'PATCH':
        return update_user(id=request.args['id'],
                           name=request.args['name'],
                           age=request.args['age'],
                           type=request.args['type'],
                           parent=request.args['parent'])
    elif request.method == 'DELETE':
        return del_user(**kwars)
    else:
        pass

if __name__ == '__main__':
   app.run (host = '0.0.0.0', port = 8080)