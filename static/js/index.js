var start_area = document.getElementById('indataid').getAttribute('s');
var end_area = document.getElementById('indataid').getAttribute('e');
var act_date = document.getElementById('indataid').getAttribute('d');
// 柱状图1模块
(function () {
    // 实例化对象
    var myChart = echarts.init(document.querySelector(".bar .chart"));

    var app = {
        xaxis: [],
        yvalues1: [],
        yvalues2: []
    };

    //发送ajax请求
    $(document).ready(function () {
        getData();
        console.log(app.xaxis);
        console.log(app.yvalues1);
        console.log(app.yvalues2);
    });
    var data = {
        data: JSON.stringify({
            'start_area': start_area,
            'end_area': end_area,
            'act_date': act_date
        }),
    }

    //设计画图
    function getData() {
        $.ajax({
            //渲染的是127.0.0.1/test 下的json数据
            url: '/planeMap/prd',
            data: data,
            type: 'POST',
            dataType: 'json',
            success: function (data) {

                app.xaxis = data.xaxis;
                app.yvalues1 = data.yvalues1;
                app.yvalues2 = data.yvalues2;

                var option = {
                    color: ["#2f89cf"],
                    tooltip: {
                        trigger: "axis",
                        axisPointer: {
                            // 坐标轴指示器，坐标轴触发有效
                            type: "shadow" // 默认为直线，可选为：'line' | 'shadow'
                        }
                    },
                    grid: {
                        left: "0%",
                        top: "10px",
                        right: "0%",
                        bottom: "4%",
                        containLabel: true
                    },
                    xAxis: [
                        {
                            type: "category",
                            data: app.xaxis,
                            axisTick: {
                                alignWithLabel: true
                            },
                            axisLabel: {
                                textStyle: {
                                    color: "rgba(255,255,255,.6)",
                                    fontSize: "12"
                                }
                            },
                            axisLine: {
                                show: false
                            }
                        }
                    ],
                    yAxis: [
                        {
                            type: "value",
                            axisLabel: {
                                textStyle: {
                                    color: "rgba(255,255,255,.6)",
                                    fontSize: "12"
                                }
                            },
                            axisLine: {
                                lineStyle: {
                                    color: "rgba(255,255,255,.1)"
                                    // width: 1,
                                    // type: "solid"
                                }
                            },
                            splitLine: {
                                lineStyle: {
                                    color: "rgba(255,255,255,.1)"
                                }
                            }
                        }
                    ],
                    series: [
                        {
                            name: "价格区间",
                            type: "bar",
                            barWidth: "35%",
                            data: app.yvalues1,
                            itemStyle: {
                                barBorderRadius: 5
                            }
                        }
                    ]
                };

                // 把配置给实例对象
                myChart.setOption(option);
                window.addEventListener("resize", function () {
                    myChart.resize();
                });

                // 数据变化
                var dataAll = [
                    {year: "当日", data: app.yvalues1},
                    {year: "明日", data: app.yvalues2}
                ];

                $(".bar h2 ").on("click", "a", function () {
                    option.series[0].data = dataAll[$(this).index()].data;
                    myChart.setOption(option);
                });
            },
            error: function (msg) {
                console.log(msg);
                alert('系统发生错误');
            }
        })
    }

})();

