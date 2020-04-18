const puppeteer = require('puppeteer');

(async () => {
    const browser = await puppeteer.launch({headless: false});
    const page = await browser.newPage();
    // await page.setViewport({ width: 1280, height: 800 });
    await page.goto('https://web.mashov.info/students/login', {waitUntil: 'networkidle2'});
    await page.waitForSelector('#mat-input-2');
    console.log('loaded needed content')

//    school = document.querySelector('#mat-input-2');
    await page.$eval('#mat-input-2', el => el.value = '444117');




    for(row of rows){
        for(child of row){
            console.log(child.innerText)
        }
    }
    // console.log(product_price.length)


    await browser.close();
})();