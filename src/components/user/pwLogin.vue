<template>
    <!-- html代码区 -->
    <el-card class="box-card">
        <el-row>
            <el-input v-model="account" placeholder="请输入邮箱号" required>
                <i slot="prefix" class="el-input__icon el-icon-user-solid"></i>
            </el-input>
        </el-row>
        <el-row>
            <el-input v-model="password" placeholder="请输入密码" show-password required>
                <i slot="prefix" class="el-input__icon el-icon-lock"></i>
            </el-input>
        </el-row>

        <el-button type="primary" @click="submit_login">登录</el-button>

        <el-row :gutter="20">
            <el-col :span="17">
                <div class="grid-content bg-purple">
                    <span>没有账号？</span>
                    <el-link @click="$router.push('/Register')" target="_blank">立即注册</el-link>
                </div>
            </el-col>
            <el-col :span="7">
                <div class="grid-content bg-purple"></div>
                <el-link @click="$router.push('/findpassWord')" target="_blank">忘记密码？</el-link>
            </el-col>
        </el-row>
    </el-card>
    <!-- 不要在此处添加其他东西 -->
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
                this.$root.$children[0].$refs.homeheader.flag = true;
                this.$router.push("/Home");
            }
            else {
                this.$message.error("登陆失败。"+data.reason);
            }
        }
    }

}
</script>

<style lang="scss" scoped>
.box-card {
    width: 100%;
    height: 100%;

    .el-input {
        margin-top: 1%;
        margin-bottom: 1%;
    }

    .el-button {
        width: 100%;
        margin-top: 5%;
        margin-bottom: 5%;
    }

    .grid-content bg-purple {
        // border: 1px solid rgb(12, 12, 12);

        .el-icon-user-solid {
            width: 150%;
            height: 150%;
        }

    }


}
</style>