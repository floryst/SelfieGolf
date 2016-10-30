// debug purposes only
function dump(obj) {
    var str = "";
    for (var prop in obj) {
        str += prop + "     ";
    }
    return str;
}

var app = {
    initialize: function() {
        this.bindEvents();
    },
    bindEvents: function() {
        document.addEventListener('deviceready', this.onDeviceReady, false);
    },
    onDeviceReady: function() {
        document.getElementById('serverConnect')
            .addEventListener('click', app.onServerConnect, false);
        console.log('ready');
    },
    onServerConnect: function(ev) {
        app.conn = new autobahn.Connection({
            url: 'ws://152.23.68.243:8000/ws',
            realm: 'golf_course'
        });

        console.log('go connect');
        app.conn.onopen = app.onConnEstablished;

        app.conn.open();
    },
    onConnEstablished: function(session, details) {
        console.log('connected');
        app.session = session;

        app.accelWatchID = navigator.accelerometer.watchAcceleration(
                app.onAccelSuccess, app.onAccelError, {
                    frequency: 20 // 40ms, minimum iOS freq
                });
        app.compassWatchID = navigator.compass.watchHeading(
                app.onCompassSuccess, app.onOrientError, {
                    frequency: 40
                });
        app.gyroWatchID = navigator.gyroscope.watch(
                app.onGyroSuccess, app.onGyroError, {
                    frequency: 20
                });

        document.addEventListener("volumeupbutton", app.onVolumeUp, false);

        document.body.setAttribute('style', 'background-color:green');
        alert("done");
    },
    onVolumeUp: function(ev) {
        document.body.setAttribute('style', 'background-color:red');
    },
    onAccelSuccess: function(acc) {
        document.getElementById('x').innerHTML = acc.x;
        document.getElementById('y').innerHTML = acc.y;
        document.getElementById('z').innerHTML = acc.z;
        // doesn't work?
        //document.getElementById('timestamp').innerHTML = acc.timestamp.toLocaleString();
        app.session.publish('com.forrestli.selfiegolf.pubsub.accel', [acc.x, acc.y, acc.z]);
    },
    onAccelError: function() {
        alert('Accel Error!');
    },
    onOrientError: function() {
        alert('orient Error!');
    },
    onGyroError: function() {
        alert('gyro Error!');
    },
    onCompassSuccess: function(heading) {
        document.getElementById('magheading').innerHTML = heading.magneticHeading;
        document.getElementById('trueheading').innerHTML = heading.trueHeading;
        app.session.publish('com.forrestli.selfiegolf.pubsub.orient',
            [heading.magneticHeading, heading.trueHeading]);
    },
    onGyroSuccess: function(speed) {
        document.getElementById('angx').innerHTML = speed.x;
        document.getElementById('angy').innerHTML = speed.y;
        document.getElementById('angz').innerHTML = speed.z;
        app.session.publish('com.forrestli.selfiegolf.pubsub.gyro', [speed.x, speed.y, speed.z]);
    }
};
