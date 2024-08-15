<template>
	<div class="func-wrap">
        <div class="func-body">
            <div class="func-body-left">
                <!-- 导航菜单 -->
                <div class="func-left-header">
                    <el-menu :default-active="func_left_header_index" mode="horizontal" @select="handleLeftHeaderMenuSelect">
                        <el-menu-item index="1" class="el-menu-item-my">基本信息</el-menu-item>
                        <el-menu-item index="2" class="el-menu-item-my">CT操作</el-menu-item>
                    </el-menu>
                </div>
                <!-- 基本 -->
                <div class="func-left-body" v-show="func_left_header_index=='1'">
                    <!-- 项目描述信息 -->
                    <template>
                        <div class="func-left-body-title">
                            <span style="font-size: 22px;font-weight:bold;">项目信息</span>
                            <div class="func-left-body-title-button-wrap">
                                <el-button size="mini" @click="choose_other_porject">选择其他项目</el-button>
                                <el-button size="mini" @click="link_exsisted_set">绑定已有集合</el-button>
                            </div>
                        </div>
                        <el-descriptions :column="1" size="mini" border class="proj-descript" style="margin-left:2%;margin-right:2%;">

                            <el-descriptions-item>
                                <template slot="label">
                                    <i class="el-icon-user"></i>
                                    项目ID
                                </template>
                                {{ project_id }}
                            </el-descriptions-item>

                            <el-descriptions-item>
                                <template slot="label">
                                    <i class="el-icon-mobile-phone"></i>
                                    项目名称
                                </template>
                                {{ project_name }}
                            </el-descriptions-item>

                            <el-descriptions-item>
                                <template slot="label">
                                    <i class="el-icon-location-outline"></i>
                                    项目创建时间
                                </template>
                                {{ project_build_time }}
                            </el-descriptions-item>

                            <el-descriptions-item>
                                <template slot="label">
                                    <i class="el-icon-location-outline"></i>
                                    项目关联集合
                                </template>
                                {{ project_sets_id }}
                            </el-descriptions-item>

                            <el-descriptions-item>
                                <template slot="label">
                                    <i class="el-icon-tickets"></i>
                                    备注
                                </template>
                                {{ project_remark }}
                            </el-descriptions-item>

                        </el-descriptions>
                    </template>
                    <!-- 集合描述信息 -->
                    <template>
                        <div class="func-left-body-title">
                            <span style="font-size: 22px;font-weight:bold;">集合信息</span>
                            <div class="func-left-body-title-button-wrap">
                                <el-button size="mini" @click="upload_CT" :disabled="set_id=='暂未选择'">上传CT</el-button>
                                <el-button size="mini" @click="seg_predict" :disabled="set_id=='暂未选择'">分割预测</el-button>
                                <el-button size="mini" @click="rebuild_3d" :disabled="set_id=='暂未选择'">3D重建</el-button>
                                <el-button size="mini" @click="download_label" :disabled="set_id=='暂未选择'">下载标签</el-button>
                            </div>
                        </div>
                        <el-descriptions :column="1" size="mini" border class="proj-descript" style="margin-left:2%;margin-right:2%;">

                            <el-descriptions-item>
                                <template slot="label">
                                    <i class="el-icon-user"></i>
                                    集合ID
                                </template>
                                {{ set_id }}
                            </el-descriptions-item>

                            <el-descriptions-item>
                                <template slot="label">
                                    <i class="el-icon-mobile-phone"></i>
                                    集合名称
                                </template>
                                {{ set_name }}
                            </el-descriptions-item>

                            <el-descriptions-item>
                                <template slot="label">
                                    <i class="el-icon-location-outline"></i>
                                    集合创建时间
                                </template>
                                {{ set_build_time }} 
                            </el-descriptions-item>

                            <el-descriptions-item>
                                <template slot="label">
                                    <i class="el-icon-location-outline"></i>
                                    是否上传数据?
                                </template>
                                <el-tag size="small" type="danger" v-if="set_nii_path==''">否</el-tag> 
                                <el-tag size="small" type="success" v-else>是</el-tag> 
                            </el-descriptions-item>

                            <el-descriptions-item>
                                <template slot="label">
                                    <i class="el-icon-location-outline"></i>
                                    是否分割预测?
                                </template>
                                <el-tag size="small" type="danger" v-if="set_label_nii_path==''">否</el-tag> 
                                <el-tag size="small" type="success" v-else>是</el-tag> 
                            </el-descriptions-item>

                            <el-descriptions-item>
                                <template slot="label">
                                    <i class="el-icon-location-outline"></i>
                                    是否3D重建?
                                </template>
                                <el-tag size="small" type="danger" v-if="set_stl_directory==''">否</el-tag> 
                                <el-tag size="small" type="success" v-else>是</el-tag> 
                            </el-descriptions-item>

                            <el-descriptions-item>
                                <template slot="label">
                                    <i class="el-icon-tickets"></i>
                                    备注
                                </template>
                                
                            </el-descriptions-item>

                        </el-descriptions>
                    </template>
                    <!-- 选择集合 -->
                    <template>
                        
                        <div class="func-left-body-title">
                            <span style="font-size: 22px;font-weight:bold;">选择集合</span>  
                        </div>
                        <setTest
                        ref="setManage"
                        :projectID="project_id"
                        :selectFunc="selectSet"
                        :getSetsFunc="loadSets"
                        :project_sets_id="project_sets_id"
                        >

                        </setTest>
                    </template>
                </div>
                <!-- CT -->
                <div class="func-left-body" v-show="func_left_header_index=='2'">
                    <!-- 标签颜色切换 -->
                    <div style="width:98%;display: flex;margin-top:1%;margin-bottom:1%;margin-left:1%;margin-right:1%;">
                        <div style="width:45%;font-size: 15px;font-weight:bold;">是否显示标签颜色</div>
                        <el-switch
                            v-model="color_show"
                            :disabled="set_label_nii_path==''"
                        >
                        </el-switch>
                    </div>
                    <div style="height:1px;width:98%;background-color: #DCDFE6;margin-left:1%;margin-right:1%;"></div>
                    <!-- CT 2D切换 -->
                    <div style="width:98%;margin-top:1%;margin-bottom:1%;margin-left:1%;margin-right:1%;">
                        <span style="font-size: 15px;font-weight:bold;">CT集合</span>
                        <!-- X -->
                        <div style="width:100%;display:flex;height:40px;line-height: 40px;">
                            <span style="width:14%;">X:{{ select_dims.x }}/{{ dims.x }}</span>
                            <el-slider
                                v-model="select_dims.x"
                                :min="0"
                                :max="Math.max(0,dims.x - 1)"
                                :step="1"
                                style="width:80%;margin-left:6%;"
                                >
                            </el-slider>
                        </div>
                        <!-- Y -->
                        <div style="width:100%;display:flex;height:40px;line-height: 40px;">
                            <span style="width:14%;">Y:{{ select_dims.y }}/{{ dims.y }}</span>
                            <el-slider
                                v-model="select_dims.y"
                                :min="0"
                                :max="Math.max(0,dims.y - 1)"
                                :step="1"
                                style="width:80%;margin-left:6%;">
                            </el-slider>
                        </div>
                        <!-- Z -->
                        <div style="width:100%;display:flex;height:40px;line-height: 40px;">
                            <span style="width:14%;">Z:{{ select_dims.z }}/{{ dims.z }}</span>
                            <el-slider
                                v-model="select_dims.z"
                                :min="0"
                                :max="Math.max(0,dims.z - 1)"
                                :step="1"
                                style="width:80%;margin-left:6%;">
                            </el-slider>
                        </div>
                    </div>
                    <div style="height:1px;width:98%;background-color: #DCDFE6;margin-left:1%;margin-right:1%;"></div>

                    
                    <div style="width:98%;margin-top:1%;margin-bottom:1%;margin-left:1%;margin-right:1%;">
                        <span style="font-size: 15px;font-weight:bold;">窗位窗宽</span>
                        <div style="margin-top:1%;margin-bottom:1%;">
                            窗宽：
                            <el-input @input="handleWWWLinput('WW')" 
                                clearable v-model="WW_input" 
                                :placeholder="WW" style="width:60%;">
                            </el-input>
                            <el-button @click="handleWWWLenter('WW')" style="margin-left:2%;">确定</el-button>
                        </div>
                        <div style="margin-top:1%;margin-bottom:1%;">
                            窗位：
                            <el-input @input="handleWWWLinput('WL')" 
                                clearable v-model="WL_input" 
                                :placeholder="WL" style="width:60%;">
                            </el-input>
                            <el-button @click="handleWWWLenter('WL')" style="margin-left:2%;">确定</el-button>
                        </div>
                    </div>
                    <div style="height:1px;width:98%;background-color: #DCDFE6;margin-left:1%;margin-right:1%;"></div>

                    <div style="width:98%;margin-top:1%;margin-bottom:1%;margin-left:1%;margin-right:1%;">
                        <span style="font-size: 15px;font-weight:bold;">标签管理</span>
                        <el-empty description="暂无标签，请进行分割预测" v-if="Object.keys(label_dict).length === 0"></el-empty>
                        <div  v-else>
                            <el-button @click="$refs.slice_test.change_visible(true)">预标注修改</el-button>
                        </div>
                        
                        <Collapse simple>
                            <Panel v-for="(v,k,index) in label_dict" :name="k" :key="'panel'+k">
                                
                                {{ label_chinese_name[k] }}
                                <ButtonGroup style="float:right;" >
                                    <div @click.stop.prevent="() => {}">
                                        <ColorPicker v-model="label_color_select[k]" size="default" format="rgb" @on-change="test_click(k)"/>
                                        <Button icon="ios-eye-outline" @click.stop="v.visible=false;" v-show="v.visible==true"></Button>
                                        <Button icon="ios-eye-off-outline" @click.stop="v.visible=true;" v-show="v.visible==false"></Button>
                                        <Button icon="ios-create-outline"></Button>
                                        <Button icon="ios-trash-outline"></Button>
                                    </div>
                                    
                                    <!-- <ColorPicker v-model="color1" @on-change="test_click" format="rgb" :alpha="false"/> -->
                                    
                                    
                                    
                                </ButtonGroup>
                                <div slot="content">
                                    透明度:{{ v.opacity }}/{{ 1 }}
                                    <el-slider
                                        v-model="v.opacity"
                                        :min="0"
                                        :max="1"
                                        :step="0.01">
                                    </el-slider>
                                    <div>
                                        数量：{{ 1 }}
                                    </div>
                                    <div>
                                        体积：{{ v.volume+" 立方厘米"  }} 
                                    </div>
                                    <div>
                                        X截面面积：{{ label_graph_space[k][0].toFixed(3) + " 平方厘米"}}
                                    </div>
                                    <div>
                                        Y截面面积：{{ label_graph_space[k][1].toFixed(3) + " 平方厘米" }}
                                    </div>
                                    <div>
                                        Z截面面积：{{ label_graph_space[k][2].toFixed(3) + " 平方厘米" }}
                                    </div>
                                    
                                </div>
                            </Panel>
                            
                        </Collapse>
                    </div>
                    
                </div>
                

            </div>
            <div class="func-body-right">
                <SliceTest
                ref="slice_test"
                :origin_url="origin_url"
                :label_url="label_url"
                :WW="WW"
                :WL="WL"
                :color_show="color_show"
                :dims="dims"
                :select_dims="select_dims"
                :label_dict="label_dict"
                :label_graph_space="label_graph_space"
                >
            
                </SliceTest>
                
            </div>
        </div>
        <uploadCT
        :dialogTableVisible="upload_CT_visible"
        :change_visible="change_upload_CT_visible"
        :get_upload_data="get_upload_params"
        >
        </uploadCT>
        <TransferSetSel
        :show_flag="project_sel_sets_flag"
        :sets="sets"
        :project_sets_id_list="project_sets_id"
        :close_dialog="handle_project_link_set_close"
        :join_sets="join_sets"
        >
        </TransferSetSel>
    </div>

