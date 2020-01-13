import express from 'express'
import dotenv from 'dotenv'
var bodyParser = require('body-parser');
dotenv.config()

var cors = require('cors')

var app = express()
//Middleware to allow Access-Control-Origin on all HTTP requests
app.use(cors())
app.options('*', cors());
app.use(bodyParser.json());
app.use(bodyParser.urlencoded({ extended: true }));
import { router } from './routes/routes'
var port = 8000

app.use(router)
app.listen(port)
console.log('Running on port ' + port)

export { app }



