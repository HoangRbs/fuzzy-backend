const mongoose = require('mongoose');

mongoose.connect('mongodb://localhost/patientsDB', {useNewUrlParser: true});

var db = mongoose.connection;
db.on('error', console.error.bind(console, 'connection error:'));
db.once('open', function() {
  console.log("database connected");
});

const patientSchema = new mongoose.Schema({
  name:{
    type: String,
    required: true
  },
  age: {
    type: Number,
    required: true
  },
  result: {
    type: String,
    required: true
  },
  // description: {
  //   type: String,   // muc do trieu chung
  //   required: true
  // }
});

const Patient = mongoose.model('patient', patientSchema);

module.exports = Patient;

