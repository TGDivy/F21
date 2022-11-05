import * as THREE from 'three';
import * as THREEMaps from '@googlemaps/three'
import * as MathUtils from 'mathutils'
import { Loader } from '@googlemaps/js-api-loader';

async function Render(){
  const mapOptions = {
    center: {
      lat: 45,
      lng: 0,
    },
   
    zoom: 5,
    heading: -45,
    tilt: 45,
  };
  const loader = new Loader({
    apiKey: "AIzaSyBETISNKTcGe2QG4UNQSla9v9zhF7Mecvg",
    version: "weekly",
    libraries: ["places"]
  });
  loader
  .load()
  .then((google) => {
    const map =new google.maps.Map(document.getElementById("map"), mapOptions);
    
  // instantiate a ThreeJS Scene
  const scene = new THREE.Scene();
  
  // Create a box mesh
  const box = new THREE.Mesh(
    new THREE.BoxBufferGeometry(10, 50, 10),
    new THREE.MeshNormalMaterial(),
  );
  
  // set position at center of map
  box.position.copy(THREEMaps.latLngToVector3(mapOptions.center));
  // set position vertically
  box.position.setY(25);
  
  // add box mesh to the scene
  scene.add(box);
  
  // instantiate the ThreeJS Overlay with the scene and map
  new THREEMaps.ThreeJSOverlayView({
    scene,
    map,
    THREE,
  });
   const camera = new THREE.PerspectiveCamera( 75, window.innerWidth / window.innerHeight, 0.1, 1000 );
   const renderer = new THREE.WebGLRenderer();
   renderer.setSize( window.innerWidth, window.innerHeight );
   document.body.appendChild( renderer.domElement );
  
  // rotate the box using requestAnimationFrame
  const animate = () => {
    //box.rotateY(MathUtils.degToRad(0.1));
    renderer.render( scene, camera );
    requestAnimationFrame(animate);
  };
  
  // start animation loop
  requestAnimationFrame(animate);
  })
  .catch(e => {
    // do something
  });
  
 
}
export default  Render;