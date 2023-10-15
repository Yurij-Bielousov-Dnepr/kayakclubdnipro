function createNewSheet(templateSheet) {
  // Get the current date.
  var date = new Date();

  // Create a new sheet.
  var newSheet = SpreadsheetApp.getActive().insertSheet();

  // Set the name of the new sheet to the current date.
  newSheet.setName(date.toLocaleDateString());

  // Copy the template sheet to the new sheet.
  templateSheet.copyTo(newSheet, {
    startRow: 1,
    endRow: templateSheet.getLastRow()
  });

  // Return the new sheet.
  return newSheet;
}
function addWeatherWidget() {
// Get the current weather for Dnipro, Ukraine.
var weather = Utilities.getWeather("Dnipro, Ukraine");

// Create a new HTML element for the weather widget.
var widget = document.createElement("div");
widget.className = "weather-widget";

// Add the weather information to the widget.
widget.innerHTML = "<h1>" + weather.temperatureCelsius + "°C</h1><p>" + weather.description + "</p>";

// Add the widget to the document.
document.body.appendChild(widget);
}
function createApp() {
  // Створити новий елемент HTML для додатка.
  var app = document.createElement("div");
  app.className = "app";

  // Створити новий елемент смуги вкладок для додатка.
  var tabBar = document.createElement("ul");
  tabBar.className = "tab-bar";

  // Створити нову вкладку для кожної сторінки додатка.
  var priceTab = document.createElement("li");
  priceTab.className = "tab";
  priceTab.innerHTML = "Ціни";

  var bookingTab = document.createElement("li");
  bookingTab.className = "tab";
  bookingTab.innerHTML = "Бронювання";

  var equipmentTab = document.createElement("li");
  equipmentTab.className = "tab";
  equipmentTab.innerHTML = "Обладнання";

  var eventsTab = document.createElement("li");
  eventsTab.className = "tab";
  eventsTab.innerHTML = "Заходи";

  var weatherTab = document.createElement("li");
  weatherTab.className = "tab";
  weatherTab.innerHTML = "Погода";

  // Додати вкладки до смуги вкладок.
  tabBar.appendChild(priceTab);
  tabBar.appendChild(bookingTab);
  tabBar.appendChild(equipmentTab);
  tabBar.appendChild(eventsTab);
  tabBar.appendChild(weatherTab);

  // Додати смугу вкладок до додатка.
  app.appendChild(tabBar);

  // Створити нову сторінку для кожної вкладки додатка.
  var pricePage = document.createElement("div");
  pricePage.className = "page";
  pricePage.innerHTML = "Ціни";

  var bookingPage = document.createElement("div");
  bookingPage.className = "page";
  bookingPage.innerHTML = "Бронювання";

  var equipmentPage = document.createElement("div");
  equipmentPage.className = "page";
  equipmentPage.innerHTML = "Обладнання";

  var eventsPage = document.createElement("div");
  eventsPage.className = "page";
  eventsPage.innerHTML = "Заходи";

  var weatherPage = document.createElement("div");
  weatherPage.className = "page";
  weatherPage.innerHTML = "Погода";

  // Додати сторінки до додатка.
  app.appendChild(pricePage);
  app.appendChild(bookingPage);
  app.appendChild(equipmentPage);
  app.appendChild(eventsPage);
  app.appendChild(weatherPage);

  // Встановити активну вкладку на вкладку цін.
  tabBar.querySelector(".tab.price").classList.add("active");
  function createPriceTable() {
// Get the price data from the table.
const priceData = document.querySelector("table").rows;

// Create a new table.
const priceTable = document.createElement("table");

// Add the header row to the table.
const headerRow = document.createElement("tr");
headerRow.appendChild(document.createElement("th"))
headerRow.appendChild(document.createTextNode("Capacity"));
priceTable.appendChild(headerRow);

// Add the body rows to the table.
for (let i = 0; i < priceData.length; i++) {
const row = priceData[i];

// Add a new row to the table.
const bodyRow = document.createElement("tr");
priceTable.appendChild(bodyRow);

// Add the capacity column to the row.
const capacityColumn = document.createElement("td");
capacityColumn.appendChild(document.createTextNode(row.querySelector("td.capacity").textContent));
bodyRow.appendChild(capacityColumn);

// Add the price column to the row.
const priceColumn = document.createElement("td");
priceColumn.appendChild(document.createTextNode(row.querySelector("td.price").textContent));
bodyRow.appendChild(priceColumn);
}

// Return the table.
return priceTable;
}

  // Повернути додаток.
  return app;
}