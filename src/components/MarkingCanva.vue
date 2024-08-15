<template>
    <el-dialog title="预标注修改" :visible.sync="dialogMarkingVisible" :before-close="handleDialogClose" width="60%"> 
        
        <div>
            <el-select v-model="choose_label" placeholder="请选择画笔的标签" style="width:160px;;margin-right:2%;">
                <el-option
                    v-for="(v,k,idx) in $parent.label_dict"
                    :key="'markin_canva_123'+k"
                    :label="$parent.$parent.label_chinese_name[k]"
                    :value="k">
                </el-option>
                
            </el-select>
            <el-select v-model="lineWidth" placeholder="请选择画笔粗细" style="width:170px;margin-left:1%;margin-right:2%;">
                <el-option
                    label="1px"
                    value="1">
                </el-option>
                <el-option
                    label="2px"
                    value="2">
                </el-option>
                <el-option
                    label="5px"
                    value="5">
                </el-option>
                <el-option
                    label="8px"
                    value="8">
                </el-option>
                <el-option
                    label="12px"
                    value="12">
                </el-option>
                <el-option
                    label="15px"
                    value="15">
                </el-option>
                <el-option
                    label="20px"
                    value="20">
                </el-option>
            </el-select>
            <!-- <select name="" id="line-width" style="margin-left:7%;margin-right:5%;">
                <option value="1">-- 1 px --</option>
                <option value="2">-- 2 px --</option>
                <option value="5">-- 5 px --</option>
                <option value="8">-- 8 px --</option>
                <option value="12">-- 12px --</option>
                <option value="15">-- 15px --</option>
            </select> -->
            <el-button
                id="btnErase"
                @click="erase_click"
            >
                <span v-if="erase">切换画笔</span>
                <span v-else>切换橡皮擦</span>
            </el-button>

            <div style="margin-top:1%;margin-bottom:1%;">
                <el-button
                    id="btnClear"
                    @click="btn_click"
                    style="margin-right:10%;margin-left:3%;"
                >
                    清除画布
                </el-button>

                <el-button
                    id="return"
                    @click="returnStep_click"
                    style="margin-right:4%;"
                >
                    返回上一步
                </el-button>

                <el-button
                    id="save"
                    @click="save_click"
                >
                    保存标注
                </el-button>
            </div>
            
            

            <!-- <input 
                type="button" 
                value="橡皮擦" 
                id="btnErase"
                @click="erase_click"
                > -->
            <!-- <input 
                type="button" 
                value="清除画布" 
                id="btnClear"
                @click="btn_click"
                > -->
            <!-- <input 
                type="button" 
                value="返回上一步" 
                id="return"
                @click="returnStep_click"
                > -->
            <!-- <input 
                type="button" 
                value="保存标注" 
                id="save"
                @click="save_click"
                > -->
            <div style="position:relative;height:510px;width:510px;">
                <canvas 
                    id="marking_canvas" 
                    :width="width" 
                    :height="height" 
                    style="display: block;border: 3px black solid;position:absolute;top:5;left:2;z-index:2;"
                    @mousedown="canvas_mousedown"
                    @mouseup="canvas_mouseup"
                    @mouseout="canvas_mouseout"
                    @mousemove="canvas_mousemove"
                >
                </canvas>
                <canvas
                    id="marking_origin_canvas"
                    :width="width" 
                    :height="height"
                    style="display: block;border: 3px black solid;position:absolute;top:5;left:2;z-index:1"
                >

                </canvas>
            </div>

            <div style="margin-top:2%;margin-bottom:1%;margin-left:10%;">
                <el-button icon="el-icon-arrow-left" @click="pre">上一页</el-button>
                {{ '&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp'+$parent.select_dims.z+'&nbsp/&nbsp '+$parent.dims.z+'&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp' }}
                <el-button @click="next">下一页<i class="el-icon-arrow-right el-icon--right"></i></el-button>
            </div>
        </div>
        
    </el-dialog>
	<!-- <div style="width:506px;margin:50px auto;">
        
        
    </div> -->
