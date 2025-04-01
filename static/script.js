//document.addEventListener('DOMContentLoaded',function(){

if (localStorage.getItem('reloaded')===false){
    location.reload(true)
    localStorage.setItem('reloaded',true)
    console.log('reloaded')
}
// -----------------extract from files items to container-----------------------

let categories = [];
let copy_main_grid;


async function init() {


    const response = await fetch('static/items_info.json');
    const products = await response.json();
    categories = [... new Set(products.map((item) => { return item }))];

    let i = 0;
    document.querySelector('.root').innerHTML = categories.map(item => {
        const desc_item = item['description'], id_item = item['id'],image = item['image'], title = item['title'], price = item['price']
        return (
            `<div class='box' data-index=${id_item}>
                <div class='box-container'>

                    <button style='display:none;' class='back-button' onclick='back_button();'>
                        <p>Back</p> <i class="fa-sharp fa-solid fa-xmark"></i>
                    </button>
                    
                    <div class='bottom'>
                        <p>${title}</p>
                        <h2>$ ${price.toFixed(2)}</h2>
                        <button class='addtocart-button' onclick='event.stopPropagation(); addtocart(${i++})'> Add to cart </button>
                    </div>

                    <div class='top'>
                        <div class='images-side'>
                            <div class='img-box'>
                                <img class='images' src=${image}></img>
                            </div>
                        </div>
                        <div class='item-info' style='display:none;'>
                            <p class='item-desc'>${desc_item}</p><!-- display:block => when box clicked--> 
                            <ul class='item-details'>

                            </ul>
                        </div>

                        <!-- display:block => when box clicked--> 
                    </div>
                </div>
            </div>
            `
        );
    }).join('');

    //------ ---------------displays details as <ul> when box clicked------------------------

    //---------------------back-button effect------------------------

    //---------------displays slider when box clicked----------------
    const item_box = document.querySelectorAll('.box');

    item_box.forEach(box => {

        const back_button = box.querySelector('.back-button');
        const mini_slider=box.querySelector('.images-side');
        
        const item_info=box.querySelector('.item-info');
        const item_details=box.querySelector('.item-details');

        const related = categories[box.dataset['index']]['related'];
        const details = categories[box.dataset['index']]['details'];
        
        box.addEventListener('click', function() {
            //Show hidden elements
            back_button.style.display='flex';
            item_info.style.display='block';
            mini_slider.style.display='flex';
            //Create Slider
            mini_slider.innerHTML='';
            related.forEach(img_path=>{
                const img = document.createElement('img');
                img.classList.add('images');
                img.src=img_path;
                mini_slider.appendChild(img);
            });     


            //Create details <ul>
            for (const [k,v] of Object.entries(details)){

                const li = document.createElement('li');
                li.textContent=`${k}: ${v}`;
                item_details.appendChild(li);
                console.log(item_details);

            };
            //set changes on webpage (it must be final step to make the script work)
            main_grid.classList.add('root_1')
            main_grid.classList.remove('.root')
            main_grid.innerHTML='';
            main_grid.innerHTML=box.innerHTML;

        });

        displaycart();

     });


};
function displaycart(a) {
    let j = 0, total = 0;


    document.getElementById('count').innerHTML = cart.length;

    document.getElementById('total').innerHTML = "$0.00";

    if (cart.length == 0) {
        document.getElementById('cartItem').innerHTML = 'Your cart is empty';
    }
    else {
        document.getElementById('cartItem').innerHTML = cart.map((item) => {

            let image = item['image'], title = item['title'], price = item['price'];
            console.log

            total += price;
            document.getElementById('total').innerHTML = "$" + total.toFixed(2);
            const pay_button = document.querySelector('.pay-button');
            if (total>0){
                pay_button.style.display = 'block';
                }

            return (
                `
                
                <div class='cart-item-container'>
                    <p>${title}</p>
                    <div class='cart-item'>

                        <i class='fa-solid fa-trash'  onclick='delElement(${j++})'></i>
                        <div class='row-info'>
                            <h2>$${price.toFixed(2)}</h2>
                        </div>
                        <div class='row-img'>
                            <img class='rowimg' src=${image}></img>
                        </div>

                    </div>

                </div>


                `

            )
        }).join('');

    }
}
init();

function back_button(){
    main_grid.classList.add('root')
    main_grid.classList.remove('root_1')
    main_grid.innerHTML=copy_main_grid;
    init();

}

function addtocart(a) {
    cart.push({ ...categories[a] });
    localStorage.setItem('cart', JSON.stringify(cart));
    displaycart();
}

function delElement(a) {
    cart.splice(a, 1);
    localStorage.setItem('cart', JSON.stringify(cart));
    displaycart();

}

//-----------------------------------------------------------
//-----------------------------------------------------------
//-----------------------------------------------------------


//---------------------display cart items on side-bar------------------------
let stored_cart = localStorage.getItem('cart');

if (stored_cart) {
    var cart = JSON.parse(stored_cart);
}

else {
    var cart = [];
    localStorage.setItem('cart',cart);
};


//-----------------------------------------------------------
//-----------------------------------------------------------
//-----------------------------------------------------------


//---------------------display cart when button pressed------------------------

const sidebar = document.querySelector('.sidebar');
const main_grid = document.querySelector('.root');
const mark = document.querySelector('#delete-mark');
const addtocart_button = document.querySelector('.cart');

mark.addEventListener('click', function () {
    sidebar.style.display = 'none';

    mark.style.display = 'none';

    main_grid.style.display = 'grid';
    main_grid.style.width = '100%';

});

addtocart_button.addEventListener('click', function () {
    sidebar.style.display = 'grid';
    mark.style.display = 'block';

    main_grid.style.display = 'none';
    sidebar.style.width = '100%';

});


//-----------------------------------------------------------
//-----------------------------------------------------------
//-----------------------------------------------------------

//-----------------------------------------------------------
//-----------------------------------------------------------
//-----------------------------------------------------------

//-----------------------------------------------------------
//-----------------------------------------------------------
//-----------------------------------------------------------



//});

