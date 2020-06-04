var mongoose = require('mongoose')

exports.AccessModel = mongoose.model('AccessModel',
{ 
    accessPoint: String,
    name: String
});