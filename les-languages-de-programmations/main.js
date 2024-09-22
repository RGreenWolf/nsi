document.addEventListener("DOMContentLoaded", function () {
    const buttons = [
        {
            text: 'Conclusion',
            href: '/conclusion/'
        }
    ]
    const dropdownButtons = [
        {
            text: 'Le début des Languages',
            href: '/themes/le-debut/'
        },
        {
            text: "Dans les années 1960 à 1990",
            href: "/themes/1960-1990/"
        },
        {
            text: 'Les langages modernes',
            href: '/themes/modernes/'
        },
        {
            text: 'Les différents types de langages',
            href: '/themes/les-types/'
        }
    ]


    buttons.forEach((button, index) => {
        const a = document.createElement('a');
        a.classList.add("nav-btn");
        a.href = button.href;
        a.textContent = button.text;
        document.querySelector('nav').appendChild(a);
    })

    dropdownButtons.forEach((button, index) => {
        const a = document.createElement('a');
        if(index != 0){
            const hr = document.createElement('hr');
            hr.classList.add("border-gray-400");
            document.querySelector('#dropdown-menu').appendChild(hr);
        }
        a.href = button.href;
        a.textContent = button.text;
        a.classList.add("nav-dropdown-btn-menu");
        document.querySelector('#dropdown-menu').appendChild(a);

    })

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

    const images = document.querySelectorAll('img');
    images.forEach(image => {
        if (!image.classList.contains("zoom-off")) {
            image.addEventListener('click', () => {
                const overlay = document.createElement('div');
                overlay.classList.add('image-overlay');

                const zoomedImage = image.cloneNode(true);
                zoomedImage.classList.add('zoomed-image');
                zoomedImage.style.transform = 'scale(1.5)';
                
                overlay.appendChild(zoomedImage);
                document.body.appendChild(overlay);
                document.body.style.overflow = 'hidden';

                setTimeout(() => {
                    overlay.classList.add('active');
                }, 10);

                overlay.addEventListener('click', (e) => {
                    if (e.target === overlay || e.target === zoomedImage) {
                        overlay.classList.remove('active');
                        document.body.style.overflow = '';
                        setTimeout(() => {
                            overlay.remove();
                        }, 300);
                    }
                });
            });
        }
    });

    const logo = document.querySelector('.logo');
    logo.addEventListener('click', () => {
        window.location.href = '/';
    });

    const analytics = document.createElement('script');
    analytics.defer = true;
    analytics.src = 'https://analytics.younity-mc.fr/script.js';
    analytics.dataset.websiteId = '485ef027-3637-4f09-b41e-c5b13805b004';
    document.head.appendChild(analytics);
});
