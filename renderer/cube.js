var scene, camera, renderer;
var geometry, material, mesh, mainBallMesh;
var conn, session;
var ballHidden = false;

window.strokes = 0;
window.ball = {x: 0, y:0, z:0, isMoving:false, heading:0, cameraHeading:3.14};
window.otherballs = {};

window.my_id = 0;

init();
animate();



function onBall(data) {
    var x = data[0],
        y = data[1],
        z = data[2],
        isStationary = data[3],
        id = data[4];
    if (id == window.my_id) {
        window.ball.x = x;
        window.ball.y = y;
        window.ball.z = z;
        window.ball.isMoving = !isStationary;
    }
    else {
        if (!(id in window.otherballs)) {
            window.otherballs[id] = makeball();
            scene.add(window.otherballs[id]);
        }
        console.log(id, x, y, z);
        window.otherballs[id].position.x = x;
        window.otherballs[id].position.y = y;
        window.otherballs[id].position.z = z;
    }
}

function onOrient(heading) {
    if (heading[2] != window.my_id) return;

    window.ball.heading = heading[0];
    window.ball.cameraHeading = heading[1];
    console.log(heading, id);
}

function onStroke(strokes) {
    if (strokes[1] != window.my_id) return;

    window.strokes = strokes[0];
    // XSS-enabled
    document.getElementById("strokes").innerText = window.strokes;
}

// hide ball by moving it below world
function hideBall(id) {
    if (id != window.my_id) return;

    window.ballHidden = true;
}

function showBall(id) {
    if (id != window.my_id) return;

    window.ballHidden = false;
}

function connEstablished(sess, details) {
    session = sess;
    session.subscribe('com.forrestli.selfiegolf.pubsub.ball', onBall);
    session.subscribe('com.forrestli.selfiegolf.pubsub.rendererOrientation', onOrient);

    session.subscribe('com.forrestli.selfiegolf.pubsub.strokes', onStroke);
    session.register('com.forrestli.selfiegolf.hide_ball', hideBall).then(function() {}, function(err) {
        console.error('Failed to register hide_ball!');
    });
    session.register('com.forrestli.selfiegolf.show_ball', showBall).then(function() {}, function(err) {
        console.error('Failed to register show_ball!');
    });
}

function makeball() {
    ballMat = new THREE.MeshLambertMaterial();
    ballGeo = new THREE.SphereGeometry(.04);
    ballMesh = new THREE.Mesh(ballGeo, ballMat);
    ballMesh.position.y = .04;
    return ballMesh;
}

function init() {

    scene = new THREE.Scene();

    camera = new THREE.PerspectiveCamera( 108, window.innerWidth / window.innerHeight, .1, 1000 );

    camera.position.y = 1;

    camera.lookAt(new THREE.Vector3(-1, 0, 1));


    geometry = new THREE.BoxGeometry( 200, 200, 200 );
    material = new THREE.MeshBasicMaterial( { color: 0xff0000, wireframe: true } );

    mesh = new THREE.Mesh( geometry, material );
    scene.add( mesh );

    var loader = new THREE.ColladaLoader();
    loader.load('course.dae', function (result) {
        scene.add(result.scene);
        console.log("loader worked i guess");
    });
    mainBallMesh = makeball();
    scene.add(mainBallMesh);

    var dir = new THREE.Vector3( 1, 0, 0 );
    var origin = new THREE.Vector3( 0, 0, 0 );
    var length = 1;
    var hex = 0xffff00;

    arrowHelper = new THREE.ArrowHelper( dir, origin, length, hex );
    scene.add( arrowHelper );

    var dirLight = new THREE.DirectionalLight(0xffffff, 1);
    dirLight.position.set(100, 100, 50);
    scene.add(dirLight);

    var ambLight = new THREE.AmbientLight(0xffffff, .1);
    scene.add(ambLight);

    renderer = new THREE.WebGLRenderer();
    renderer.setSize( window.innerWidth, window.innerHeight );
    renderer.setClearColor( 0xffffff, 1 );

    document.body.appendChild( renderer.domElement );

    // connect to server
    conn = new autobahn.Connection({
        url: 'ws://' + location.hostname + "/controllerws/ws",
        realm: 'golf_course'
    });

    conn.onopen = connEstablished;

    conn.open();
}

function animate() {


    requestAnimationFrame( animate );

    mesh.rotation.x += 0.01;
    mesh.rotation.y += 0.02;

    mainBallMesh.position.x = window.ball.x;
    if (window.ballHidden)
        mainBallMesh.position.y = -42;
    else
        mainBallMesh.position.y = window.ball.y;
    mainBallMesh.position.z = window.ball.z;
    if(window.ball.isMoving){
      camera.lookAt(new THREE.Vector3(window.ball.x, window.ball.y, window.ball.z));
      arrowHelper.position.copy(new THREE.Vector3(1000, 1000, 1000));
    } else {
      arrowHelper.position.copy(new THREE.Vector3(window.ball.x, window.ball.y, window.ball.z))
      // height of ball is 0.4
      arrowHelper.setDirection(new THREE.Vector3(Math.cos(window.ball.heading), 0.2, Math.sin(window.ball.heading)));
      camera.position.x = window.ball.x;
      camera.position.z = window.ball.z;
      var lookx = window.ball.x + Math.cos(window.ball.cameraHeading);
      var looky = 0;
      var lookz = window.ball.z + Math.sin(window.ball.cameraHeading);
      camera.lookAt(new THREE.Vector3(lookx, looky, lookz));
    }

    // also hide arrow
    if (window.ballHidden) {
      arrowHelper.position.copy(new THREE.Vector3(1000, 1000, 1000));
    }

    renderer.render( scene, camera );

}
