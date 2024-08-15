<template>
    <div>
        <Echarts :option="option" id="graph2" ref="graph2" :styleObject="styleObject"></Echarts>
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
            Data1: {
                title: {
                    text: '体积统计'
                },
               
                series: [
                    {
                        name: '体积',
                        type: 'pie',
                        data: [
                            {value:235, name:'正常体积'},
                            {value:274, name:'体积偏大'},
                            {value:310, name:'体积偏小'},
                        ]
                    }
                ]
            },
            styleObject: {
                width: '600px',
                height: '300px'
            },
        }
    },
    components: {
        Echarts,
    },
    created() { },
    methods: {},
};
</script>
  
<style></style>