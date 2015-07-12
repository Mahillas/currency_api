'use strict';

var _ = require('koa-route');
var bodyParser = require('koa-bodyparser');
var koa = require('koa');
var Trade = require('./models/trades').Trade;
var Q = require('q');
var logger = require('winston');
var cassandra = require('cassandra-driver');
var co = require('co');
var Client = require('co-cassandra')(require('cassandra-driver').Client);
var client = new Client({contactPoints: ['localhost']});
var app = koa();
app.use(bodyParser());

var api = {
  list: function *(){
    try{
      this.body = yield Trade.find().exec();
    }
    catch (e) {
      logger.error("Could not fetch trades via the API:" + e.message);
      this.message = e.message;
      this.status = 500;
    }
  },

  show: function *(id){
    this.body = yield Trades.findById(id);
  },

  add: function *(){
    //get posts;
    var tradeData = this.request.body;
    var trade;
    var result;

    try {
      trade = new Trade(tradeData);
      result = (yield Q.ninvoke(trade, 'save'));
      this.body = 'Trade successfully created';
      this.status = 201;
    } catch (e) {
      logger.error("Could not add trade via the API:" + e.message);
      this.message = e.message;
      this.status = 400;
    }
  },

  cass: function *(){
    var query = 'select key from system.local';
    var result =  yield client.execute(query);
    this.body = result.rows;
  }
};

app.use(_.get('/trade', api.list));
app.use(_.post('/trade', api.add));
app.use(_.get('/trade/:id', api.show));
app.use(_.get('/cass', api.cass));

app.listen(3000);

console.log('listening on port 3000');
