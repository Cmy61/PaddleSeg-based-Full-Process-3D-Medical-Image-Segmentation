<template>
    <div>
        <div class="showdiv2">
            <div class="showdiv1"> </div>
            <!-- <img src="../images/00003.webp" alt="" class="mainlogo"> -->
            <button class="buttonlogin" @click="to_login()">登录</button>
            <h1 style="font-size: 3rem; position: absolute;top:34%;left:38%;color: #00BFFF;">腹部器官分割系统</h1>
        </div>
        <Card class="show-Card">
            <div style="text-align:center">
                <h1>功能介绍</h1>
            </div>
            <div class="action1">
                <div style="text-align:center;margin-top:6%;"><img src="../assets/统计1.png" alt="" class="imgQQgcz" /></div>
                <h2 style="text-align:center;margin-top:7%;">器官统计信息</h2>
            </div>
            <div class="action2">
                <div style="text-align:center"><img src="../assets/统计2.png" alt="" class="imgQQgcz" /></div>
                <h2 style="text-align:center">表格统计详情</h2>
            </div>
            <div class="action3">
                <div style="text-align:center"><img src="../assets/项目管理.png" alt="" class="imgQQgcz" /></div>
                <h2 style="text-align:center;margin-top:3%;">项目管理</h2>
            </div>
            <div class="action4">
                <div style="text-align:center"><img src="../assets/集合管理.png" alt="" class="imgQQgcz" /></div>
                <h2 style="text-align:center">集合管理</h2>
            </div>
            <div class="action5">
                <div style="text-align:center;margin-top:2%;"><img src="../assets/CT展示1.png" alt="" class="imgQQgcz" /></div>
                <h2 style="text-align:center;margin-top:1%;">原图2D-3D展现</h2>
            </div>
            <div class="action6">
                <div style="text-align:center;margin-top:2%;"><img src="../assets/CT展示2.png" alt="" class="imgQQgcz" /></div>
                <h2 style="text-align:center">标签2D-3D展现</h2>
            </div>
            <div style="text-align: center;">
                <button class="btn-grad" @click="to_help()">了解更多</button>
            </div>
        </Card>
        <!-- <div style="text-align:center;position: absolute;
		top: 160%; 
		left: 42%; ">
		<h1>我们的团队</h1>
	</div> -->
    </div>
</template>
<script>
export default {
    data() {
        return {
            value2: 0
            , img1: require("../images/00003.webp")
            , img2: require("../images/00003.webp")
            , img3: require("../images/00003.webp")
            , img4: require("../images/00003.webp")
        }
    },
    methods: {
        to_help() {
            this.$router.replace("/help");
        },
        to_about() {
            this.$router.replace("/about");
        },
        to_login() {
            this.$router.replace("/login");
        }
    },
    mounted(){
        
    }
}
</script>

<style lang="scss" scoped>
// 	.CarouselItem_wrap{
//     width:100%;
//     height: 100%;
//      margin: auto;
//         display: flex;
//     display: -webkit-flex;
//         align-items:center;
//         justify-content:center;
//     .img{
//         max-width:100%;
//         max-height: 100%;
//         //  margin: auto;
//         // display: flex;
//         // display: -webkit-flex;
//         // align-items:center;
//         // justify-content:center;
//     }
// }
.mainlogo {
    width: 25%;
    max-height: 60%;
    position: absolute;
    top: 15%;
    left: 20%;
}

.showdiv1 {
    width: 100%;
    height: 100%;
    background-color: #5b6270;
    background-image: url("../assets/CT医院2.jpg");
    background-size: cover;
    opacity: 0.2;
}

.showdiv2 {
    width: 100%;
    height: 100%;
    background-color: #5b6270;
    // background-image: url("../assets/homeMain1.png");
    // background-size: cover;
    opacity: 0.9;
}

// .show-Card{
// 	height:70%;
// 	width: 90%;
// 	position: absolute;
// 	top: 110%; 
// 	left: 5%; 
// }
.show-Card {
    height: 110%;
    width: 90%;
    position: absolute;
    top: 110%;
    left: 5%;
    vertical-align:middle;
}

