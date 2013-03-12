from flask import Flask, Response
from flask.ext import restful
from flask.ext.restful import reqparse, abort

import lxc

app = Flask(__name__)
api = restful.Api(app)

class LxcContainers(restful.Resource):
  def get(self):
    containers = lxc.all_as_dict()
    return containers

  def post(self):
    parser = reqparse.RequestParser()
    parser.add_argument('name', type=str, required=True)
    parser.add_argument('config', type=str)
    parser.add_argument('template', type=str)
    parser.add_argument('template_options', type=str)
    args = parser.parse_args()
    try:
      lxc.create(args['name'], config_file=args['config'], template=args['template'], template_options=args['template_options'])
      return '/'+args['name'], 201
    except Exception as e:
      return str(e), 500


class LxcContainer(restful.Resource):
  def get(self, name):
    if lxc.exists(name):
      container = lxc.info(name)
      return container
    else:
      abort(404)

  def delete(self, name):
    if lxc.exists(name):
      lxc.destroy(name)
      return Response(status=204)
    else:
      abort(404)


class LxcContainerState(restful.Resource):
  def get(self, name):
    if lxc.exists(name):
      state = lxc.info(name)['state:']
      return state
    else:
      abort(404)

  def put(self, name):
    if lxc.exists(name):
      parser = reqparse.RequestParser()
      parser.add_argument('state', type=str, required=True)
      newState = parser.parse_args()['state']
      oldState = lxc.info(name)['state:']
      if newState == oldState:
        return Response(status=204)
      else:
        if newState == 'RUNNING':
          if oldState == 'STOPPED':
            lxc.start(name)
          elif oldState == 'FROZEN':
            lxc.start(name)
        elif newState == 'STOPPED':
          lxc.stop(name)
        elif newState == 'FROZEN':
          lxc.freeze(name)
        return lxc.info(name)
    else:
      abort(404)

api.add_resource(LxcContainers, '/')
api.add_resource(LxcContainer, '/<string:name>')
api.add_resource(LxcContainerState, '/<string:name>/state')
