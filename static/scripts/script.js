let cartCount = 0;

const cartButtons = document.querySelectorAll('.add-to-cart');

const cartDisplay = document.querySelector('.login-cart a:nth-child(2)');

let cartItems = [];

cartButtons.forEach(button => {
    button.addEventListener('click', () => {
        const productName = button.closest('.product').querySelector('h2').textContent;

        if (cartItems.some(item => item.name === productName)) {
            return;
        }

        const price = parseFloat(button.getAttribute('data-price'));
        cartItems.push({ name: productName, price: price });

        cartCount++;
        cartDisplay.textContent = `Carrinho (${cartCount})`;
    });
});

function openPopup() {
    document.getElementById('loginPopup').style.display = 'block';
}

function closePopup() {
    document.getElementById('loginPopup').style.display = 'none';
}

window.onclick = function (event) {
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

window.onclick = function (event) {
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

    function addToCart(productName, price) {
        if (cartItems.some(item => item.name === productName)) {
            alert("Você só pode adicionar uma unidade de cada produto.");
            return;
        }

        cartItems.push({ name: productName, price: parseFloat(price) });
        cartCount++;
        cartDisplay.textContent = `Carrinho (${cartCount})`;

        const newItem = document.createElement('li');
        newItem.textContent = `${productName} - ${parseFloat(price).toFixed(2)} BRL`;

        const removeButton = document.createElement('button');
        removeButton.textContent = "X";
        removeButton.className = 'remove-button';
        removeButton.addEventListener('click', function () {
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

    cartButtons.forEach(button => {
        button.addEventListener('click', function () {
            const productName = button.closest('.product').querySelector('h2').textContent;
            const priceText = button.closest('.product').querySelector('.price').textContent;
            const price = priceText.replace(' BRL', '').trim();

            addToCart(productName, price);
        });
    });

    function openCheckoutPopup() {
        document.getElementById('checkoutPopup').style.display = 'block';
        updateTotal();
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
function finalizarCompra() {
    const items = [];
    const totalValue = 0.00;
    const paymentMethod = document.querySelector('input[name="payment"]:checked').value;

    document.querySelectorAll('#orderItems li').forEach(item => {
        if (!item.classList.contains('total')) {
            items.push(item.innerText);
        }
    });

    const data = {
        tipoPagamento: paymentMethod,
        valorPago: totalValue,
    };

    fetch('/finalizarCompra', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(data),
    })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                alert('Compra finalizada com sucesso!');
                closeCheckoutPopup();
            } else {
                alert('Erro ao finalizar a compra.');
            }
        })
        .catch(error => {
            console.error('Erro:', error);
        });
}
function openRegisterPopup() {
    document.getElementById('loginPopup').style.display = 'none';
    document.getElementById('registerPopup').style.display = 'block';
}

function closeRegisterPopup() {
    document.getElementById('registerPopup').style.display = 'none';
    document.getElementById('loginPopup').style.display = 'block';
}
document.getElementById('registerForm').onsubmit = async function (event) {
    event.preventDefault();

    const formData = new FormData(this);

    const response = await fetch('/register', {
        method: 'POST',
        body: formData
    });

    const result = await response.json();

    if (response.ok) {
        alert(result.message);
        closeRegisterPopup();
        openPopup();
    } else {
        alert('Erro ao registrar: ' + result.message);
    }
};
function openPopup() {
    document.getElementById('loginPopup').style.display = 'block';
}

function closePopup() {
    document.getElementById('loginPopup').style.display = 'none';
}

function closeRegisterPopup() {
    document.getElementById('registerPopup').style.display = 'none';
    openPopup();
}

function finalizarCompra() {
    const items = document.querySelectorAll('#orderItems li');
    const produtos = [];

    items.forEach(item => {
        if (!item.classList.contains('total')) {
            produtos.push(item.textContent);
        }
    });

    const pagamento = document.querySelector('input[name="payment"]:checked').value;

    fetch('/finalizar_compra', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ produtos, pagamento }),
    })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                alert('Compra finalizada com sucesso!');
                closeCheckoutPopup();
            } else {
                alert('Erro ao finalizar compra: ' + data.message);
            }
        })
        .catch(error => {
            console.error('Erro:', error);
            alert('Erro ao finalizar compra.');
        });
}
