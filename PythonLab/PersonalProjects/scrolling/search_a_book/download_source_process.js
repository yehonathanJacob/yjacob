// URL: https://www.e-vrit.co.il/Category/37/%D7%A2%D7%A1%D7%A7%D7%99%D7%9D_%D7%95%D7%A0%D7%99%D7%94%D7%95%D7%9C
window.scrollTo(0, document.body.scrollHeight); // LOOP

before = ".product-div.product-item-container#";
after_for_title = " .product-item .product-container .product-right-details a";
after_for_text = " .product-item .product-container .product-left-details .inner-div-details .tab-content__about-book p";
arr = $('.product-div.product-item-container');
full_data = [];

for (i = 0; i < arr.length; i++) {
    data = {};
    row = arr[i];
    product_id = row.id;
    data['name'] = $(before + product_id + after_for_title)[0].title;
    data['link'] = $(before + product_id + after_for_title)[0].href;
    data['pargraph'] = $(before + product_id + after_for_text).text();
    full_data.push(data);
}

text_output = JSON.stringify(full_data);

function download_file(filename, text) {
    var element = document.createElement('a');
    element.setAttribute('href', 'data:text/plain;charset=utf-8,' + encodeURIComponent(text));
    element.setAttribute('download', filename);

    element.style.display = 'none';
    document.body.appendChild(element);

    element.click();

    document.body.removeChild(element);
}

download_file('source.json', text_output);
