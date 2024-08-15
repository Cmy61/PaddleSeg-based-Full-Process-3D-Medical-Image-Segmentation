<template>
    <div class="proj_sel-wrap">
        <projTable
        :key="'proj_sel'+'table'"

        :resData="resData"
        :propsData="propsData"
        :labelData="labelData"
        :widthData="widthData"
        :get_update="get_update"
        :edit_update="edit_update"
        :add_update="add_update"
        :remove_update="remove_update"
        >
        </projTable>
        <!-- html代码区 -->
    </div>
    <!-- 不要在此处添加其他东西 -->
</template>

<script>
import projTable from "@/components/projTable.vue"
// import {get_data,add_data,edit_data,remove_data} from "@/api/index.js"
import {getProjects,builiProject,updateProject,deleteProject} from "@/api/index.js"
export default {
    name: "proj_sel",

	components: {
        //组件
        projTable,
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

            var data = await getProjects({});
            if (data.status == "OK"){
                console.log("get_update_success");
                this.resData = data.projects;
                this.propsData = Object.keys(this.resData[0]);
                this.labelData = ["项目ID","项目名称","创建时间","备注","集合列表"];
                this.widthData = [150,150,250,400,300];
                this.$forceUpdate();
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
            // console.log(row);
            var data = await builiProject(row)
            if (data.status == "OK"){
                console.log("add_update success");
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
            var data = await updateProject({project:row})
            if (data.status == "OK"){
                console.log("edit_update success");
                return true;
            }
            else if (data.status == "fail"){
                console.log("edit_update fail");
                return false;
            }
            else{
                console.log("fail!!!!!!!!!!!!!!");
                return false;
            }
        },
        async remove_update(row){
            var data = await deleteProject({project_id:row.project_id})
            if (data.status == "OK"){
                console.log("remove_update success");
                return true;
            }
            else if (data.status == "fail"){
                console.log("remove_update fail");
                return false;
            }
            else{
                console.log("fail!!!!!!!!!!!!!!");
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
.proj_sel-wrap{
    width:90%;
    height:85%;
    margin-left:5%;
    margin-right: 5%;
    margin-top:2%;
    margin-bottom:4%;
    border: 1px solid #909399;
    border-radius: 1%;
    box-shadow: 0 0 3px 3px #EBEEF5;
    .proj_sel-wrap-header{
        width:95%;
        height:10%;
        // border: 1px solid rgb(8, 8, 8);
        margin-top: 2.5%;
        margin-left: 2.5%;
        margin-right: 2.5%;
    }
    .proj_sel-wrap-body{
        width:95%;
        height:75%;
        // border: 1px solid rgb(8, 8, 8);
        margin-left: 2.5%;
        margin-right: 2.5%;
    }
}
</style>