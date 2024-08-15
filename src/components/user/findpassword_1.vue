<template>
  <div class="findpassword-1-wrap">
    <!-- html代码区 -->
      <div class="verilogin-wrap">
        <!-- html代码区 -->
            <el-card class="box-card">
                <el-row>
                    <el-input v-model="account"  placeholder="请输入账号" required>
                        <i slot="prefix" class="el-input__icon el-icon-user-solid"></i>
                    </el-input>
                </el-row>
                    <el-input v-model="confirm_code" placeholder="请输入新密码" required>
                        <i slot="prefix" class="el-input__icon el-icon-message"></i>
                    </el-input>
                <el-button type="primary" @click="findpasswordEmail_action()">重置</el-button>
                <el-row :gutter="20">
                    <el-col :span="17">
                        <div class="grid-content bg-purple">
                            <span>记起密码？</span>
                            <el-link @click="$router.push('/Login')" target="_blank">返回登录</el-link>
                        </div>
                    </el-col>
                    <el-col :span="7">
                        <div class="grid-content bg-purple">
                            <el-link @click="$router.push('/Register')" target="_blank">进入注册</el-link>
                        </div>
                    </el-col>
                </el-row>
            </el-card>
    </div>
  </div>
  <!-- 不要在此处添加其他东西 -->
</template>

<script>
import {get_confirm_code, forget_email} from "@/api/index.js"

export default {
    name: "findpassword_1",
    props: ["next"],
    components: {
        //组件
    },
    data() {
        //属性
        return {
        account: null,
        confirm_code: null,
        }
    },
    methods: {
        //方法
        async GetConfirmCode_action() {
        var data = await get_confirm_code({
            "account": this.account
        });
        //验证该账号是否有效 返回0：表示账号还未注册
        if (data.result == 0)
            this.$Message.error("发送失败");
        else
            this.$Message.success("发送成功");
        },

        //
        async findpasswordEmail_action() {
            this.next(this.account);
            // return;
            if (this.confirm_code == "") {
            this.$Message.warning("验证码不能为空");
            return;
            }
            var data = await forget_email({
                account: this.account,
                confirm_code: this.confirm_code
            });
            if (data['result'] == 1) {
                this.next(this.account);
            }
            else if (data['result']==0){
                this.$Message.error("验证码错误");
            }
            else if (data['result']==2){
                this.$Message.error("用户不存在");
            }
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
.findpassword-1-wrap {
  width: 100%;
  height: 80%;
  //border: 1px solid rgb(24, 23, 23);

    .box-card {
        height: 85%;
        width: 100%;
        .el-input {
            margin-top: 1%;
            margin-bottom: 1%;
        }

        .el-button {
            width: 100%;
            margin-top: 5%;
            margin-bottom: 5%;
        }
    }
  .el-input {
    margin-top: 5%;
  }

  .el-button {
    margin-top: 5%;
  }
}
</style>