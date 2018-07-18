import React from "react"
import { render } from "react-dom"

import PDFContainer from "./containers/PDFContainer"
class PDF extends React.Component {
  render() {
    return (
        <PDFContainer user={user}/>
    )
  }
}

render(<PDF/>, document.getElementById('PDF'))