// 折线图定制
(function () {
    // 基于准备好的dom，初始化echarts实例
    var myChart = echarts.init(document.querySelector(".line .chart"));

    var app = {
        xaxis: [],
        yvalues1: [],
    };

    //发送ajax请求
    $(document).ready(function () {
        getData();
        console.log(app.xaxis);
        console.log(app.yvalues1);
    });
    var data = {
        data: JSON.stringify({
            'start_area': start_area,
            'end_area': end_area,
            'act_date': act_date
        }),
    }

    //设计画图
    function getData() {
        $.ajax({
            //渲染的是127.0.0.1/test 下的json数据
            url: '/planeMap/lrd',
            data: data,
            type: 'POST',
            dataType: 'json',
            success: function (datab) {

                app.xaxis = datab.xaxis;
                app.yvalues1 = datab.yvalues1;

                let dataAxis = app.xaxis;
                // prettier-ignore
                let data = app.yvalues1;
                let yMax = 0.2;
                let dataShadow = [];
                for (let i = 0; i < data.length; i++) {
                    dataShadow.push(yMax);
                }
                option = {
                    tooltip: {
                        trigger: "axis",
                        axisPointer: {
                            // 坐标轴指示器，坐标轴触发有效
                            type: "line" // 默认为直线，可选为：'line' | 'shadow'
                        }
                    },
                    /*title: {
                        text: '特性示例：渐变色 阴影 点击缩放',
                        subtext: 'Feature Sample: Gradient Color, Shadow, Click Zoom'
                    },*/
                    grid: {
                        left: "0%",
                        top: "10px",
                        right: "0%",
                        bottom: "4%",
                        containLabel: true
                    },
                    xAxis: {
                        data: dataAxis,
                        axisLabel: {
                            inside: true,
                            color: '#fff'
                        },
                        axisTick: {
                            show: false
                        },
                        axisLine: {
                            show: false
                        },
                        z: 10
                    },
                    yAxis: {
                        axisLine: {
                            show: false
                        },
                        axisTick: {
                            show: false
                        },
                        axisLabel: {
                            color: '#999'
                        }
                    },
                    dataZoom: [
                        {
                            type: 'inside'
                        }
                    ],
                    series: [
                        {
                            name: '晚点/取消率',
                            type: 'bar',
                            showBackground: true,
                            itemStyle: {
                                barBorderRadius: 4,
                                color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
                                    {offset: 0, color: '#A5FECB'},
                                    {offset: 0.5, color: '#20BDFF'},
                                    {offset: 1, color: '#5433FF'}
                                ])
                            },
                            emphasis: {

                                itemStyle: {
                                    color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
                                        {offset: 0, color: '#2378f7'},
                                        {offset: 0.7, color: 'rgb(204,147,197)'},
                                        {offset: 1, color: 'rgb(232,191,205)'}
                                    ])
                                }
                            },
                            data: data
                        }
                    ]
                };
// Enable data zoom when user click bar.
                const zoomSize = 6;
                myChart.on('click', function (params) {
                    console.log(dataAxis[Math.max(params.dataIndex - zoomSize / 2, 0)]);
                    myChart.dispatchAction({
                        type: 'dataZoom',
                        startValue: dataAxis[Math.max(params.dataIndex - zoomSize / 2, 0)],
                        endValue:
                            dataAxis[Math.min(params.dataIndex + zoomSize / 2, data.length - 1)]
                    });
                });
                // 重新把配置好的新数据给实例对象
                myChart.setOption(option);
                window.addEventListener("resize", function () {
                    myChart.resize();
                });

            },
            error: function (msg) {
                console.log(msg);
                alert('系统发生错误');
            }
        })
    }


})();

