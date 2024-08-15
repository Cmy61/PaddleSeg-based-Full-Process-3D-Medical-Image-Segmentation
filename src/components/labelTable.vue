<template>
    <!-- html代码区 -->
<div class="myTable-wrap">
    <div class="myTable-wrap-header">
        <el-input placeholder="请输入内容" v-model="search_text" class="input-with-select">
            <el-select v-model="search_select" slot="prepend" placeholder="请选择" style="width:90px;">
                <el-option label="全局搜索" value="0"></el-option>
                <el-option v-for="(item,i) in labelData" :key="i" :label="labelData[i]" :value="i+1"></el-option>
            </el-select>
            
            <el-button slot="append" icon="el-icon-search" @click="search" style="width:50px;"></el-button>
        </el-input>
        <template v-if="right_level==1 || right_level==0">
            <el-button @click="refresh" icon="el-icon-refresh-left" circle style="margin-left:4%;"></el-button>
            <el-button @click="add" icon="el-icon-plus" style="margin-left:3%;">添加</el-button>
        </template>
        <template v-if="right_level==2">
            <el-button @click="refresh" icon="el-icon-refresh-left" circle style="margin-left:54%;"></el-button>
            <!-- <el-button @click="add" icon="el-icon-plus" style="margin-left:2%;">添加</el-button> -->
        </template>
    </div>
    <div class="myTable-wrap-body">
        <el-table
            stripe
            v-loading="loading"
            ref="singleTable"
            :data="tableData.slice((currentPage-1)*pageSize,currentPage*pageSize)"
            border
            style="width: 100%;"
            highlight-current-row
            @current-change="handleCurrentRowChange"
            :key="table_key"
            height="91%"
            :header-cell-style="{background:'#f4f3f9',color:'#606266'}"
            >
            <el-table-column
                v-for="(item,i) in propsData"
                :key="i"
                :prop="propsData[i]"
                :label="labelData[i]"
                :width="widthData[i]"
            >
            </el-table-column>
            

            <el-table-column
                fixed="right"
                label="操作"
                width="125">
                <template slot-scope="scope">
                    <div>
                        <el-button @click="enter(scope.row,(currentPage-1)*pageSize + scope.$index)" type="text" size="small" icon="el-icon-view">选择</el-button>
                        <el-button @click="view(scope.row,(currentPage-1)*pageSize + scope.$index)" type="text" size="small" icon="el-icon-view">查看</el-button>
                    </div>
                    <div>
                        <el-button @click="edit(scope.row,(currentPage-1)*pageSize + scope.$index)" type="text" size="small" icon="el-icon-edit" v-if="right_level==0" style="color:#67C23A;">编辑</el-button>
                        <el-button @click="remove(scope.row,(currentPage-1)*pageSize + scope.$index)" type="text" size="small" icon="el-icon-delete" v-if="right_level==0" style="color:#F56C6C;">删除</el-button>
                    </div>
                    
                    
                </template>
            </el-table-column>
        </el-table>
        <el-pagination
            @size-change="handleSizeChange"
            @current-change="handleCurrentChange"
            :current-page="currentPage"
            :page-sizes="[4,5,6,7]"
            :page-size="pageSize"
            layout="total, sizes, prev, pager, next, jumper"
            :total="tableData.length">
        </el-pagination>  
    </div>
    <el-dialog title="信息" :visible.sync="dialogTableVisible" :before-close="handleDialogClose"> 
        <!-- 查看 -->
        <el-descriptions border v-if="dialog_mode==1" :column="2">
            <el-descriptions-item v-for="(val,key,idx) in currentRow" :key="labelData[idx]+''+idx" :label="labelData[idx]">
                {{val}}
            </el-descriptions-item>
        </el-descriptions>
        <!-- 修改 -->
        
        <el-form ref="form" :model="currentRow_temp" label-width="100px" v-if="dialog_mode==2">
            
                <el-form-item :label="labelData[idx]" v-for="(val,key,idx) in currentRow_temp" :key="labelData[idx]" v-if="key!='id'">
                <!-- $set(currentRow_temp, key, $event.target.value); -->
                    <el-col :span="15">
                        <el-input v-model="currentRow_temp[key]" @input="$forceUpdate(); " :disabled="key=='role'"></el-input>
                    </el-col>
                </el-form-item>
                <el-form-item>
                    <el-button type="primary" @click="comfirm_edit">确定修改</el-button>
                    <el-button @click="Object.assign(currentRow_temp, currentRow);$forceUpdate();">取消修改</el-button>
                </el-form-item>
            
        </el-form>

        <!-- 增加 -->
        <el-form ref="form" :model="currentRow_temp" label-width="100px" v-if="dialog_mode==3">
            
                <el-form-item :label="labelData[idx]" v-for="(val,key,idx) in currentRow_temp" :key="labelData[idx]" v-if="key!='id'" :required="true">
                <!-- $set(currentRow_temp, key, $event.target.value); -->
                    <el-col :span="15">
                        <el-input v-model="currentRow_temp[key]" @input="$forceUpdate();"></el-input>
                    </el-col>
                </el-form-item>
                <el-form-item>
                    <el-button type="primary" @click="comfirm_add">确定增加</el-button>
                    <el-button @click="clear(currentRow_temp);$forceUpdate();">清空</el-button>
                </el-form-item>
            
        </el-form>

    </el-dialog>
