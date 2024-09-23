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

// Fechar o popup se o usuário clicar fora dele
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
            const priceText = button.closest('.product').querySelector('.price').textContent; // Acessa o preço corretamente
            const price = priceText.replace(' BRL', '').trim(); // Remove ' BRL' e espaços

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
    const items = []; // Coletar itens do carrinho
    const totalValue = 0.00; // Calcular o total real
    const paymentMethod = document.querySelector('input[name="payment"]:checked').value;

    // Exemplo de como coletar os itens do carrinho
    document.querySelectorAll('#orderItems li').forEach(item => {
        if (!item.classList.contains('total')) {
            items.push(item.innerText); // Adapte conforme a estrutura real
        }
    });

    // Montar o objeto de dados para enviar
    const data = {
        tipoPagamento: paymentMethod,
        valorPago: totalValue,
        // Adicione mais dados se necessário
    };

    // Enviar os dados para o servidor
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
                // Fechar o popup e limpar o carrinho
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
    document.getElementById('loginPopup').style.display = 'none';  // Fecha a popup de login
    document.getElementById('registerPopup').style.display = 'block';  // Abre a popup de registro
}

function closeRegisterPopup() {
    document.getElementById('registerPopup').style.display = 'none';  // Fecha a popup de registro
    document.getElementById('loginPopup').style.display = 'block';  // Reabre a popup de login, se necessário
}
document.getElementById('registerForm').onsubmit = async function (event) {
    event.preventDefault();  // Impede o envio padrão do formulário

    const formData = new FormData(this);

    const response = await fetch('/register', {
        method: 'POST',
        body: formData
    });

    const result = await response.json();

    if (response.ok) {
        alert(result.message);  // Exibe uma mensagem de sucesso
        closeRegisterPopup();    // Fecha o popup de registro
        openPopup();             // Abre o popup de login
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
    openPopup();  // Abre o popup de login após fechar o de registro
}

function finalizarCompra() {
    const items = document.querySelectorAll('#orderItems li');
    const produtos = [];

    items.forEach(item => {
        if (!item.classList.contains('total')) {
            produtos.push(item.textContent); // Coleta detalhes do item
        }
    });

    const pagamento = document.querySelector('input[name="payment"]:checked').value; // Obtém método de pagamento

    // Aqui, você deve enviar os dados para o seu backend
    fetch('/finalizar_compra', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ produtos, pagamento }),
    })
        .then(response => response.json())
        .then(data => {
            // Verifique a resposta do servidor
            if (data.success) {
                alert('Compra finalizada com sucesso!');
                closeCheckoutPopup(); // Fecha o popup após a compra
            } else {
                alert('Erro ao finalizar compra: ' + data.message);
            }
        })
        .catch(error => {
            console.error('Erro:', error);
            alert('Erro ao finalizar compra.');
        });
}
