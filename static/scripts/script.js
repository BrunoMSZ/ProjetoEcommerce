// Inicializando a contagem de itens no carrinho
let cartCount = 0;

// Selecionando todos os botões "CARRINHO" de produtos
const cartButtons = document.querySelectorAll('.add-to-cart');

// Selecionando o elemento do carrinho na navbar
const cartDisplay = document.querySelector('.login-cart a:nth-child(2)');

// Array para armazenar os itens do carrinho
let cartItems = [];

// Adicionando evento de clique a cada botão "CARRINHO"
cartButtons.forEach(button => {
    button.addEventListener('click', () => {
        const productName = button.closest('.product').querySelector('h2').textContent;

        // Verifica se o produto já foi adicionado ao carrinho
        if (cartItems.some(item => item.name === productName)) {
            return;
        }

        // Adiciona o produto ao carrinho
        const price = parseFloat(button.getAttribute('data-price'));
        cartItems.push({ name: productName, price: price });

        cartCount++; // Incrementa o número de itens no carrinho
        cartDisplay.textContent = `Carrinho (${cartCount})`; // Atualiza o display do carrinho
    });
});

function openPopup() {
    document.getElementById('loginPopup').style.display = 'block';
}

function closePopup() {
    document.getElementById('loginPopup').style.display = 'none';
}

// Fechar o popup se o usuário clicar fora dele
window.onclick = function(event) {
    if (event.target == document.getElementById('loginPopup')) {
        closePopup();
    }
}

function openCheckoutPopup() {
    document.getElementById('checkoutPopup').style.display = 'block';
}

function closeCheckoutPopup() {
    document.getElementById('checkoutPopup').style.display = 'none';
}

// Fechar o popup se o usuário clicar fora dele
window.onclick = function(event) {
    if (event.target == document.getElementById('checkoutPopup')) {
        closeCheckoutPopup();
    }
}

document.addEventListener('DOMContentLoaded', function () {
    let cartCount = 0;
    const cartButtons = document.querySelectorAll('.add-to-cart');
    const cartDisplay = document.querySelector('.login-cart a:nth-child(2)');
    let cartItems = [];
    const orderItemsList = document.getElementById('orderItems');
    const totalElement = document.querySelector('.total');

    function updateTotal() {
        let total = cartItems.reduce((acc, item) => acc + item.price, 0);
        totalElement.textContent = `Total: ${total.toFixed(2)} BRL`;
    }

    function addToCart(event) {
        const productName = event.target.closest('.product').querySelector('h2').textContent;
        const price = parseFloat(event.target.getAttribute('data-price'));

        if (cartItems.some(item => item.name === productName)) {
            alert("Você só pode adicionar uma unidade de cada produto.");
            return;
        }

        cartItems.push({ name: productName, price: price });
        cartCount++;
        cartDisplay.textContent = `Carrinho (${cartCount})`;

        const newItem = document.createElement('li');
        newItem.textContent = `${productName} - ${price.toFixed(2)} BRL`;

        const removeButton = document.createElement('button');
        removeButton.textContent = "X";
        removeButton.className = 'remove-button';
        removeButton.addEventListener('click', function() {
            removeFromCart(productName, newItem);
        });

        newItem.appendChild(removeButton);
        orderItemsList.insertBefore(newItem, totalElement);

        updateTotal();
    }

    function removeFromCart(productName, itemElement) {
        cartItems = cartItems.filter(item => item.name !== productName);
        orderItemsList.removeChild(itemElement);
        cartCount--;
        cartDisplay.textContent = `Carrinho (${cartCount})`;
        updateTotal();
    }

    cartButtons.forEach(button => button.addEventListener('click', addToCart));

    function openCheckoutPopup() {
        document.getElementById('checkoutPopup').style.display = 'block';
    }

    function closeCheckoutPopup() {
        document.getElementById('checkoutPopup').style.display = 'none';
    }

    document.querySelector('.login-cart a:nth-child(2)').onclick = openCheckoutPopup;
    document.querySelector('.checkout-close').onclick = closeCheckoutPopup;

    window.onclick = function (event) {
        if (event.target == document.getElementById('checkoutPopup')) {
            closeCheckoutPopup();
        }
    }
});
