function getQueryParams(qs) {
    qs = qs.split("+").join(" ");

    var params = {}, tokens,
        re = /[?&]?([^=]+)=([^&]*)\//g;

    while (tokens = re.exec(qs)) {
        params[decodeURIComponent(tokens[1])]
            = decodeURIComponent(tokens[2]);
    }

    return params;
}
var query = getQueryParams(document.location.search);
var file = "fake";
if('file' in query){
    file = query.file
}
console.log("load",file);

React.render(<Loader data_url={"data/"+file+".csv"} />, document.getElementById('content'))
