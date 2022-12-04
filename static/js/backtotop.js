const backtotop = document.getElementById("backtotop");

const moveBackToTop = () => {
    if ( window.pageYOffset > 0 ) {
        window.scroll({top : 0, behavior : "smooth"})
    }
}

const checkScroll = () => {
    if ( window.pageYOffset === 0 ){
        backtotop.style.visibility = "hidden"
    }
    else{
        backtotop.style.visibility = "visible"
    }
}
window.addEventListener("scroll", checkScroll);
backtotop.addEventListener("click", moveBackToTop);

/*-------------------------------------------------------*/
const arrowPrev = document.getElementsByClassName("arrow-prev");
const arrowNext = arrowPrev[0].nextElementSibling;
const arrowContainer = arrowPrev[0].parentElement;

const transformNext = (event) => {
    const next = event.target;
    const prev = next.previousElementSibling;
    let activeLi = classList.getAttribute("data-position");
    const liList = classList.getElementsByTagName("li");

    if( classList.clientWidth < Number(activeLi) + (liList.length * 240)){
        activeLi = Number(activeLi) - 170;

        if( classList.clientWidth > Number(activeLi) + (liList.length * 240) ){
            next.style.color = "#ccc";
            next.classList.remove("arrow-next-hover");
            next.removeEventListener("click", transformNext);
        }
        prev.style.color = "red";
        prev.classList.add("arrow-prev-hover");
        prev.addEventListener("click", transformPrev);
    }
    classList.style.transition = "transform 1s";
    classList.style.transform = "translateX(" + String(activeLi) + "px)";
    classList.setAttribute("data-position", activeLi);
}

const transformPrev = (event) => {
    const prev = event.target;
    const next = prev.nextElementSibling;
    let activeLi = classList.getAttribute("data-position");
    const liList = classList.getElementsByTagName("li");

    if ( activeLi < 0 ){
        activeLi = Number(activeLi) + 170;
        next.style.color = "red";
        next.classList.add("arrow-next-hover");
        next.addEventListener("click", transformNext)
        if ( activeLi === 0 ){
            prev.style.color = "#ccc";
            prev.classList.remove("arrow-prev-hover");
            prev.removeEventListener("click", transformPrev);
        }
    }
    
    classList.style.transition = "transform 1s";
    classList.style.transform = "translateX(" + String(activeLi) + "px)";
    classList.setAttribute("data-position", activeLi);
}

let classList = arrowPrev[0].parentElement.nextElementSibling;
let liList = classList.getElementsByTagName("li");
if ( classList.clientWidth < (liList.length * 240)){
    arrowNext.classList.add("arrow-next-hover");
    arrowNext.addEventListener("click", transformNext);
}   else{
    arrowContainer.removeChild(arrowPrev[0].nextElementSibling);
    arrowContainer.removeChild(arrow[0]);
}
/*------------------------------------*/
