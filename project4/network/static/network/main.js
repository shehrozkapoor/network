// DOMContent Loaded
document.addEventListener("DOMContentLoaded", function () {
    // this query will hide all the edit post block from the post
    document.querySelectorAll('.edit_post_block').forEach(item => item.style.display = 'none');
    // this function will select all the edit buttons from html and then 
    // if user clicked on eny edit post then it will go to edit post function
    document.querySelectorAll('#edit_btn').forEach(btn => btn.addEventListener('click', function (event) {
        event.target.style.display='none';
        edit_post(event.target.name);
    }));
    // this query will select  all save buttons if user click on save button then 
    // it will go to edit_save_post function
    document.querySelectorAll('.edit_save_btn').forEach(btn => btn.addEventListener('click',(event)=>{
        edit_save_post(event.target.name);
        document.querySelector(`.edit_btn_${event.target.name}`).style.display='block';
    }));
    // this query will select all the like icons from the HTMl and then if user 
    // click on any one it will got to liked function
    document.querySelectorAll('svg').forEach(btn => btn.addEventListener('click',(btn)=>{
        liked(btn.target.parentElement.id);
    }));
});
// if user click on a edit button then this will call api method in views.py 
// file and get the response and display the textarea field to user and save button
function edit_post(btn) {
    fetch(`/edit_post/${btn}`, {
            method: "GET"
        })
        .then(response => response.json())
        .then(item => {
            document.querySelector(`.text_area_${btn} .edit_post_block`).style.display = 'block';
            document.querySelector(`.text_area_${btn} h3`).style.display = 'none';
        })
}
// when the user clicks on save button then it will call the api method in views.py 
// file and then put a request to api and then save the post statically
function edit_save_post(btn) {
    let get_text = document.querySelector(`.text_area_field_${btn}`);
    fetch(`/edit_post/${btn}`, {
            method: "PUT",
            body: JSON.stringify({
                content: get_text.value,
            })
        })
        .then(response => response.json())
        .then(result => {
            if(result.message === "succesfull"){
                document.querySelector(`.text_area_${btn} .edit_post_block`).style.display='none';
                document.querySelector(`.text_area_${btn} h3`).innerText = get_text.value;
                document.querySelector(`.text_area_${btn} h3`).style.display = 'block';
            }
        })
}
// if user clicked on liked icon (SVG) this will call an API and then get the response 
// if the response is notliked then it will like the post if the post is liked then it will unlike the post
function liked(id){
    fetch(`/liked/${id}`,{method:"GET"})
    .then(response => response.json())
    .then(result => {
        if(result.message ==="notliked"){
            const liked_count = parseInt(document.querySelector(`.post_likes_count_${id}`).innerText);
            document.querySelector(`.svg_icon_${id} svg`).setAttribute('fill','red');
            document.querySelector(`.post_likes_count_${id}`).innerText = liked_count+1;
            fetch(`/liked/${id}`,{method:"PUT"})
        }
        else{
            const liked_count = parseInt(document.querySelector(`.post_likes_count_${id}`).innerText);
            document.querySelector(`.svg_icon_${id} svg`).setAttribute('fill','black');
            document.querySelector(`.post_likes_count_${id}`).innerText = liked_count-1;
            fetch(`/liked/${id}`,{method:"PUT"})
        }
    })
}