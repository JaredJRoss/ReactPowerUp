import React from "react"
import BarChart from 'react-d3-components/lib/BarChart'
import PieChart from 'react-d3-components/lib/PieChart'
import Datetime from "react-datetime"

export default class Dashboard extends React.Component {
    constructor(props){
      super(props);
      this.state={
        Start:'',
        End:'',
      };
      fetch('/api/dash?'+this.props.search_terms+'&',{
        credentials:'include'
      }).then(function(response){
        return response.json()
      }).then(data => this.setState({bar:data.TimeOfDay,pie:data.TypeOfCharge,total:data.count,avg:data.avg}));

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
      }).then(data => this.setState({bar:data.TimeOfDay,pie:data.TypeOfCharge,total:data.count,avg:data.avg}));
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
      }).then(data => this.setState({bar:data.TimeOfDay,pie:data.TypeOfCharge,total:data.count,avg:data.avg}));
      }
      else{
        fetch('/api/dash?'+this.props.search_terms+'&date='+date,{
          credentials:'include'
        }).then(function(response){
          return response.json()
        }).then(data => this.setState({bar:data.TimeOfDay,pie:data.TypeOfCharge,total:data.count,avg:data.avg}));
      }
      this.setState({date:date})
    }
    render() {
      return (
        <div className="dash">
        <div className = "transparentbox">
        <table>
          <tbody>
            <tr>
              <td>
                <h3 style={{textAlign:'center'}}>Charges By Time Of Days</h3>
                <BarChart
                data={this.state.bar}
                height={400}
                width={400}
                margin={{top:10,bottom:50,left:50,right:10}}
                tooltipHtml={this.tooltipBar}/>

            </td>
              <td>
              <h3 style={{textAlign:'center'}}>Charges By Type</h3>

                <PieChart
                data={this.state.pie}
                width={400}
                height={400}
                margin={{top:10,bottom:50,left:50,right:50}}
                sort={null}
                tooltipHtml = {this.tooltipPie}
                />
              </td>
            </tr>
            <tr>
              <td>
                <h3 style={{textAlign:'center'}}>Total Charges:{this.state.total}</h3>
              </td>
              <td>
                <h3 style={{textAlign:'center'}}>Average Charge:{this.state.avg}</h3>
              </td>
            </tr>
            </tbody>
        </table>
        </div>
        <div className="spacing1"> </div>

        <div style={{textAlign:'center'}}>
        <a onClick ={this.handleDate('all')} style={{text_decoration:"none"}} className="transparent_btn">All Time</a>
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
