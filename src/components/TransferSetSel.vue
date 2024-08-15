<template>
    <el-dialog
    title="绑定现有集合"
    :visible.sync="show_flag"
    width="45%"
    :before-close="handleClose">
        <el-transfer 
        v-if="show_transfer"
        filterable
        filter-placeholder="输入搜索"
        v-model="value"
        target-order="push"
        :data="sets_data">
        </el-transfer>
        <span slot="footer" class="dialog-footer">
            <el-button @click="no_comfirm">取 消</el-button>
            <el-button type="primary" @click="comfirm">确 定</el-button>
        </span>
    </el-dialog>
	
</template>

<script>

	export default {
		components: {
			
		},
		data() {
            
			return {
                sets_data: null,
                value: null,
                show_transfer:false,
			};
		},
        computed:{
        },

		props: ['show_flag','sets','project_sets_id_list','close_dialog','join_sets'],
		watch: {
			show_flag(newT,oldT){
                console.log(oldT);
                console.log(newT);
                if (newT){
                    this.init();                
                }
            }
		},
		mounted() {
			
			
		},
		methods: {
            init(){
                const arr = [];
                console.log("begin_arr")
                console.log(Object.keys(this.sets[0]))
                for (let i=0;i < this.sets.length;++i){
                    arr.push({
                        key: this.sets[i].set_id,
                        label: this.sets[i].set_id + '--' + this.sets[i].set_name
                    })
                }
                console.log("finish_arr")
                const arr1 = [];
                console.log("begin_arr1")
                for (let i=0;i<this.project_sets_id_list.length;++i){
                    arr1.push(this.project_sets_id_list[i]);
                }
                console.log("finish_arr1")
                console.log(arr);
                console.log(arr1);
                this.sets_data = arr;
                this.value = arr1;
                this.show_transfer = true;
            },
            handleClose() {
                this.$confirm('确认关闭？')
                .then(_ => {
                    this.close_dialog();
                    this.show_transfer = false;
                    //调用外部函数改变visible
                })
                .catch(_ => {});
            },
            //确定
            comfirm(){
                this.join_sets(this.value);
                this.project_sets_id_list.length = 0;
                // 新增
                for (let i =0;i<this.value.length;++i){
                    this.project_sets_id_list.push(this.value[i]);

                }
                this.close_dialog();
                this.show_transfer = false;
            },
            //取消
            no_comfirm(){
                this.close_dialog();
                this.show_transfer = false;
            }
            

    	},
			
			
		
	};
</script>

<style lang="scss" scoped>

</style>