</template>

<script>
import SliceTest from "@/components/slice_test.vue"
import setTest from "@/components/setTest.vue"
import uploadCT from "@/components/uploadCT.vue"
import TransferSetSel from "@/components/TransferSetSel.vue"
import {build3D,getLabel,joinSets,segPredict,exportLabel} from "@/api/index.js"
	export default {
		components: {
            SliceTest,
            setTest,
            uploadCT,
            TransferSetSel
		},
		data() {
			return {
                
                //选择的项目信息
                project_id:0,
                project_name:null,
                project_build_time:null,
                project_sets_id:[],
                project_remark:null,
                project_sel_sets_flag:false,
                
                //选择的set信息
                sets:[{set_id:0,set_name:0}],
                set_id:"暂未选择",
                set_name:"暂未选择",
                set_build_time:"",
                set_origin_path:"",
                set_nii_path:"",
                set_label_nii_path:"",
                set_label_path:"",
                set_stl_directory:"",

                //对应的label信息
                label_dict: {},
                label_color_select: {},
                label_chinese_name:
                [
                    "",
					"脾脏",
					"右肾",
					"左肾",
					"胆囊",
					"食道",
					"肝脏",
					"胃",
					"主动脉",
					"下腔静脉",
					"胰腺",
					"右肾上腺",
					"左肾上腺",
					"十二指肠",
					"膀胱",
					"前列腺/子宫"
				], // 下标对应id
                //面积
                label_graph_space:
                {
                    1:[0,0,0],
                    2:[0,0,0],
                    3:[0,0,0],
                    4:[0,0,0],
                    5:[0,0,0],
                    6:[0,0,0],
                    7:[0,0,0],
                    8:[0,0,0],
                    9:[0,0,0],
                    10:[0,0,0],
                    11:[0,0,0],
                    12:[0,0,0],
                    13:[0,0,0],
                    14:[0,0,0],
                    15:[0,0,0]
                },



                //标签页下标
                func_left_header_index:'1',
                //slice展示使用
                origin_url:"",
                label_url:"",
                WW:256,     WW_input:'',
                WL:0,       WL_input:'',
                color_show:false,

                dims:{x:0,y:0,z:0},
                select_dims:{x:0,y:0,z:0},

                //上传CT弹窗可视化
                upload_CT_visible:false,

            }
		},
		props: {
			
		},
		watch: {
			
		},
		mounted() {
            //判断是否选择了项目后，进入的该界面
            try{
                console.log(this.$route.params);
                if (this.$route.params.project_id && this.$route.params.project_name){
                    this.project_id = this.$route.params.project_id;
                    this.project_name = this.$route.params.project_name;
                    this.project_build_time = this.$route.params.project_build_time;
                    this.project_sets_id = this.$route.params.sets_id;
                    this.project_remark = this.$route.params.remark;
                }
                else {
                    // this.$router.push({
                    //     name:'ProjSel',
                    // })
                }
            } catch(error){
                // this.$router.push({
                //     name:'ProjSel',
                // })
            }
		},
		methods: {
            //用于处理菜单的切换select事件
            handleLeftHeaderMenuSelect(key, keyPath){
                this.func_left_header_index = key;
            },
            //用于处理窗位窗宽的输入
            handleWWWLinput(type){
                if (type=='WW'){
                    // 先把非数字的都替换掉，除了数字和 .
                    this.WW_input = this.WW_input.replace(/[^\d.]/g, "")
                    // 保证只有出现一个 . 而没有多个 .
                    this.WW_input = this.WW_input.replace(/\.{2,}/g, ".")
                    // 必须保证第一个为数字而不是 .
                    this.WW_input = this.WW_input.replace(/^\./g, "")
                    // 如果位数不为1，那么第一位数不能输入0
                    if (this.WW_input.length > 1){
                        this.WW_input = this.WW_input.replace(/^0/g, '')
                    }
                    
                }

                else if (type=='WL'){
                    let fu = "";
                    if (this.WL_input[0] == "-") {
                        fu = "-"
                    }
                    // 先把非数字的都替换掉，除了数字和 .
                    this.WL_input = this.WL_input.replace(/[^\d.]/g, "")
                    // 保证只有出现一个 . 而没有多个 .
                    this.WL_input = this.WL_input.replace(/\.{2,}/g, ".")
                    // 必须保证第一个为数字而不是 .
                    this.WL_input = this.WL_input.replace(/^\./g, "")
                    // 如果位数不为1，那么第一位数不能输入0
                    if (this.WL_input.length > 1){
                        this.WL_input = this.WL_input.replace(/^0/g, '')
                    }
                    this.WL_input = fu + this.WL_input;
                }
            },
            //用于处理窗位窗宽的确定修改
            handleWWWLenter(type){
                if (type=='WW'){
                    let num = this.WW_input * 1;
                    if (num <= 0 || num >= 4096){
                        this.$message.error("WW窗宽应该大于0且小于4096,取值范围错误");
                    }
                    else {
                        this.WW = num;
                        this.WW_input = '';
                    }
                }
                else if (type=='WL'){
                    let num = this.WL_input * 1;
                    if (num <= -2048 || num >= 2048){
                        this.$message.error("WL窗位应该大于-2048且小于2048,取值范围错误");
                    }
                    else {
                        this.WL = num;
                        this.WL_input = '';
                    }
                }
            },
            //选择集合
            selectSet(row){
                this.set_id = row.set_id;
                this.set_name = row.set_name;
                this.set_build_time = row.build_time;
                this.set_origin_path = row.original_path;
                this.set_nii_path = row.nii_path;
                this.set_label_nii_path = row.label_path;
                this.set_label_path = row.nii_after_path;
                this.set_stl_directory = row.stl_directory;

                // 处理slice使用的url
                if (this.set_nii_path != ''){
                    this.origin_url = 'http://localhost:8888/download/' + this.set_nii_path;
                }
                else {
                    this.origin_url = '';
                }

                if (this.set_label_nii_path != ''){
                    this.label_url = 'http://localhost:8888/download/' + this.set_label_nii_path;
                    this.get_label();
                }
                else {
                    this.label_url = '';
                }

                
                
                
            },
            //从子组件中获得sets
            loadSets(get_sets){
                this.sets = get_sets;
            },
            //选择其他项目
            choose_other_porject(){
                this.$router.push({
                    name:'ProjSel',
                })
            },
            //绑定已有集合
            link_exsisted_set(){
                //暂未实现
                this.project_sel_sets_flag = true;
                console.log(this.project_sel_sets_flag);
                console.log(this.sets);
                console.log(this.sets[0]);
                console.log(this.project_sets_id_list);
                
                // this.$message.error("暂未实现");
                return
            },
            //绑定已有集合的关闭函数
            handle_project_link_set_close(){
                this.project_sel_sets_flag = false;
                this.$refs.setManage.$refs.set_sel_table.refresh();
            },
            //绑定已有集合的处理函数
            async join_sets(sets_id_list){
                const data = await joinSets({
                    project_id:this.project_id,
                    sets_id_list:sets_id_list
                });
            },
            //上传CT数据
            upload_CT(){
                this.change_upload_CT_visible(true);
                
                return
            },
            //改变上传CT数据的弹窗可视化参数
            async change_upload_CT_visible(state){
                this.upload_CT_visible = state;
                if (!state){
                    await this.$refs.setManage.$refs.set_sel_table.refresh();
                    for (let i=0;i<this.sets.length;++i){
                        let row = this.sets[i];
                        if (row.set_id == this.set_id){
                            this.selectSet(row);
                            console.log("selectRow success")
                            break;
                        }
                    }
                    this.$forceUpdate();
                }
            },
            //设置获取上传的参数
            get_upload_params(){
                return {
                    'set_id':this.set_id,
                    're_upload':false
                }
            },
            //分割预测
            async seg_predict(){
                var data = await segPredict({
                    set_id:this.set_id
                });
                if (data.status=="OK"){
                    await this.$refs.setManage.$refs.set_sel_table.refresh();
                    for (let i=0;i<this.sets.length;++i){
                        let row = this.sets[i];
                        if (row.set_id == this.set_id){
                            this.selectSet(row);
                            console.log("selectRow success")
                            break;
                        }
                    }
                    this.$forceUpdate();
                }
            },
            //3D重建
            async rebuild_3d(){
                let data = await build3D({
                    'set_id':this.set_id
                });
                if (data.status=="OK"){
                    await this.$refs.setManage.$refs.set_sel_table.refresh();
                    for (let i=0;i<this.sets.length;++i){
                        let row = this.sets[i];
                        if (row.set_id == this.set_id){
                            this.selectSet(row);
                            console.log("selectRow success")
                            break;
                        }
                    }
                    this.$forceUpdate();
                }
            },
            //下载标签
            async download_label(){
                var data = await exportLabel({
                    set_id:this.set_id
                });
                console.log(data);
                let binaryData = [];
                binaryData.push(data);
                let objectUrl = window.URL.createObjectURL(new Blob(binaryData));
                let downloadLink = document.createElement('a');
                downloadLink.href = objectUrl;
                downloadLink.style.display = 'none';
                // downloadLink.download = ""+this.set_name+"标签"+".nii"
                downloadLink.setAttribute('download', ""+this.set_name+"标签"+".nii");
                document.body.appendChild(downloadLink);
                downloadLink.click();
                window.URL.revokeObjectURL(downloadLink.href);
                document.body.removeChild(downloadLink);
                
            },
            //获取标签
            async get_label(){
                const data = await getLabel({
                    set_id:this.set_id
                })
                console.log(data);

                this.label_dict = data.label_list;
                console.log(Object.keys(data.label_list));
                const key_list = Object.keys(data.label_list);
                for (let i=0;i<key_list.length;++i){
                    let key = key_list[i];
                    // console.log(data.label_list[key])
                    this.label_color_select[key] = "rgba(" + data.label_list[key].r + "," + data.label_list[key].g + ","+ data.label_list[key].b +",1)";
                }
                
                

            },
            //
            test_click(key){
                // this.color1 = val;
                let val = (this.label_color_select[key]+'').match(/(\d(\.\d+)?)+/g);
                this.label_dict[key].r = val[0];
                this.label_dict[key].g = val[1];
                this.label_dict[key].b = val[2];
            }
		},
        
	}
