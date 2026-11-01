// JENA FASHION - Website interactions

// 1. Mobile navigation menu
const menuToggle = document.getElementById("menuToggle");
const navigation = document.querySelector(".navigation");

if (menuToggle && navigation) {
    menuToggle.addEventListener("click", function () {
        navigation.classList.toggle("open");
    });

    // Close the mobile menu after clicking a navigation link
    navigation.querySelectorAll("a").forEach(function (link) {
        link.addEventListener("click", function () {
            navigation.classList.remove("open");
        });
    });
}

// 2. Simple shopping bag demonstration
let shoppingBag = [];

const cartMessage = document.getElementById("cartMessage");
const addButtons = document.querySelectorAll(".add-button");

addButtons.forEach(function (button) {
    button.addEventListener("click", function () {
        const productName = button.dataset.name;
        const productPrice = Number(button.dataset.price);

        shoppingBag.push({
            name: productName,
            price: productPrice
        });

        updateShoppingBag();
    });
});

function updateShoppingBag() {
    if (!cartMessage) return;

    const totalItems = shoppingBag.length;
    const totalPrice = shoppingBag.reduce(function (total, item) {
        return total + item.price;
    }, 0);

    cartMessage.textContent =
        "Shopping bag: " + totalItems +
        (totalItems === 1 ? " item" : " items") +
        " | Total: ₹" + totalPrice.toLocaleString("en-IN");
}

// JENA FASHION - Product Search

const searchForm = document.getElementById("searchForm");
const productSearch = document.getElementById("productSearch");
const searchMessage = document.getElementById("searchMessage");

if (searchForm && productSearch && searchMessage) {

    searchForm.addEventListener("submit", function (event) {
        event.preventDefault();

        const searchText = productSearch.value
            .trim()
            .toLowerCase();

        const products = document.querySelectorAll(".product-card");

        let visibleCount = 0;

        products.forEach(function (product) {
            const productName = product.textContent.toLowerCase();

            const matches = productName.includes(searchText);

            product.style.display = matches ? "" : "none";

            if (matches) {
                visibleCount++;
            }
        });

        if (searchText === "") {
            searchMessage.textContent = "Showing all products.";
        } else if (visibleCount > 0) {
            searchMessage.textContent =
                visibleCount + " product(s) found.";
        } else {
            searchMessage.textContent =
                "No products found. Try another search.";
        }
    });

    productSearch.addEventListener("input", function () {
        if (productSearch.value.trim() === "") {
            document.querySelectorAll(".product-card").forEach(
                function (product) {
                    product.style.display = "";
                }
            );

            searchMessage.textContent = "";
        }
    });
}