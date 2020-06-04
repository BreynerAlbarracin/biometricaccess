var access = require('../models/accessModel').AccessModel;

exports.GetAccess = (req, res) => {
    let data = req.body

    console.log('Query')
    console.log(data)

    access.findOne({ accessPoint: data.accessPoint }, (err, accss) => {
        if (err) throw err
        console.log('send data')

        if (accss) {
            res.send(accss.name)
        } else {
            res.send('---')
        }
    })
}

exports.SetAccess = (req, res) => {
    let data = req.body

    console.log('RegisterAccess')
    console.log(data)

    access.findOneAndUpdate(
        {
            accessPoint: data.accessPoint
        },
        {
            accessPoint: data.accessPoint,
            name: data.name
        },
        { upsert: true }, (err, accss) => {
            if (err) throw err
            console.log('send data')

            if (accss) {
                res.send(data.name)
            } else {
                res.send('---')
            }
        })
}

exports.RegisterAccess = (req, res) => {
    let data = req.body

    console.log('RegisterAccess')
    console.log(data)

    let newAccess = new access({
        accessPoint: data.accessPoint,
        name: data.name
    })

    newAccess.save((err) => {
        if (err) throw err
        res.send(newAccess)
    })
}