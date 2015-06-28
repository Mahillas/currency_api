'use strict';

var _ = require('koa-route');
var bodyParser = require('koa-bodyparser');
var koa = require('koa');
var Trade = require('./models/trades').Trade;
var Q = require('q');
var logger = require('winston');

var app = koa();
app.use(bodyParser());



var currency = {
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

    console.log(tradeData);

    try {
      trade = new Trade(tradeData);
      result = (yield Q.ninvoke(trade, 'save'));
      this.body = 'Trade successfully created';
      this.status = 201;
    } catch (e) {
      logger.error("Could not add trade via the API:" + e.message)
      this.message = e.message;
      this.status = 400;
    }
  }
};

app.use(_.get('/trade', currency.list));
app.use(_.post('/trade', currency.add));
app.use(_.get('/trade/:id', currency.show));

app.listen(3000);
console.log('listening on port 3000');
