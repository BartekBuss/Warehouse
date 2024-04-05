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

    if (productName && !isNaN(productQuantity) && productQuantity > 0) {
        try {
            const response = await fetch('/api/products', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    name: productName,
                    quantity: productQuantity
                })
            });
            fetchProducts(); // Fetch and display products after adding
            document.getElementById('productName').value = '';
            document.getElementById('productQuantity').value = '';
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
        fetchProducts(); // Fetch and display products after deletion
    } catch (error) {
        console.error('Błąd usuwania produktu:', error);
    }
}

async function modifyProduct(id) {
    const newQuantity = parseInt(prompt('Podaj nową ilość produktu:'));
    if (!isNaN(newQuantity) && newQuantity >= 0) {
        try {
            await fetch(`/api/products/${id}`, {
                method: 'PUT',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ quantity: newQuantity })
            });
            fetchProducts(); // Fetch and display products after modification
        } catch (error) {
            console.error('Błąd modyfikacji produktu:', error);
        }
    } else {
        alert('Podaj poprawną ilość produktu.');
    }
}

function displayProducts(products) {
    const productList = document.getElementById('productList');
    productList.innerHTML = '';
    products.forEach(product => {
        const li = document.createElement('li');
        li.innerHTML = `
            <span>${product.name} - ${product.quantity}</span>
            <div>
                <button onclick="deleteProduct(${product.id})">Usuń</button>
                <button onclick="modifyProduct(${product.id})">Modyfikuj</button>
            </div>
        `;
        productList.appendChild(li);
    });
}

window.onload = function () {
    fetchProducts();
};