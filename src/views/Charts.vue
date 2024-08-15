<template>
	<!-- 统计图表区 -->
	<div style="height: 100%; width: 100%;" v-if="finish">
		<!-- 两个图 -->
		<div style="width: 79%; border: 1px solid #ccc; padding: 0.8% 3%; margin: 0.5% 10%;">
			<div style="width: 79%;margin-top: 1%;margin-left:0%;font-size: 18px;font-weight:bold;">项目--器官统计</div>
			<div style="height:1px;width:93%;margin-left:0%;margin-right:3.5%;background-color: #DCDFE6;margin-bottom:1%;"></div>
			<el-select v-model="project" placeholder="请选择项目" class="charts_el_select" @change="update_graphs">
				<el-option v-for="item in select_project" :key="item.value" :label="item.label" :value="item.value">
				</el-option>
			</el-select>
			<el-select v-model="organ" placeholder="请选择器官" class="charts_el_select" @change="update_graphs">
				<el-option v-for="item in select_organ" :key="item.value" :label="item.label" :value="item.value">
				</el-option>
			</el-select>
			<div style=" display:flex;">
				<graph1 :option="graph1_option"></graph1>
				<graph2 :option="graph2_option"></graph2>
			</div>
		</div>
		<!-- 表格 -->
		<div style="height: 85%; width: 79%; margin: 0.5% 10%; padding: 0 0; border: 1px solid #ccc">
			<div style="width: 79%;margin-top: 1%;margin-left:3.2%;font-size: 18px;font-weight:bold;">集合--器官体积</div>
			<div style="height:1px;width:93%;margin-left:3.2%;margin-right:3.5%;background-color: #DCDFE6;"></div>
			<div style="width: 93%;margin-top: 1%;margin-left:3.2%;font-size: 8px;">
				<span style="color: #F56C6C;">红色</span>
				代表体积偏大。
				<span style="color: #67C23A;">绿色</span>
				代表体积处于正常范围。
				<span style="color: #E6A23C;">黄色</span>
				代表体积偏小。
				<span style="color: #909399;">灰色</span>
				代表暂无此数据。
				<span style="color: #409EFF;">蓝色</span>
				代表此数据受个体影响较大，无可参考区间。
				<span style="color: #303133;">无含义</span>
				代表此数据对于该器官无意义（如血管）。
			</div>
			
			<ChartTable :key="'set_sel' + 'table'" ref="set_sel_table" :resData="resData" :propsData="propsData"
				:labelData="labelData" :widthData="widthData" :selectFunc="selectFunc" :get_update="get_update" 
				:organ_normal_volume="organ_normal_volume">
			</ChartTable>
			
		</div>
	</div>
</template>

<script>
import ChartTable from '../components/tables/ChartTable.vue';
import graph1 from "@/components/graphs/graph1.vue"
import graph2 from '../components/graphs/graph2.vue';

import { getProjects, getSets, getLabel } from "@/api/index.js"



