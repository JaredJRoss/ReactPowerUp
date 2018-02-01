import React from "react"
import Radium from "radium"


export default class SampleAppContainer extends React.Component {
  handleClick() {
    let {dispatch} = this.props;
    dispatch(counterActions.increaseCounter())
  }

  render() {
    let {counters} = this.props
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
            Start Date: <input type="text" name="start"></input>   &nbsp;   &nbsp;
            End Date: <input type="text" name="end"></input>
            <input style={{text_decoration:"none"}} type= "submit"class="transparent_btn" ></input>
          </form>
          <div className="spacing1"> </div>
          <a style={{text_decoration:"none"}} href="#hidden-div" data-target="#hidden-div" className="transparent_btn" data-toggle="collapse">Advanced Search</a>
            <div id ="hidden-div" className ="collapse" style={{color:"black"}}>
              <div className="spacing1"> </div>
              <form>
              <fieldset>
                Location: <select name="Location" className="form-control" id="id_Location" data-autocomplete-light-url="/location-autocomplete/" data-autocomplete-light-function="select2" multiple="multiple"></select>
                &nbsp;  &nbsp; Client: <select name="Client" className="form-control" id="id_Client" data-autocomplete-light-url="/client-autocomplete/" data-autocomplete-light-function="select2" multiple="multiple"></select>
                <div className="spacing1"> </div>

                Kiosk ID: <select name="ID" className="form-control" id="id_ID" data-autocomplete-light-url="/kiosk-autocomplete/" data-autocomplete-light-function="select2" multiple="multiple"></select>
                &nbsp;  &nbsp;  Type: <select name="Type" className="form-control" id="id_Type" data-autocomplete-light-url="/type-autocomplete/" data-autocomplete-light-function="select2" multiple="multiple"></select>

              </fieldset>
              <div className="spacing1"> </div>
              <input style={{text_decoration:"none"}} value = "Search" type= "submit" class="transparent_btn" ></input>
              </form>

             </div>
          </div>
          <div className="spacing1"> </div>
          <div className="spacing1"> </div>
          <div className="spacing1"> </div>
          <div className="spacing1"> </div>

          <h1>Table Title</h1>
          <div className="spacing1"> </div>

          <div className="tbl-header">
            <table cellPadding="0" cellspacing="0" border="0">
              <thead>
                <tr>
                  <th>Client</th>
                  <th>Logo</th>
                  <th>Location</th>
                  <th>Kiosk </th>
                  <th>Total Charge</th>
                </tr>
              </thead>
            </table>
          </div>
          <div className="tbl-content">
            <table cellPadding="0" cellspacing="0" border="0">
              <tbody>
              </tbody>
            </table>
          </div>
          <div className="spacing1"> </div>
        </section>


      </div>
    )
  }
}
