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
                    frequency: 40 // 40ms, minimum iOS freq
                });
        app.compassWatchID = navigator.compass.watchHeading(
                app.onCompassSuccess, app.onOrientError, {
                    frequency: 40
                });
        app.gyroWatchID = navigator.gyroscope.watch(
                app.onGyroSuccess, app.onGyroError, {
                    frequency: 40
                });

        document.addEventListener("volumeupbutton", app.onVolumeUp, false);
    },
    onVolumeUp: function(ev) {
        app.session.publish('com.forrestli.selfiegolf.pubsub.boop', ["boop"]);
    },
    onAccelSuccess: function(acc) {
        app.session.publish('com.forrestli.selfiegolf.pubsub.accel', [acc.x, acc.y, acc.z]);
    },
    onAccelError: function() {
        console.log('Accel Error!');
    },
    onOrientError: function() {
        console.log('orient Error!');
    },
    onGyroError: function() {
        console.log('gyro Error!');
    },
    onCompassSuccess: function(heading) {
        app.session.publish('com.forrestli.selfiegolf.pubsub.orient',
            [heading.magneticHeading, heading.trueHeading]);
    },
    onGyroSuccess: function(speed) {
        app.session.publish('com.forrestli.selfiegolf.pubsub.gyro', [speed.x, speed.y, speed.z]);
    }
};
