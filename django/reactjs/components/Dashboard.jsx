import React from "react"
import BarChart from "react-d3-components/lib/BarChart"
import PieChart from "react-d3-components/lib/PieChart"
import Datetime from "react-datetime"
import ResponsiveBarChart from "../components/ResponsiveBar"
import ResponsivePieChart from "../components/ResponsivePie"
import HighPieChart from "../components/HighPie"
import HighBarChart from "../components/HighBar"

export default class Dashboard extends React.Component {
    constructor(props){
      super(props);
      this.state={
        Start:'',
        End:'',
        colorScale:d3.scale.ordinal().domain([0,1,2,3]).range(["gray", "green", "blue", "orange"]),
      };
      fetch('/api/dash?'+this.props.search_terms+'&',{
        credentials:'include'
      }).then(function(response){
        return response.json()
      }).then(data => this.setState({bar:data.TimeOfDay,pie:data.TypeOfCharge,total:data.count,avg:data.avg,highBar:data.TimeOfDayHigh,highPie:data.TypeOfChargeHigh}));

      this.tooltipBar = this.tooltipBar.bind(this);
      this.tooltipPie = this.tooltipPie.bind(this);
      this.HandleCustomStart = this.HandleCustomStart.bind(this);
      this.HandleCustomEnd = this.HandleCustomEnd.bind(this);
    }

    componentWillReceiveProps(nextProps) {
      fetch('/api/dash?'+nextProps.search_terms+'&',{
        credentials:'include'
      }).then(function(response){
        return response.json()
      }).then(data => this.setState({bar:data.TimeOfDay,pie:data.TypeOfCharge,total:data.count,avg:data.avg,highBar:data.TimeOfDayHigh,highPie:data.TypeOfChargeHigh}));
    }
    HandleCustomEnd(event){
      console.log(event)
      this.setState({End:event.format("MM/DD/YYYY HH:mm:ss")})
    }
    HandleCustomStart(event){
      this.setState({Start:event.format("MM/DD/YYYY HH:mm:ss")})
    }

      tooltipBar = function(x,y0,y,total){
        return y.toString();
      }
      tooltipPie = function(x,y){
        return y.toString();
      }
    handleDate = (date)=>(event)=>{
      this.props.onUpdate(date,this.state.Start,this.state.End)
      if(date == ''){
        fetch('/api/dash?'+this.props.search_terms+'&start='+this.state.Start+'&end='+this.state.End,{
          credentials:'include'
        }).then(function(response){
          return response.json()
        }).then(data => this.setState({bar:data.TimeOfDay,pie:data.TypeOfCharge,total:data.count,avg:data.avg,highBar:data.TimeOfDayHigh,highPie:data.TypeOfChargeHigh}));
      }
      else{
        fetch('/api/dash?'+this.props.search_terms+'&date='+date,{
          credentials:'include'
        }).then(function(response){
          return response.json()
        }).then(data => this.setState({bar:data.TimeOfDay,pie:data.TypeOfCharge,total:data.count,avg:data.avg,highBar:data.TimeOfDayHigh,highPie:data.TypeOfChargeHigh}));
      }
      this.setState({date:date})

    }
    render() {
      return (
        <div className="dash" style={{width:'100%'}}>
        <div className = "transparentbox">
        <table className=".table">
          <tbody>
          <tr>
            <td>
              <h3 style={{textAlign:'center'}}>Average Charge Duration<div className="spacing1"> </div>
                                              {this.state.avg}</h3>
            </td>
            <td>
              <h3 style={{textAlign:'center'}}>Total Charges<div className="spacing1"></div>
                                              {this.state.total}</h3>

            </td>
          </tr>
          <tr>
            <td colSpan={2}>
              <HighBarChart
              data = {this.state.highBar}
              />
              </td>
          </tr>
          <tr>
            <td colSpan={2}>
            <HighPieChart
            data={this.state.highPie}
            />
            </td>
          </tr>

            </tbody>
        </table>
        </div>
        <div className="spacing1"> </div>

        <div style={{textAlign:'center'}}>
        <a onClick ={this.handleDate('all')} style={{text_decoration:"none"}} className="transparent_btn">Total Charges</a>
        <a onClick ={this.handleDate('year')} style={{text_decoration:"none"}} className="transparent_btn">Last Year</a>
        <a onClick ={this.handleDate('quarter')} style={{text_decoration:"none"}} className="transparent_btn">Last Quarter</a>
        <a onClick ={this.handleDate('month')} style={{text_decoration:"none"}} className="transparent_btn">Last Month</a>
        <a onClick ={this.handleDate('week')} style={{text_decoration:"none"}} className="transparent_btn">Last Week</a>
        <a onClick ={this.handleDate('day')} style={{text_decoration:"none"}} className="transparent_btn">Last Day</a>
        <a onClick ={this.handleDate('hour')} style={{text_decoration:"none"}} className="transparent_btn">Last Hour</a>
        <div className="spacing1"> </div>
          Start Date: <Datetime onChange={this.HandleCustomStart} inputProps={{name:"start"}}/>
          <div className="spacing1"> </div>
          End Date: <Datetime onChange={this.HandleCustomEnd} inputProps={{name:"end"}}/>
          <div className="spacing1"> </div>

          <input style={{text_decoration:"none"}} onClick={this.handleDate('')} value ={"Submit Custom Date"}type= "submit"className="transparent_btn" ></input>

        <div className="spacing1"> </div>
        </div>
      </div>

      )
    }
  }
