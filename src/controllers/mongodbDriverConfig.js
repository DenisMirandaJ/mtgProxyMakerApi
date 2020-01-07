import { MongoClient } from 'mongodb'
import assert from 'assert'

//mongoDB driver configuration
var db
const url = 'mongodb://localhost:27017';
const dbName = 'ScryfallDump';
const collectionName = "ScryfallDump"

MongoClient
    .connect(
        url, 
        { poolSize: 10 }
    )
    .then(client => {
        db = client.db(dbName).collection(collectionName);
    })
    .catch(error => console.error(error));

export { db }