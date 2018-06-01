import React from "react"
import { render } from 'react-dom'
import Highcharts from "highcharts"
import HighchartsReact from 'highcharts-react-official'

export default class HighBarChart extends React.Component {


  constructor(props){
    super(props);
    this.state = {
      data:[0,0,0,0,0,0,0,0,0,0]
    };
  }
  componentWillReceiveProps(nextProps) {
    this.setState({data:nextProps.data})
  }
  render(){
    const options = {
      chart: {
          type: 'column'
      },
      title: {
          text: 'Charges By Hour'
      },
      xAxis: {
          categories: ['1 AM','2 AM','3 AM','4 AM','5 AM','6 AM','7 AM','8 AM','9 AM', '10 AM', '11 AM', '12 PM', '1 PM', '2 PM', '3 PM', '4 PM', '5 PM', '6 PM','7 PM','8 PM','9 PM','10 PM','11 PM','12 AM'],
          title: {
              text: null
          }
      },
      yAxis: {
          min: 0,
          title: {
              text: 'Charges',
              align: 'high'
          },
          labels: {
              overflow: 'justify'
          }
      },
      plotOptions: {
          bar: {
              dataLabels: {
                  enabled: true
              }
          }
      },
      credits: {
          enabled: false
      },
      series: [
         {
          name: 'Charges',
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
