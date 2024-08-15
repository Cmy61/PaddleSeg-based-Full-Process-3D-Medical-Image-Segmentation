<template>
  <div class="homeheader-wrap">
    <Menu mode="horizontal" active-name="1">
      <row>
        <Col span="3" style="width:100%;height: 100%;">
			<div style="width: 100%;height:100%;">
          <img src="../assets/logo.png" alt="" class="headerlogo">
		  </div>
        </Col>
        <Col span="3" style="width:100%;">
          <MenuItem name="2" to="/" style="width:100%;">
            <Icon type="md-home" />
            首页
          </MenuItem>
        </Col>
		<Col span="3" style="width:100%;">
		  <MenuItem @click.native="to_display()" name="5" style="width:100%;">
		    <Icon type="ios-paper" />
		    统计数据
		  </MenuItem>
		</Col>
		<Col span="3" style="width:100%;">
		  <MenuItem @click.native="to_patient()" name="6" style="width:100%;">
		    <Icon type="ios-people" />
		    项目选择
		  </MenuItem>
		</Col>
        
        <Col span="8" style="width:100%;"></Col>
        <Col span="1">
          <div style="margin-top:7.5px;height:52.5px;">
            <el-avatar shape="square" :size="45" :src="squareUrl" v-if="flag"></el-avatar>
            <el-avatar shape="square" :size="45" v-else src="https://cube.elemecdn.com/3/7c/3ea6beec64369c2642b92c6726f1epng.png"></el-avatar>
          </div>
          
        </Col>
        <Col span="3" style="width:100%;margin-top:0;">
          <Submenu name="7" style="width:100%;">
            <template slot="title">
              个人中心
            </template>
            <MenuGroup title="用户">
              <MenuItem name="3-1" @click.native="to_login()">登录</MenuItem>
              <MenuItem name="3-2" @click.native="to_register()">注册</MenuItem>
              <MenuItem name="3-3" @click.native="logout()">注销</MenuItem>
            </MenuGroup>
          </Submenu>
        </Col>
      </row>
    </Menu>
  </div>
</template>

<script>
// import global from "@/store/data.js";
import {logout} from "@/api/index.js"
export default {
  data(){
    return {
      squareUrl:require("@/assets/QQgcz.jpg"),
      flag:false
    }
  },
  computed:{
    
  },
  methods: {
    async handleClick() {
      this.$router.push({
        path: "about",
      });
      const data = await getPostData({ name: "xxx" });
    },
    to_user() {
      if (false) {
		  if(this.$router.currentRoute.fullPath !== "/login"){
			  
			  this.$router.replace("/login");
			  this.$Message.info('请先进行登录');
		  }
      } else {
		if(this.$router.currentRoute.fullPath !== "/user"){
			this.$router.replace("/user");
		}
      }
    },
    to_login() {
      if (true) { 
		  if(this.$router.currentRoute.fullPath !== "/login"){
			  this.$router.replace("/login");
		  }
      }
    },
    to_register() {
		if(this.$router.currentRoute.fullPath !== "/register"){
			this.$router.replace("/register");
		}
    },
    to_patient() {
      if (false) {
		  if(this.$router.currentRoute.fullPath !== "/login"){
			  this.$router.replace("/login");
			  this.$Message.info('请先进行登录');
		}
      } else {
		  if(this.$router.currentRoute.fullPath !=="/projSel"){
			   this.$router.replace("/projSel");
		  }
      }
    },
    to_display() {
      if (false) {
		  if(this.$router.currentRoute.fullPath !=="/login"){
			  this.$router.replace("/login");
			  this.$Message.info('请先进行登录');
		  }
      } else {
		if(false){
			if(this.$router.currentRoute.fullPath !=="/patient"){
				this.$router.replace("/patient");
				this.$Message.info('请选定患者');
			}
		  }else{
			  if(this.$router.currentRoute.fullPath !=="/Display"){
				  this.$router.replace("/charts"); 
			  }
		  }
      }
    },
    logout() {	
		// global.username = "";
      logout();
      this.flag = false;
    },
  },
  mounted(){
    this.flag = this.$cookie.get('account');
  }
};
</script>

<style lang="scss">
	.headerlogo{
		// position: absolute;
		max-width:80%;
		max-height: 80%;
		margin-top:4%;
		margin-left:13%;
		// margin-right: 15%;
		// margin-right: 20%;
		// margin-bottom: 40%;
	}
.homeheader-wrap {
  width: 90%;
  height: 100%;
  margin: 0 auto;
  .ivu-row {
    width:100%;
    height: 100%;
    align-items: center;
    // font-size: 20px;
  }
}
// .ivu-menu-submenu-title{
//   // font-size:0.1rem;
// }
</style>