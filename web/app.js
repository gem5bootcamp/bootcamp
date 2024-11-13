/* Constant parameters */
const slide_url_base = './slides/'
const slide_url_ext = '.html'
const pdf_url_base = './pdf/'
const pdf_url_ext = '.pdf'
const slide_link_height = 25;

/* Button Names variables */
SHOW_SOLUTION_BUTTON_TEXT = "Show Solution";
HIDE_SOLUTION_BUTTON_TEXT = "Hide Solution";

/* Global references and variables */
let slide_list = [];
let slide_id = -1;

window.addEventListener('load', function() {
    let slide_registry = get_slide_registry();
    populate_sidebar(slide_registry);

    /* Follow url hash */
    document.querySelector('#slideFrame').addEventListener('load', slide_onload);
    route(window.location.hash, false);
});

/* ========================================================================= *
 * Routing
 * ========================================================================= */

function route(url, push=true) {
    if (push) {
        /* Push onto browser history */
        window.history.pushState('', '', url);
    }
    /* Check for home page */
    let home_page = document.querySelector('#home');
    let slide_page = document.querySelector('#slideView')
    if (url === '' || url === '#') {
        home_page.classList.remove('hidden');
        slide_page.classList.add('hidden');
        return;
    }
    /* Set iframe src */
    let full_url = slide_url_base + url.substring(1) + slide_url_ext;
    document.querySelector('#slideFrame').src = full_url;
    document.querySelector('#slideFrame').title = url;
    /* Find slide id number */
    slide_id = -1;
    for (const slide of slide_list) {
        if (url === slide.getAttribute('slide-url')) {
            slide_id = parseInt(slide.getAttribute('slide-id'));
            break;
        }
    }
    if (slide_id < 0) {
        /* Slide not found, just bring up splash page to hide the mess */
        home_page.classList.remove('hidden');
        slide_page.classList.add('hidden');
    } else {
        home_page.classList.add('hidden');
        slide_page.classList.remove('hidden');
    }
    /* Set slide name */
    document.querySelector('#slideName').textContent = url.substring(1);
    /* Configure buttons */
    let prev = document.querySelector('#prevSlide');
    let next = document.querySelector('#nextSlide');
    if (slide_id <= 0) {
        prev.classList.add('hidden');
    } else {
        prev.classList.remove('hidden');
        prev.children[1].textContent = slide_list[slide_id - 1].textContent;
    }
    if (slide_id >= slide_list.length - 1) {
        next.classList.add('hidden');
    } else {
        next.classList.remove('hidden');
        next.children[1].textContent = slide_list[slide_id + 1].textContent;
    }
    /* Configure pdf link */
    let pdf = document.querySelector('#slidePdf');
    let pdf_url = pdf_url_base + url.substring(1) + pdf_url_ext;
    pdf.href = pdf_url;
}

window.addEventListener('popstate', () => {
	route(window.location.hash, false);
});

/* ========================================================================= *
 * Slide Navigation
 * ========================================================================= */

function prev_slide() {
    if (slide_id > 0) {
        route(slide_list[slide_id - 1].getAttribute('slide-url'));
    }
}

function next_slide() {
    if (slide_id < slide_list.length - 1) {
        route(slide_list[slide_id + 1].getAttribute('slide-url'));
    }
}

function sidebar_category_onclick(e) {
    let curr_clicked = this.parentElement;
    let prev_selected = document.querySelectorAll('.sidebar-category.selected');
    /* Close all previously selected categories */
    let clicked_already_selected = false;
    for (const cat of prev_selected) {
        cat.classList.remove('selected');
        cat.children[1].style.height = '';
        if (cat === curr_clicked)
            clicked_already_selected = true;
    }
    /* Clicking already-selected button should just close it */
    if (clicked_already_selected)
        return;
    /* Open category */
    let slides = curr_clicked.children[1];
    curr_clicked.classList.add('selected');
    let height = slide_link_height * slides.children.length;
    slides.style.height = `${height}px`;
}

/* ========================================================================= *
 * Copy functionality
 * ========================================================================= */
