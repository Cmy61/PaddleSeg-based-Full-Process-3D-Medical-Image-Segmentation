<template>
	<div class="width:100%;height:100%;">
		<!-- <el-button @click="pre()">上一张</el-button>
		<el-button @click="next()">下一张</el-button> -->
		<canvas id="tutorial" style="display:none;">

		</canvas>
		<canvas id="tutorial-show" @mousewheel="handleScroll($event,'z')">

		</canvas>
	</div>
</template>

<script>
import * as Nifti from 'nifti-reader-js';
import {getfile} from "@/api/index.js";
import * as THREE from "three/build/three";
	export default {
		components: {
			
		},
		data() {
			return {
				nii_header: null,  	//label.nii的头部信息
				dims:null,		   	//维度信息(x,y,z)
				pixeldims:null,		//像素长度信息
				label_data: null,  	//label.nii的数据
				label_list: null,  	//label的取值范围，之后变为字典格式
				image_data:null,
				select_dims:null,	//三视图中分别选择的x,y,z 
			}
		},

		props: {
			Select_url: {
				type: [String, Number],
				default: "http://localhost:8888/path/C:/Users/92090/Desktop/3D医学影像/base_train/labelsTr/test_label.nii", //默认值为空现在测试阶段
			},
		},
		watch: {
			Select_url: {
				handler(val) {
                    if (this.Select_url){
						this.get_nii();
                        this.display();
                    }
				},
			}
		},
		async mounted() {
			await this.get_nii();
			const canvas = document.getElementById("tutorial");
			canvas.width = this.dims.x;
			canvas.height = this.dims.y;
			const ctx = canvas.getContext("2d");
			console.log(ctx);

			const canvas_show = document.getElementById("tutorial-show");
			canvas_show.width = this.dims.x;
			canvas_show.height = this.dims.y;
			const ctx_show = canvas_show.getContext("2d");
			
			this.image_data = ctx.createImageData(this.dims.x, this.dims.y);
			
			const data = this.image_data.data;
			console.log(this.image_data);
			for (let i=0;i<this.dims.x;++i){
				for (let j=0;j<this.dims.y;++j){
					data[i*150*4+j*4] = 255;
					data[i*150*4+j*4+1] = 0;
					data[i*150*4+j*4+2] = 0;
					data[i*150*4+j*4+3] = 255;
				}
			}
			ctx.putImageData(this.image_data, 0, 0);
			
			
			this.select_dims = {'x':0,'y':0,'z':9};
			ctx.scale(2,2);
			this.display();
			
		},
		methods: {
			async get_nii(){
				const data = await getfile('http://localhost:8888/path/C:/Users/92090/Desktop/3D医学影像/base_train/labelsTr/test_label.nii');
				const niftiHeader = Nifti.readHeader(data);
				this.nii_header = niftiHeader;
				this.dims = {'x':this.nii_header.dims[1],'y':this.nii_header.dims[2],'z':this.nii_header.dims[3]};
				this.pixeldims = {'x':this.nii_header.pixDims[1],'y':this.nii_header.pixDims[2],'z':this.nii_header.pixDims[3]};
				console.log(this.nii_header);
				const niftiImage = Nifti.readImage(niftiHeader, data);
				
				var typedData;

				if (niftiHeader.datatypeCode === Nifti.NIFTI1.TYPE_UINT8) {
					typedData = new Uint8Array(niftiImage);
				} else if (niftiHeader.datatypeCode === Nifti.NIFTI1.TYPE_INT16) {
					typedData = new Int16Array(niftiImage);
				} else if (niftiHeader.datatypeCode === Nifti.NIFTI1.TYPE_INT32) {
					typedData = new Int32Array(niftiImage);
				} else if (niftiHeader.datatypeCode === Nifti.NIFTI1.TYPE_FLOAT32) {
					typedData = new Float32Array(niftiImage);
				} else if (niftiHeader.datatypeCode === Nifti.NIFTI1.TYPE_FLOAT64) {
					typedData = new Float64Array(niftiImage);
				} else if (niftiHeader.datatypeCode === Nifti.NIFTI1.TYPE_INT8) {
					typedData = new Int8Array(niftiImage);
				} else if (niftiHeader.datatypeCode === Nifti.NIFTI1.TYPE_UINT16) {
					typedData = new Uint16Array(niftiImage);
				} else if (niftiHeader.datatypeCode === Nifti.NIFTI1.TYPE_UINT32) {
					typedData = new Uint32Array(niftiImage);
				} else {
					return;
				}

				console.log(typedData);

				this.label_data = typedData;
				this.label_list = Array.from(new Set(typedData)).sort(function(a, b){return a-b});
				console.log(this.label_list);
			},
			display(){
				// this.display_no_rgb();
				// return;
				const color_array = [0x000000,0xFF0000,0xFFA500,0xFF7F50,0xFAFAD2,0xBDB76B,0x7FFF00,0x9ACD32,0x3CB371,0xFF0000,0xAFEEEE,0x7B68EE,0xEE82EE,0xC0C0C0,0xDAA520];
				// const data = this.image_data.data;
				const canvas = document.getElementById("tutorial");
				const ctx = canvas.getContext("2d");
				// const image_data = ctx.getImageData(0,0,this.dims.x, this.dims.y);
				const data = this.image_data.data;
				
				for (let i=0;i<this.dims.x*this.dims.y;++i){
					const this_color = new THREE.Color(color_array[this.label_data[this.select_dims.z *this.dims.x*this.dims.y + i]]);
					// if (this.select_dims.z == 10){
						
					// }
					// if (this.label_data[this.select_dims.z *this.dims.x*this.dims.y + i] != 0){
					// 	this_color = new THREE.Color(0xFF0000);
					// 	// console.log(this.label_data[this.select_dims.z *this.dims.x*this.dims.y + i]);
					// 	// console.log(this_color.r);
					// 	// console.log(this_color.g);
					// 	// console.log(this_color.b);
					// }
					data[i*4] = Math.round(this_color.r*255);
					data[i*4 + 1] = Math.round(this_color.g*255);
					data[i*4 + 2] = Math.round(this_color.b*255);
					data[i*4 + 3] = 255;
				}
				
				ctx.putImageData(this.image_data, 0, 0);
				const canvas_show = document.getElementById("tutorial-show");
				const ctx_show = canvas_show.getContext("2d");
				ctx_show.drawImage(canvas,0,0,512,512,0,0,256,256);
				console.log(this.select_dims.z);
				// console.log(ctx);
			},
			display_no_rgb(){
				const canvas = document.getElementById("tutorial");
				const ctx = canvas.getContext("2d");
				// const image_data = ctx.getImageData(0,0,this.dims.x, this.dims.y);
				const data = this.image_data.data;
				const label_min = this.label_list[0]
				const label_max_minus_min = this.label_list[this.label_list.length-1] - this.label_list[0];
				
				for (let i=0;i<this.dims.x*this.dims.y;++i){
					const this_color = (this.label_data[this.select_dims.z *this.dims.x*this.dims.y + i] - label_min)*255/label_max_minus_min;
					// if (this.select_dims.z == 10){
						
					// }
					// if (this.label_data[this.select_dims.z *this.dims.x*this.dims.y + i] != 0){
					// 	this_color = new THREE.Color(0xFF0000);
					// 	// console.log(this.label_data[this.select_dims.z *this.dims.x*this.dims.y + i]);
					// 	// console.log(this_color.r);
					// 	// console.log(this_color.g);
					// 	// console.log(this_color.b);
					// }
					data[i*4] = this_color;
					data[i*4 + 1] = this_color;
					data[i*4 + 2] = this_color;
					data[i*4 + 3] = 255;
				}
				ctx.putImageData(this.image_data, 0, 0);
				const canvas_show = document.getElementById("tutorial-show");
				const ctx_show = canvas_show.getContext("2d");
				ctx_show.drawImage(canvas,0,0,512,512,0,0,256,256);

				console.log(this.select_dims.z);
			},
			next(type){
				if (this.select_dims[type] < this.dims[type] - 1){
					this.select_dims[type] += 1;
				}
				this.display();
			},
			pre(type){
				if (this.select_dims[type] > 0){
					this.select_dims[type] -= 1;
				}
				this.display();
			},
			//节流函数
			// debounce(fn,interval) {
			// 	let timeout = null; // 创建一个标记用来存放定时器的返回值
			// 	return function () {
			// 		clearTimeout(timeout); // 每当用户输入的时候把前一个 setTimeout clear 掉
			// 		timeout = setTimeout(() => {
			// 			// 然后又创建一个新的 setTimeout, 这样就能保证输入字符后的
			// 			// interval 间隔内如果还有字符输入的话，就不会执行 fn 函数
			// 			fn.apply(this, arguments);
			// 		}, interval);
			// 	}
			// },
			//鼠标滚轮滑动事件,未封装节流
			handleScroll(e,type){
				let direction = e.deltaY > 0 ? 'down':'up';
				console.log(direction);
				if (direction == 'down'){
					this.next(type);
				}
				else if (direction == "up"){
					this.pre(type);
				}
			},
			// //封装节流的滚轮滑动事件
			// handleScroll_debounce(e,type){
			// 	this.debounce(this.handleScroll(e,type),2000);
			// }


    	},
			
			
		
	}
</script>

<style scoped>
	.nifti-image-container{
		display: flex;
		flex-flow: row wrap;
		width: 100%;
		height: auto;
	}
	.nifti-image {
		margin: 30px 10px 10px 20px;
		width: 400px;
		height: 200px;
	}
	.dicom-info{
		color: #FFFFFF;
		position: absolute;
		bottom: 20px;
		left: 40px;
		z-index: 11;
	}
</style>

