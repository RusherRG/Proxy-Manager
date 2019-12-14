function sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}

async function send_requests(request_json) {
    try {
        const config = {
            method: request_json['type'],
            headers: {
                'Accept': 'application/json',
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({'value': request_json['value'], 'id': request_json['id']})
        }
        console.log("Sending " + request_json['id']);
        const response = await fetch(request_json['url'], config);
        const response_json = await response.json();
        await console.log(response_json);
    } catch (error) {
        console.log(error);
    }
}

async function create_requests() {
        //get request
    var i = 100;
    var request_json = null;
    while(i--){
        $.get("http://localhost:5000/generate_request", function(data){
            request_json = data;
            request_json['id'] = i;
        });
        send_requests(request_json);    
        await sleep(3000);
    }
}

create_requests()
