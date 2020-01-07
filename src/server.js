import express from 'express'
import {router} from './routes/routes'
var app = express()
var port = 8000

//Middleware to allow Access-Control-Origin on all HTTP requests
app.use(function (req, res, next) {
    res.header("Access-Control-Allow-Origin", "*");
    res.header("Access-Control-Allow-Headers", "Origin, X-Requested-With, Content-Type, Accept");
    res.header('Access-Control-Allow-Methods', 'PUT, POST, GET, DELETE, OPTIONS');
    next();
});

app.use(router)
app.listen(port)
console.log('Running on port ' + port)

export {app}



