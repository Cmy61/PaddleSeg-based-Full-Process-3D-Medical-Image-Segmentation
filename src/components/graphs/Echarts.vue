<template>
	<div :id="id" :style="styleObject" />
</template>
<script>
import * as echarts from "echarts";
import "echarts/lib/chart/pie";
import "echarts/lib/component/title";
import { setTimeout } from "timers";

export default {
	props: {
		styleObject: {
			type: Object,
			default: () => ({ height: "180px", width: "100%" }),
		},
		option: {
			type: Object,
			default: () => { },
		},
		id: {
			type: String,
			default: "echart2020" + ("_" + Math.random()).replace(".", "_"),
		},
	},
	data: function () {
		return {
			resizeTimer: null,
			myChart: null,
		};
	},
	methods: {
		refresh() {
			setTimeout(() => {
				this.initPie(this.id);
			}, 500);
		},
		initPie(id) {
			const { option } = this;
			let chart = echarts.getInstanceByDom(window.document.getElementById(id));
			if (chart === undefined) {
				chart = echarts.init(window.document.getElementById(id));
			}
			chart.setOption(option);
			this.myChart = chart;
		},
		resizePie() {
			if (this.myChart) {
				this.myChart.resize();
			}
		},
		refreshData(data) {
			if (this.myChart) {
				this.myChart.setOption(data);
			}
		},
	},
	created() { },
	watch: {
		option: {
			handler() {
				this.refresh();
			},
			immediate: true,
			deep: true,
		},
	},
	mounted() {
		this.refresh();
		let _this = this;
		window.addEventListener("resize", function () {
			if (_this.resizeTimer) {
				clearTimeout(_this.resizeTimer);
			}
			_this.resizeTimer = setTimeout(function () {
				if (_this.myChart !== undefined) {
					_this.myChart.resize();
				}
			}, 100);
		});
	},
};
</script>
  