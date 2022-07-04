document.querySelector('.toggle').addEventListener('click', function() {
    document.querySelector('.header-menu').classList.toggle('expanded');  
    show_span();
    show_close_btn();
  });


document.getElementById('toolbar_btn').addEventListener('click', ()=>{
    document.getElementById('toolbar').classList.toggle('show_toolbar');
})

function show_span(){
    spans = document.querySelectorAll('.nav-item');
    for(i=0; i< spans.length; i++){
        spans[i].classList.toggle('hidden');
    }
}

function show_close_btn(){
    btn = document.querySelector('.header-container, .toggle');
    button = document.querySelector('.toggle');
    btn.classList.toggle('close'); 
    button.classList.toggle('close');
}






