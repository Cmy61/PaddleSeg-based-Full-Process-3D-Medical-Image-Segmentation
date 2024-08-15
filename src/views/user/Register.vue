<template>
    <div class="register-wrap">
        <!-- html代码区 -->
        <h1 style="margin-left:74%;margin-top:10%;margin-bottom:0;color:#fff;font-weight:600">腹部器官分割系统</h1>
        <div class="register-wrap-main">
            <div class="register-wrap-main-body">
                <el-tabs v-model="activeName" :stretch=true style="margin-top:2%;">
                    <el-tab-pane :label="register_name" name="first"></el-tab-pane>
                    <register_1 v-if="step == 0" :next="next"></register_1>
                    <register_2 v-if="step == 1" :account="account"></register_2>
                </el-tabs>
            </div>
            <!-- <el-container>
                <el-aside width="250px">
                    <img :src="im" style="width: 250px;height: 345px;">
                </el-aside>
                <el-main>
                    <el-tabs v-model="activeName">
                        <el-tab-pane :label="register_name" name="first"></el-tab-pane>
                        <register_1 v-if="step==0" :next="next"></register_1>
                        <register_2 v-if="step==1" :account="account"></register_2>
                    </el-tabs>



                </el-main>
            </el-container> -->
            <!--            -->
            <!-- <div v-if="step==0" style="width:100%;height:100%;">
                <register_1></register_1>
            </div>
            <div v-if="step==1" style="width:100%;height:100%;">
                <register_2></register_2>
            </div> -->

            <!--            -->
        </div>

    </div>
    <!-- 不要在此处添加其他东西 -->
</template>

<script>
import register_1 from "@/components/user/register_1.vue"
import register_2 from "@/components/user/register_2.vue"
export default {
    name: "register",
    components: {
        register_1,
        register_2
        //组件
    },
    data() {
        //属性
        return {
            step: null,
            account: null,
            im: require("@/images/a.jpg"),
            activeName: "first",
            register_name: "注册"
        }
    },
    methods: {
        //方法
        next(account) {
            this.step = (this.step + 1) % 2;
            this.account = account;
            // console.log(account);
            // console.log(this.account);
        },
        //验证是否登录。 已登录则加载home，否则跳转到登录界面
        cookie_verify() {
            var flag = this.$cookies.isKey('account');
            if (flag) {
                this.$router.push("/Home");
            }
        }
    },
    mounted() {
        //this.cookie_verify();
        //网页生成前调用，用于初始化
        this.step = 0;
    },
    destroyed() {
        //网页销毁【或跳转】调用，用于清除缓存
    },
}
</script>

<style lang="scss" scoped>
.register-wrap {
    width: 100%;
    height: 92%;
    position: absolute;
    //border: 1px solid rgb(24, 23, 23);
    background: url('../../assets/CT医院.jpg') no-repeat;
    background-size: cover;

    .register-wrap-main {
        width: 24%;
        height: 41.5%;
        
        margin-left: 70%;
        margin-top: 2%;
        display: flex;

        .register-wrap-main-aside {
            width: 35%;
            height: 100%;
        }

        .register-wrap-main-body {
            width: 100%;
            height: 100%;
            background-color: white;
            border: 1px solid rgb(12, 12, 12);
        }
    }

}
</style>