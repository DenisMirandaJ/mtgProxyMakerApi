import { db } from './mongodbDriverConfig'
import { RequestHandler } from './requestHandler'
import { v1 as uuid4 } from 'uuid'
import { response } from 'express'
let { PythonShell } = require('python-shell')

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

    async downloadImageFile(req, res) {
        let uuidRegex = /^[0-9a-f]{8}-[0-9a-f]{4}-[0-5][0-9a-f]{3}-[089ab][0-9a-f]{3}-[0-9a-f]{12}$/i
        let match = req.params.deckfilename.match(uuidRegex)
        if (match) {
            return res.download('./python_image/decks/' + req.params.deckfilename + '.png')
        }
        res.status(400).send('File Not Found')
    }

    async callPythonDeckBuilder(req, res) {
        const fs = require('fs');
        let deckDataId = uuid4()
        let filename = "./python_image/deckInfo/" + deckDataId + '.deck'
        if (!fs.existsSync("./python_image/")) {
            fs.mkdirSync("./python_image/");
        }
        if (!fs.existsSync("./python_image/deckinfo/")) {
            fs.mkdirSync("./python_image/deckinfo/");
        }
        fs.writeFile(filename, JSON.stringify(req.body.cardDic), { flag: 'wx' }, function (err) {
            if (err) {
                return console.log(err);
            }
        })
        var options = { 
            args: [
                filename,
                'img'
            ] 
        }
        PythonShell.run('./src/controllers/python_image/deckImageCreator.py', options, function (err, data) {
            if (err) {
                console.log(err)
                return res.send(err)
            }
            try {
                response = data
                console.log(data)
            } catch {
                return res.status(302).send('Bad Request')
            }
            res.send(response)
        })
    }
}