<template>
    <div class="register-2-wrap">
        <!-- html代码区 -->
        <el-card class="box-card">
            <el-input placeholder="请输入密码" v-model="password1" show-password></el-input>
            <el-input placeholder="请输入密码" v-model="password2" show-password></el-input>
            <el-button @click="register_action" type="primary">注册</el-button>
            <el-row :gutter="20">
                <el-col :span="17">
                    <div class="grid-content bg-purple">
                        <span>已有账号？</span>
                        <el-link @click="$router.push('/Login')" target="_blank">点击登录</el-link>
                    </div>
                </el-col>
                <el-col :span="7">
                    <div class="grid-content bg-purple"></div>
                </el-col>
            </el-row>
        </el-card>

<!--        <el-input placeholder="请输入密码" v-model="password1" show-password></el-input>-->
<!--        <el-input placeholder="请输入密码" v-model="password2" show-password></el-input>-->

    </div>
    <!-- 不要在此处添加其他东西 -->
</template>

<script>
import {register} from "@/api/index.js"
export default {
    name: "register_2",
    props:["account"],
	components: {
        //组件
	},
    data () {
        //属性
	    return {
            password1:null,
            password2:null,
        }
    },
	methods: {
        //方法
        async register_action(){
            if(this.password1!=this.password2)
                this.$Message.warning("两次密码不一样");
            else{
                var data = await register({
                account:this.account,
                password:this.password1,
                });
                var result = data.result;
                if (result==0)
                {
                    this.$Message.success("注册成功")
                    this.$router.push("/login");
                }
                else
                    this.$Message.error("注册失败")
            }
        }
    },
    mounted() {
        //网页生成前调用，用于初始化
        // console.log("count"+this.account);
    },
    destroyed() {
        //网页销毁【或跳转】调用，用于清除缓存
    },
}
</script>

<style lang="scss" scoped>
.register-2-wrap{
    width:100%;
    height:75%;
    //border: 1px solid rgb(24, 23, 23);
    .box-card{
        height:85%;
        .el-input{
            margin-top:1%;
            margin-bottom:1%;
        }
        .el-button{
            width:100%;
            margin-top:5%;
            margin-bottom:5%;
        }

    }
}
</style>