// 饼形图定制
// 折线图定制
(function () {
    // 基于准备好的dom，初始化echarts实例
    var myChart = echarts.init(document.querySelector(".pie .chart"));
    var app = {
        xday: [],
        yvalue: []
    };

    //发送ajax请求
    $(document).ready(function () {
        getData();
        console.log(app.xday);
        console.log(app.yvalue)
    });
    var data = {
        data: JSON.stringify({
            'start_area': start_area,
            'end_area': end_area,
            'act_date': act_date
        }),
    }

    //设计画图
    function getData() {
        $.ajax({
            //渲染的是127.0.0.1/test 下的json数据
            url: '/planeMap/trd',
            data: data,
            type: 'POST',
            dataType: 'json',
            success: function (data) {

                app.xday = data.xdays;
                app.yvalue = data.yvalues;

                var time_datas = [];
                for (var j = 0; j < app.xday.length; j++) {
                    var tmp = {value: app.yvalue[j], name: app.xday[j]};
                    time_datas[j] = tmp;
                }
                //alert(time_datas);
                option = {
                    tooltip: {
                        trigger: "item",
                        formatter: "{a} <br/>{b}: {c} ({d}%)",
                        position: function (p) {
                            //其中p为当前鼠标的位置
                            return [p[0] + 10, p[1] - 10];
                        }
                    },
                    legend: {
                        top: "80%",
                        itemWidth: 40,
                        itemHeight: 8,
                        data: app.xday,
                        textStyle: {
                            color: "rgba(255,255,255,.5)",
                            fontSize: "12"
                        }
                    },
                    series: [
                        {
                            name: "时间分布",
                            type: "pie",
                            center: ["50%", "42%"],
                            radius: ["40%", "60%"],
                            color: [
                                "#6F61C0",
                                "#065aab",
                                "#06dcab",
                                "#A084E8",
                                "#06b4ab",
                                "#D5FFE4",
                                "#066eab",
                                "#8BE8E5"
                            ],
                            label: {show: false},
                            labelLine: {show: false},
                            data: time_datas
                        }
                    ]
                };

                // 使用刚指定的配置项和数据显示图表。
                myChart.setOption(option);
                window.addEventListener("resize", function () {
                    myChart.resize();
                });
            },
            error: function (msg) {
                console.log(msg);
                alert('系统发生错误');
            }
        })
    }


})();
// 学习进度柱状图模块
(function () {

    // 基于准备好的dom，初始化echarts实例
    var myChart = echarts.init(document.querySelector(".bar1 .chart"));
    // prettier-ignore

    var app = {
        xaxis: [],
        yvalues1: [],
        sum: 0
    };

    //发送ajax请求
    $(document).ready(function () {
        getData();
        console.log(app.xaxis);
        console.log(app.yvalues1);
        console.log(app.sum);
    });
    var data = {
        data: JSON.stringify({
            'start_area': start_area,
            'end_area': end_area,
            'act_date': act_date
        }),
    }

    //设计画图
    function getData() {
        $.ajax({
            //渲染的是127.0.0.1/test 下的json数据
            url: '/planeMap/ptd',
            data: data,
            type: 'POST',
            dataType: 'json',
            success: function (datab) {

                app.xaxis = datab.xaxis;
                app.yvalues1 = datab.yvalues1;
                app.sum = datab.sum;
                var sum = app.sum;

                var pdata = [];
                for (var j = 0;j < app.yvalues1.length;j++) {
                    var tmp = app.yvalues1[j] * 100 / sum;
                    pdata.push(tmp);
                }
                var downdata = [];
                for (var j = 0;j < app.yvalues1.length;j++) {
                    downdata.push(100);
                }

                var data = pdata;
                var titlename = app.xaxis;
                var valdata = app.yvalues1;
                var myColor = ["#1089E7", "#F57474", "#56D0E3", "#F8B448", "#8B78F6"];
                option = {
                    //图标位置
                    grid: {
                        top: "10%",
                        left: "22%",
                        bottom: "10%"
                    },
                    xAxis: {
                        show: false
                    },
                    yAxis: [
                        {
                            show: true,
                            data: titlename,
                            inverse: true,
                            axisLine: {
                                show: false
                            },
                            splitLine: {
                                show: false
                            },
                            axisTick: {
                                show: false
                            },
                            axisLabel: {
                                color: "#fff",

                                rich: {
                                    lg: {
                                        backgroundColor: "#339911",
                                        color: "#fff",
                                        borderRadius: 15,
                                        // padding: 5,
                                        align: "center",
                                        width: 15,
                                        height: 15
                                    }
                                }
                            }
                        },
                        {
                            show: true,
                            inverse: true,
                            data: valdata,
                            axisLabel: {
                                textStyle: {
                                    fontSize: 12,
                                    color: "#fff"
                                }
                            }
                        }
                    ],
                    series: [
                        {
                            name: "条",
                            type: "bar",
                            yAxisIndex: 0,
                            data: data,
                            barCategoryGap: 50,
                            barWidth: 10,
                            itemStyle: {
                                normal: {
                                    barBorderRadius: 20,
                                    color: function (params) {
                                        var num = myColor.length;
                                        return myColor[params.dataIndex % num];
                                    }
                                }
                            },
                            label: {
                                normal: {
                                    show: true,
                                    position: "inside",
                                    formatter: "{c}%"
                                }
                            }
                        },
                        {
                            name: "框",
                            type: "bar",
                            yAxisIndex: 1,
                            barCategoryGap: 50,
                            data: downdata,
                            barWidth: 15,
                            itemStyle: {
                                normal: {
                                    color: "none",
                                    borderColor: "#00c1de",
                                    borderWidth: 3,
                                    barBorderRadius: 15
                                }
                            }
                        }
                    ]
                };

                // 使用刚指定的配置项和数据显示图表。
                myChart.setOption(option);
                window.addEventListener("resize", function () {
                    myChart.resize();
                });
            },
            error: function (msg) {
                console.log(msg);
                alert('系统发生错误');
            }
        })
    }


})();
// 折线图 优秀作品
(function () {
    // 基于准备好的dom，初始化echarts实例
    var myChart = echarts.init(document.querySelector(".line1 .chart"));

    var app = {
        xaxis: [],
        yvalues1: [],
        yvalues2: []
    };

    //发送ajax请求
    $(document).ready(function () {
        getData();
        console.log(app.xaxis);
        console.log(app.yvalues1);
        console.log(app.yvalues2);
    });
    var data = {
        data: JSON.stringify({
            'start_area': start_area,
            'end_area': end_area,
            'act_date': act_date
        }),
    }

    //设计画图
    function getData() {
        $.ajax({
            //渲染的是127.0.0.1/test 下的json数据
            url: '/planeMap/apd',
            data: data,
            type: 'POST',
            dataType: 'json',
            success: function (data) {

                app.xaxis = data.xaxis;
                app.yvalues1 = data.yvalues1;
                app.yvalues2 = data.yvalues2;

                option = {
        tooltip: {
            trigger: "axis",
            axisPointer: {
                lineStyle: {
                    color: "#dddc6b"
                }
            }
        },
        legend: {
            top: "0%",
            textStyle: {
                color: "rgba(255,255,255,.5)",
                fontSize: "12"
            }
        },
        grid: {
            left: "10",
            top: "30",
            right: "10",
            bottom: "10",
            containLabel: true
        },

        xAxis: [
            {
                type: "category",
                boundaryGap: false,
                axisLabel: {
                    textStyle: {
                        color: "rgba(255,255,255,.6)",
                        fontSize: 12
                    }
                },
                axisLine: {
                    lineStyle: {
                        color: "rgba(255,255,255,.2)"
                    }
                },

                data: app.xaxis
            },
            {
                axisPointer: {show: false},
                axisLine: {show: false},
                position: "bottom",
                offset: 20
            }
        ],

        yAxis: [
            {
                type: "value",
                axisTick: {show: false},
                axisLine: {
                    lineStyle: {
                        color: "rgba(255,255,255,.1)"
                    }
                },
                axisLabel: {
                    textStyle: {
                        color: "rgba(255,255,255,.6)",
                        fontSize: 12
                    }
                },

                splitLine: {
                    lineStyle: {
                        color: "rgba(255,255,255,.1)"
                    }
                }
            }
        ],
        series: [
            {
                name: "最低票价",
                type: "line",
                smooth: true,
                symbol: "circle",
                symbolSize: 5,
                showSymbol: false,
                lineStyle: {
                    normal: {
                        color: "#0184d5",
                        width: 2
                    }
                },
                areaStyle: {
                    normal: {
                        color: new echarts.graphic.LinearGradient(
                            0,
                            0,
                            0,
                            1,
                            [
                                {
                                    offset: 0,
                                    color: "rgba(1, 132, 213, 0.4)"
                                },
                                {
                                    offset: 0.8,
                                    color: "rgba(1, 132, 213, 0.1)"
                                }
                            ],
                            false
                        ),
                        shadowColor: "rgba(0, 0, 0, 0.1)"
                    }
                },
                itemStyle: {
                    normal: {
                        color: "#0184d5",
                        borderColor: "rgba(221, 220, 107, .1)",
                        borderWidth: 12
                    }
                },
                data: app.yvalues1
            },
            {
                name: "平均票价",
                type: "line",
                smooth: true,
                symbol: "circle",
                symbolSize: 5,
                showSymbol: false,
                lineStyle: {
                    normal: {
                        color: "#00d887",
                        width: 2
                    }
                },
                areaStyle: {
                    normal: {
                        color: new echarts.graphic.LinearGradient(
                            0,
                            0,
                            0,
                            1,
                            [
                                {
                                    offset: 0,
                                    color: "rgba(0, 216, 135, 0.4)"
                                },
                                {
                                    offset: 0.8,
                                    color: "rgba(0, 216, 135, 0.1)"
                                }
                            ],
                            false
                        ),
                        shadowColor: "rgba(0, 0, 0, 0.1)"
                    }
                },
                itemStyle: {
                    normal: {
                        color: "#00d887",
                        borderColor: "rgba(221, 220, 107, .1)",
                        borderWidth: 12
                    }
                },
                data: app.yvalues2
            }
        ]
    };

    // 使用刚指定的配置项和数据显示图表。
    myChart.setOption(option);
    window.addEventListener("resize", function () {
        myChart.resize();
    });
            },
            error: function (msg) {
                console.log(msg);
                alert('系统发生错误');
            }
        })
    }


})();

