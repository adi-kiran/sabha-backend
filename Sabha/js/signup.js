function sendJSON(){ 
               
    full_name = document.getElementById("fname"); 
    username = document.getElementById("uname"); 
    password = document.getElementById("pwd"); 
       
    // Creating a XHR object 
    let xhr = new XMLHttpRequest(); 
    let url = "localhost:5000/api/user/add"; 

    // open a connection 
    xhr.open("PUT", url, true); 

    // Set the request header i.e. which type of content you are sending 
    xhr.setRequestHeader("Content-Type", "application/json"); 

    // Create a state change callback 
    xhr.onreadystatechange = function () { 
        if (xhr.readyState === 4 && xhr.status === 200) { 

            // Do the necessary action

        } 
    }; 

    // Converting JSON data to string 
    var data = JSON.stringify({ "full_name": full_name.value, "username": username.value , "password": password.value }); 

    // Sending data with the request 
    xhr.send(data); 
} 