document.getElementById('searchBtn').addEventListener('click',function(){
    document.querySelector('.mobile-search-form').classList.toggle('expanded');
    document.querySelector('.mobile-search').classList.toggle('search-bg');
    document.getElementById('openSearchbar').classList.toggle('hide');
    document.getElementById('closeSearchbar').classList.toggle('show');
})
window.addEventListener('resize', function(){
    const width = window.innerWidth;
    if(width >= 780){
        document.querySelector('.sidebar-container').classList.remove('mobile-sidebar');
    }
})
document.getElementById('topicBtn').addEventListener('click', function(){
    
    document.querySelector('.sidebar-container').classList.toggle('mobile-sidebar');
})

