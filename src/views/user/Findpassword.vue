<template>
    <div class="findpassword-wrap">
        <!-- html代码区 -->
        <h1 style="margin-left:74%;margin-top:10%;margin-bottom:0;color:#fff;font-weight:600">腹部器官分割系统</h1>
        <div class="findpassword-wrap-main">
            <div class="findpassword-wrap-main-body">
                <el-tabs v-model="activeName" :stretch=true style="margin-top:2%;">
                    <el-tab-pane :label="findpassword_name" name="first"></el-tab-pane>
                    <findpassword_1 v-if="step == 0" :next="next"></findpassword_1>
                    <findpassword_2 v-if="step == 1" :account="account"></findpassword_2>
                </el-tabs>
            </div>
        </div>
    </div>
    <!-- 不要在此处添加其他东西 -->
</template>

<script>
import findpassword_1 from "@/components/user/findpassword_1.vue"
import findpassword_2 from "@/components/user/findpassword_2.vue"
export default {
    name: "findpassword",
    components: {
        findpassword_1,
        findpassword_2
        //组件
    },
    data() {
        //属性
        return {
            step: null,
            account: null,
            activeName: "first",
            findpassword_name: "重置密码"
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
        // //验证是否登录。 已登录则加载home，否则跳转到登录界面
        // cookie_verify(){
        //     var flag = this.$cookies.isKey('account');
        //     if (flag){
        //         this.$router.push("/Home");
        //     }
        //     else{
        //         this.$router.push("/login");
        //     }
        // }
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
.findpassword-wrap {
    width: 100%;
    height: 92%;
    //border: 1px solid rgb(24, 23, 23);
    position: absolute;
    background: url('../../assets/CT医院.jpg') no-repeat;
    background-size: cover;

    .findpassword-wrap-main {
        width: 24%;
        height: 41.5%;
        
        margin-left: 70%;
        margin-top: 2%;
        display: flex;

        .findpassword-wrap-main-aside {
            width: 35%;
            height: 100%;
        }

        .findpassword-wrap-main-body {
            width: 100%;
            height: 100%;
            background-color: white;
            border: 1px solid rgb(12, 12, 12);
        }
    }
}</style>