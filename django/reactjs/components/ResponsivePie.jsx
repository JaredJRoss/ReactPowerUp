import React from "react"
import  ReactDOM from 'react-dom';
import PieChart from "react-d3-components/lib/PieChart"


export default class ResponsivePieChart extends React.Component {
  constructor(props){
    super(props);
    this.state={
      size:{w:0,h:0},
    };
    console.log("Date")
    console.log(this.props.data)
    console.log(this.props.margin)
  }

  fitToParentSize() {
      const elem = ReactDOM.findDOMNode(this);
      const w = elem.parentNode.offsetWidth;
      const h = 400;
      const currentSize = this.state.size;
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
      <div className="RespPie">
          <PieChart
          data={this.props.data}
          width={width}
          height={height}
          margin={this.props.margin}
          colorScale={this.props.colorScale}
          sort={null}
          tooltipHtml = {this.props.tooltipHtml}
          />
      </div>
    )
  }
}
