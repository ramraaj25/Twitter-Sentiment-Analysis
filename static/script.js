function ani() {
    wel_btn = document.querySelector('.welcome');
    wel_btn.classList.add('animate__zoomOut');

    var delayInMilliseconds = 500; //1 second

    setTimeout(function () {
        wel_btn.style.display = 'none';
    }, delayInMilliseconds);

    choose_btns = document.querySelector('.btns')
    setTimeout(function () {
        choose_btns.classList.add('animate__fadeInDown')
        choose_btns.style.display = 'block'
    }, delayInMilliseconds);


}


