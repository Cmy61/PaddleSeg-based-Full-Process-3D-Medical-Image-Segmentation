<template>
	<div style="width:100%;height:100%;">
            <Split v-model="split1" mode="vertical" @on-moving="split_move" @on-move-end="split_move_end">
                <div slot="top" class="demo-split-pane">
                    <div style="width:100%;height:100%;">
                        <Split v-model="split2" @on-moving="split_move" @on-move-end="split_move_end">
                            <div slot="left" class="demo-split-pane">
                                <slice
                                ref="z_canvas"
                                type="z"
                                :height="dims.x"
                                :width="dims.y"
                                :show_height="dims.x/2"
                                :show_width="dims.y/2"
                                :Lpixel="Lpixel"
                                :Rpixel="Rpixel"
                                :show_origin_data="show_origin_datas.z"
                                :show_label_data="show_label_datas.z"
                                :label_dict="label_dict"
                                :color_show="color_show"
                                :next="next"
                                :pre="pre"
                                >
                                </slice>
                            </div>
                            <div slot="right" class="demo-split-pane">
                                <slice
                                ref="y_canvas"
                                type="y"
                                :height="dims.x"
                                :width="dims.z"
                                :show_height="dims.x/2"
                                :show_width="dims.z*512/90/2"
                                :Lpixel="Lpixel"
                                :Rpixel="Rpixel"
                                :show_origin_data="show_origin_datas.y"
                                :show_label_data="show_label_datas.y"
                                :label_dict="label_dict"
                                :color_show="color_show"
                                :next="next"
                                :pre="pre"
                                >
                                </slice>
                            </div>
                        </Split>
                    </div>
                </div>
                <div slot="bottom" class="demo-split-pane">
                    <div style="width:100%;height:100%;">
                        <Split v-model="split3" @on-moving="split_move" @on-move-end="split_move_end">
                            <div slot="left" class="demo-split-pane">
                                <slice
                                ref="x_canvas"
                                type="x"
                                :height="dims.z"
                                :width="dims.y"
                                :show_height="dims.z*512/90/2"
                                :show_width="dims.y/2"
                                :Lpixel="Lpixel"
                                :Rpixel="Rpixel"
                                :show_origin_data="show_origin_datas.x"
                                :show_label_data="show_label_datas.x"
                                :label_dict="label_dict"
                                :color_show="color_show"
                                :next="next"
                                :pre="pre"
                                >
                                </slice>
                            </div>
                            <div slot="right" class="demo-split-pane">
                                <SubScene1 
                                ref="scene_3D"
                                sceneName="object_test"
                                :object="meshs"
                                :dims="dims"
                                :pixel_dims="pixeldims"
                                :label_dict="label_dict"
                                >

                                </SubScene1>
                            </div>
                        </Split>
                    </div>
                    
                </div>
            </Split>
            
            <MarkingCanva
                :dialogMarkingVisible="dialogMarkingVisible"
                :change_visible="change_visible"
            ></MarkingCanva>
            

        
	</div>
</template>