// 点位分布统计模块
(function () {
    // 1. 实例化对象
    var myChart = echarts.init(document.querySelector(".pie1  .chart"));

    var app = {
        xaxis: [],
        yvalues1: []
    };

    //发送ajax请求
    $(document).ready(function () {
        getData();
        console.log(app.xaxis);
        console.log(app.yvalues1)
    });
    var data = {
        data: JSON.stringify({
            'start_area': start_area,
            'end_area': end_area,
            'act_date': act_date
        }),
    }

    //设计画图
    function getData() {
        $.ajax({
            //渲染的是127.0.0.1/test 下的json数据
            url: '/planeMap/acomd',
            data: data,
            type: 'POST',
            dataType: 'json',
            success: function (data) {

                app.xaxis = data.xaxis;
                app.yvalues1 = data.yvalues1;

                var aircom_datas = [];
                for (var j = 0; j < app.xaxis.length; j++) {
                    var tmp = {value: app.yvalues1[j], name: app.xaxis[j]};
                    aircom_datas[j] = tmp;
                }
                console.log(aircom_datas);
                var option = {
                    legend: {
                        top: "82%",
                        itemWidth: 10,
                        itemHeight: 8,
                        textStyle: {
                            color: "rgba(255,255,255,.5)",
                            fontSize: "12"
                        }
                    },
                    tooltip: {
                        trigger: "item",
                        formatter: "{a} <br/>{b} : {c} ({d}%)"
                    },
                    // 注意颜色写的位置
                    color: [
                        "#006cff",
                        "#60cda0",
                        "#ed8884",
                        "#ff9f7f",
                        "#0096ff",
                        "#9fe6b8",
                        "#32c5e9",
                        "#1d9dff"
                    ],
                    series: [
                        {
                            name: "点位统计",
                            type: "pie",
                            // 如果radius是百分比则必须加引号
                            radius: ["10%", "70%"],
                            center: ["50%", "42%"],
                            roseType: "radius",
                            data: aircom_datas,
                            // 修饰饼形图文字相关的样式 label对象
                            label: {
                                fontSize: 10
                            },
                            // 修饰引导线样式
                            labelLine: {
                                // 连接到图形的线长度
                                length: 10,
                                // 连接到文字的线长度
                                length2: 10
                            }
                        }
                    ]
                };

                // 3. 配置项和数据给我们的实例化对象
                myChart.setOption(option);
                // 4. 当我们浏览器缩放的时候，图表也等比例缩放
                window.addEventListener("resize", function () {
                    // 让我们的图表调用 resize这个方法
                    myChart.resize();
                });
            },
            error: function (msg) {
                console.log(msg);
                alert('系统发生错误');
            }
        })
    }
})();
