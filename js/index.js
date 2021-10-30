const express = require('express');
const sequelize = require('./util/database');
const User = require('./models/users');

const app = express();
app.use(express.json());
app.use(express.urlencoded({ extended: true}));

app.use((req, res, next) => {
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'GET,POST,PUT,DELETE');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type');
  next();
})

//ROUTES
app.get('/', (req, res) => {
  res.send("Ciao")
})
app.use('/users', require('./routes/users'));


(async () => {
  try {
    console.log(process.env);
    await sequelize.sync(
      { force: false }
    );
    app.listen(process.env.EXTERNAL_PORT);
    console.log("js listening on port ", process.env.EXTERNAL_PORT);
  } catch (error) {
    console.log(error);
  }
})();