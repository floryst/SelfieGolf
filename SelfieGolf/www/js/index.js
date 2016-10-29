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
    },
    onServerConnect: function(ev) {
        app.conn = new autobahn.Connection({
            url: 'ws://152.23.68.243:8000/ws',
            realm: 'golf_course'
        });

        app.conn.onopen = app.onConnEstablished;
    },
    onConnEstablished: function() {
        app.accelWatchID = navigator.accelerometer.watchAcceleration(
                app.onAccelSuccess, app.onAccelError, {
                    frequency: 40 // 40ms, minimum iOS freq
                });
        app.compassWatchID = navigator.compass.watchHeading(
                app.onCompassSuccess, app.onAccelError, {
                    frequency: 40
                });

        document.addEventListener("volumeupbutton", app.onVolumeUp, false);

        document.body.setAttribute('style', 'background-color:green');
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
    },
    onAccelError: function() {
        alert('Error!');
    },
    onCompassSuccess: function(heading) {
        document.getElementById('magheading').innerHTML = heading.magneticHeading;
        document.getElementById('trueheading').innerHTML = heading.trueHeading;
    }
};
