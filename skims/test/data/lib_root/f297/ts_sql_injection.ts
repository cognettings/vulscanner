var db = require('./mysql/dbConnection.js');

function vuln (req, res) {
  var name = req.query.name; // user-controlled input
  var password = crypto.createHash('sha256').update(req.query.password).digest('base64');

  var sql = "select * from user where name = '" + name + "' and password = '" + password + "'";

  db.query(sql, function(err, result) { // Noncompliant
     // something
  })
}

function safe (req, res) {
  var name = req.query.name; // user-controlled input
  var password = crypto.createHash('sha256').update(req.query.password).digest('base64');

  var sql = "select * from user where name = ? and password = ?"; // the query is parameterized

  db.query(sql, [name, password], function(err, result) { // Compliant
     // something
  })
}
