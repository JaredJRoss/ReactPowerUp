import React from "react"
import Dashboard from "../components/Dashboard"
import Datetime from "react-datetime"

export default class SampleApp2Container extends React.Component {
  constructor(props){
    super(props);
    this.state={
      ports:[],
      dashboard:<Dashboard search_terms={'ID='+this.props.kiosk} onUpdate={this.onUpdate.bind(this)}/>,
      online:false,
    }
    fetch('/api/kiosk?ID='+this.props.kiosk,{
      credentials: 'include',
    }).then(function(response){
      return response.json()
    }).then(data => this.setState({ports:data.ports, online:data.online}));
  }

  onUpdate(date,start,end){
    fetch('/api/kiosk?ID='+this.props.kiosk+'&date='+date+'&start='+start+'&end='+end,{
      credentials: 'include',
    }).then(function(response){
      return response.json()
    }).then(data => this.setState({ports:data.ports,online:data.online}));
  }

  render(){
    return(
      <div name="Dashboard">
      {
        this.state.online ?
        <h1><img style={{height:'25px'}} src="/static/images/Green_sphere.png"/> <span>Station {this.props.kiosk} Details</span></h1>
        :<h1><img style={{height:'25px'}} src="/static/images/Red_sphere.png"/> <span>Station  {this.props.kiosk} Details</span></h1>
      }
      <div className="spacing1"> </div>
      {this.state.dashboard}
      <div className="spacing2"> </div>
      <div className="tbl-header">
        <table>
          <thead>
            <tr>
              <th>Port</th>
              <th>Type</th>
              <th>Total Charges</th>
              <th>Last Updated</th>
              <th>Flag</th>
              <th>Action</th>
            </tr>
          </thead>
        </table>
      </div>
      <div className="tbl-content" style={{height:400}}>
        <table className ="table-responsive-lg">
          <tbody>
          {this.state.ports.map(p=>
            <tr key = {p.Port}>
              <td>{p.Port}</td>
              <td>{p.Type}</td>
              <td>{p.Total}</td>
              <td>{p.Last_Update}</td>
              <td>{
              p.Flag ? <img style={{height:15}} src="/static/images/RedFlag.png"/>:''}
              </td>
              <td> <a href={"/edit_port/"+p.pk} style={{text_decoration:"none"}} className="transparent_btn" >Edit</a>
              </td>
            </tr>
          )}
          </tbody>
        </table>

      </div>

      </div>
    )
  }
}
