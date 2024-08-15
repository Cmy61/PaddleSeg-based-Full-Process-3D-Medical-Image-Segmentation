<template>
    <div class="set_sel-wrap">
        <labelTable
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
        </labelTable>
        <!-- html代码区 -->
    </div>
    <!-- 不要在此处添加其他东西 -->
</template>

<script>
import labelTable from "@/components/labelTable.vue"
// import {get_data,add_data,edit_data,remove_data} from "@/api/index.js"
import {getLabel} from "@/api/index.js"
export default {
    name: "label_sel",
    props:['projectID','selectFunc'],
	components: {
        //组件
        labelTable,
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
                this.propsData = Object.keys(this.resData[0]);
                this.labelData = ["集合ID","集合名称","集合目录","原CT路径","nii-CT路径","标签nii路径","转换后的标签路径","STL文件夹","创建时间","备注"];
                this.widthData = [150,150,200,200,200,200,200,200,200,200,200];
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
            console.log(row);
            return false;
            // var data = await buildSet({
            //     'project_id':this.projectID,
            //     'set_name':row.set_name
            // })
            // if (data.status == "OK"){
            //     console.log("add_update success");
            //     return true;
            // }
            // else if (data.status == "fail"){
            //     console.log("add_update fail");
            //     return false;
            // }
            // else{
            //     console.log("fail!!!!!!!!!!!!!!");
            //     return false;
            // }
            
        },
        async edit_update(row){
            return false;
            var data = await edit_data({
                table_type:"set_sel",
                data:row
            })
            if (data.result==1){
                console.log("edit_update success");
                return true;
            }
            else if (data.result==0){
                console.log("edit_update fail");
                return false;
            }
            else{
                console.log("fail!!!!!!!!!!!!");
                return false;
            }
            
        },
        async remove_update(row){
            return false;
            var data = await remove_data({
                table_type:"set_sel",
                data:row
            })
            if (data.result==1){
                console.log("remove_update success");
                return true;
            }
            else if (data.result==0){
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