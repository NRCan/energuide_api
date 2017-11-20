'use strict';

Object.defineProperty(exports, "__esModule", {
  value: true
});

var _express = require('express');

var _express2 = _interopRequireDefault(_express);

var _bodyParser = require('body-parser');

var _bodyParser2 = _interopRequireDefault(_bodyParser);

var _apolloServerExpress = require('apollo-server-express');

var _graphqlTools = require('graphql-tools');

function _interopRequireDefault(obj) { return obj && obj.__esModule ? obj : { default: obj }; }

var typeDefs = '\n  type Query {\n    hello: String\n  }\n';
var resolvers = {
  Query: {
    hello: function hello() {
      return 'world';
    }
  }
};

var schema = (0, _graphqlTools.makeExecutableSchema)({ typeDefs: typeDefs, resolvers: resolvers });

function Server() {
  var server = (0, _express2.default)();
  server.use('/graphql', _bodyParser2.default.json(), (0, _apolloServerExpress.graphqlExpress)(function (request) {
    return {
      schema: schema,
      context: {}
    };
  }));
  server.get('/graphiql', (0, _apolloServerExpress.graphiqlExpress)({ endpointURL: '/graphql' }));
  return server;
}

exports.default = Server;