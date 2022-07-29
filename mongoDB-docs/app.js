const { client, close } = require('./connection')

const db = client.db('sample_airbnb')
const listingsAndReviews = db.collection('listingsAndReviews')
const cursor = listingsAndReviews.find({ bedrooms: 3, price: { $lt: 80 } })

// Cursor traversal is async in mongo
// cursor.forEach needs an await or a .then

// Queries in mongo are by default AND-ed i.e. the query on the cursor above is an AND
// If you wanna be explicit, an equivalent query would be:

const cursorExplicit = listingsAndReviews.find({
    $and: [{ bedrooms: 3 }, { price: { $lt: 80 } }]
})

// OR is the same, but use the $or keyword

async function insertManyExample() {
    const newListing = [
        { apt: '1221 Broadway', x: 1 },
        { apt: 'Inspire Downtown', x: 2 }
    ]

    const result = await listingsAndReviews.insertMany(newListing)
    return result
}

async function updateManyExample() {
    const filter = { x: { $exists: true } }
    const updateDoc = {
        $mul: {
            x: 2
        }
    }

    await listingsAndReviews.updateMany(filter, updateDoc, (err, result) => {
        console.log(result)
    })
}


