<template>
    <div class="set_sel-wrap">
        <setTable
        
        :key="'set_sel'+'table'"
        ref="set_sel_table"
        :resData="resData"
        :propsData="propsData"
        :labelData="labelData"
        :widthData="widthData"
        :selectFunc="selectFunc"
        :get_update="get_update"
        :edit_update="edit_update"
        :add_update="add_update"
        :remove_update="remove_update"
        >
        </setTable>
        <!-- html代码区 -->
    </div>
    <!-- 不要在此处添加其他东西 -->
</template>

<script>
import setTable from "@/components/setTable.vue"
// import {get_data,add_data,edit_data,remove_data} from "@/api/index.js"
import {getSets,buildSet,updateSet,deleteSet} from "@/api/index.js"
export default {
    name: "set_sel",
    props:['projectID','selectFunc',"getSetsFunc","project_sets_id"],
	components: {
        //组件
        setTable,
	},
    data () {
        //属性
	    return {
            resData:[],
            propsData:[],
            labelData:[],
            widthData:[],         
        }
    },
	methods: {
        //方法
        async get_update(){
            // this.resData = [
            //     {
            //         project_name:"xhr",
            //     },
            //     {
            //         project_name:"cxq",
            //     },
            // ]
            // this.propsData = Object.keys(this.resData[0]);
            // this.labelData = ["项目ID","项目名称"];
            // this.widthData = [300,,1500];
            // this.$forceUpdate();
            // return true;

            var data = await getSets({
                "project_id":this.projectID
            });
            if (data.status == "OK"){
                console.log("get_update_success");
                if (!data.sets){
                    this.resData = [
                        {
                            'set_id':'12',
                            'set_name':"xhrxhr",
                        },
                        {
                            'set_id':'22',
                            'set_name':"cxqzxq",
                        },
                    ];
                }
                else {
                    // var temp = [];
                    // for (let key in data.sets){
                    //     temp.push({
                    //         'set_id':key
                    //         ,'set_name':data.sets[key]
                    //     })
                    // }
                    this.resData = data.sets;
                    this.resData = this.resData.filter((item)=>{
                        return (this.project_sets_id.indexOf(item.set_id)!==-1)
                    })
                    // this.resData = [
                    //     {
                    //         'set_id':'12',
                    //         'set_name':"xhrxhr",
                    //     },
                    //     {
                    //         'set_id':'22',
                    //         'set_name':"cxqzxq",
                    //     },
                    // ];
                }
                // this.propsData = Object.keys(this.resData[0]);
                this.propsData = ['set_id', 'set_name', 'directory', 'original_path', 'nii_path', 'label_path', 'nii_after_path', 'stl_directory', 'build_time', 'remark'];
                this.labelData = ["集合ID","集合名称","集合目录","原CT路径","nii-CT路径","标签nii路径","转换后的标签路径","STL文件夹","创建时间","备注"];
                this.widthData = [150,150,200,200,200,200,200,200,200,200,200];
                this.$forceUpdate();
                this.getSetsFunc(data.sets);
                return true;
            }
            else if (data.status == "fail"){
                console.log("get_update_fail");
                return false;
            }
            else {
                console.log("fail!!!!!");
                return false;
            }
            
        },
        async add_update(row){
            // return false;
            console.log(row);
            var data = await buildSet({
                'project_id':this.projectID,
                'set_name':row.set_name,
                'set_id':row.set_id,
                'remark':row.remark
            })
            if (data.status == "OK"){
                console.log("add_update success");
                this.$parent.project_sets_id.push(row.set_id*1);
                this.getSetsFunc(data.sets);
                this.$forceUpdate();
                return true;
            }
            else if (data.status == "fail"){
                console.log("add_update fail");
                return false;
            }
            else{
                console.log("fail!!!!!!!!!!!!!!");
                return false;
            }
            
        },
        async edit_update(row){
            // return false;
            var data = await updateSet({
                set:row
            })
            if (data.status=="OK"){
                console.log("edit_update success");
                this.$refs.set_sel_table.refresh();
                return true;
            }
            else if (data.status=="fail"){
                console.log("edit_update fail");
                return false;
            }
            else{
                console.log("fail!!!!!!!!!!!!");
                return false;
            }
            
        },
        async remove_update(row){
            // return false;
            var data = await deleteSet({
                set_id:row.set_id
            })
            if (data.status=="OK"){
                console.log("remove_update success");
                
                await this.$parent.project_sets_id.splice(this.$parent.project_sets_id.indexOf(row.set_id*1),1);
                this.$refs.set_sel_table.refresh();
                this.$forceUpdate();
                return true;
            }
            else if (data.status=="fail"){
                console.log("remove_update fail");
                return false;
            }
            else{
                console.log("fail!!!!!!!");
                return false;
            }
            
        }
    },
    mounted() {
        //网页生成前调用，用于初始化
    },
    
    destroyed() {
        //网页销毁【或跳转】调用，用于清除缓存
    },
}
</script>

<style lang="scss" scoped>
.set_sel-wrap{
    width:100%;
    height:100%;
    // border: 1px solid rgb(8, 8, 8);
    .set_sel-wrap-header{
        width:95%;
        height:10%;
        // border: 1px solid rgb(8, 8, 8);
        margin-top: 2.5%;
        margin-left: 2.5%;
        margin-right: 2.5%;
    }
    .set_sel-wrap-body{
        width:95%;
        height:75%;
        // border: 1px solid rgb(8, 8, 8);
        margin-left: 2.5%;
        margin-right: 2.5%;
    }
}
</style>