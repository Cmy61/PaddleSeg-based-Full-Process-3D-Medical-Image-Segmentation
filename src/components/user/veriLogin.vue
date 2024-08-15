<template>
    <div class="verilogin-wrap">
        <!-- html代码区 -->
            <el-card class="box-card">
                <el-row>
                <el-input v-model="account"  placeholder="请输入邮箱号" required>
                    <i slot="prefix" class="el-input__icon el-icon-user-solid"></i>
                </el-input>
                </el-row>
                <el-input v-model="veriCode" placeholder="请输入邮箱验证码" required>
                    <i slot="prefix" class="el-input__icon el-icon-message"></i>
                    <el-button slot="suffix" type="primary" id="sendCode" @click="sendCode()"
                    size="mini">获取验证码</el-button>
                </el-input>
                <el-button type="primary" @click="Login_action">登录</el-button>
            </el-card>
    </div>
    <!-- 不要在此处添加其他东西 -->
</template>

<script>
import {get_confirm_code, login_veri, register_email} from "@/api/index.js"
export default {
    name: "veriLogin",
	components: {
        //组件
	},
    data () {
        //属性
	    return {
            account:null,
            veriCode:null,
        }
    },
	methods: {
        //方法
        async sendCode(){
            var data=await get_confirm_code({
                account:this.account
            });
            if (data.result==1){
                return true;
            }
        },
        async Login_action(){
            console.log("调用登录函数");
            console.log("account is " + this.account);
            console.log("veriCode is " + this.veriCode);
            // 调用请求函数 Login
            var data = await login_veri({
                account: this.account,
                confirm_code: this.veriCode,
            });
            if (data.result==1){
                await register_email({
                    account:this.account,
                    password:""
                });
                this.$Message.success('登录成功');
                this.$router.push("/home");
                // this.$alert('登录成功', '提示信息', {
                //     confirmButtonText: '确定',
                //     callback: action => {
                //         this.$message({type: 'info', message: `action: ${action}`});
                //         this.$router.push("/home");

                //     }
                // });
            } else {
                this.$Message.error('验证码错误');
                // this.$alert('验证码错误', '提示信息', {
                //     confirmButtonText: '确定',
                //     callback: action => {
                //         this.$message({type: 'info', message: `action: ${action}`});
                //     }
                // });
            }
            // data 是一个json数据类型，可以理解字典
        },
        
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
.verilogin-wrap{
    width:100%;
    height:100%;
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