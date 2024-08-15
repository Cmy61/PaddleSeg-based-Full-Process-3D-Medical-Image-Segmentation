<!-- <template>
    <div class="login-wrap">
        <div class="login-div">
            <el-input v-model="account" placeholder="请输入账号"></el-input>
            <el-input v-model="password" placeholder="请输入密码" show-password></el-input>
            <el-button @click="submit_login">确认登录</el-button>
        </div>
    </div>
</template>

<script>
import {login} from '@/api/index.js';
export default {
    data() {
        return {
            account: null,
            password: null
        }
    },
    methods: {
        async submit_login(){
            let data = await login({
                'account':this.account,
                'password':this.password
            })
            console.log(data);
            if (data.status == 'OK'){
                this.$message({
                    message: '登陆成功',
                    type: 'success'
                });
                console.log(this.$cookie.get('account'));
                this.$router.push("/Home");
            }
            else {
                this.$message.error("登陆失败。"+data.reason);
            }
        }
    }

}
</script>

<style lang="scss">
.login-wrap{
    width:100%;
    height:100%;
    .login-div{
        width:40%;
        height:30%;
        margin: auto;
        background-color: aqua;
    }
}
</style> -->

<template>
    <div class="login-wrap">
        <!-- html代码区 -->
        <h1 style="margin-left:74%;margin-top:10%;margin-bottom:0;color:#fff;font-weight:600">腹部器官分割系统</h1>
        <div class="login-wrap-main">
            <div class="login-wrap-main-body">

                <el-tabs v-model="activeName" @tab-click="handleClick" :stretch=true style="margin-top:2%;">
                    <el-tab-pane :label=label1 name="first"></el-tab-pane>
                    <pwLogin></pwLogin>
                </el-tabs>
            </div>
            <!-- <el-container>
                    <el-aside width="40%">
                        <img :src="im" style="width: 100%;height: 100%;">
                    </el-aside>
                    <el-main>
                        <el-tabs v-model="activeName" @tab-click="handleClick">
                            <el-tab-pane FormItem :label="label1" name="first">
                                <pwLogin></pwLogin>
                            </el-tab-pane>
                            <el-tab-pane FormItem :label="label2" name="second">
                                <veriLogin></veriLogin>
                            </el-tab-pane>
                        </el-tabs>
                    </el-main>
                </el-container> -->
        </div>
    </div>
    <!-- 不要在此处添加其他东西 -->
</template>

<script>
import pwLogin from "@/components/user/pwLogin.vue"

export default {
    name: "Login",
    components: {
        //组件
        pwLogin
    },
    data() {
        //属性
        return {
            step: null,
            activeName: 'first',
            // label1: '\xa0'.repeat(10) + '账号密码登录' + '\xa0'.repeat(10),
            // label2: '\xa0'.repeat(14) + '验证码登录' + '\xa0'.repeat(14)
            label1: '账号密码登录',
            label2: '验证码登录'
        }
    },
    methods: {
        //方法
        cookie_verify() {
            var flag = this.$cookies.isKey('account');
            if (flag) {
                this.$router.push("/Home");
            }
        },
        // data 是一个json数据类型，可以理解字典
        handleClick(tab, event) {
            console.log(tab, event);
        }
    },
    mounted() {
        // this.cookie_verify();
        //网页生成前调用，用于初始化
    },
    destroyed() {
        //网页销毁【或跳转】调用，用于清除缓存
    },
}
</script>

<style lang="scss">
.login-wrap {
    width: 100%;
    height: 92%;
    position: absolute;
    background: url('../../assets/CT医院.jpg') no-repeat;
    background-size: cover;

    .login-wrap-main {
        width: 24%;
        height: 41.5%;
        
        margin-left: 70%;
        margin-top: 2%;
        display: flex;

        .login-wrap-main-aside {
            width: 35%;
            height: 100%;
        }

        .login-wrap-main-body {
            width: 100%;
            height: 100%;
            background-color: white;
            border: 1px solid rgb(12, 12, 12);
        }
    }
}
</style>
