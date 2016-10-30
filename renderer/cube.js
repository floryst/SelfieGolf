var scene, camera, renderer;
var geometry, material, mesh;
var conn, session;

window.ball = {x: 0, y:0, z:0, isMoving:false, heading:0};

init();
animate();



function onBall(data) {
    var x = data[0],
        y = data[1],
        z = data[2],
        isMoving = data[3];
    window.ball.x = x;
    window.ball.y = y;
    window.ball.z = z;
    window.ball.isMoving = isMoving;
}

function onOrient(heading) {
    window.ball.heading = heading[1];
}

function connEstablished(sess, details) {
    session = sess;
    session.subscribe('com.forrestli.selfiegolf.pubsub.ball', onBall);
    session.subscribe('com.forrestli.selfiegolf.pubsub.orientation', onOrient);
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
    ballMat = new THREE.MeshLambertMaterial();
    ballGeo = new THREE.SphereGeometry(.04);
    ballMesh = new THREE.Mesh(ballGeo, ballMat);
    ballMesh.position.y = .04;
    scene.add(ballMesh);

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
        url: 'ws://localhost:8000/ws',
        realm: 'golf_course'
    });

    conn.onopen = connEstablished;

    conn.open();
}

function animate() {


    requestAnimationFrame( animate );

    mesh.rotation.x += 0.01;
    mesh.rotation.y += 0.02;

    ballMesh.position.x = window.ball.x;
    ballMesh.position.z = window.ball.z;
    if(window.ball.isMoving){
      camera.lookAt(new THREE.Vector3(window.ball.x, window.ball.y, window.ball.z));
    } else {
      camera.position.x = window.ball.x;
      camera.position.z = window.ball.z;
      var lookx = window.ball.x + Math.cos(2 * Math.PI * window.ball.heading / 360.0);
      var looky = 0;
      var lookz = window.ball.z + Math.sin(2 * Math.PI * window.ball.heading / 360.0);
      camera.lookAt(new THREE.Vector3(lookx, looky, lookz));
    }

    renderer.render( scene, camera );

}
