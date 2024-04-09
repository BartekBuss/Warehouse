
async function fetchProducts() {
    try {
        const response = await fetch('/api/products');
        const products = await response.json();
        displayProducts(products);
    } catch (error) {
        console.error('Błąd pobierania produktów:', error);
    }
}

async function addProduct() {
    const productName = document.getElementById('productName').value;
    const productQuantity = parseInt(document.getElementById('productQuantity').value);
    const productPrice = parseFloat(document.getElementById('productPrice').value);
    const productType = document.getElementById('productType').value;

    if (productName && !isNaN(productQuantity) && productQuantity > 0 && !isNaN(productPrice) && productPrice > 0) {
        try {
            const response = await fetch('/api/products', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    name: productName,
                    quantity: productQuantity,
                    price: productPrice,
                    type: productType
                })
            });
            fetchProducts();
            document.getElementById('productName').value = '';
            document.getElementById('productQuantity').value = '';
            document.getElementById('productPrice').value = '';
            document.getElementById('productType').value = '';
        } catch (error) {
            console.error('Błąd dodawania produktu:', error);
        }
    }
}

async function deleteProduct(id) {
    try {
        await fetch(`/api/products/${id}`, {
            method: 'DELETE'
            
        });
        fetchProducts();
    } catch (error) {
        console.error('Błąd usuwania produktu:', error);
    }
}

async function modifyProduct(id) {
    const newQuantity = parseInt(prompt('Podaj nową ilość produktu:'));
    const newPrice = parseFloat(prompt('Podaj nową cenę produktu:'));
    const newType = prompt('Podaj nowy typ produktu:');

    if (!isNaN(newQuantity) && newQuantity >= 0 && !isNaN(newPrice) && newPrice > 0 && newType.trim() !== '') {
        try {
            await fetch(`/api/products/${id}`, {
                method: 'PUT',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ quantity: newQuantity, price: newPrice, type: newType })
            });
            fetchProducts();
        } catch (error) {
            console.error('Błąd modyfikacji produktu:', error);
        }
    } else {
        alert('Podaj poprawną ilość i cenę produktu.');
    }
}

function displayProducts(products) {
    const productList = document.getElementById('productList');
    productList.innerHTML = '';
    products.forEach(product => {
        const li = document.createElement('li');
        li.innerHTML = `
            <span>${product.name} - ${product.quantity} - ${product.price } - ${product.type}</span>
            <div class="button-container">
                <button class="modifyButton" onclick="deleteProduct(${product.id})">Usuń</button>
                <button class="modifyButton" onclick="modifyProduct(${product.id})">Edytuj</button>
            </div>
        `;
        productList.appendChild(li);
    });
}


async function checkUser() {

        var login = document.getElementById('loginInput').value;
        var password = document.getElementById('passwordInput').value;

        try {
            const response = await fetch('api/users/?login=' + encodeURIComponent(login) + '&password=' + encodeURIComponent(password));
            if (!response.ok) {
                throw new Error('Błąd połączenia');
            }
            const data = await response.json();

            //nie działa gówno lokalnie
            window.location.href = "warehouse.html"

        } catch (error) {
            console.error('Error:', error);
            alert("Zły login lub hasło");
        }
}


document.addEventListener('DOMContentLoaded', function() {
    const loginButton = document.getElementById('loginButton');
    if(loginButton) {
        loginButton.addEventListener('click', function() {
            checkUser();
        });
    }
});


window.onload = function () {
    fetchProducts();
};
