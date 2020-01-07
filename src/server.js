import express from 'express'
var cors = require('cors')

var app = express()
//Middleware to allow Access-Control-Origin on all HTTP requests
app.use(cors())
app.options('*', cors());
import { router } from './routes/routes'
var port = 8000

app.use(router)
app.listen(port)
console.log('Running on port ' + port)

export { app }



