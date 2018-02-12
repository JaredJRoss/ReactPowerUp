import React from "react"
import { render } from "react-dom"

import SampleAppContainer from "./containers/SampleAppContainer"

class SampleApp extends React.Component {
  render() {
    return (
        <SampleAppContainer user={user}/>
    )
  }
}

render(<SampleApp/>, document.getElementById('SampleApp'))
