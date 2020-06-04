var express = require('express')
var mongoose = require('mongoose')
var cors = require('cors')
var body = require('body-parser')
var server = express()
var accessController = require('./controllers/accessController')
conString = 'animalgeek.sytes.net:27017/biometricaccess'

mongoose.connect('mongodb://' + conString, (err) => {
    if (err) throw err
    console.log('Mongo Successful')
});

server.use(cors({
    origin: '*'
}))
server.use(body.json())

server.post('/GetCurrent', accessController.GetAccess)
server.post('/SetCurrent', accessController.SetAccess)
server.post('/Register', accessController.RegisterAccess)

server.listen(8888, () => {
    console.log('Server Ready');
})