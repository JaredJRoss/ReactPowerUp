import React from "react"
import { render } from 'react-dom'
import Highcharts from "highcharts"
import HighchartsReact from 'highcharts-react-official'

export default class HighBarDayChart extends React.Component {

  constructor(props){
    super(props);
    this.state = {
      data:[],
    };
  }
  componentWillReceiveProps(nextProps) {
    console.log(nextProps.data)
    this.setState({data:nextProps.data})
  }
  render(){
    const options = {
      chart: {
          zoomType:'x',
      },
      title: {
          text: 'Foot Traffic By Day'
      },
      xAxis: {
          type:'datetime',
          dateTimeLabelFormats:{
              da:'%e of %b'
          }
      },
      yAxis: {
          title:{
              text:'Charges'
          }
      },
      plotOptions: {
          area:{
            fillColor: {
                linearGradient: {
                    x1: 0,
                    y1: 0,
                    x2: 0,
                    y2: 1
                },
                stops: [
                    [0, Highcharts.getOptions().colors[0]],
                    [1, Highcharts.Color(Highcharts.getOptions().colors[0]).setOpacity(0).get('rgba')]
                ]
            },
            marker: {
                radius: 2
            },
            lineWidth: 1,
            states: {
                hover: {
                    lineWidth: 1
                }
            },
            threshold: null
        } 
      },
      series: [
         {
          type:'area',
          name:'Charges',
          data:this.state.data
      }]
  }
    return(
      <div className = "highBarDay">
      <HighchartsReact
      highcharts={Highcharts}
      options={options}
      />
      </div>
    )
  }

}
