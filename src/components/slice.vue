<template>
	<!-- 注意，该组件外部传参的show_width，height等已无用 -->
	<div class="slice-wrap" :id="'canvas-div-wrap-'+type">
		<canvas :id="'tutorial'+type" style="display:none;">

		</canvas>
        <div class="canvas-div-wrap" >
            <canvas :id="'tutorial-show'+type" @mousewheel="handleScroll($event,type)">

            </canvas>
        </div>
		
	</div>
</template>

<script>
import * as THREE from "three/build/three";
	export default {
		components: {
			
		},
		data() {
			return {
                // 隐藏的真实像素canvas
				canvas:null,
                cts:null,
                // 用于展示的canvas
                show_canvas:null,
                show_ctx:null,
                // canvas的像素点数据
                canvas_pixel_data:null,

				clear_flag:false, // 是否执行了clear。当执行init之后，设置为false。
                
			}
		},
        computed:{
            
        },

		props: {
            //显示的2D canvas类型，x,y,z
            type:null,
            // 像素宽度,用于canvas
            width:null,
            //像素高度,用于canvas
            height:null,
            //展示宽度,用于show_canvas
            show_width:null,
            //展示高度,用于show_canvas
            show_height:null,
			//展示的原始数据
			show_origin_data:null,
			//展示的窗宽窗位计算出需要映射至[0,255]的范围[Lpixel,Rpixel]
			Lpixel:null,
			Rpixel:null,
            //展示的标签数据
            show_label_data:null,
            //标签对应的属性
            label_dict:null,
			//是否展现颜色，或者说标签
			color_show:null,
            // //是否强制更新canvas(调用display)
            // update:Boolean,
			//翻页函数
			next:null,
			pre:null,
        },
		watch: {
			color_show:{
				handler(val){
					const that = this;
					this.$nextTick(()=>{
						that.display();
					})
					
				}
			}
		},
		mounted() {
			this.canvas = document.getElementById("tutorial"+this.type);
			this.ctx = this.canvas.getContext("2d");
			this.canvas_show = document.getElementById("tutorial-show"+this.type);
			this.ctx_show = this.canvas_show.getContext("2d");
			
			
		},
		methods: {
            //展示图像
			display(){
				const data = this.canvas_pixel_data.data;
				
				if (this.color_show){
					//优先上色，type为0的则改为基于窗位窗宽展现原始图像的灰度图
					for (let i=0;i<this.width * this.height;++i){
						if (this.show_label_data[i] in this.label_dict){
							data[i*4] = this.label_dict[this.show_label_data[i]].r;
							data[i*4 + 1] = this.label_dict[this.show_label_data[i]].g;
							data[i*4 + 2] = this.label_dict[this.show_label_data[i]].b;
							data[i*4 + 3] = 255;
						}
						else{
							if (this.show_origin_data[i] <= this.Lpixel){
								data[i*4] = 0;
								data[i*4 + 1] = 0;
								data[i*4 + 2] = 0;
								data[i*4 + 3] = 255;
							}
							else if ((this.show_origin_data[i] >= this.Rpixel)){
								data[i*4] = 255;
								data[i*4 + 1] = 255;
								data[i*4 + 2] = 255;
								data[i*4 + 3] = 255;
							}
							else {
								let pixel_color = Math.round((this.show_origin_data[i] - this.Lpixel)/(this.Rpixel-this.Lpixel) * 255);
								data[i*4] = pixel_color;
								data[i*4 + 1] = pixel_color;
								data[i*4 + 2] = pixel_color;
								data[i*4 + 3] = 255;
							}
						}
					}
				}
				else{
					for (let i=0;i<this.width * this.height;++i){
						if (this.show_origin_data[i] <= this.Lpixel){
							data[i*4] = 0;
							data[i*4 + 1] = 0;
							data[i*4 + 2] = 0;
							data[i*4 + 3] = 255;
						}
						else if ((this.show_origin_data[i] >= this.Rpixel)){
							data[i*4] = 255;
							data[i*4 + 1] = 255;
							data[i*4 + 2] = 255;
							data[i*4 + 3] = 255;
						}
						else {
							let pixel_color = Math.round((this.show_origin_data[i] - this.Lpixel)/(this.Rpixel-this.Lpixel) * 255);
							data[i*4] = pixel_color;
							data[i*4 + 1] = pixel_color;
							data[i*4 + 2] = pixel_color;
							data[i*4 + 3] = 255;
						}
					}
				}
				
				const wrap = document.getElementById('canvas-div-wrap-'+this.type)
				const show_width = wrap.offsetWidth;
				const show_height = wrap.offsetHeight;
				this.ctx.putImageData(this.canvas_pixel_data, 0, 0);
				this.canvas_show.width = show_width;
				this.canvas_show.height = show_height;
			    this.ctx_show.drawImage(this.canvas,0,0,this.width,this.height,0,0,show_width,show_height);
			},
           
			//鼠标滚轮滑动事件,未封装节流
			handleScroll(e,type){
				if (this.clear_flag){
					return;
				}
				else {
					let direction = e.deltaY > 0 ? 'down':'up';
					// console.log(direction);
					if (direction == 'down'){
						this.next(type);
					}
					else if (direction == "up"){
						this.pre(type);
					}
				}
				
			},
			resize_canvas(){
				const wrap = document.getElementById('canvas-div-wrap-'+this.type)
				const show_width = wrap.offsetWidth;
				const show_height = wrap.offsetHeight;
				this.canvas_show.width = show_width;
				this.canvas_show.height = show_height;
				if (this.clear_flag){
					this.ctx_show.drawImage(this.canvas,0,0,150,150,0,0,show_width,show_height);
				}
				else {
					this.ctx_show.drawImage(this.canvas,0,0,this.width,this.height,0,0,show_width,show_height);
				}
				
			},
			//清空画布，或者显示黑色
			clear(){
				this.canvas.width = 150;
				this.canvas.height = 150;
				this.ctx.fillStyle = "rgb(0,0,0)";
      			this.ctx.fillRect(0, 0, 150, 150);
				const wrap = document.getElementById('canvas-div-wrap-'+this.type)
				const show_width = wrap.offsetWidth;
				const show_height = wrap.offsetHeight;
				this.canvas_show.width = show_width;
				this.canvas_show.height = show_height;
				this.ctx_show.drawImage(this.canvas,0,0,150,150,0,0,show_width,show_height);
				this.clear_flag = true;
				console.log("clear")
			},
			//获得数据后,初始化画布
			init(){
				this.canvas = document.getElementById("tutorial"+this.type);
				this.canvas.width = this.width;
				this.canvas.height = this.height;
				this.ctx = this.canvas.getContext("2d");
				this.canvas_pixel_data = this.ctx.createImageData(this.width, this.height);

				const data = this.canvas_pixel_data.data;
				// console.log(this.canvas_pixel_data);
				let index;
				for (let i=0;i<this.height;++i){
					for (let j=0;j<this.width;++j){
						index = i * this.width * 4 + j * 4
						data[index] = 0;
						data[index+1] = 0;
						data[index+2] = 0;
						data[index+3] = 255;
					}
				}
				this.ctx.putImageData(this.canvas_pixel_data, 0, 0);
				
				this.display();
				this.clear_flag = false;
				this.$forceUpdate();
			}


    	},
			
			
		
	}
</script>

<style lang="scss" scoped>
.slice-wrap{
    width:100%;
    height:100%;
    .canvas-div-wrap{
        width:100%;
        height:100%;
    //     position: relative;
    //     .canvas-wrap{
    //         position: absolute;
    //         top: 50%;
    //         left: 50%;
    //         transform: translate(-50%,-50%);
    //     }
    }
    
}
</style>

