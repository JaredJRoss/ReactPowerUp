import React from "react"
import Radium from "radium"
import DjangoCSRFToken from 'django-react-csrftoken'


export default class SampleAppContainer extends React.Component {
  constructor(props){
    super(props);
    this.state = {
        search_terms:'',
        url:'/api/search?',
        kiosks:[]
    };
    fetch('/api/search',{
      credentials: 'include',
    }).then(function(response){
      return response.json()
    }).then(data => this.setState({kiosks:data}));

    this.handleSearch = this.handleSearch.bind(this);

  }
  handleSearch(event) {
    var search_terms = '';
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
    event.preventDefault();
  }

  render() {
    let {counters} = this.props
    const test = true;
    return (
      <div classNameName="container">

      <section>
          <h1>Welcome</h1>
          <div className="spacing1">

          </div>

          <div className = "transparentbox"> </div>
          <div className="spacing1"> </div>

          <div style={{textAlign:'center'}}>
          <a style={{text_decoration:"none"}} className="transparent_btn" href="?date=all">All Time</a>
          <a style={{text_decoration:"none"}} className="transparent_btn" href="?date=year">Last Year</a>
          <a style={{text_decoration:"none"}} className="transparent_btn" href="?date=quarter">Last Quarter</a>
          <a style={{text_decoration:"none"}} className="transparent_btn" href="?date=month">Last Month</a>
          <a style={{text_decoration:"none"}} className="transparent_btn" href="?date=week">Last Week</a>
          <a style={{text_decoration:"none"}} className="transparent_btn" href="?date=day">Last Day</a>
          <a style={{text_decoration:"none"}} className="transparent_btn" href="?date=hour">Last Hour</a>
          <div className="spacing1"> </div>
          <form action="#" method="get">
          <DjangoCSRFToken/>
            Start Date: <input type="text" name="start"></input>   &nbsp;   &nbsp;
            End Date: <input type="text" name="end"></input>
            <input style={{text_decoration:"none"}} type= "submit"className="transparent_btn" ></input>
          </form>
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
