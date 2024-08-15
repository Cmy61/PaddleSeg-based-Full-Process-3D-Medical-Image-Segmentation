<template>
	<!-- <div>
		<el-button @click="init_three">111</el-button>
	</div> -->
	<div style="width:1000px;height:500px;">
        <SubScene1 
        sceneName="object"
        :object="meshs"
		v-if="meshs.length === 13">

        </SubScene1>
    </div>

</template>

<script>
    import * as THREE from 'three';
	import {STLLoader} from 'three/examples/jsm/loaders/STLLoader.js'
    import SubScene1 from '../components/SubScene1.vue';

	import {getfile} from '@/api/index.js'



	export default {
		components: {
			SubScene1,
		},
		data() {
			return {
                meshs : [],
				stl_loader : null,
            }
		},
		props: {
			
		},
		watch: {
			
		},
		mounted() {
			this.stl_loader = new STLLoader();
            this.init_three();
		},
		methods: {
			async init_three(){
				const url_path = 'http://localhost:8888/path/C:/Users/92090/Desktop/3D医学影像/后端/nii2stl/0c593893-56d7-4169-8f8e-703d9b205196_';
				// const url_path = "http://localhost:8888/path/C:/Users/92090/Desktop/test_pro3d/test.stl";
				const label_array = [1,2,3,4,5,6,7,8,9,10,11,12,13];
				var color_array = [0xFFA07A,0xCD5C5C,0xFFA500,0xFF7F50,0xFAFAD2,0xBDB76B,0x7FFF00,0x9ACD32,0x3CB371,0xE0FFFF,0xAFEEEE,0x7B68EE,0xEE82EE,0xC0C0C0,0xDAA520];
				const suffix = '.stl'

				for (let i = 0; i < label_array.length; ++i){
					let label = label_array[i];
					const binary_stl = await getfile(url_path+label+suffix);
					var geometry = this.stl_loader.parse(binary_stl);
					var mat = new THREE.MeshStandardMaterial({
						color: color_array[i],
						side: THREE.DoubleSide,
						opacity: 0.9,
						transparent: true,
						flatShading: THREE.SmoothShading,
						alphaTest:0.1,
						depthTest:true
					});
    				var mesh = new THREE.Mesh(geometry, mat);
					this.meshs.push(mesh);
				}
				

			}


		},
        
	}
</script>

<style>

</style>

