// Installed Packages
const { MongoClient } = require('mongodb')
require('dotenv').config()

const connectionString = process.env.CONNECTION_STRING
const client = new MongoClient(connectionString)

// Function to connect to mongoDB
async function run() {
    await client.connect()
}

async function close() {
    await client.close()
}

run().catch(console.dir)

// Export connection to other files
module.exports = {
    client,
    close
}