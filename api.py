from flask import Flask
from flask_restful import Resource, Api, reqparse

app = Flask(__name__)
api = Api(app)

CATS = {
    '1': {'name': 'Samson', 'age': 4, 'fur color': 'gray'},
    '2': {'name': 'Monty', 'age': 11, 'fur color': 'orange'},
    '3': {'name': 'Molly', 'age': 2, 'fur color': 'white'},
    '4': {'name': 'Miss Kitty', 'age': 15, 'fur color': 'calico'}
}

parser = reqparse.RequestParser()


class CatList(Resource):
    def get(self):
        return CATS

    def post(self):
        parser.add_argument('name')
        parser.add_argument('age')
        parser.add_argument('fur color')

        # combine the args
        args = parser.parse_args()

        # create new id increment
        cat_id = int(max(CATS.keys())) + 1

        # turn cat_id back into a string
        cat_id = '%i' % cat_id
        CATS[cat_id] = {
            'name': args['name'],
            'age': args['age'],
            'fur color': args['fur color']
        }
        return CATS[cat_id], 201


class Cat(Resource):
    def get(self, cat_id):
        if cat_id not in CATS:
            return "not found", 404
        else:
            return CATS[cat_id]

    def put(self, cat_id):
        parser.add_argument('name')
        parser.add_argument('age')
        parser.add_argument('fur color')
        args = parser.parse_args()

        if cat_id not in CATS:
            return "cat not found", 404
        else:
            cat = CATS[cat_id]
            cat['name'] = args['name'] if args['name'] is not None else cat['name']
            cat['age'] = args['age'] if args['age'] is not None else cat['age']
            cat['fur color'] = args['fur color'] if args['fur color'] is not None else cat['fur color']
            return cat, 200

    def delete(self, cat_id):
        if cat_id not in CATS:
            return 'cat not found', 404
        else:
            del CATS[cat_id]
            return 'that cat has been deleted', 204


api.add_resource(CatList, '/cats/')
api.add_resource(Cat, '/cats/<cat_id>')
if __name__ == '__main__':
    app.run(debug=True)