function addCopyButtonsInIframe() {
    let frame = document.querySelector('#slideFrame');
    if (!frame) {
        console.error("Error: #slideFrame element not found.");
        return;
    }

    // Function to insert copy buttons in <marp-pre><code> blocks inside the iframe
    const insertCopyButtons = () => {
        const frame = document.querySelector('#slideFrame');
        const codeBlocks = frame.contentDocument.querySelectorAll('marp-pre code');

        codeBlocks.forEach((block) => {
            if (block.parentElement.querySelector('.copy-button')) return; // Avoid duplicates

            // Create the copy button element
            let copyButton = document.createElement('button');
            copyButton.classList.add('copy-button');
            copyButton.innerHTML = `<svg width="26px" height="26px" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                                        <path d="M15.24 2H11.3458C9.58159 1.99999 8.18418 1.99997 7.09054 2.1476C5.96501 2.29953 5.05402 2.61964 4.33559 3.34096C3.61717 4.06227 3.29833 4.97692 3.14701 6.10697C2.99997 7.205 2.99999 8.60802 3 10.3793V16.2169C3 17.725 3.91995 19.0174 5.22717 19.5592C5.15989 18.6498 5.15994 17.3737 5.16 16.312L5.16 11.3976L5.16 11.3024C5.15993 10.0207 5.15986 8.91644 5.27828 8.03211C5.40519 7.08438 5.69139 6.17592 6.4253 5.43906C7.15921 4.70219 8.06404 4.41485 9.00798 4.28743C9.88877 4.16854 10.9887 4.1686 12.2652 4.16867L12.36 4.16868H15.24L15.3348 4.16867C16.6113 4.1686 17.7088 4.16854 18.5896 4.28743C18.0627 2.94779 16.7616 2 15.24 2Z" fill="#007BFF"/>
                                        <path d="M6.6001 11.3974C6.6001 8.67119 6.6001 7.3081 7.44363 6.46118C8.28716 5.61426 9.64481 5.61426 12.3601 5.61426H15.2401C17.9554 5.61426 19.313 5.61426 20.1566 6.46118C21.0001 7.3081 21.0001 8.6712 21.0001 11.3974V16.2167C21.0001 18.9429 21.0001 20.306 20.1566 21.1529C19.313 21.9998 17.9554 21.9998 15.2401 21.9998H12.3601C9.64481 21.9998 8.28716 21.9998 7.44363 21.1529C6.6001 20.306 6.6001 18.9429 6.6001 16.2167V11.3974Z" fill="#007BFF"/>
                                    </svg>`;

            // Set the CSS position directly with JavaScript
            copyButton.style.position = 'absolute';
            copyButton.style.top = '2px';
            copyButton.style.right = '2px';
            copyButton.style.background = 'none';
            copyButton.style.border = 'none';
            copyButton.style.padding = '4px';
            copyButton.style.cursor = 'pointer';
            copyButton.style.opacity = '0.7';

            // Apply position to the <marp-pre> container
            block.parentElement.style.position = 'relative';

            // Insert the copy button at the beginning of each <marp-pre> element
            block.parentElement.insertBefore(copyButton, block);

            // Add the copy functionality
            copyButton.addEventListener('click', () => {
                navigator.clipboard.writeText(block.innerText);
            });
        });
    };


    // MutationObserver to detect changes within the iframe's content
    const observer = new MutationObserver(insertCopyButtons);

    // Listen for when the iframe content loads
    frame.addEventListener('load', () => {
        // Observe the iframe's document for added <marp-pre><code> blocks
        observer.observe(frame.contentDocument.body, { childList: true, subtree: true });
        insertCopyButtons();  // Initial call for existing code blocks
    });
}

// Run addCopyButtonsInIframe after the main DOM is fully loaded
document.addEventListener('DOMContentLoaded', addCopyButtonsInIframe);

/* ========================================================================= *
 * Hidden slides logic handeling
 * ========================================================================= */
function setupToggleButtons() {
    const frame = document.querySelector('#slideFrame');

    // Check if iframe exists and load content
    if (frame) {
        frame.addEventListener('load', () => {
            const contentDoc = frame.contentDocument || frame.contentWindow.document;

            // Select all toggle buttons and toggle-content sections in the iframe
            const toggleButtons = contentDoc.querySelectorAll('.toggle-button');
            const toggleContents = contentDoc.querySelectorAll('.toggle-content');

            // Force initial hidden state for all toggle-content elements
            toggleContents.forEach(content => {
                content.style.display = 'none';  // Ensure they are hidden at the start
            });

            // Initialize each button's text to "Show Content" and add inline styles
            toggleButtons.forEach(button => {
                button.textContent = SHOW_SOLUTION_BUTTON_TEXT;

                // Apply inline styles to the toggle button
                button.style.cursor = 'pointer';
                button.style.backgroundColor = '#007bff'; // Blue color
                button.style.color = 'white';
                button.style.padding = '10px';
                button.style.border = 'none';
                button.style.borderRadius = '5px';
                button.style.fontSize = '16px';
                button.style.marginTop = '10px';

                // Hover effect
                button.addEventListener('mouseover', () => {
                    button.style.backgroundColor = '#0056b3'; // Darker blue on hover
                });
                button.addEventListener('mouseout', () => {
                    button.style.backgroundColor = '#007bff'; // Original blue
                });
            });

            // Add click event listener to each toggle button
            toggleButtons.forEach((button, index) => {
                button.addEventListener('click', () => {
                    const content = toggleContents[index];
                    if (content) {
                        // Toggle the display of the content
                        if (content.style.display === 'none') {
                            content.style.display = 'block';
                            button.textContent = HIDE_SOLUTION_BUTTON_TEXT;
                        } else {
                            content.style.display = 'none';
                            button.textContent = SHOW_SOLUTION_BUTTON_TEXT;
                        }
                    }
                });
            });
        });
    } else {
        console.error("Error: #slideFrame element not found.");
    }
}

