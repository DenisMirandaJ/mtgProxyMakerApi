import { db } from './mongodbDriverConfig'
import { RequestHandler } from './requestHandler'

export class Controller {

    constructor() {
        this.requestHandler = new RequestHandler(1, 100)
    }

    async getCardJsonByOracleId(req, res) {
        let response = await db.find({ 'oracle_id': req.params.oracleId }).toArray()
        res.status(200).json(response)
    }

    /**
     * Uses the public Scryfall API, see https://scryfall.com/docs/api
     */
    async getCardsJsonByName(req, res) {
        let response = await this.requestHandler.getCardJsonByName(req.params.cardName)
        return res.status(200).json(response)
    }
}