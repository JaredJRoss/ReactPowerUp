webpackJsonp([2],{0:function(e,t,n){"use strict";function r(e){return e&&e.__esModule?e:{"default":e}}function l(e,t){if(!(e instanceof t))throw new TypeError("Cannot call a class as a function")}function a(e,t){if(!e)throw new ReferenceError("this hasn't been initialised - super() hasn't been called");return!t||"object"!=typeof t&&"function"!=typeof t?e:t}function o(e,t){if("function"!=typeof t&&null!==t)throw new TypeError("Super expression must either be null or a function, not "+typeof t);e.prototype=Object.create(t&&t.prototype,{constructor:{value:e,enumerable:!1,writable:!0,configurable:!0}}),t&&(Object.setPrototypeOf?Object.setPrototypeOf(e,t):e.__proto__=t)}var u=function(){function e(e,t){for(var n=0;n<t.length;n++){var r=t[n];r.enumerable=r.enumerable||!1,r.configurable=!0,"value"in r&&(r.writable=!0),Object.defineProperty(e,r.key,r)}}return function(t,n,r){return n&&e(t.prototype,n),r&&e(t,r),t}}(),i=n(4),c=r(i),s=n(73),f=n(165),p=r(f),d=function(e){function t(){return l(this,t),a(this,(t.__proto__||Object.getPrototypeOf(t)).apply(this,arguments))}return o(t,e),u(t,[{key:"render",value:function(){return c["default"].createElement(p["default"],{kiosk:kiosk})}}]),t}(c["default"].Component);(0,s.render)(c["default"].createElement(d,null),document.getElementById("SampleApp2"))},165:function(e,t,n){"use strict";function r(e){return e&&e.__esModule?e:{"default":e}}function l(e,t){if(!(e instanceof t))throw new TypeError("Cannot call a class as a function")}function a(e,t){if(!e)throw new ReferenceError("this hasn't been initialised - super() hasn't been called");return!t||"object"!=typeof t&&"function"!=typeof t?e:t}function o(e,t){if("function"!=typeof t&&null!==t)throw new TypeError("Super expression must either be null or a function, not "+typeof t);e.prototype=Object.create(t&&t.prototype,{constructor:{value:e,enumerable:!1,writable:!0,configurable:!0}}),t&&(Object.setPrototypeOf?Object.setPrototypeOf(e,t):e.__proto__=t)}Object.defineProperty(t,"__esModule",{value:!0}),t["default"]=void 0;var u=function(){function e(e,t){for(var n=0;n<t.length;n++){var r=t[n];r.enumerable=r.enumerable||!1,r.configurable=!0,"value"in r&&(r.writable=!0),Object.defineProperty(e,r.key,r)}}return function(t,n,r){return n&&e(t.prototype,n),r&&e(t,r),t}}(),i=n(4),c=r(i),s=n(93),f=r(s),p=function(e){function t(e){l(this,t);var n=a(this,(t.__proto__||Object.getPrototypeOf(t)).call(this,e));return n.state={ports:[],dashboard:c["default"].createElement(f["default"],{search_terms:"ID="+n.props.kiosk,onUpdate:n.onUpdate.bind(n)}),online:!1},fetch("/api/kiosk?ID="+n.props.kiosk,{credentials:"include"}).then(function(e){return e.json()}).then(function(e){return n.setState({ports:e.ports,online:e.online})}),n}return o(t,e),u(t,[{key:"onUpdate",value:function(e,t,n){var r=this;fetch("/api/kiosk?ID="+this.props.kiosk+"&date="+e+"&start="+t+"&end="+n,{credentials:"include"}).then(function(e){return e.json()}).then(function(e){return r.setState({ports:e.ports,online:e.online})})}},{key:"render",value:function(){return c["default"].createElement("div",{name:"Dashboard"},this.state.online?c["default"].createElement("h1",null,c["default"].createElement("img",{style:{height:"25px"},src:"https://upload.wikimedia.org/wikipedia/commons/thumb/5/5d/Green_sphere.svg/256px-Green_sphere.svg.png"})," ",c["default"].createElement("span",null,"Kiosk ",this.props.kiosk," Details")):c["default"].createElement("h1",null,c["default"].createElement("img",{style:{height:"25px"},src:"https://upload.wikimedia.org/wikipedia/commons/thumb/6/60/Nuvola_apps_krec.svg/256px-Nuvola_apps_krec.svg.png"})," ",c["default"].createElement("span",null,"Kiosk  ",this.props.kiosk," Details")),c["default"].createElement("div",{"class":"spacing1"}," "),this.state.dashboard,c["default"].createElement("div",{className:"spacing2"}," "),c["default"].createElement("div",{className:"tbl-header"},c["default"].createElement("table",null,c["default"].createElement("thead",null,c["default"].createElement("tr",null,c["default"].createElement("th",null,"Port"),c["default"].createElement("th",null,"Type"),c["default"].createElement("th",null,"Total Charges"),c["default"].createElement("th",null,"Last Updated"),c["default"].createElement("th",null,"Flag"))))),c["default"].createElement("div",{className:"tbl-content"},c["default"].createElement("table",null,c["default"].createElement("tbody",null,this.state.ports.map(function(e){return c["default"].createElement("tr",{key:e.Port},c["default"].createElement("td",null,e.Port),c["default"].createElement("td",null,e.Type),c["default"].createElement("td",null,e.Total),c["default"].createElement("td",null,e.Last_Update),c["default"].createElement("td",null,e.Flag?c["default"].createElement("img",{style:{height:15},src:"https://publicdomainvectors.org/photos/HirnlichtspieleRedFlag.png"}):""))})))))}}]),t}(c["default"].Component);t["default"]=p}});