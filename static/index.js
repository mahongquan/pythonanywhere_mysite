let host = '';
var stringifyPrimitive = function(v) {
  switch (typeof v) {
    case 'string':
      return v;

    case 'boolean':
      return v ? 'true' : 'false';

    case 'number':
      return isFinite(v) ? v : '';

    default:
      return '';
  }
};

function queryString_stringify(obj, sep, eq, name) {
  sep = sep || '&';
  eq = eq || '=';
  if (obj === null) {
    obj = undefined;
  }

  if (typeof obj === 'object') {
    return Object.keys(obj).map(function(k) {
      var ks = encodeURIComponent(stringifyPrimitive(k)) + eq;
      if (Array.isArray(obj[k])) {
        return obj[k].map(function(v) {
          return ks + encodeURIComponent(stringifyPrimitive(v));
        }).join(sep);
      } else {
        return ks + encodeURIComponent(stringifyPrimitive(obj[k]));
      }
    }).join(sep);

  }

  if (!name) return '';
  return encodeURIComponent(stringifyPrimitive(name)) + eq +
         encodeURIComponent(stringifyPrimitive(obj));
};
function checkStatus(response) {
  if (response.status >= 200 && response.status < 300) {
    return response;
  }
  const error = new Error(`HTTP Error ${response.statusText}`);
  error.status = response.statusText;
  error.response = response;
  throw error;
}
function parseJSON(response) {
  var r = response.json();
  return r;
}
function myFetch(method, url, body, cb, headers2, err_callback) {
  let data;
  let headers;
  if (headers2) {
    headers = headers2;
  } else {
    headers = { 'Content-Type': 'application/json' };
  }
  if (method === 'GET') {
    data = {
      method: method,
      credentials: 'include',
      headers: headers,
    };
  } else {
    data = {
      method: method,
      credentials: 'include',
      headers: headers,
      body: body,
    };
  }
  return fetch(host + url, data)
    .then(checkStatus)
    .then(parseJSON)
    .then(cb)
    .catch(error => {
      if (err_callback) err_callback(error);
      else alert(error + '\n请检查服务器/刷新网页/登录');
    });
}
function getRaw(url, cb, err_callback) {
  return myFetch('GET', url, undefined, cb, undefined, err_callback);
}
function get(url, data, cb, err_callback) {
  url = url + '?' + queryString_stringify(data);
  console.log(url);
  return getRaw(url, cb, err_callback);
}
function delete1(url, data, cb) {
  var method = 'DELETE';
  return myFetch(method, url, JSON.stringify(data), cb);
}
function post(url, data, cb) {
  var method = 'POST';
  return myFetch(method, url, JSON.stringify(data), cb);
}
function put(url, data, cb) {
  var method = 'PUT';
  return myFetch(method, url, JSON.stringify(data), cb);
}
class A extends React.Component{
    constructor(props) {
        super(props);
        this.state={contacts:[]};
    }
    componentDidMount = () => {
        get("/app1/contact",{},(res)=>{
            console.log(res);
            this.setState({contacts:res.data})
        },null);
    }
    render(){
        let contacts_tr=this.state.contacts.map((one,index)=>{
            return(<tr key={index}><td>{index}</td></tr>)
        })
        return(<div>
<table>
<tbody>
{
    contacts_tr
}
</tbody>
</table>
        </div>);
    }
}
ReactDOM.render(
<A />,
document.getElementById('root')
);
