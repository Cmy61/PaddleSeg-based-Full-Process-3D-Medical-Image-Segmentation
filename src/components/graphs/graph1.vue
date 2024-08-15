<template>
    <div>
        <Echarts :option="option" id="graph1" ref="graph1" :styleObject="styleObject"></Echarts>
    </div>
</template>
  
<script>
import Echarts from "./Echarts.vue";

export default {
    props: {
		option: {
			type: Object,
			default: () => { },
		},
	},
    data: function () {
        return {
            Data1: {},
            styleObject: {
                width: '600px',
                height: '300px'
            },
        }
    },
    components: {
        Echarts,
    },
    mounted() {
        this.Data1={
            title: {
                text: '集合统计'
            },
            tooltip: {},
            legend: {
                data: ['体积']
            },
            xAxis: {
                data: ['集合1', '集合2', '集合3', '集合4', '集合5', '集合6']
            },
            yAxis: {},
            series: [
                {
                    name: '体积',
                    type: 'line',
                    data: [5, 20, 36, 10, 10, 20]
                }
            ]
        };
        // this.Data1={};
    },
    methods: {},
};
</script>
  
<style></style>