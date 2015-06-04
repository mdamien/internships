//have server api and fake api ?

API = {}

API.URL = "127.0.0.1:5000/"

API.call = function(endpoint, query, callback){
    $.getJSON({
        url:API.URL+endpoint,
        method:'get',
        params:query,
        sucess:function(data){
            callback(data);
        }
    })
}
