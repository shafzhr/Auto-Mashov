const puppeteer = require('puppeteer');

(async () => {
    const browser = await puppeteer.launch({headless: false});
    const page = await browser.newPage();
    // await page.setViewport({ width: 1280, height: 800 });
    await page.goto('https://web.mashov.info/students/login', {waitUntil: 'networkidle2'});
    await page.waitForSelector('#mat-input-2');
    console.log('loaded needed content')

    //select school
    await page.type('#mat-input-2', , {delay: 100});
    await page.waitForSelector('#mat-option-136');
    console.log('appeared')
    await page.click('#mat-option-136');

    //select year
    await page.waitForSelector('#mat-input-2');
    console.log('loaded needed content')
    await page.click('#mat-select-0 > div > div.mat-select-value.ng-tns-c131-4 > span');
    await page.click('#mat-select-0 > div > div.mat-select-value.ng-tns-c131-4 > span');

    //type id
    await page.type('#mat-input-0', );

    //type password
    await page.type('#mat-input-1', );

    //press submit
    await page.click('#mat-tab-content-0-0 > div > div > button');

    //wait for navigation
    await page.waitForNavigation({ waitUntil: 'networkidle0' });

    //enter live streaming
    await page.click('#mainView > mat-sidenav-content > mshv-student-dashboard > mat-card > mat-card-content > div.dashboard-header-click.ng-tns-c169-11.ng-star-inserted > mat-card.mat-card.dashboard-red.ng-tns-c169-11');
    console.log("eneterd live streaming")
    //wait for navigation
//        await page.waitForNavigation({ waitUntil: 'networkidle0' });

    await page.waitFor(2000)
        console.log("Finished navigating")


    //enter first lesson
    first_lesson = await page.evaluate(() => {
        element = document.querySelectorAll('#mainView > mat-sidenav-content > mshv-student > mshv-student-bbb > mat-card > mat-nav-list > a')
        console.log(element.innerText)
        return element[0].href
    });
    await page.goto(first_lesson, {waitUntil: 'networkidle2'});
    console.log("went to first lesson")

//    await page.click('#mainView > mat-sidenav-content > mshv-student > mshv-student-bbb > mat-card > mat-nav-list > a > div')



    // console.log(product_price.length)
    const sleep = (milliseconds) => {
      return new Promise(resolve => setTimeout(resolve, milliseconds))
    }

    sleep(50000).then(() => {
      //do stuff
      console.log('waiting')
      browser.close();
    })

})();