const cors = require('cors')
const express = require('express')
const { METHODS } = require('http')
const jwt = require('jsonwebtoken')
const mysql = require('mysql')
const dotenv = require('dotenv');
dotenv.config();

const bcrypt = require('bcrypt')
const saltRounds = 10

const bodyParser = require('body-parser');
const cookieParser = require('cookie-parser')
const session = require('express-session')

conn = mysql.createConnection({
    host: process.env.DB_HOST,
    user: process.env.DB_USER,
    password: process.env.DB_PASSWORD,
    database: process.env.DB_NAME
    })

const app = express()
app.use(express.json());
app.use(cors({
    origin: ["http://localhost:3000"],
    METHODS: ['GET', 'POST'],
    credentials: true,
}))

function generateAccessToken(password) {
    return jwt.sign(username, process.env.TOKEN_SECRET, { expiresIn: '1800s' });
}

app.get("/", cors(), async (req, res) => {
    res.send("Hello World!");
  });

app.post('/signup/', (req, res) => {
    const username = req.body.username
    const password = req.body.password
    const email    = req.body.email
    bcrypt.hash(password, saltRounds, (err, hash) =>{
        if (err){
            console.log(err)
        }
        conn.query(
            `INSERT INTO users (username, password, email) VALUES ('${username}', '${hash}', '${email}');`,
            (err) => {
                console.log(err);
            } 
        )
    })
})

app.post('/signin/', (req, res) => {
    const username = req.body.username
    const password = req.body.password
    conn.query(
        `SELECT username, password FROM users WHERE username = '${username}';`,
        (err, result) => {
            if (err) {
                res.send({err: err})
            }
            if (result.length > 0) {
                bcrypt.compare(password, result[0].password, (err, bcrypt_result) => {
                    if (bcrypt_result){
                        res.send(result)
                    }
                    else{
                        res.send({message: "Wrong username/Password combination!"})
                    }
                })
            }
            else {
                res.send({message: "User doesn't exist!"})
            }
        }
    )
})

app.listen(4000, () => {
    console.log('Node server is running at http://localhost:4000')
})