
console.log('Try download');
var admin = require("firebase-admin");
var fs = require('fs');

var serviceAccount = require("./some-ff1f3-firebase-adminsdk-x0ied-214bc48c68.json");

admin.initializeApp({
  credential: admin.credential.cert(serviceAccount),
  databaseURL: "https://some-ff1f3.firebaseio.com",
  storageBucket: "gs://some-ff1f3.appspot.com"
});

var db = admin.database();
var ref = db.ref('/user');
var bucket = admin.storage().bucket();

var p = [];

ref.once("value", function(snapshot) {
	  snapshot.forEach(function(userSnapshot) {
	  console.log(userSnapshot.key, userSnapshot.val());
	  var user_name = userSnapshot.val()['user'];
	  var choice = userSnapshot.val()['choice'];
	  var file_name = userSnapshot.val()['file'];
	  var file = bucket.file('images/' + user_name + '/' + file_name);
	  if(!fs.existsSync('./image/user-' + user_name + '-' + choice)){
	  	fs.mkdirSync('./image/user-' + user_name + '-' + choice);
	  }
	  file.download({
	  	destination: './image/user-' + user_name + '-' + choice +'/' + file_name
	  }, function(err) {});
	  
	  ref.child(userSnapshot.key).remove();
	  
	  
	});
});
setTimeout(function(){admin.app().delete();process.exit()}, 13500);


/*
var bucket = admin.storage().bucket()

var file = bucket.file('images/chill.jpg');
file.download({
  destination: './chill.jpg'
}, function(err) {});
*/
