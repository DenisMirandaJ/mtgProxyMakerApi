import { Router } from 'express'
import { Controller } from '../controllers/controller'

const router = Router()
const controller = new Controller()

router.get('/api/download/:deckfilename', controller.downloadImageFile.bind(this))
router.post('/api/build/deck', controller.callPythonDeckBuilder.bind(this))
router.get('/api/:oracleId', controller.getCardJsonByOracleId)
router.get('/api/named/:cardName', controller.getCardsJsonByName.bind(controller))

export { router }