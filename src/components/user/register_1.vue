<template>
  <div class="register-1-wrap">
    <!-- html代码区 -->
      <div class="verilogin-wrap">
        <!-- html代码区 -->
            <el-card class="box-card">
                <el-row>
                    <el-input v-model="account"  placeholder="请输入账号" required>
                        <i slot="prefix" class="el-input__icon el-icon-user-solid"></i>
                    </el-input>
                </el-row>
                    <el-input v-model="confirm_code" placeholder="请输入密码" required>
                        <i slot="prefix" class="el-input__icon el-icon-message"></i>
                        
                    </el-input>
                
                <el-button type="primary" @click="register_direct()">注册</el-button>
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
    </div>


<!--    <el-input v-model="account" placeholder="请输入邮箱"></el-input>-->
<!--    <el-button @click="GetConfirmCode_action()" style="margin-left: 0%;">获取验证码</el-button>-->
<!--    <el-input v-model="confirm_code" placeholder="请输入验证码"></el-input>-->
<!--    <el-button @click="RegisterEmail_action()" type="primary" style="margin-left: 5%;">下一步</el-button>-->
  </div>
  <!-- 不要在此处添加其他东西 -->
</template>

<script>
import {get_confirm_code, register_email, register} from "@/api/index.js"

export default {
  name: "register_1",
  props: ["next"],
  components: {
    //组件
  },
  data() {
    //属性
    // eslint-disable-next-line no-mixed-spaces-and-tabs
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
      console.log(2);
      if (data.result == 0)
        this.$Message.warning("账号已注册");
      else
        this.$Message.success("发送成功");
    },
    async register_direct(){
      if (this.confirm_code == "") {
        this.$Message.warning("密码不能为空");
        return;
      }
      var data = await register({
        user_account: this.account,
        user_password: this.confirm_code
      });
      console.log(data);
      if (data.status == 'OK'){
          this.$message({
              message: '注册成功',
              type: 'success'
          });
          this.$router.push("/login");
      }
      else {
          this.$message.error("注册失败。"+data.reason);
      }
    },
    async RegisterEmail_action() {
        // this.next(this.account);
        // return;
        ///////////////////////////
      if (this.confirm_code == "") {
        this.$Message.warning("验证码不能为空");
        return;
      }
      var data = await register_email({
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
        this.$Message.error("账号已存在");
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
.register-1-wrap {
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