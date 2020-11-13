/*------------------------------------
|             GLOBALS                |
------------------------------------*/

let nav_open = false
let opt_open = false
let nav = document.getElementById('page-nav')
let opt = document.getElementById('controls')
let tweak = document.getElementById('settings-wrapper')
let height = nav.scrollHeight.toString()


function toggleNav(){
    if(nav_open === true){
        nav.style.height = '0'
        nav_open = !nav_open
    }else if(nav_open === false){
        nav.style.height = `${height}px`
        nav_open = !nav_open
    }
}

function toggleOptions(){
    if(opt_open === true){
        opt.style.height = '0'
        opt_open = false
    }else if(opt_open === false){
        opt.style.height = `${opt.scrollHeight.toString()}px`
        opt_open = true
    }
}

function showSettings(){
    tweak.classList.remove('d-none')
}

// KeyframeEffect:{
//     from: {
//         opacity: 0;
//     }
//     to: {
//         opacity: 1;
//     }
// }

function hideSettings(){
    tweak.classList.add('d-none')
    // tweak.animate()

}
