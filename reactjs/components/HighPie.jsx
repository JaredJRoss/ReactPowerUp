import React from "react"
import { render } from 'react-dom'
import Highcharts from "highcharts"
import HighchartsReact from 'highcharts-react-official'

export default class HighPieChart extends React.Component {


  constructor(props){
    super(props);
    this.state = {
      data:[{name:'No Data',y:100}]
    };
  }
  componentWillReceiveProps(nextProps) {
    this.setState({data:nextProps.data})
  }
  render(){
    const options = {
      chart: {
    plotBackgroundColor: null,
    plotBorderWidth: null,
    plotShadow: false,
    type: 'pie'
    },
    title: {
        text: 'Type Of Charges'
    },
    tooltip: {
        pointFormat: '{series.name}: <b>{point.percentage:.1f}%</b>'
    },
    plotOptions: {
        pie: {
            allowPointSelect: true,
            cursor: 'pointer',
            dataLabels: {
                enabled: true,
                format: '<b>{point.name}</b>: {point.percentage:.1f} %',
                style: {
                    color: (Highcharts.theme && Highcharts.theme.contrastTextColor) || 'black'
                }
            }
        }
    },
    series: [{
        name: 'Type',
        colorByPoint: true,
        data: this.state.data
    }]
  }
    return(
      <div className = "highBar">
      <HighchartsReact
      highcharts={Highcharts}
      options={options}
      />
      </div>
    )
  }

}
