const express = require('express');
const app = express();
const cors = require('cors');
const fs = require('fs');
const cp = require('child_process');
const Patient = require('./database/database');
// const morgan = require('morgan');


app.use(cors());
app.use(express.json());

app.get('/', (req, res) => res.send('Hello World!'))

app.get('/api/getPatientsDatabase', async (req,res) => {
  let results = await Patient.find({});
  res.send({
    status: 'success',
    data: results
  });
})

app.post('/api/getUserResult', (req, res) => {

  let {symtomsLevel,userName,userAge} = req.body;

  // store result, user info, symtoms Level inside mongodb
  let name = userName;
  let age = userAge;
  let description = "";  

  symtomEntries = Object.entries(symtomsLevel);

  symtomEntries.forEach(entrie => {
    let level = entrie[1];
    switch(level){
      case 0: level = "no"; break;
      case 0.25: level = "low"; break;
      case 0.5: level = "maybe"; break;
      case 0.75: level = "high"; break;
      case 1: level = "extra high"; break;
    }
    description = description.concat(`${entrie[0]} : ${level} \n`);
  });

  // for direct response to user
  symtomsLevel = JSON.stringify(symtomsLevel);

  fs.writeFileSync("input.json",symtomsLevel);

  // call python script / program
  // result will be stored in output.txt 
  cp.spawnSync('python',['fuzzySetApplication.py']);

  let result = fs.readFileSync('output.txt','utf8');

  const newPatient = new Patient({
    name,age,result
  });

  newPatient.save();

  // send back to client
  res.send({
    status: 'success',
    data: result
  });
})

const port = process.env.PORT || 3000;

app.listen(port, () => console.log(`app listenning at :${port}`))