</script>

<style lang="scss">
.func-wrap{
    height:90%;
    width:100%;
    overflow: hidden;
    .func-body{
        height:100%;
        width:100%;
        border: 1px solid rgb(228, 225, 225); //外边框
        display: flex;
        .func-body-left{
            height:100%;
            width:30%;
            border: 1px solid rgb(228, 225, 225); //外边框
            .func-left-header{
                height:5%;
                width:100%;
                border: 1px solid rgb(228, 225, 225); //外边框
                .el-menu-item-my {
                    width:50%;
                    height:100%;
                    text-align: center;
                }
            }
            .func-left-body{
                height:90%;
                width:100%;
                padding-top: 2%;
                overflow: auto;
                .func-left-body-title{
                    max-height:10%;
                    width:100%;
                    // border-bottom: 1px solid rgb(228, 225, 225);
                    border-top: 1px solid rgb(228, 225, 225);
                    margin-bottom:1.5%;
                    margin-top:1.5%;
                    text-align: center;
                    font-size: large;
                    .func-left-body-title-button-wrap{
                        width:95%;
                        margin-left:2.5%;
                        margin-right:2.5%;
                        height:60%;
                        display: flex;
                        justify-content: space-between;
                    }
                }
            }
        }
        .func-body-right{
            height:100%;
            width:70%;
            border: 1px solid rgb(228, 225, 225); //外边框
        }
    }
}
</style>

