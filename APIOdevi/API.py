from flask import Flask, request
from flask_restful import Api, Resource
import pandas as pd

app = Flask(__name__)
api = Api(app)


class Users(Resource):
    def get(self):
        data = pd.read_csv('world_classics.csv')
        data = data.to_dict('records')
        return {'data': data}, 200

    def post(self):
        name = request.args['name']
        author = request.args['author']


        data = pd.read_csv('world_classics.csv')

        new_data = pd.DataFrame({
            'name': [name],
            'author': [author],

        })

        data = data.append(new_data, ignore_index=True)
        data.to_csv('world_classics.csv', index=False)
        return {'data': new_data.to_dict('records')}, 200

    def delete(self):
        name = request.args['name']
        data = pd.read_csv('world_classics.csv')
        data = data[data['name'] != name]

        data.to_csv('world_classics.csv', index=False)
        return {'message': 'Record deleted successfully.'}, 200


class Author(Resource):
    def get(self):
        data = pd.read_csv('world_classics.csv', usecols=[2])
        data = data.to_dict('records')

        return {'data': data}, 200


class Name(Resource):
    def get(self, name):
        data = pd.read_csv('world_classics.csv')
        data = data.to_dict('records')
        for entry in data:
            if entry['name'] == name:
                return {'data': entry}, 200
        return {'message': 'No entry found with this name !'}, 404


# Add URL endpoints
api.add_resource(Users, '/users')
api.add_resource(Author, '/author')
api.add_resource(Name, '/<string:name>')

if __name__ == '__main__':
         #app.run(host="0.0.0.0", port=5000)
    app.run()