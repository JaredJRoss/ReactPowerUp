import React from "react"
import Radium from "radium"
import DjangoCSRFToken from 'django-react-csrftoken'
import BarChart from 'react-d3-components/lib/BarChart'
import PieChart from 'react-d3-components/lib/PieChart'
import Dashboard from '../components/Dashboard'
require('react-datetime');

export default class SampleAppContainer extends React.Component {
  constructor(props){
    super(props);
    this.state = {
        search_terms:'',
        url:'/api/search?',
        kiosks:[],
        dashboard:<Dashboard search_terms={''} onUpdate={this.onUpdate.bind(this)}/>,
    };

    fetch('/api/search',{
      credentials: 'include',
    }).then(function(response){
      return response.json()
    }).then(data => this.setState({kiosks:data}));
    this.handleSearch = this.handleSearch.bind(this);

  }

  onUpdate(date,start,end){
    fetch(this.state.url+'&date='+date+'&start='+start+'&end='+end,{
      credentials: 'include',
    }).then(function(response){
      return response.json()
    }).then(data => this.setState({kiosks:data}));
    this.setState({date:date,start:start,end:end})

  }

  handleSearch(event) {
    var search_terms = '';
    var url = '/api/search?';
    for(var l of this.Location.selectedOptions){
      search_terms = search_terms+ '&Location='+l.value+'&';
    }
    for(var c of this.Client.selectedOptions){
      search_terms =search_terms+ '&Client='+c.value+'&';
    }
    for(var k of this.Kiosk.selectedOptions){
      search_terms =search_terms+ '&ID='+k.value+'&';
    }
    for(var t of this.Type.selectedOptions){
      search_terms=search_terms+'Type='+t.value+'&';
    }

    url =url+search_terms;
    console.log('Url'+url)
    this.setState({url:url,search_terms:search_terms})

    fetch(url+'&date='+this.state.date+'&start='+this.state.start+'&end='+this.state.end,{
      credentials: 'include',
    }).then(function(response){
      return response.json()
    }).then(data => this.setState({kiosks:data}));

    this.setState({dashboard:<Dashboard search_terms={search_terms} onUpdate={this.onUpdate.bind(this)} />})
    console.log('search '+search_terms)
    event.preventDefault();
  }

  render() {
    return (

      <div className="container" style={{paddingRight:'0px', paddingLeft:'0px'}}>
      <section>
          <h1>Overview Dashboard</h1>
          <div className="spacing1"></div>
          {this.state.dashboard}
          <div style={{textAlign:'center'}}>
          <a style={{text_decoration:"none"}} href="#hidden-div" data-target="#hidden-div" className="transparent_btn" data-toggle="collapse">Advanced Search</a>
            <div id ="hidden-div" className ="collapse" style={{color:"black"}}>
              <div className="spacing1"> </div>
              <form onSubmit={this.handleSearch}>
              <fieldset>

                Location: <select ref={(input)=>this.Location = input} name="Location" className="form-control" id="id_Location" data-autocomplete-light-url="/location-autocomplete/" data-autocomplete-light-function="select2" multiple="multiple"></select>
                &nbsp;  &nbsp; Client: <select  ref={(input)=>this.Client= input} name="Client" className="form-control" id="id_Client" data-autocomplete-light-url="/client-autocomplete/" data-autocomplete-light-function="select2" multiple="multiple"></select>
                <div className="spacing1"> </div>

                Station ID: <select name="ID"  ref={(input)=>this.Kiosk = input} className="form-control" id="id_ID" data-autocomplete-light-url="/kiosk-autocomplete/" data-autocomplete-light-function="select2" multiple="multiple"></select>
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

          <h1>Stations</h1>
          <div className="spacing1"> </div>
            <table cellPadding="5" cellSpacing="5" border="0" className ="table-responsive-lg">
              <thead className = "tbl-header">
                <tr>
                  <th>Online</th>
                  <th>Station</th>
                  <th>Client</th>
                  <th>Location</th>
                  <th>Last Charge</th>
                  <th>Total Charge</th>
                  <th>Action</th>
                  <th>Refresh</th>
                </tr>
              </thead>
              <tbody className = "tbl-content">
              {this.state.kiosks.map(k=>
                  <tr key={k.ID} style={{height:12}}>
                  <td>{k.online ?
                  <img style={{height:10}} src="/static/images/Green_sphere.png"/>
                  :<img style={{height:10}} src="/static/images/Red_sphere.png"/>}</td>
                  <td><a title="More info" href ={'/kiosk/'+k.ID}>{k.ID}</a></td>
                  <td>{k.Client}</td>
                  <td>{k.Loc}</td>
                  <td>{k.last_update}</td>
                  <td>{k.Tot}</td>
                  <td> <a href={"/edit_kiosk/"+k.ID} style={{text_decoration:"none", lineHeight:"0%"}} className="transparent_btn" >Edit</a></td>
                  </tr>
              )}
              </tbody>
            </table>
          <div className="spacing1"> </div>
        </section>


      </div>
    )
  }
}
