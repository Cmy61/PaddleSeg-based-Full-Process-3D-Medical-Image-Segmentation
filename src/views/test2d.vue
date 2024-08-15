<template>
	<div style="width:100%;height:100%;">
        <div style="display:flex;">
            <el-upload
                ref="upload_com"
                action="http://localhost:8888/upload/"
                :auto-upload="false"
                :accept="file_ext_type"
                :show-file-list="true"
                :multiple = "false"
                :on-success="handle_upload_success"
                :file-list="fileList">
                <el-button size="small" type="primary">选择文件</el-button>
                <div slot="tip" class="el-upload__tip">只能上传dcm,nii,nii.gz,raw文件</div>
            </el-upload>
            <el-button @click="uploadFile()">点击上传文件</el-button>
            <el-button @click="test_post()">post测试</el-button>
        </div>
        


        <el-button @click="changeSelectUrl()">改变URL</el-button>
        <!-- <scene2D :Select_url="Select_url">

        </scene2D> -->
        <slice_test :Select_url="Select_url">
            
        </slice_test>
    </div>

</template>

<script>

    import scene2D from '@/components/scene2D.vue';
    import slice_test from '@/components/slice_test.vue';
    import {getPostData} from "@/api";


	export default {
		components: {
			scene2D,
            slice_test
		},
		data() {
			return {
                Select_url:"",
                fileList:[],
                file_ext_type:".nii,.nii.gz,.dcm.gz,.raw,.mhd",
            }
		},
		props: {
			
		},
		watch: {
			
		},
		mounted() {
            if (this.Select_url){
                console.log(1);
            }
            console.log(0);
		},
		methods: {
            changeSelectUrl(){
                // this.Select_url = "http://localhost:8888/path/C:/Users/92090/Desktop/3D医学影像/base_train/labelsTr/test_label.nii";
                this.Select_url = "http://localhost:8888/download/C:/Users/92090/Desktop/test_pro3d/test.nii"
            },
            uploadFile(){
                console.log(this.fileList);
                this.$refs.upload_com.submit();
            },
            handle_upload_success(res,file,filelist){
                if (res.status == "OK"){
                    console.log(res.file_path);
                    this.Select_url = "http://localhost:8888/download/"+res.file_path;
                    this.$refs.upload_com.clearFiles();
                }
            },
            async test_post(){
                var data = await getPostData(
                    {
                        "user_id": 123,
                        "temp":"get",
                    }
                );
                console.log(data);
            }
		},
        
	}
</script>

<style>

</style>