// Run setupToggleButtons after the main DOM is fully loaded
document.addEventListener('DOMContentLoaded', setupToggleButtons);

/* ========================================================================= *
 * Relative Link to Git Translation !!TEMPORARY!!
 * ========================================================================= */

const bootcamp_base = 'https://github.com/gem5bootcamp/2024/tree/main/';
const gem5_base = 'https://github.com/gem5/gem5/tree/stable/';
const gem5_resources_base = 'https://github.com/gem5/gem5-resources/tree/stable/';
function translate_rel_link(base_url, link) {
    if (!link.includes(window.location.origin)) {
        /* All non-relative links, just return the original */
        return link;
    }
    /* Determine which location to translate to */
    link = link.replace(window.location.origin + '/', '');
    let g;
    if ((g = /^gem5\/(.+)/.exec(link))) {
        /* gem5 repo */
        return gem5_base + g[1];
    }
    if ((g = /^gem5-resources\/(.+)/.exec(link))) {
        /* gem5 resources repo */
        return gem5_resources_base + g[1];
    }
    if (g = /^slides\/(.+)\.md/.exec(link)) {
        /* local slides */
        return '/#' + g[1];
    }
    /* Everything else, send to bootcamp repo */
    return bootcamp_base + link;
}

/* ========================================================================= *
 * Slide Augmentation
 * ========================================================================= */

function slide_onload(event) {
    /* Have all hyperlinks in iframe open in new tab */
    let frame = document.querySelector('#slideFrame');
    let links = frame.contentDocument.querySelectorAll('a');
    for (const a of links) {
        a.setAttribute('target', '_blank');
    }
    /* Translate links to github repos */
    let base_url = location.hash.substring(1);
    for (const a of links) {
        a.href = translate_rel_link(base_url, a.href);
    }
}

/* ========================================================================= *
 * Element generators and DOM populators
 * ========================================================================= */

function make_slide_link(name, link) {
    let elem = document.createElement('div');
    elem.classList.add('slide-link');
    elem.textContent = name;
    elem.href = '#';
    elem.setAttribute('slide-id', slide_list.length);
    elem.setAttribute('slide-url', link);
    elem.addEventListener('click', (e) => {
        e.preventDefault();
        route(elem.getAttribute('slide-url'));
    });
    slide_list.push(elem);
    return elem;
}

function make_category(cat) {
    let elem = document.createElement('div');
    elem.classList.add('sidebar-category');
    /* Add `category-button` */
    elem.append((() => {
        let elem = document.createElement('div');
        elem.classList.add('category-button');
        elem.onclick = sidebar_category_onclick;
        /* Add `category-name` */
        elem.append((() => {
            let elem = document.createElement('span');
            elem.classList.add('category-name');
            elem.textContent = cat.name;
            return elem;
        })());
        /* Add `dropdown-arrow` */
        elem.append((() => {
            let elem = document.createElement('img');
            elem.classList.add('dropdown-arrow');
            elem.src = 'chevron.svg';
            return elem;
        })());
        return elem;
    })());

    /* Add slide links */
    let link_base = `#${cat.name}/`;
    elem.append((() => {
        let elem = document.createElement('div');
        elem.classList.add('category-slides');
        for (const slide of cat.slides) {
            elem.append(make_slide_link(slide, `${link_base}${slide}`));
        }
        return elem;
    })());

    return elem;
}

function populate_sidebar(slide_registry) {
    let sidebar = document.querySelector('.sidebar');
    for (const cat of slide_registry) {
        sidebar.append(make_category(cat));
    }
}
