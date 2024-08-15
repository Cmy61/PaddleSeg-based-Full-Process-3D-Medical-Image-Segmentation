<template>
     <el-dialog title="上传CT" :visible.sync="dialogTableVisible" :before-close="handleDialogClose"> 
        <el-upload
                drag
                ref="upload_CT"
                action="http://localhost:8888/upload/"
                :auto-upload="false"
                :accept="file_ext_type"
                :show-file-list="true"
                :data="get_upload_data()"
                :multiple = "false"
                :on-success="handle_upload_success"
                :file-list="fileList">
                <i class="el-icon-upload"></i>
                <div class="el-upload__text">将文件拖到此处，或<em>点击选择</em></div>
                <div slot="tip" class="el-upload__tip">只能上传dcm.gz,nii,nii.gz,raw,mhd.gz文件</div>
        </el-upload>
        <el-button @click="uploadFile()">点击上传文件</el-button>
    </el-dialog>
    <!-- 不要在此处添加其他东西 -->
</template>

<script>
import {getPostData} from "@/api";
export default {
    
    name: "uploadCT",
    props:['dialogTableVisible','change_visible','get_upload_data'],
	components: {
        //组件
        
	},
    data () {
        //属性
	    return {
            // dialogTableVisible:false,
            Select_url:"",
            fileList:[],
            file_ext_type:".nii,.nii.gz,.dcm.gz,.raw,.mhd",
        }
    },
	methods: {
        handleDialogClose(){
            this.$confirm('确定退出吗？')
            .then(_ => {
                this.change_visible(false);
                this.$refs.upload_CT.clearFiles();
            })
            .catch(_ => {});
        },
        uploadFile(){
            console.log(this.fileList);
            this.$refs.upload_CT.submit();
        },
        handle_upload_success(res,file,filelist){
            if (res.status == "OK"){
                console.log(res.file_path);
                this.Select_url = "http://localhost:8888/download/"+res.file_path;
                this.$refs.upload_CT.clearFiles();
                this.change_visible(false);
                
                this.$forceUpdate();
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
.uploadCT-wrap{
    
}
</style>