<script>
import * as Nifti from 'nifti-reader-js';
import {getfile} from "@/api/index.js";
import * as THREE from "three/build/three";
import slice from '@/components/slice.vue';
import {STLLoader} from 'three/examples/jsm/loaders/STLLoader.js'
import SubScene1 from '../components/SubScene1.vue';
import {_throttle} from '@/utils/throttle.js'
import MarkingCanva from "@/components/MarkingCanva.vue"


	export default {
		components: {
			slice,
            SubScene1,
            MarkingCanva
		},
		data() {
			return {
                show_flag: false,   //是否展示的标签，当为true时进行展示
				nii_header: null,  	//label.nii的头部信息
				// dims:null,		   	//维度信息(x,y,z)
				pixeldims:{'x':0,'y':0,'z':0},		//像素长度信息
                origin_data:null,   //原始nii数据
				label_data: null,  	//label.nii的数据
				// label_list: null,  	//label的取值范围，之后变为字典格式  
				// select_dims:null,	//三视图中分别选择的x,y,z 
                show_label_datas:{x:new Array(),y:new Array(),z:new Array()},    //需要展示的标签数据，对应x,y,z
                show_origin_datas:{x:new Array(),y:new Array(),z:new Array()},   //需要展示的原始数据，对应x,y,z
                // label_to_color:null,    //label到color的查找表，rgba

                // 3D
                meshs : [],
				stl_loader : null,

                //split 组件用
                split1: 0.5,
                split2: 0.5,
                split3: 0.5,


                dialogMarkingVisible:false,
			}
		},

		props: {
            //标签图像路由
			label_url: {
				type: [String, Number],
				default: "http://localhost:8888/download/C:/Users/92090/Desktop/3D医学影像/base_train/labelsTr/test_label.nii", //默认值为空现在测试阶段
			},
            //原始图像路由
            origin_url: {
                type: [String, Number],
				default: "http://localhost:8888/download/C:/Users/92090/Desktop/3D医学影像/base_train/imagesTr/test.nii", //默认值为空现在测试阶段
            },
            //是否展现color（即是否展现标签）
            color_show:{
                type:Boolean,
                default: false
            },
            //窗宽窗位（WW,WL）
            WW:{
                type:Number,
                default: 255
            },
            WL:{
                type:Number,
                default: 0
            },
            dims:{
                default: {x:0,y:0,z:0}
            },
            select_dims:{
                default: {x:0,y:0,z:0}
            },
            //标签相关信息
            label_dict:{
                default:{}
            },
            //标签截面面积
            label_graph_space:{
                default:{}
            }
		},
        computed:{
            // 根据窗宽窗位计算需要将[Lpixel,Rpixel]映射至[0,255]
            Lpixel(){
                return Math.ceil(this.WL-this.WW/2)
            },
            Rpixel(){
                return Math.floor(this.WL+this.WW/2)
            },
            LRpixel(){
                return [this.Lpixel,this.Rpixel]
            },
            both_url() {
                const { origin_url, label_url } = this
                return {
                    origin_url,
                    label_url
                }
            }
        },
		watch: {
			both_url: {
				async handler(val) {
                    console.log(val);
                    if (val.label_url != '' && val.origin_url != ''){
                        this.show_flag = false;
                        await this.get_nii();
                        if (this.color_show){
                            await this.get_label();
                        }
                        await this.reinit();
                        await this.display();
                        await this.init_three();
                    }
                    else if (val.label_url == '' && val.origin_url != ''){
                        this.show_flag = false;
                        await this.get_nii();
                        await this.reinit();
                        await this.display();
                        await this.init_three();
                    }
                    else{
                        await this.clear();
                    }
				},
                deep: true
			},
            LRpixel:{
                handler(val){
                    this.display();
                },
                deep:true
            },
            select_dims:{
                handler(val){
                    this.display();
                },
                deep:true
            },
            label_dict:{
                handler(newV,oldV){
                    try {
                        this.display();
                        if (Object.keys(oldV).length != Object.keys(newV).length){
                            this.init_three();
                        }
                        else{
                            this.update_three(newV);
                        }
                    } catch (error) {
                        console.log(error)
                    }
                },
                deep:true
            },
            color_show:{
                async handler(newV,oldV){
                    if (newV && this.label_data == null){
                        await this.get_label();
                    }
                },
            }

		},
		async mounted() {
			// await this.get_nii();
            // await this.get_label();
            // this.display();
            // this.$nextTick(() => {
            //     this.show_flag = true;
            // });
            // const that = this;
            // this.$nextTick(() => {
            //     that.clear();
            // });
            console.log("OK");
            // document.body.style.overflow='hidden';
            const that = this;
			setTimeout(function() {
				that.clear();
                that.$forceUpdate();
			}, 100);
            // this.clear();
            // 3D
            this.stl_loader = new STLLoader();
            
		},
		methods: {
			async get_nii(){
				const data = await getfile(this.origin_url);
				const niftiHeader = Nifti.readHeader(data);
				this.nii_header = niftiHeader;
                console.log(niftiHeader)
				// this.dims = {'x':this.nii_header.dims[1],'y':this.nii_header.dims[2],'z':this.nii_header.dims[3]};
                this.dims.x = this.nii_header.dims[1];
                this.dims.y = this.nii_header.dims[2];
                this.dims.z = this.nii_header.dims[3];
                // this.select_dims = {'x':0,'y':0,'z':0};
                this.select_dims.x = 0;
                this.select_dims.y = 0;
                this.select_dims.z = 0;
                this.pixeldims.x = this.nii_header.pixDims[1];
                this.pixeldims.y = this.nii_header.pixDims[2];
                this.pixeldims.z = this.nii_header.pixDims[3];
				// this.pixeldims = {'x':this.nii_header.pixDims[1],'y':this.nii_header.pixDims[2],'z':this.nii_header.pixDims[3]};
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
				this.origin_data = typedData;
                this.show_origin_datas = {'x':new Array(this.dims.y * this.dims.z).fill(0),'y':new Array(this.dims.x * this.dims.z).fill(0),'z':new Array(this.dims.x * this.dims.y).fill(0)};
			},
            async get_label(){
                const data = await getfile(this.label_url);
                const niftiHeader = Nifti.readHeader(data);
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
				this.label_data = typedData;
				
                this.show_label_datas = {'x':new Array(this.dims.y * this.dims.z).fill(0),'y':new Array(this.dims.x * this.dims.z).fill(0),'z':new Array(this.dims.x * this.dims.y).fill(0)};
                // this.label_list = Array.from(new Set(typedData)).sort(function(a, b){return a-b});
                // const color_array = [0x000000,0xFF0000,0xFFA500,0xFF7F50,0xFAFAD2,0xBDB76B,0x7FFF00,0x9ACD32,0x3CB371,0xFF0000,0xAFEEEE,0x7B68EE,0xEE82EE,0xC0C0C0,0xDAA520];
                // this.label_to_color = {};
                // for (let i=0;i<this.label_list.length;++i){
                //     let this_color = new THREE.Color(color_array[this.label_list[i]]);
                //     this.label_to_color[this.label_list[i]] = [Math.round(this_color.r*255),Math.round(this_color.g*255),Math.round(this_color.b*255),255];
                // }
                // console.log(this.label_to_color);
            },
            //获得数据后，初始化画布
            reinit(){
                this.$refs.x_canvas.init();
                this.$refs.y_canvas.init();
                this.$refs.z_canvas.init();
            },
            clear(){
                this.$refs.x_canvas.clear();
                this.$refs.y_canvas.clear();
                this.$refs.z_canvas.clear();
                this.dims.x = 0;
                this.dims.y = 0;
                this.dims.z = 0;
                this.select_dims.x = 0;
                this.select_dims.y = 0;
                this.select_dims.z = 0;
            },
            display:_throttle(function(){
                this.change_data('x');
                this.change_data('y');
                this.change_data('z');
            },45),
            change_data(type){
                let index;
                let label_map = {0:0,1:0,2:0,3:0,4:0,5:0,6:0,7:0,8:0,9:0,10:0,11:0,12:0,13:0,14:0,15:0};
                let flag = (Object.keys(this.label_dict).length != 0) && this.label_data && (this.label_data.length != 0);
                
                if (type=='x'){
                    for (let k=0;k<this.dims.z;++k){ 
                        for (let j=0;j<this.dims.y;++j){
                            index = k * this.dims.x * this.dims.y + this.select_dims.x * this.dims.y + j;
                            if (this.color_show){
                                this.show_label_datas.x[k*this.dims.y + j] = this.label_data[index];
                            }
                            if (flag){
                                ++label_map[this.label_data[index]];
                            }
                            this.show_origin_datas.x[k*this.dims.y + j] = this.origin_data[index];
                        }
                    }
                    this.$refs.x_canvas.display();
                    for (let i=1;i<=15;++i){
                        this.label_graph_space[i][0] = label_map[i] * this.pixeldims.y * this.pixeldims.z / 100;
                    }
                    this.$forceUpdate();
                    
                }
                else if (type=='y'){
                    for (let i=0;i<this.dims.x;++i){ 
                        for (let k=0;k<this.dims.z;++k){
                            index = k * this.dims.x * this.dims.y + i * this.dims.y + this.select_dims.y;
                            if (this.color_show){
                                this.show_label_datas.y[i*this.dims.z + k] = this.label_data[index];
                            }
                            if (flag){
                                ++label_map[this.label_data[index]];
                            }
                            this.show_origin_datas.y[i*this.dims.z + k] = this.origin_data[index];
                        }
                    }
                    this.$refs.y_canvas.display();
                    for (let i=1;i<=15;++i){
                        this.label_graph_space[i][1] = label_map[i] * this.pixeldims.x * this.pixeldims.z / 100;
                    }
                    this.$forceUpdate();
                }
                else if (type=='z'){
                    for (let i=0;i<this.dims.x;++i){ 
                        for (let j=0;j<this.dims.y;++j){
                            index = this.select_dims.z * this.dims.x * this.dims.y +  i * this.dims.y + j;
                            if (this.color_show){
                                this.show_label_datas.z[i*this.dims.y + j] = this.label_data[index];
                            }
                            if (flag){
                                ++label_map[this.label_data[index]];
                            }
                            this.show_origin_datas.z[i*this.dims.y + j] = this.origin_data[index];
                        }
                    }
                    this.$refs.z_canvas.display();
                    for (let i=1;i<=15;++i){
                        this.label_graph_space[i][2] = label_map[i] * this.pixeldims.x * this.pixeldims.y / 100;
                    }
                    this.$forceUpdate();
                }
            },
             //下一张
			next(type){
				if (this.select_dims[type] < this.dims[type] - 1){
					this.select_dims[type] += 1;
                    this.change_data(type);
				}
				
			},
            //上一张
			pre(type){
				if (this.select_dims[type] > 0){
					this.select_dims[type] -= 1;
                    this.change_data(type);
				}
				
			},
            async init_three(){
				// const url_path = 'http://localhost:8888/download/C:/Users/92090/Desktop/3D_medical/后端/nii2stl/0c593893-56d7-4169-8f8e-703d9b205196_';
				// const url_path = "http://localhost:8888/path/C:/Users/92090/Desktop/test_pro3d/test.stl";
				const label_array = Object.keys(this.label_dict);
				// var color_array = [0xFFA07A,0xCD5C5C,0xFFA500,0xFF7F50,0xFAFAD2,0xBDB76B,0x7FFF00,0x9ACD32,0x3CB371,0xE0FFFF,0xAFEEEE,0x7B68EE,0xEE82EE,0xC0C0C0,0xDAA520];
				// const color_array = [0xFF0000,0xFFA500,0xFF7F50,0xFAFAD2,0xBDB76B,0x7FFF00,0x9ACD32,0x3CB371,0xFF0000,0xAFEEEE,0x7B68EE,0xEE82EE,0xC0C0C0,0xDAA520];
                // const suffix = '.stl'
                if (label_array.length !== 0 && this.label_dict[label_array[0]].stl_path != null && this.label_dict[label_array[0]].stl_path.length != 0){

                    for (let i = 0; i < label_array.length; ++i){
                        let label = label_array[i];
                        let label_info = this.label_dict[label];
                        console.log(label_info)
                        const binary_stl = await getfile('http://localhost:8888/download/' + label_info.stl_path);
                        var geometry = this.stl_loader.parse(binary_stl);
                        var mat = new THREE.MeshStandardMaterial({
                            color: new THREE.Color(label_info.r/255,label_info.g/255,label_info.b/255),
                            side: THREE.DoubleSide,
                            opacity: label_info.opacity,
                            transparent: true,
                            flatShading: THREE.SmoothShading,
                            visible: label_info.visible
                        });
                        var mesh = new THREE.Mesh(geometry, mat);
                        this.meshs.push(mesh);
                    }
                }
				

                this.$refs.scene_3D.load_box();
                this.$refs.scene_3D.load_mesh();
                this.$refs.scene_3D.scene_resize();
				

			},
            update_three(new_label_dict){
                const label_array = Object.keys(new_label_dict);
                try {
                    for (let i = 0; i < label_array.length; ++i){
                        let label = label_array[i];
                        
                        let label_info = this.label_dict[label];
                        this.meshs[i].material.color = new THREE.Color(label_info.r/255,label_info.g/255,label_info.b/255);
                        this.meshs[i].material.opacity = label_info.opacity;
                        this.meshs[i].material.visible = label_info.visible;
                    }
                } catch (error) {
                    this.init_three();
                }
                
            },

            split_move: _throttle(function () {
                // await this.$nextTick();
                this.$refs.x_canvas.resize_canvas();
                this.$refs.y_canvas.resize_canvas();
                this.$refs.z_canvas.resize_canvas();
                this.$refs.scene_3D.scene_resize();
            }, 25),
            // split_move(){
            //     this.$refs.x_canvas.resize_canvas();
            //     this.$refs.y_canvas.resize_canvas();
            //     this.$refs.z_canvas.resize_canvas();
            // },

            split_move_end(){
                console.log(1)
                // await this.$nextTick();
                this.$refs.x_canvas.resize_canvas();
                this.$refs.y_canvas.resize_canvas();
                this.$refs.z_canvas.resize_canvas();
                this.$refs.scene_3D.scene_resize();
            },
            change_visible(val){
                this.dialogMarkingVisible = val;
            },
        }
		
	}
</script>

<style>
    .demo-split-pane{
        height:100%;
        width:100%;
        padding: 10px;
    }
</style>

