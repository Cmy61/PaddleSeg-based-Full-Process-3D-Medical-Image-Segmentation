<template>
  <!-- 用于只选择一个object时的显示 -->
  <div style="width:100%;height:100%;display:flex;">
      <div class="moudle-show-part" :id="'moudle-show-container' + sceneName">
      </div>
      <div class="gui-show-part" :id="'gui-show-part' + sceneName" style="display:none;"></div>
  </div>
</template>

<script>
import * as Three from "three/build/three";
import { OrbitControls } from "three/examples/jsm/controls/OrbitControls";
import { ViewHelper } from 'three/examples/jsm/helpers/ViewHelper.js';
import { GUI } from 'three/examples/jsm/libs/lil-gui.module.min.js';
import { TrackballControls } from 'three/examples/jsm/controls/TrackballControls.js';

export default {
  props: ["sceneName", "object", "dims", "pixel_dims",'label_dict'],
  data() {
    return {
      // geometry: null,
      camera: null, //相机
      scene: null, //场景
      renderer: null,
      controls: null,
      lights: [],
      animationId: null,
      raycaster: null,
      pointer: null,
      show: false,
      gui_parameters:null,
      gui:null,
      sel_object:null,
      sel_object_change_state: null, //用于判定选择得object是否改变。改变时更改gui但不执行更新函数。

      INTERSECTED: null,
      innerWidth: "",
      innerHeight: "",

      box_group: null, //nii对应的空间长方体模型
      mesh_group: null, //标签对应的group
      helper: null, //视角旋转器辅助
      clock: null,
      
    };
  },
  methods: {
    scene_resize() {
      const container = document.getElementById(
        "moudle-show-container" + this.sceneName
      );
      this.camera.aspect = container.clientWidth / container.clientHeight; //相机视角长宽比
      this.camera.updateProjectionMatrix();
      this.renderer.setSize(container.clientWidth, container.clientHeight);
      this.innerWidth = container.clientWidth;
      this.innerHeight = container.clientHeight;
      
    },
    
    onPointerDB(event) {
      // 将鼠标位置归一化为设备坐标。x 和 y 方向的取值范围是 (-1 to +1)
      // console.log(event.offsetX,event.offsetY)
      this.pointer.x = (event.offsetX / this.innerWidth) * 2 - 1;
      this.pointer.y = -(event.offsetY / this.innerHeight) * 2 + 1;
      this.show = true;
    },
    initLight() {
      const lightWeight = 0.3;
      const distance = 1000;
      for (let i = 0; i < 2; i++) {
        const x = Math.pow(-1, i) * distance;
        for (let j = 0; j < 2; j++) {
          const y = Math.pow(-1, j) * distance;
          for (let k = 0; k < 2; k++) {
            const z = Math.pow(-1, k) * distance;
            const directionalLight = new Three.DirectionalLight(
              0xffffff,
              lightWeight
            );
            directionalLight.position.set(x, y, z);
            this.scene.add(directionalLight);
          }
        }
      }
    },
    helper_click(event){
      console.log('mouse_up');
      this.helper.handleClick(event);
    },
    init() {
      this.raycaster = new Three.Raycaster();
      this.pointer = new Three.Vector2();
      const container = document.getElementById(
        "moudle-show-container" + this.sceneName
      );
      window.addEventListener("resize", this.scene_resize, false);

      container.addEventListener("dblclick", this.onPointerDB);
      console.log(
        "webgl view-size:",
        container.clientWidth,
        container.clientHeight
      );
      this.innerWidth = container.clientWidth;
      this.innerHeight = container.clientHeight;
      this.camera = new Three.PerspectiveCamera(
        45,
        container.clientWidth / container.clientHeight,
        0.01,
        3000
      );
      this.camera.position.z = 1000;
      this.camera.lookAt(0, 0, 0);
      this.controls = new OrbitControls(this.camera, container);
      // this.controls = new TrackballControls(this.camera, container);
      // this.controls.rotateSpeed = 15.0;
      // this.controls.staticMoving = true;
      this.scene = new Three.Scene();
      this.scene.background = new Three.Color("#e8eaec");
      // this.scene.background = new Three.Color("#000000");
      this.renderer = new Three.WebGLRenderer({ antialias: true });
      this.renderer.autoClear = false;
      this.renderer.setSize(container.clientWidth, container.clientHeight);
      container.appendChild(this.renderer.domElement);
      this.initLight();
      this.helper = new ViewHelper( this.camera, this.renderer.domElement );
      this.helper.controls = this.controls;
      this.helper.controls.center = this.controls.target;
      const div = document.createElement( 'div' );
      div.id = 'viewHelper';
      div.style.position = 'absolute';
      div.style.right = 0;
      div.style.bottom = 0;
      div.style.height = '128px';
      div.style.width = '128px';
      
      container.appendChild(div);
      console.log("123");
      div.addEventListener( 'pointerup', this.helper_click );
      // container.addEventListener( 'pointerup', (event) => this.helper.handleClick( event ) );
      this.clock = new Three.Clock();

      // this.load_box();
      // this.load_model();
      // this.value = new Three.Group();
      // this.scene.add(this.value);
      // var mesh_group = new Three.Group();
      // for (let i=0;i<this.object.length;++i){
      //   if (this.object[i] != null){
      //     mesh_group.add(this.object[i]);
      //     console.log(this.object[i].position)
      //   }
      // }
      // 512 * 0.782 , 512 * 0.782 , 90 * 5
      // var geometry = new Three.BoxGeometry(512 * 0.782, 512 * 0.782, 90 * 5); //这个是nii对应的长方体，根据dims和pixeldim结合计算
      // var material = new Three.MeshLambertMaterial({color: 'red'});
      // var cube = new Three.Mesh(geometry, material);
      

      // this.scene.add(mesh_group);
      // //移动到中心位置
      // var box = new Three.Box3();
      // box.expandByObject(mesh_group);
      // console.log(box);
      // mesh_group.position.x = (-(box.max.x - box.min.x)/2);
      // mesh_group.position.y = (-(box.max.y - box.min.y)/2);
      // mesh_group.position.z = (-(box.max.z - box.min.z)/2);
      
      // cube.position.x = ((512 * 0.782 - 0)/2)-(box.max.x - box.min.x)/2;
      // cube.position.y = ((512 * 0.782 - 0)/2)-(box.max.y - box.min.y)/2;
      // cube.position.z = ((90 * 5 - 0)/2)-(box.max.z - box.min.z)/2;
      // cube.visible = false;
			// const cube_box = new Three.BoxHelper( cube );
			// this.scene.add( cube_box );
      // this.scene.add(cube);


      if (this.object.length != 0){
        this.sel_object = this.object[0];
        this.gui_parameters = { 'opacity': 0, 'color' : 0x000000, 'visible':true};
        this.gui = new GUI({autoPlace:false});
        document.getElementById('gui-show-part' + this.sceneName).append(this.gui.domElement);
        this.gui_reinit();
        this.sel_object_change_state = false;
      }
    },
    load_box(){
      console.log(this.dims);
      console.log(this.pixel_dims);
      var geometry = new Three.BoxGeometry(this.dims.x * this.pixel_dims.x, this.dims.y * this.pixel_dims.y, this.dims.z * this.pixel_dims.z); //这个是nii对应的长方体，根据dims和pixeldim结合计算
      var material = new Three.MeshLambertMaterial({color: 'red'});
      var cube = new Three.Mesh(geometry, material);
      cube.position.x = ((this.dims.x * this.pixel_dims.x - 0)/2);
      cube.position.y = ((this.dims.y * this.pixel_dims.y - 0)/2);
      cube.position.z = ((this.dims.z * this.pixel_dims.z - 0)/2);
      cube.visible = false;
			const cube_box = new Three.BoxHelper( cube );
      const box_group = new Three.Group();
      box_group.add(cube);
      box_group.add(cube_box);

      if (this.box_group != null){
        this.scene.remove(this.box_group);
      }
      this.box_group = box_group;
      this.scene.add(this.box_group);
      
      console.log(cube.position);
      this.camera.lookAt(this.box_group.position.x,this.box_group.position.y,this.box_group.position.z);
      // this.camera.position.x = 
    },
    load_mesh(){

      var mesh_group = new Three.Group();
      for (let i=0;i<this.object.length;++i){
        if (this.object[i] != null){
          mesh_group.add(this.object[i]);
          // console.log(this.object[i].position)
        }
      }
      mesh_group.position.x = this.box_group.position.x;
      mesh_group.position.y = this.box_group.position.y;
      mesh_group.position.z = this.box_group.position.z;
      if (this.mesh_group != null){
        this.scene.remove(this.mesh_group);
      }
      this.mesh_group = mesh_group;
      this.scene.add(this.mesh_group);
      
    },
    db_raycaster(){
      //用于双击之后的显示处,用在animate中
      this.raycaster.setFromCamera(this.pointer, this.camera);
      const intersects = this.raycaster.intersectObjects(this.object,false);
      if (intersects.length > 0) {
        console.log(intersects);
        console.log(intersects[0].object);
        if (intersects[0].object != this.sel_object){
          //设置sel_object_change_state，避免animate更新
          this.sel_object_change_state = true;
          this.sel_object = intersects[0].object;
          this.gui_reinit();
          this.sel_object_change_state = false;
        }
      }
    },
    animate() {
      if (this.show) {
        this.db_raycaster();
        this.show = false;
      }

      this.animationId = requestAnimationFrame(this.animate);
      const delta = this.clock.getDelta();
      if ( this.helper.animating ) this.helper.update( delta );
      this.controls.update();
      this.renderer.clear();
      this.renderer.render(this.scene, this.camera);
      this.helper.render( this.renderer );
    },
    gui_reinit(){
      //用于生成GUI
      this.gui_parameters.opacity = this.sel_object.material.opacity;
      this.gui_parameters.color = this.sel_object.material.color;
      this.gui_parameters.visible = this.sel_object.material.visible;
      Array.from( this.gui.children ).forEach( c => c.destroy() );
      let idx = this.object.indexOf(this.sel_object);
      this.gui.title("第"+(idx+1)+"个对象");
      this.gui.add(this.gui_parameters, 'opacity', 0.1, 1, 0.01 ).onChange( this.gui_update );
      this.gui.addColor(this.gui_parameters, 'color').onChange( this.gui_update );
      this.gui.add(this.gui_parameters, 'visible').onChange( this.gui_update );
    },
    gui_update(){
      //用于GUI参数变更之后，对object的更新
      if (!this.sel_object_change_state){
        this.sel_object.material.opacity = this.gui_parameters.opacity;
        this.sel_object.material.color = this.gui_parameters.color;
        this.sel_object.material.visible = this.gui_parameters.visible;
      }
    }
  },
  mounted() {
    // this.Img = new Three.TextureLoader().load("/public/disc.png");

    this.init();
    this.animate();
  },
  destroyed() {
    if (this.animationId) {
      cancelAnimationFrame(this.animationId);
    }

    this.lights.forEach((light) => this.scene.remove(light));
    this.scene.clear();

    this.renderer.renderLists.dispose();
    this.renderer.dispose();
    this.renderer.forceContextLoss();
    this.renderer.domElement = null;
    this.renderer.content = null;
    this.renderer = null;
    this.camera = null;

    this.controls.dispose();
    this.controls = null;

    // Three.Cache.clear();
    window.removeEventListener("resize", this.scene_resize, false);
    console.log("clear scene " + this.sceneName + " content ");
  },
  watch: {
    // object(newT, oldT) {
    //   if (oldT === null) {
    //     this.scene.add(newT);
    //   } else {
    //     this.scene.remove(oldT);
    //     this.scene.add(newT);
    //   }
    // },
  },
};
</script>

<style>
.moudle-show-part {
  width: 100%;
  height: 100%;
}
.gui-show-part{
  width: 15%;
  height: 100%;
}
</style>