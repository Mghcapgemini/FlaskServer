import os
import sys

# AST libraries
import ast
from ast2json import ast2json

# Import the framework
from flask import Flask, g
from flask_restful import Resource, Api, reqparse

plugin_name = "python-plugin"

eto_fields = [
"filename",
"content",
"charset"
]

# Create an instance of Flask
app = Flask(__name__)

# Create the API
api = Api(app)

class Connection(Resource):
    def get(self):
        return True

class isValidInput(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        for field in eto_fields:
            parser.add_argument(field, required=True)

        # Parse the arguments into an object
        args = parser.parse_args()
        extension = os.path.splitext(os.path.basename(args['filename']))[1]
        return extension == ".py"

class getInputModel(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        for field in eto_fields:
            parser.add_argument(field, required=True)

        # Parse the arguments into an object
        args = parser.parse_args()
        content = args['content']
        path = args['filename']
        parsed_ast = ast.parse(content)


        return {'path': path, 'model': ast2json(parsed_ast)}

api.add_resource(Connection,f'/processmanagement/{plugin_name}/isConnectionReady')
api.add_resource(isValidInput, f'/processmanagement/{plugin_name}/isValidInput')
api.add_resource(getInputModel, f'/processmanagement/{plugin_name}/getInputModel')
