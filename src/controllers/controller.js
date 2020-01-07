import { db } from './mongodbDriverConfig'

export class Controller {
    // static getCardsByOracleId(req, res) {
    //     console.log(mongodb)
    //     mongodb.collection("ScryfallDump").find({'oracle_id': req.params.oracleId}).toArray(function(err, cards) {
    //         assert.equal(err, null);
    //         res.send(cards)
    //       });
    // }

    static wea(req, res) {
        db.find({ 'oracle_id': req.params.oracleId })
            .toArray()
            .then (
                response => res.status(200).json(response)
            )
    }
}