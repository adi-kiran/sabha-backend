<script>
function getJSON(){ 
let xhr = new XMLHttpRequest(); 
let url = "http://localhost:5000/api/posts"; 
xhr.open("POST", url, true); 
xhr.setRequestHeader("Content-Type", "application/json"); 
xhr.onreadystatechange = function () { 
if (this.readyState === 4 && this.status === 200) { 
    console.log(this.responseText);
    var div_post = document.getElementById("posts")
    // return the post, author, content, timestamp and hastag if we're keeping a search and store it in arr
    // var arr = data['collection_name'].split(';')
    var title = document.createElement("h3");
    var author = document.createElement("h5");
    var content = document.createElement("h6");
    var timestamp = document.createElement("h6")
    var upvotes = document.createElement("button");
    upvotes.innerHTML = "upvote";
    // upvotes.onclick	= function(){
    // increment upvotes value and reflect it 
    // }
    var downvotes = document.createElement("button");
    downvotes.innerHTML = "downvote";
    // downvotes.onclick	= function(){
    // decrement downvotes value and reflect it 
    // }

    author.innerHTML = arr[0].split(',')[0];
    title.innerHTML = arr[0].split(',')[1];
    content.innerHTML = arr[0].split(',')[2];
    timestampe.innerHTML = arr[0].split(',')[7];

    div_post.appendChild(title);
    div_post.appendChild(author);
    div_post.appendChild(content);
    div_post.appendChild(timestamp);
    div_post.appendChild(upvotes);
    div_post.appendChild(downvotes);
            
        $('.toast').toast('show');
    }
else{
    console.log(this.responseText);
    }
       }; 
       

xhr.send(); 
}

title.setAttribute('onclick', function(){loadPost(title)});
</script>
