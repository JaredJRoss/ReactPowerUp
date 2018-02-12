import React from "react"
import Radium from "radium"
import DjangoCSRFToken from 'django-react-csrftoken'
import BarChart from 'react-d3-components/lib/BarChart'
import PieChart from 'react-d3-components/lib/PieChart'
export default class SampleAppContainer extends React.Component {
  constructor(props){
    super(props);
    this.state = {
        search_terms:'',
        url:'/api/search?',
        kiosks:[],
        Start:'',
        End:'',
    };

    fetch('/api/dash',{
      credentials:'include'
    }).then(function(response){
      return response.json()
    }).then(data => this.setState({bar:data.TimeOfDay,pie:data.TypeOfCharge,total:data.count,avg:data.avg}));

    fetch('/api/search',{
      credentials: 'include',
    }).then(function(response){
      return response.json()
    }).then(data => this.setState({kiosks:data}));
    this.handleSearch = this.handleSearch.bind(this);
    this.tooltipBar = this.tooltipBar.bind(this);
    this.tooltipPie = this.tooltipPie.bind(this);
    this.HandleCustomStart = this.HandleCustomStart.bind(this);
    this.HandleCustomEnd = this.HandleCustomEnd.bind(this);

  }

  HandleCustomEnd(event){
    this.setState({End:event.target.value})
  }
  HandleCustomStart(event){
    this.setState({Start:event.target.value})
  }

  handleDate = (date)=>(event)=>{
    fetch('/api/dash?'+this.state.search_terms+'&date='+date+'&start='+this.state.Start+'&end='+this.state.End,{
      credentials:'include'
    }).then(function(response){
      return response.json()
    }).then(data => this.setState({bar:data.TimeOfDay,pie:data.TypeOfCharge,total:data.count,avg:data.avg}));

    this.setState({date:date})
    console.log(date);
  }

  tooltipBar = function(x,y0,y,total){
    return y.toString();
  }
  tooltipPie = function(x,y){
    return y.toString();
  }
  handleSearch(event) {
    var search_terms = '&';
    var url = '/api/search?';
    for(var l of this.Location.selectedOptions){
      search_terms = search_terms+ '&Location='+l.value+'&';
      console.log(l.value)
    }
    for(var c of this.Client.selectedOptions){
      search_terms =search_terms+ '&Client='+c.value+'&';
      console.log(c.value)
    }
    for(var k of this.Kiosk.selectedOptions){
      search_terms =search_terms+ '&ID='+k.value+'&';
      console.log(k.value)
    }
    for(var t of this.Type.selectedOptions){
      search_terms=search_terms+'Type='+t.value+'&';
      console.log(t.value)
    }

    url =url+search_terms;
    console.log(url)
    this.setState({url:url,search_terms:search_terms})
    fetch(url,{
      credentials: 'include',
    }).then(function(response){
      return response.json()
    }).then(data => this.setState({kiosks:data}));
    console.log(this.state.bar)
    fetch('/api/dash?'+search_terms,{
      credentials:'include'
    }).then(function(response){
      return response.json()
    }).then(data => this.setState({bar:data.TimeOfDay,pie:data.TypeOfCharge,total:data.count,avg:data.avg}));

    event.preventDefault();
  }

  render() {

    return (

      <div classNameName="container">

      <section>
          <h1>Welcome {this.props.user}</h1>
          <div className="spacing1">

          </div>

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
            Start Date: <input type="text" value = {this.state.Start} onChange={this.HandleCustomStart} name="start"></input>   &nbsp;   &nbsp;
            End Date: <input type="text" value = {this.state.End} onChange={this.HandleCustomEnd}name="end"></input>
            <input style={{text_decoration:"none"}} onClick={this.handleDate('')} type= "submit"className="transparent_btn" ></input>
          <div className="spacing1"> </div>
          <a style={{text_decoration:"none"}} href="#hidden-div" data-target="#hidden-div" className="transparent_btn" data-toggle="collapse">Advanced Search</a>
            <div id ="hidden-div" className ="collapse" style={{color:"black"}}>
              <div className="spacing1"> </div>
              <form onSubmit={this.handleSearch}>
              <DjangoCSRFToken/>
              <fieldset>

                Location: <select ref={(input)=>this.Location = input} name="Location" className="form-control" id="id_Location" data-autocomplete-light-url="/location-autocomplete/" data-autocomplete-light-function="select2" multiple="multiple"></select>
                &nbsp;  &nbsp; Client: <select  ref={(input)=>this.Client= input} name="Client" className="form-control" id="id_Client" data-autocomplete-light-url="/client-autocomplete/" data-autocomplete-light-function="select2" multiple="multiple"></select>
                <div className="spacing1"> </div>

                Kiosk ID: <select name="ID"  ref={(input)=>this.Kiosk = input} className="form-control" id="id_ID" data-autocomplete-light-url="/kiosk-autocomplete/" data-autocomplete-light-function="select2" multiple="multiple"></select>
                &nbsp;  &nbsp;  Type: <select   ref={(input)=>this.Type = input} name="Type" className="form-control" id="id_Type" data-autocomplete-light-url="/type-autocomplete/" data-autocomplete-light-function="select2" multiple="multiple"></select>

              </fieldset>
              <div className="spacing1"> </div>
              <input style={{text_decoration:"none"}} value = "Search" type= "submit" className="transparent_btn" ></input>
              </form>

             </div>
          </div>
          <div className="spacing1"> </div>
          <div className="spacing1"> </div>
          <div className="spacing1"> </div>
          <div className="spacing1"> </div>

          <h1>Kiosks</h1>
          <div className="spacing1"> </div>

          <div className="tbl-header">
            <table cellPadding="0" cellSpacing="0" border="0">
              <thead>
                <tr>
                  <th>Online</th>
                  <th>Kiosk</th>
                  <th>Client</th>
                  <th>Location</th>
                  <th>Last Charge</th>
                  <th>Total Charge</th>
                </tr>
              </thead>
            </table>
          </div>
          <div className="tbl-content">
            <table cellPadding="0" cellSpacing="0" border="0">
              <tbody>

              {this.state.kiosks.map(k=>
                  <tr key={k.ID}>
                  <td>{k.online ?
                  <img style={{height:15}} src="https://upload.wikimedia.org/wikipedia/commons/thumb/5/5d/Green_sphere.svg/256px-Green_sphere.svg.png"/>
                  :<img style={{height:15}} src="https://upload.wikimedia.org/wikipedia/commons/thumb/6/60/Nuvola_apps_krec.svg/256px-Nuvola_apps_krec.svg.png"/>}</td>
                  <td><a href ={'/kiosk/'+k.ID}>{k.ID}</a></td>
                  <td>{k.Client}</td>
                  <td>{k.Loc}</td>
                  <td>{k.last_update}</td>
                  <td>{k.Tot}</td>
                  </tr>
              )}
              </tbody>
            </table>
          </div>
          <div className="spacing1"> </div>
        </section>


      </div>
    )
  }
}
