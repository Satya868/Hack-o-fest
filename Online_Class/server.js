const express = require('express')
const request = require('request');

app = express();
const PORT = 3000;

app.get('/', function(req, res) {
    request('http://127.0.0.1:5000/', function (error, response, body) {
        console.error('error:', error); 
        console.log('statusCode:', response && response.statusCode); 
        console.log('body:', body); 
        res.send(body); 
      });      
});

app.get('/register', function(req, res){
    request('http://127.0.0.1:5000/register', function(error, response, body){
        console.error('error:', error); 
        console.log('statusCode:', response && response.statusCode); 
        console.log('body:', body); 
        res.send(body);
    })
})

app.get('/login', function(req, res){
    request('http://127.0.0.1:5000/login', function(error, response, body){
        console.error('error:', error); 
        console.log('statusCode:', response && response.statusCode); 
        console.log('body:', body); 
        res.send(body);
    })
})

app.listen(PORT, function (){ 
    console.log('Listening on Port 3000');
});