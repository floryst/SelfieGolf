var scene, camera, renderer;
var geometry, material, mesh;



init();
animate();


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

    var dirLight = new THREE.DirectionalLight(0xffffff, 1);
    dirLight.position.set(100, 100, 50);
    scene.add(dirLight);

    var ambLight = new THREE.AmbientLight(0xffffff, .1);
    scene.add(ambLight);

    renderer = new THREE.WebGLRenderer();
    renderer.setSize( window.innerWidth, window.innerHeight );
    renderer.setClearColor( 0xffffff, 1 );

    document.body.appendChild( renderer.domElement );

}

function animate() {


    requestAnimationFrame( animate );

    mesh.rotation.x += 0.01;
    mesh.rotation.y += 0.02;

    renderer.render( scene, camera );

}
