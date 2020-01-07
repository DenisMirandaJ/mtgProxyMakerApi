import {Router} from 'express'
import {Controller} from '../controllers/controller'

const router = Router()

router.get('/api/:oracleId', Controller.wea)

export {router}