// import TransferSetSel from "@/components/TransferSetSel.vue"
export default {
	data() {
		return {
			finish: false,
			projects_data_temp: [],
			sets_data_temp: [],
			set_1_labels_temp: [],
			set_2_labels_temp: [],
			set_3_labels_temp: [],
			sets_data: {},
			// 表格数据
			propsData: [],
			labelData: [],
			resData: [],
			widthData: [],

			// 图中的选项
			select_project: [],
			select_organ: [],
			project: '',
			organ: '',

			// 图中数据
			graph1_option: {
				title: {
					text: '集合统计'
				},
				tooltip: {},
				legend: {
					data: ['体积']
				},
				xAxis: {
					data: []
					// data: ['集合1', '集合2', '集合3', '集合4', '集合5', '集合6']
				},
				yAxis: {},
				series: [
					{
						name: '体积',
						type: 'line',
						data: [],
						// data: [5, 20, 36, 10, 10, 20]
					}
				]
			},
			graph2_option: {
				title: {
					text: '体积统计'
				},
				series: [
					{
						name: '体积',
						type: 'pie',
						data: []
					}
				]
			},
			LABEL_NAMES: {
				1: "spleen",
				2: "right kidney",
				3: "left kidney",
				4: "gall bladder",
				5: "esophagus",
				6: "liver",
				7: "stomach",
				8: "aorta",
				9: "postcava",
				10: "pancreas",
				11: "right adrenal gland",
				12: "left adrenal gland",
				13: "duodenum",
				14: "bladder",
				15: "prostate/uterus"
			},
			organ_normal_volume: {
				1: [50, 250],
				2: [100, 200],
				3: [100, 150],
				4: [30, 50],
				5: [0, 1],
				6: [1200, 1600],
				7: [900, 1500],
				8: [0, 1],
				9: [0, 1],
				10: [60, 100],
				11: [0, 1],
				12: [0, 1],
				13: [0, 1],
				14: [300, 500],
				15: [0, 1]
			}
		};
	},
	methods: {
		selectFunc() { },

		// 当选择新的器官时更新图数据
		async update_graphs() {
			// 如果值为空则不更新
			if (this.project == '' || this.organ == '') {
				return false;
			}
			// 更新数据
			await this.get_update();

			// 从项目获取对应集合
			var project_sets_id = [];
			var project_sets_name = [];
			var project_sets_val = [];
			var normalvolume = 0;
			var bigvolume = 0;
			var smallvolume = 0;

			// 获取当前项目对应的集合
			this.projects_data_temp.projects.forEach(element => {
				if (element.project_id == this.project) {
					project_sets_id = element.sets_id;
				}
			});

			// 统计正常体积、偏小体积、偏大体积
			project_sets_id.forEach(element => {
				var val_temp = this.sets_data[element].labels[this.organ].volume;
				console.log(val_temp);
				console.log(111);
				// 将当前器官对应集合名字和器官体积放入图数据中
				project_sets_name.push(this.sets_data[element].set_name);
				project_sets_val.push(val_temp);
				if (val_temp < this.organ_normal_volume[this.organ][0]) {
					smallvolume += 1;
				} else if (val_temp < this.organ_normal_volume[this.organ][1]) {
					normalvolume += 1;
				} else {
					bigvolume += 1;
				}
			});

			// 更新折线图
			this.graph1_option.xAxis = { data: project_sets_name };
			this.graph1_option.series[0].data = project_sets_val;

			// 更新饼图
			this.graph2_option.series[0].data = [
				{ value: normalvolume, name: '正常体积' ,itemStyle: {color:'#67C23A'}},
				{ value: bigvolume, name: '体积偏大' ,itemStyle: {color:'#F56C6C'}},
				{ value: smallvolume, name: '体积偏小' ,itemStyle: {color:'#E6A23C'}},
			];
		},
		async get_update() {
			// await this.getData();
			// 更新
			this.get_table_data();

			this.resData = [];
			this.sets_data_temp.sets.forEach(element => {
				var set_id = element.set_id;
				var set_name = element.set_name;
				// 获取set数据
				// var set_labels = {
				// 	1: { name: "spleen", volume: 44 },
				// 	6: { name: "liver", volume: 32 },
				// 	14: { name: "bladder", volume: 23 },
				// };
				console.log(this.sets_data)
				var set_labels = this.sets_data[set_id].labels;
				console.log(set_labels);
				var temp = { set: set_id };
				var labelData_temp = ["set"];
				var propsData_temp = ["set"];
				for (var key in set_labels) {
					var item = set_labels[key];
					labelData_temp.push(item.name);
					propsData_temp.push(item.name);
					temp[item.name] = item.volume;
				}
				console.log(temp);
				console.log(labelData_temp);
				console.log(propsData_temp);
				this.resData.push(temp);
				this.labelData = [
					"CT集合",
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
				];
				this.propsData = [
					"set",
					"spleen",
					"right kidney",
					"left kidney",
					"gall bladder",
					"esophagus",
					"liver",
					"stomach",
					"aorta",
					"postcava",
					"pancreas",
					"right adrenal gland",
					"left adrenal gland",
					"duodenum",
					"bladder",
					"prostate/uterus"
				];
				// 更新图上方两个选项
				this.get_selectchoice();

				this.$forceUpdate();

				console.log(this.resData);
			});

			return true;
		},
		async get_selectchoice() {
			console.log("inti get select")
			var select_project_temp = [];

			this.projects_data_temp.projects.forEach(element => {
				select_project_temp.push({
					value: element.project_id,
					label: element.project_id + " ----- " + element.project_name,
					sets: element.sets_id
				});
			});
			this.select_project = select_project_temp;


			var select_organ_temp = [];
			for (var key in this.LABEL_NAMES) {
				var item = this.LABEL_NAMES[key];
				select_organ_temp.push({
					value: key,
					label: this.labelData[key]
				});
			}

			this.select_organ = select_organ_temp;
			console.log(this.select_project);
			console.log(this.select_organ);
		},
		async get_table_data() {
			// this.sets_data_temp.sets.forEach(element => {
			// 	this.sets_data[element.set_id] = {
			// 		set_id: element.set_id,
			// 		set_name: element.set_name,
			// 		label_path: element.label_path,
			// 		labels: this.set_1_labels_temp
			// 	}
			// });
		},
		// 从后端获取数据
		async getData() {
			// 项目数据
			// this.projects_data_temp = {
			// 	projects: [
			// 		{ project_id: 12, project_name: "qqq", sets_id: [1, 2] },
			// 		{ project_id: 22, project_name: "qb", sets_id: [2, 3] }
			// 	]
			// };
			this.projects_data_temp = await getProjects({});
			console.log(this.projects_data_temp);
			// 集合基本数据
			// this.sets_data_temp = {
			// 	sets: [
			// 		{ set_id: 1, set_name: "www", label_path: "" },
			// 		{ set_id: 2, set_name: "qwq", label_path: "http://test" },
			// 		{ set_id: 3, set_name: "QAQ", label_path: "http://123" }
			// 	]
			// };
			this.sets_data_temp = await getSets({});
			console.log(this.sets_data_temp);

			for (let i = 0; i < this.sets_data_temp.sets.length; i++) {
				var element = this.sets_data_temp.sets[i];
				var set_id = element.set_id;
				// 获取labels
				// var set_labels_temp = {
				// 	1: { name: "spleen", volume: 44 },
				// 	6: { name: "liver", volume: 32 },
				// 	14: { name: "bladder", volume: 23 },
				// };
				var set_labels_temp = await getLabel({
					set_id: set_id
				})
				console.log(set_labels_temp.label_list);
				this.sets_data[element.set_id] = {
					set_id: element.set_id,
					set_name: element.set_name,
					label_path: element.label_path,
					labels: set_labels_temp.label_list
				}
			}
			console.log(this.sets_data);
			// 分次获取集合内对应器官的体积
			// this.set_1_labels_temp = {
			// 	1: { name: "spleen", volume: 44 },
			// 	6: { name: "liver", volume: 32 },
			// 	14: { name: "bladder", volume: 23 },
			// };
			// this.set_2_labels_temp = {
			// 	1: { name: "spleen", volume: 44 },
			// 	3: { name: "right kidney", volume: 77 },
			// 	14: { name: "bladder", volume: 22 },
			// };
			// this.set_3_labels_temp = {
			// 	1: { name: "spleen", volume: 44 },
			// 	3: { name: "right kidney", volume: 22 },
			// 	14: { name: "bladder", volume: 12 },
			// };
			// /*
			// 总：
			// projects：一次获得全部，无需额外参数。会返回拥有的sets
			// sets：一次获得全部，无需额外参数。通过label_path判定是否有labels
			// labels：多次获取。需要提供对应的set_id。
			// */
			// // get_projects 接口获得，无需其他参数。得到的是该用户所有的projects。
			// const projects_data = {
			// 	projects: [
			// 		{ project_id: 12, project_name: "qqq", sets: [1, 2] },
			// 		{ project_id: 22, project_name: "qb", sets: [2, 3] }
			// 	]
			// }
			// // get_sets 接口获得，无需其他参数。得到的是该用户所有的sets，起哄label_path为空字符串代表没有label标签。
			// const sets_data = {
			// 	sets: [
			// 		{ set_id: 1, set_name: "www", label_path: "" },
			// 		{ set_id: 2, set_name: "qwq", label_path: "http://test" },
			// 		{ set_id: 3, set_name: "QAQ", label_path: "http://123" }
			// 	]
			// }
			// // 对于每个set，只能得到一个labels。接口参数需要提供set_id。key与value中的name对应。因此不会返回没有的器官的key-value对。volume是体积。
			// const set_1_labels = {
			// 	1: { name: "spleen", volume: 44 },
			// 	6: { name: "liver", volume: 32 },
			// 	14: { name: "bladder", volume: 23 },
			// };
			// const set_2_labels = {
			// 	1: { name: "spleen", volume: 44 },
			// 	3: { name: "right kidney", volume: 77 },
			// 	14: { name: "bladder", volume: 22 },
			// };
			// const set_3_labels = {
			// 	1: { name: "spleen", volume: 44 },
			// 	3: { name: "right kidney", volume: 22 },
			// 	14: { name: "bladder", volume: 12 },
			// };
			// 器官名
			// this.LABEL_NAMES = {
			// 	1: "spleen",
			// 	2: "right kidney",
			// 	3: "left kidney",
			// 	4: "gall bladder",
			// 	5: "esophagus",
			// 	6: "liver",
			// 	7: "stomach",
			// 	8: "aorta",
			// 	9: "postcava",
			// 	10: "pancreas",
			// 	11: "right adrenal gland",
			// 	12: "left adrenal gland",
			// 	13: "duodenum",
			// 	14: "bladder",
			// 	15: "prostate/uterus"
			// }
		}
	},
	async mounted() {
		// 从后端获取数据
		await this.getData();
		this.finish = true;
		console.log("mouted1");
		this.update_graphs();

	},
	components: {
		ChartTable,
		graph1,
		graph2
	}
};
</script>

<style lang="scss">
.charts_el_select {
	margin: 0 1% 1%;
}
</style>