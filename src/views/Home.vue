<!-- <template>
    <div id="home-warp">
        <el-button>
            <router-link to="test2d">2D测试</router-link> 
        </el-button>
        <el-button>
            <router-link to="test3d">3D测试</router-link> 
        </el-button>
        <el-button>
            <router-link to="Login">登录测试</router-link> 
        </el-button>
        <el-button>
            <router-link to="Func">功能界面测试</router-link> 
        </el-button>
        <el-button>
            <router-link to="ProjSel">项目表格</router-link> 
        </el-button>
        <div>
            <el-button @click="change_visible(true)">打开弹窗</el-button>
        </div>
        <MarkingCanva
                :dialogMarkingVisible="dialogMarkingVisible"
                :change_visible="change_visible"
            >
        </MarkingCanva>
    </div>
</template>

<script>
import Cookies from 'js-cookie'
import MarkingCanva from '../components/MarkingCanva.vue';
export default {
    components:{
        MarkingCanva
    },
    mounted() {
        if (!this.$cookie.get('account')){
            this.$router.push("/Login");
        }
    },
    data(){
        return {
            dialogMarkingVisible:false,
        }
    },
    methods:{
        change_visible(val){
            this.dialogMarkingVisible = val;
        }
    }
};
</script>

<style>
</style> -->

<template>
    <div class="body-style">
        <HomeMain class="HomeMain-style"></HomeMain>
    </div>
</template>

<script>
import HomeMain from "@/components/HomeMain.vue"
export default {
    components:{
        HomeMain
    }
};
</script>

<style lang="scss" scoped>
	.body-style{
		background-color: 	#F0F8FF;
		width:90%;
		   height: calc(240vh - 60px);
		   margin:0 auto;
		  // background-color: #ccc;
		    border:1px solid #ccc;
		    // overflow: hidden;
	}
	.Homeheader-style{
	    width: 100%;
	    height: 64px;

	}
	
	.HomeMain-style{
	    width: 100%;
	    height: calc(100vh - 64px);
	}
</style>