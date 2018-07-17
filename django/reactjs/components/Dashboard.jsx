import React from "react"
import Datetime from "react-datetime"
import HighPieChart from "../components/HighPie"
import HighBarChart from "../components/HighBar"
import HighBarDayChart from "../components/HighBarDay"

export default class Dashboard extends React.Component {
    constructor(props){
      super(props);
      this.state={
        Start:'',
        End:'',
        date:'',
      };
      
      this.tooltipBar = this.tooltipBar.bind(this);
      this.tooltipPie = this.tooltipPie.bind(this);
      this.HandleCustomStart = this.HandleCustomStart.bind(this);
      this.HandleCustomEnd = this.HandleCustomEnd.bind(this);
      fetch('/api/dash?',{
        credentials:'include'
      }).then(function(response){
        return response.json()
      }).then(data => this.setState({bar:data.TimeOfDay,pie:data.TypeOfCharge,total:data.count,avg:data.avg,highBar:data.TimeOfDayHigh,highPie:data.TypeOfChargeHigh,barDay:data.BarDay}));
    }

    componentWillReceiveProps(nextProps){
      if (nextProps.date ==""){
        fetch('/api/dash?'+nextProps.search_terms+'&start='+nextProps.start+'&end='+nextProps.end,{
          credentials:'include'
        }).then(function(response){
          return response.json()
        }).then(data => this.setState({bar:data.TimeOfDay,pie:data.TypeOfCharge,total:data.count,avg:data.avg,highBar:data.TimeOfDayHigh,highPie:data.TypeOfChargeHigh,barDay:data.BarDay}));
          this.setState({Start:nextProps.start , End: nextProps.end})
      }
      else{
        fetch('/api/dash?'+nextProps.search_terms+'&date='+nextProps.date,{
          credentials:'include'
        }).then(function(response){
          return response.json()
        }).then(data => this.setState({bar:data.TimeOfDay,pie:data.TypeOfCharge,total:data.count,avg:data.avg,highBar:data.TimeOfDayHigh,highPie:data.TypeOfChargeHigh,barDay:data.BarDay}));
        this.setState({date:nextProps.date})
        }
      }
    
    HandleCustomEnd(event){
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
        }).then(data => this.setState({bar:data.TimeOfDay,pie:data.TypeOfCharge,total:data.count,avg:data.avg,highBar:data.TimeOfDayHigh,highPie:data.TypeOfChargeHigh,barDay:data.BarDay}));
      }
      else{
        fetch('/api/dash?'+this.props.search_terms+'&date='+date,{
          credentials:'include'
        }).then(function(response){
          return response.json()
        }).then(data => this.setState({bar:data.TimeOfDay,pie:data.TypeOfCharge,total:data.count,avg:data.avg,highBar:data.TimeOfDayHigh,highPie:data.TypeOfChargeHigh,barDay:data.BarDay}));
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
              <h3 style={{textAlign:'center'}}>Dwell Time<div className="spacing1"> </div>
                                              {this.state.avg}</h3>
            </td>
            <td>
              <h3 style={{textAlign:'center'}}>Total Charges<div className="spacing1"></div>
                                              {this.state.total}</h3>

            </td>
          </tr>
          <tr>
            <td colSpan={2}>
            <HighBarDayChart
              data={this.state.barDay}
            />
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
