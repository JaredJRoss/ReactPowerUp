webpackJsonp([1],{0:function(e,t,n){"use strict";function l(e){return e&&e.__esModule?e:{"default":e}}function r(e,t){if(!(e instanceof t))throw new TypeError("Cannot call a class as a function")}function a(e,t){if(!e)throw new ReferenceError("this hasn't been initialised - super() hasn't been called");return!t||"object"!=typeof t&&"function"!=typeof t?e:t}function o(e,t){if("function"!=typeof t&&null!==t)throw new TypeError("Super expression must either be null or a function, not "+typeof t);e.prototype=Object.create(t&&t.prototype,{constructor:{value:e,enumerable:!1,writable:!0,configurable:!0}}),t&&(Object.setPrototypeOf?Object.setPrototypeOf(e,t):e.__proto__=t)}var u=function(){function e(e,t){for(var n=0;n<t.length;n++){var l=t[n];l.enumerable=l.enumerable||!1,l.configurable=!0,"value"in l&&(l.writable=!0),Object.defineProperty(e,l.key,l)}}return function(t,n,l){return n&&e(t.prototype,n),l&&e(t,l),t}}(),i=n(3),c=l(i),s=n(26),f=n(300),p=l(f),d=function(e){function t(){return r(this,t),a(this,(t.__proto__||Object.getPrototypeOf(t)).apply(this,arguments))}return o(t,e),u(t,[{key:"render",value:function(){return c["default"].createElement(p["default"],{kiosk:kiosk})}}]),t}(c["default"].Component);(0,s.render)(c["default"].createElement(d,null),document.getElementById("SampleApp2"))},300:function(e,t,n){"use strict";function l(e){return e&&e.__esModule?e:{"default":e}}function r(e,t){if(!(e instanceof t))throw new TypeError("Cannot call a class as a function")}function a(e,t){if(!e)throw new ReferenceError("this hasn't been initialised - super() hasn't been called");return!t||"object"!=typeof t&&"function"!=typeof t?e:t}function o(e,t){if("function"!=typeof t&&null!==t)throw new TypeError("Super expression must either be null or a function, not "+typeof t);e.prototype=Object.create(t&&t.prototype,{constructor:{value:e,enumerable:!1,writable:!0,configurable:!0}}),t&&(Object.setPrototypeOf?Object.setPrototypeOf(e,t):e.__proto__=t)}Object.defineProperty(t,"__esModule",{value:!0}),t["default"]=void 0;var u=function(){function e(e,t){for(var n=0;n<t.length;n++){var l=t[n];l.enumerable=l.enumerable||!1,l.configurable=!0,"value"in l&&(l.writable=!0),Object.defineProperty(e,l.key,l)}}return function(t,n,l){return n&&e(t.prototype,n),l&&e(t,l),t}}(),i=n(3),c=l(i),s=n(102),f=(l(s),n(82)),p=(l(f),n(251)),d=(l(p),n(117)),m=(l(d),n(255)),h=(l(m),n(259)),y=(l(h),function(e){function t(e){r(this,t);var n=a(this,(t.__proto__||Object.getPrototypeOf(t)).call(this,e));return n.state={ports:[],online:!1},fetch("/api/kiosk?ID="+n.props.kiosk,{credentials:"include"}).then(function(e){return e.json()}).then(function(e){return n.setState({ports:e.ports,online:e.online})}),n}return o(t,e),u(t,[{key:"onUpdate",value:function(e,t,n){var l=this;fetch("/api/kiosk?ID="+this.props.kiosk+"&date="+e+"&start="+t+"&end="+n,{credentials:"include"}).then(function(e){return e.json()}).then(function(e){return l.setState({ports:e.ports,online:e.online})})}},{key:"render",value:function(){return c["default"].createElement("div",{name:"Dashboard1"},this.state.online?c["default"].createElement("h1",null,c["default"].createElement("img",{style:{height:"25px"},src:"/static/images/Green_sphere.png"})," ",c["default"].createElement("span",null,"Station ",this.props.kiosk," Details")):c["default"].createElement("h1",null,c["default"].createElement("img",{style:{height:"25px"},src:"/static/images/Red_sphere.png"})," ",c["default"].createElement("span",null,"Station  ",this.props.kiosk," Details")),c["default"].createElement("div",{className:"spacing1"}," "),c["default"].createElement("div",{className:"spacing2"}," "),c["default"].createElement("div",{className:"tbl-header"},c["default"].createElement("table",null,c["default"].createElement("thead",null,c["default"].createElement("tr",null,c["default"].createElement("th",null,"Port"),c["default"].createElement("th",null,"Type"),c["default"].createElement("th",null,"Total Charges"),c["default"].createElement("th",null,"Last Updated"),c["default"].createElement("th",null,"Flag"),c["default"].createElement("th",null,"Action"))))),c["default"].createElement("div",{className:"tbl-content",style:{height:400}},c["default"].createElement("table",{className:"table-responsive-lg"},c["default"].createElement("tbody",null,this.state.ports.map(function(e){return c["default"].createElement("tr",{key:e.Port},c["default"].createElement("td",null,e.Port),c["default"].createElement("td",null,e.Type),c["default"].createElement("td",null,e.Total),c["default"].createElement("td",null,e.Last_Update),c["default"].createElement("td",null,e.Flag?c["default"].createElement("img",{style:{height:15},src:"/static/images/RedFlag.png"}):""),c["default"].createElement("td",null," ",c["default"].createElement("a",{href:"/edit_port/"+e.pk,style:{text_decoration:"none"},className:"transparent_btn"},"Edit")))})))))}}]),t}(c["default"].Component));t["default"]=y}});