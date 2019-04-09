import React from "react"
import  ReactDOM from 'react-dom';
import BarChart from "react-d3-components/lib/BarChart"


export default class ResponsiveBarChart extends React.Component {
  constructor(props){
    super(props);
    this.state={
      size:{w:0,h:0},
    };

  }

  fitToParentSize() {
      const elem = ReactDOM.findDOMNode(this);
      const w = elem.parentNode.offsetWidth;
      const h = 400;
      const currentSize = this.state.size;
      console.log(elem.parentNode.offsetHeight)
      if (w !== currentSize.w || h !== currentSize.h) {
        this.setState({
          size: { w, h },
        });
      }

    }


    componentDidMount() {
        window.addEventListener('resize', ::this.fitToParentSize);
        this.fitToParentSize();

    }

    componentWillReceiveProps() {
      this.fitToParentSize();
    }

    componentWillUnmount() {
         window.removeEventListener('resize', ::this.fitToParentSize);
      }


  render(){
    let { width, height, margin,data, ...others } = this.props;

       // Determine the right graph width to use if it's set to be responsive
       width = this.state.size.w || 400;
       height = this.state.size.h || 400;


    return(
      <div className="RespBar">
      <BarChart
      data={this.props.data}
      height={height}
      width={width}
      margin={this.props.margin}
      tooltipHtml ={this.props.tooltipHtml}
      />
      </div>
    )
  }
}