</template>

<script>
import * as Three from "three";

	export default {
		components: {
			
		},
		data() {
			return {
                //在slice内部隐藏的canvas，数据直接复用
                oral_canvas:null,
                //
                canvas:null,
                context:null,
                //将所有像素点信息存储在数组中，后续返回上一步时可用到
                restore:null,
                //获取画笔宽度
                lineWidth:null,
                btn:null,
                returnStep:null,
                save:null,
                isDraw:null,

                erase:false,
                r:5,


                //CT

                width:512,
                height:512,
                type2color:{},
                //选择的label
                choose_label:null,

			}
		},
        computed:{
            color(){
                if (this.choose_label){
                    let label_item = this.$parent.label_dict[this.choose_label];
                    let item = new Three.Color("rgb(" + label_item.r +", "+label_item.g+", "+label_item.b+")");
                    return "#"+item.getHexString();
                }
                else {
                    return "#000000";
                }
                
            }
        },
		props: {
            dialogMarkingVisible:{
                default:false
            },
            change_visible:{
                default: ()=>{console.log("111")}
            }
        },
		watch: {
			dialogMarkingVisible:{
                handler(newV,oldV){
                    if (newV){
                        this.$nextTick(()=>{
                            this.init()
                        })
                    }
                }
            }
		},
		mounted() {
            
		
		},
		methods: {
            init(){
                this.oral_canvas = document.getElementById("tutorial"+'z')
                //
                this.canvas = document.getElementById("marking_canvas");
                this.context = this.canvas.getContext("2d");
                this.context.clearRect(0,0,this.width,this.height);
                
                //将所有像素点信息存储在数组中，后续返回上一步时可用到
                this.restore = [this.oral_canvas.getContext("2d").getImageData(0, 0, this.width, this.height)];
        
                //获取画笔颜色
                // this.color = document.getElementById("color");
                //获取画笔宽度
                // this.lineWidth = document.getElementById("line-width");
                this.btn = document.getElementById("btnClear");
                this.returnStep = document.getElementById("return");
                // this.save = document.getElementById("save");
                this.isDraw = false;
                //橡皮擦
                this.erase = false;
                this.r = this.lineWidth;

                const origin_canvas = document.getElementById("marking_origin_canvas");
                const origin_ctx = origin_canvas.getContext("2d");
                origin_ctx.putImageData(this.oral_canvas.getContext("2d").getImageData(0, 0, this.width, this.height),0,0);

                this.type2color = {};
                let label_dict_keys = Object.keys(this.$parent.label_dict)
                for (let i=0;i<label_dict_keys.length;++i){
                    let label_key = label_dict_keys[i];
                    let item = this.$parent.label_dict[label_key];
                    this.type2color[label_key] = [item.r,item.g,item.b,255];
                }
            },
            handleDialogClose(){
                let that = this;
                this.$confirm('确定退出吗？')
                .then(_ => {
                    that.change_visible(false);
                })
                .catch(_ => {});
            },
            canvas_mousedown(event){
                this.isDraw = true;
                if (this.erase){
                    this.r = this.lineWidth;
                }
                else {
                    this.context.lineWidth = this.lineWidth;
                    this.context.strokeStyle = this.color;
    
                    this.context.beginPath();
                    this.context.moveTo(event.offsetX, event.offsetY);
                }
                
            },
            canvas_mousemove(event){
                if (this.isDraw) {
                    if (this.erase){
                        this.context.save();
                        var x = event.offsetX;
                        var y = event.offsetY;
                        this.context.beginPath();
                        this.context.arc(x, y, this.r, 0, 2 * Math.PI);
                        this.context.clip();
                        this.context.clearRect(0,0,this.width,this.height);
                        this.context.closePath();
                        this.context.restore();
                    }
                    else {
                        this.context.lineTo(event.offsetX, event.offsetY);
                        this.context.stroke();
                    }
                    
                }
            },
            canvas_mouseup(event){
                this.isDraw = false;
                //将此时绘制的信息存储到restore数组中
                this.restore[this.restore.length] = this.context.getImageData(0, 0, this.canvas.width, this.canvas.height);
            },
            canvas_mouseout(event){
                if (this.isDraw){
                    this.isDraw = false;
                    this.restore[this.restore.length] = this.context.getImageData(0, 0, this.canvas.width, this.canvas.height);
                }
            },
            btn_click(event){
                this.context.clearRect(0, 0, this.canvas.width, this.canvas.height);
                this.restore[this.restore.length] = this.context.getImageData(0, 0, this.canvas.width, this.canvas.height);
            },
            returnStep_click(event){
                if (this.restore.length > 1) {
                    this.context.putImageData(this.restore[this.restore.length - 2], 0, 0);
                    this.restore.length--;
                }
            },
            erase_click(event){
                this.erase = !this.erase;
            },
            save_click(event){
                var margin_pixel_data = document.getElementById("marking_canvas").getContext("2d").getImageData(0,0,this.width,this.height);
                var margin_origin_pixel_data = document.getElementById("marking_origin_canvas").getContext("2d").getImageData(0,0,this.width,this.height);
                console.log(margin_pixel_data);
                console.log(margin_origin_pixel_data);
                // const type2color = {1:[0,0,0,255],2:[255,0,0,255],3:[255,255,255,255]};
                const types = Object.keys(this.type2color);
                for (let i=0;i<this.width;++i){
                    for (let j=0;j<this.height;++j){
                        let index = (i*this.height + j)*4;
                        // 没有上色的部分，不考虑
                        if (margin_pixel_data.data[index+3] === 0){
                            continue;
                        }
                        else {
                            for (let m=0;m<types.length;++m){
                                let label_type = types[m];
                                let color_arr = this.type2color[label_type];
                                let flag = true; // 是否匹配
                                for (let n=0;n<4;++n){
                                    if (margin_pixel_data.data[index + n] != color_arr[n]){
                                        flag = false;
                                        break;
                                    }
                                }
                                if (flag){
                                    for (let n=0;n<4;++n){
                                        margin_origin_pixel_data.data[index + n] = margin_pixel_data.data[index + n]
                                        this.$parent.label_data[this.$parent.select_dims.z * this.$parent.dims.x * this.$parent.dims.y +  i * this.$parent.dims.y + j] = types[m];
                                    }
                                    break;
                                }
                            }
                        }
                    }
                }
                // 改变背景，清空上层canvas内容。
                document.getElementById("marking_origin_canvas").getContext("2d").clearRect(0,0,this.width,this.height);
                document.getElementById("marking_origin_canvas").getContext("2d").putImageData(margin_origin_pixel_data,0,0);
                document.getElementById("marking_canvas").getContext("2d").clearRect(0,0,this.width,this.height);
            },
            pre(){
                this.$parent.pre('z');
                this.restore.length = 0;
                this.restore.push(this.oral_canvas.getContext("2d").getImageData(0, 0, this.width, this.height))
                document.getElementById("marking_origin_canvas").getContext("2d").clearRect(0,0,this.width,this.height);
                document.getElementById("marking_origin_canvas").getContext("2d").putImageData(this.oral_canvas.getContext("2d").getImageData(0, 0, this.width, this.height),0,0);
                document.getElementById("marking_canvas").getContext("2d").clearRect(0,0,this.width,this.height);
            },
            next(){
                this.$parent.next('z');
                this.restore.length = 0;
                this.restore.push(this.oral_canvas.getContext("2d").getImageData(0, 0, this.width, this.height))
                document.getElementById("marking_origin_canvas").getContext("2d").clearRect(0,0,this.width,this.height);
                document.getElementById("marking_origin_canvas").getContext("2d").putImageData(this.oral_canvas.getContext("2d").getImageData(0, 0, this.width, this.height),0,0);
                document.getElementById("marking_canvas").getContext("2d").clearRect(0,0,this.width,this.height);
            }
    	},
			
			
		
	}
</script>

<style lang="scss" scoped>

</style>