.show-Card1 {
    height: 70%;
    width: 90%;
    position: absolute;
    top: 230%;

    left: 5%;
}

.img1 {
    height: 60%;
    width: 70%;
    position: absolute;
    top: 170%;
    left: 15%;
}

//功能介绍
.action1 {
    width: 30%;
    height: 70%;
    position: absolute;
    top: 15%;
    left: 5%;

    .imgQQgcz {
        max-width: 80%;
        max-height: 50%;
        // border-radius: 50%;//圆形图片设置
    }
}

.action2 {
    width: 30%;
    height: 70%;
    position: absolute;
    top: 15%;
    left: 35%;

    .imgQQgcz {
        max-width: 80%;
        max-height: 50%;
        // border-radius: 50%;
    }
}

.action3 {
    width: 30%;
    height: 70%;
    position: absolute;
    top: 15%;
    left: 65%;

    .imgQQgcz {
        max-width: 80%;
        max-height: 50%;
        // border-radius: 50%;
    }
}

.action4 {
    width: 30%;
    height: 70%;
    position: absolute;
    top: 50%;
    left: 5%;

    .imgQQgcz {
        max-width: 80%;
        max-height: 50%;
        // border-radius: 50%;
    }
}

.action5 {
    width: 30%;
    height: 70%;
    position: absolute;
    top: 50%;
    left: 35%;

    .imgQQgcz {
        max-width: 80%;
        max-height: 50%;
        // border-radius: 50%;
    }
}

.action6 {
    width: 30%;
    height: 70%;
    position: absolute;
    top: 50%;
    left: 65%;

    .imgQQgcz {
        max-width: 80%;
        max-height: 50%;
        // border-radius: 50%;
    }
}

//关于我们
.zxq {
    width: 30%;
    height: 70%;
    position: absolute;
    top: 20%;
    left: 5%;

    .imgQQgcz {
        max-width: 40%;
        max-height: 40%;
        border-radius: 50%;
    }
}

.xhr {
    width: 30%;
    height: 70%;
    position: absolute;
    top: 20%;
    left: 35%;

    .imgQQgcz {
        max-width: 40%;
        max-height: 40%;
        border-radius: 50%;
    }
}

.gcz {
    width: 30%;
    height: 70%;
    position: absolute;
    top: 20%;
    left: 65%;

    .imgQQgcz {
        max-width: 40%;
        max-height: 40%;
        border-radius: 50%;
    }
}

//登录按键css
.buttonlogin {
    width: 15%;
    display: inline-block;
    padding: 15px 25px;
    font-size: 24px;
    cursor: pointer;
    text-align: center;
    text-decoration: none;
    outline: none;
    color: #777;
    // background-color: #4CAF50;
    background-image: linear-gradient(120deg, #a1c4fd 0%, #c2e9fb 100%);
    border: none;
    border-radius: 15px;
    box-shadow: 0 9px #999;
    position: absolute;
    top: 64%;
    left: 42.5%;
}

.buttonlogin:hover {
    background-color: #3e8e41
}

.buttonlogin:active {
    background-color: #3e8e41;
    box-shadow: 0 5px #666;
    transform: translateY(4px);
}

//界面转换按键

.btn-grad {
    background-image: linear-gradient(to right, #77A1D3 0%, #79CBCA 51%, #77A1D3 100%)
}

.btn-grad {
    margin: 10px;
    padding: 15px 45px;
    text-align: center;
    text-transform: uppercase;
    transition: 0.5s;
    background-size: 200% auto;
    color: white;
    box-shadow: 0 0 20px #eee;
    border-radius: 10px;
    display: block;
    position: absolute;
    top: 80%;
    left: 42.5%;
}

.btn-grad:hover {
    background-position: right center;
    /* change the direction of the change here */
    color: #fff;
    text-decoration: none;
}
</style>
