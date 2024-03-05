const express = require('express');
const path = require('path');
const argon2 = require('argon2');
const { error } = require('console');

const app = express();
const port = 3000;
const salt = Buffer.from('NoSaltPleaseToday', 'utf-8');
app.use(express.json())
app.use(express.static(path.join(__dirname, 'public')));

// sendFile will go here
app.get('/', function(req, res) {
  res.sendFile(path.join(__dirname, '/index.html'));
});

app.post('/createAccount', async (req, res) => {
  const { user, password } = req.body;
  console.log('Creating account for user: ' + user);
  let hash;

  try {
      if (!password) {
          throw new Error('Password is undefined');
      }
      hash = await argon2.hash(password, {salt,hashLength:256,type: argon2.argon2id,timeCost:30});
  } catch (err) {
      console.error(err);
      res.status(500).send('Error creating account');
      return;
  } finally {
      console.log('Hash created: ' + hash.split('p=')[1]);
  }
  
  res.status(200).send('Account Created');
});


app.listen(port);
console.log('Server started at http://localhost:' + port);


