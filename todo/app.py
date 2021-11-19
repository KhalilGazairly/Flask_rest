from flask import Flask, request
from flask_restful import Resource, Api, abort
from models import db, Todo
import logging

logging.basicConfig(filename='/media/khalil-gazairly/aser/ITI/Flask/flask_todo/flask.logs',
                    format='%(asctime)s %(name)s - %(levelname)s - %(message)s',
                    datefmt='%d-%b-%y %H:%M:%S')

todo_flask_api = Flask(__name__)
todo_api = Api(todo_flask_api)

todo_flask_api.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db'
todo_flask_api.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

todo_list = [
    {'name': 'a', 'id': 0, 'priority': 5},
    {'name': 'b', 'id': 1, 'priority': 5},
    {'name': 'c', 'id': 2, 'priority': 5}
]


@todo_flask_api.route('/', methods=['GET'])
def hello():
    return 'Hello, From Flask!'


class TodoRUD(Resource):
    def get(self, **kwargs):
        todo_id = kwargs.get('todo_id')
        task = Todo.query.get(todo_id)
        if not task:
            abort(404, message='Not Found')

        data = {
            'id': task.id,
            'name': task.name,
            'priority': task.priority,
            'description': task.description,
            'finished': task.finished
        }

        return data, 200

    def delete(self, *args, **kwargs):
        todo_id = kwargs.get('todo_id')
        todo_obj = Todo.query.get(todo_id)

        db.session.delete(todo_obj)
        db.session.commit()

        return {'message': 'Deleted Successfully'}, 200


class TodoLC(Resource):
    def post(self):
        try:
            data = {
                'name': request.form.get('name'),
                'priority': request.form.get('priority'),
                'description': request.form.get('description'),
                'finished': False
            }
            todo_obj = Todo(**data)
            db.session.add(todo_obj)
            db.session.commit()
            # todo_list.append(data)

            return {'message': 'Task Created Successfully'}, 201
        except Exception as e:
            abort(500, message='Internal Server Error')

    def get(self):
        try:
            todo_objects = Todo.query.filter().all()
            limit = request.args.get('limit')
            # my_list = []
            # if limit:
            #     my_list = todo_list[:int(limit)]
            # else:
            #     my_list = todo_list

            my_new_list = []

            for task in todo_objects:
                data = {
                    'id': task.id,
                    'name': task.name,
                    'priority': task.priority,
                    'description': task.description,
                    'finished': task.finished
                }
                my_new_list.append(data)
            if limit:
                print(type(limit))
                my_new_list = my_new_list[:int(limit)]

            return my_new_list

        except Exception as e:
            abort(500, message="Internal Server Error {}".format(e))


todo_api.add_resource(TodoRUD, '/api/v1/todo/<int:todo_id>')
todo_api.add_resource(TodoLC, '/api/v1/todo')

db.init_app(todo_flask_api)


@todo_flask_api.before_first_request
def initiate_data_base_tables():
    db.create_all()


todo_flask_api.run(debug=True)

