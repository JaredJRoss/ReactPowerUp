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
          <h1>Monthly Snapshot</h1>
          <div className="spacing1">

          </div>

          <div className = "transparentbox"> </div>
          <div className="spacing1"> </div>

          <div style={{text_align:'center'}}>
              <a style={{text_decoration: 'none'}} className="transparent_btn" href="#">Do something with this button</a>
              <div className="spacing1"> </div>
              <a style={{text_decoration:"none"}} href="#hidden-div" data-target="#hidden-div" className="transparent_btn" data-toggle="collapse">This is the button that shows collapsed elements</a>
              <div id ="hidden-div" className ="collapse" style={{color:"black"}}>
                  <div className="spacing1"> </div>
                  Place search/ whatever in here

              </div>



          </div>

          <div className="spacing1"> </div>
          <div className="spacing1"> </div>
          <div className="spacing1"> </div>
          <div className="spacing1"> </div>

          <h1>Table Title</h1>
          <div className="spacing1"> </div>

          <div className="tbl-header">
            <table cellpadding="0" cellspacing="0" border="0">
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
            <table cellpadding="0" cellspacing="0" border="0">
              <tbody>
              </tbody>
            </table>
          </div>
          <div className="spacing1"> </div>
          <a className="transparent_btn" href="#">Add</a>
        </section>

        <div className="spacing1"> </div>
        <div className="spacing1"> </div><div className="spacing1"> </div><div className="spacing1"> </div>

      </div>
    )
  }
}