</div>
    

    


    
<!-- 不要在此处添加其他东西 -->
</template>

<script>

export default {
name: "labelTable",
props: { 
    //总数据
    resData:{
        type: Array,
        default:[]
    },
    //参数key数据
    propsData:{
        type: Array,
        default:[]
    },
    //展示给用户的标题数据
    labelData:{
        type: Array,
        default:[]
    },
    //宽度数据
    widthData:{
        type: Array,
        default:[]
    },
    selectFunc:{
        type: Function,
        default: () => {console.log("select_update ");}
    },
    //获取更新
    get_update:{
        type:Function,
        default: () => {console.log("get_update ");}
    },
    //增加更新
    add_update:{
        type:Function,
        default: (Row) => {console.log("add_update ");}
    },
    //修改更新
    edit_update:{
        type:Function,
        default: (Row) => {console.log("edit_update ");}
    },
    //删除更新
    remove_update:{
        type:Function,
        default: (Row) => {console.log("remove_update ");}
    },
    
},
components: {
    //组件
},
data () {
    //属性
    return {
        //表格展示数据
        tableData: [],
        // 当前页
        currentPage: 1,
        // 每页多少条
        pageSize: 7,
        // 已选取的行数据
        currentRow:null,
        // 已选取的行对应的index
        currentRowIndex:null,
        // 临时的行数据，用于修改与增加
        currentRow_temp:null,
        // 临时的修改状态数据，用于修改与增加
        currentRow_temp_flag:null,

        // 弹框是否可见
        dialogTableVisible:false,

        // 搜索功能选取的列。若为0则代表全局搜索，否则从左往右依次对应1,2,3。。。
        search_select:null,
        // 模糊搜索内容
        search_text:null,
        // 默认，查看、增加、修改 模式 [0,1,2,3]，用于不同弹框的生成
        dialog_mode:null,
        // 用于强制使table刷新
        table_key:0,
        //权限等级
        right_level:2,

        //增加禁止的标签下标，在其中的标签说明无法被修改
        disable_add_props:[0,1],
        //
        loading:null,
    }
},
methods: {
    //方法
    //改变每页显示多少页pageSize
    handleSizeChange(val) {
        // console.log(`每页 ${val} 条`);
        this.setCurrentRow();
        this.pageSize = val;
    },
    //改变现在第几页currentPage 
    handleCurrentChange(val) {
        // console.log(`当前页: ${val}`);
        this.setCurrentRow();
        this.currentPage = val;
    },
    //改变当前选中哪一行
    handleCurrentRowChange(val){
        this.currentRow = val;
    },
    //设置当前选中哪一行
    setCurrentRow(row) {
        if (row==null){
            this.currentRowIndex = null;
        }
        this.$refs.singleTable.setCurrentRow(row);
    },
    //清空行信息
    clear(row){
        for (let item in row){
            row[item] = null;
        }
    },
    //进入选择的当前行
    enter(row,idx){
        this.currentRowIndex = idx;
        this.setCurrentRow(row);
        console.log(row);
        this.selectFunc(row);
        // this.$router.push({ 
        //     name:'Func',
        //     //params传参 需要使用 name 否则取不到；对应路由配置的 name
        //     params: {
        //         project_id:row.project_id,
        //         project_name:row.project_name
        //     }
        // })
    },
    //查看当前行信息
    view(row,idx){
        // print(this.currentRow);
        
        this.currentRowIndex = idx;
        this.setCurrentRow(row);
        this.dialogTableVisible = true;
        this.dialog_mode=1;
        // console.log(row[this.propsData[0]]);
    },
    //修改当前行信息
    edit(row,idx){
        this.currentRowIndex = idx;
        this.setCurrentRow(row);

        this.currentRow_temp = {};
        this.currcurrentRow_temp_flag = [];
        for(let item in this.currentRow){
            this.currentRow_temp[item] = this.currentRow[item];
            this.currcurrentRow_temp_flag.push(false);
        }

        this.dialogTableVisible = true;
        this.dialog_mode=2;
    },
    //确定修改行
    async comfirm_edit(){
        var flag = await this.edit_update(this.currentRow_temp);
        if (flag){
            Object.assign(this.resData[this.currentRowIndex], this.currentRow_temp);
            this.dialogTableVisible = false;
            this.table_key = (this.table_key+1)%2;
            this.$forceUpdate();
        }
        else{
            this.$Message.error('修改失败');
            Object.assign(this.currentRow_temp, this.currentRow);
            this.$forceUpdate();
        } 
    },
    //增加行
    add(){
        this.setCurrentRow();

        this.currentRow_temp = {};
        this.currcurrentRow_temp_flag = [];
        for(let item in this.resData[0]){
            this.currentRow_temp[item] = null;
            this.currcurrentRow_temp_flag.push(false);
        }

        this.dialogTableVisible = true;
        this.dialog_mode=3;
        
    },
    //确定增加行
    async comfirm_add(){
        for (let item in this.currentRow_temp){
            if (item=='id') {continue;}
            if(this.currentRow_temp[item]==null){
                this.$Message.error('必要信息未填写完全');
                return;
            }
        }
        var flag = await this.add_update(this.currentRow_temp);
        if (flag){
            this.resData.push(this.currentRow_temp);
            this.dialogTableVisible = false;
            this.refresh();
            this.$forceUpdate();
        }
        else{
            this.$Message.error('增加失败');
        }
    },
    //删除
    async remove(row,idx){
        this.setCurrentRow(row);
        this.$confirm('确定删除吗？')
            .then(async _ => {
                var flag = await this.remove_update(row);
                if (flag){
                    this.setCurrentRow();
                    this.tableData.splice(idx,1);
                    this.resData.forEach(function(item, index, arr) {
                        if(item.id == row.id) {
                            arr.splice(index, 1);
                        }
                    });
                    this.$forceUpdate();
                }
                else{
                    this.$Message.error('删除失败');
                }
                
            })
            .catch(_ => {});
    },
    //刷新
    async refresh(){
        var flag = await this.get_update();
        if (flag){
            this.tableData = this.resData;
            this.search_select = null;
            this.search_text = null;
            this.loading = false;
            await this.$nextTick();
            this.$refs.singleTable.doLayout();
        }
        else{
            this.$Message.error('刷新失败');
        }
        
    },
    //搜索
    search(){
        // 全局搜索
        this.setCurrentRow();
        if (this.search_select*1 === 0){
            let func = (item) => {
                for (let i=0;i<this.propsData.length;i+=1){
                    if (((item[this.propsData[i]]+"")+"").indexOf(this.search_text) != -1 ){
                        return true;
                    }
                }
                return false;
            };
            this.tableData = this.resData.filter(func);
        }
        //局部搜索
        else {
            let func = (item) => {
            
            if (this.propsData[this.search_select*1 - 1] in item){
                if ((item[this.propsData[this.search_select*1 - 1]+""]+"").indexOf(this.search_text) != -1 ){
                    return true;
                }
            }
            return false;            
            };
            this.tableData = this.resData.filter(func);
        }

        return;
    },
    //处理弹框关闭前，进行确定关闭
    handleDialogClose(done) {
        this.$confirm('确定退出吗？')
            .then(_ => {
                this.dialogTableVisible = false;
                this.dialog_mode = 0;
            })
            .catch(_ => {});
    },
    
},
mounted() {
    //网页生成前调用，用于初始化
    this.loading = true;
    this.pageSize = 7;
    this.currentPage = 1;
    this.refresh();
    this.right_level = 0;
    // this.tableData = this.resData;
    //浅拷贝 this.tableData = Object.assign([],this.resData)
    // console.log(this.labelData);
},
// activated(){
//     this.pageSize = 7;
//     this.currentPage = 1;
//     this.refresh();

//     this.tableData = this.resData;
// },
destroyed() {
    //网页销毁【或跳转】调用，用于清除缓存
},
watch:{
    // currentRowIndex(new_val,old_val){
    //     this.$forceUpdate();
    // }
}
}
</script>

<style lang="scss" scoped>
.myTable-wrap{
width:100%;
height:100%;
// border: 1px solid rgb(8, 8, 8);
.myTable-wrap-header{
    width:95%;
    height:10%;
    // border: 1px solid rgb(8, 8, 8);
    margin-top: 2.5%;
    margin-left: 2.5%;
    margin-right: 2.5%;
    margin-bottom:1.5%;
    // text-align: center;
    .input-with-select{
        width:60%;
        margin-top:1%;
        margin-left:1%;
    }
}
.myTable-wrap-body{
    width:95%;
    height:75%;
    // border: 1px solid rgb(8, 8, 8);
    box-shadow: 0 2px 4px rgba(0, 0, 0, .12), 0 0 6px rgba(0, 0, 0, .04);
    margin-left: 2.5%;
    margin-right: 2.5%;
} 
.actionbar{
    width:50%;
    height:40%;
    left:30%;
    top:25%;
    z-index: 2147483647;
    position:absolute;
    // border: 1px solid rgb(8, 8, 8);
    background-color: white;
    border-radius: 20px;
} 
}

</style>