'use strict';
var mongoose = require('mongoose');
var connection = mongoose.connect('mongodb://localhost/trades', function(err) {

    if(err) {
        console.log('database connection error', err);
    } else {
        console.log('successfully connected to db');
    }
});

var TradeSchema = new mongoose.Schema({
  userId: Number,
  currencyFrom: String,
  currencyTo: String,
  amountSell: Number,
  amountBuy: Number,
  rate: Number,
  timePlaced: Date,
  originatingCountry: String

});

// Convert the Schema into Model and export it.
exports.Trade = connection.model('Trade', TradeSchema);
