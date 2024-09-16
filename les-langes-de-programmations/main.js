document.addEventListener("DOMContentLoaded", function () {
    const button = document.querySelector('#dropdown-button');
    const dropdown = document.querySelector('#dropdown-menu');

    button.addEventListener('click', function () {
        dropdown.classList.toggle('hidden');
    });
    const links = document.getElementsByTagName("a")
    for (let index = 0; index < links.length; index++) {
        if(links[index].href == window.location.href){
            links[index].classList.add("bg-teal-500");
        }
    }
});
