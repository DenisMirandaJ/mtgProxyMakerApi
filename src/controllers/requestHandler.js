import Axios from 'axios'
import rateLimit from 'axios-rate-limit'

export class RequestHandler {
    constructor(maxRequests, perMilliseconds) {
        this.requestHandler = new rateLimit(Axios.create(), { maxRequests: maxRequests, perMilliseconds: perMilliseconds})
    }

    async getCardJsonByName(cardName) {
        let url = "https://api.scryfall.com/" + 'cards/named?fuzzy=' + cardName
            let response = {}
        try {
            response = await this.requestHandler.get(url)
        } catch(err) {
            return{'error': 'could not reach scryfall api'}
        }
        return response['data']
    }
}