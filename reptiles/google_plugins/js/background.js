var is_form_data = true;


chrome.runtime.onMessage.addListener(function(message, sender, sendResponse) {
  if (message.type === 'facebook') {
    // 示例使用 Fetch API 发送 GET 请求
    // 在 background.js 中使用 Fetch API 发送 POST 请求
    fetch('http://127.0.0.1:8000/tool/set_facebook_posts', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ data: message.data })
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json();
    })
    .then(data => {
        console.log(data);
    })
    .catch(error => {
        console.error('Error:', error);
    });

    console.log('Message received in content_script.js:', message.data);
    // 在這裡處理從 inject_script 收到的消息   http://127.0.0.1:8000/tool/post_facebook_data
  }


});

chrome.runtime.onMessage.addListener(function(message, sender, sendResponse) {
  if (message.type === 'facebook_user') {
    // 示例使用 Fetch API 发送 GET 请求
    // 在 background.js 中使用 Fetch API 发送 POST 请求
    fetch('http://127.0.0.1:8000/tool/set_facebook_user', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ data: message.data })
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json();
    })
    .then(data => {
        console.log(data);
    })
    .catch(error => {
        console.error('Error:', error);
    });

    console.log('Message received in content_script.js:', message.data);
    // 在這裡處理從 inject_script 收到的消息   http://127.0.0.1:8000/tool/post_facebook_data
  }

});


//
//chrome.webRequest.onBeforeRequest.addListener(
//  function(details) {
//    if (details.method === 'POST' && details.url === 'https://www.facebook.com/api/graphql/') {
//      if (details.requestBody && details.requestBody.formData) {
//        let formData = details.requestBody.formData;
//        if(is_form_data){
//            is_form_data =false
//            fetch('http://127.0.0.1:8000/tool/post_facebook_secret', {
//                method: 'POST',
//                headers: {
//                    'Content-Type': 'application/json'
//                },
//                body: JSON.stringify({ data: formData })
//            })
//            .then(response => {
//                if (!response.ok) {
//                    throw new Error('Network response was not ok');
//                }
//                return response.json();
//            })
//            .then(data => {
//                console.log(data);
//            })
//            .catch(error => {
//                console.error('Error:', error);
//            });
//
//        }
//        console.log("请求完成，响应数据：", formData);
//      }
//    }
//
//
//  },
//  { urls: ["<all_urls>"] },
//  ['requestBody']
//);




//chrome.runtime.onMessage.addListener(function(message, sender, sendResponse) {
//  if (message.type === 'fb_response') {
//      console.log('Message received from inject.js:', message.data);
//
//    // Handle message from inject.js
//    // You can send a response back to inject.js if needed
//    sendResponse({ received: true });
//  }
//});

// chrome.devtools.network.onRequestFinished.addListener(request => {
//  request.getContent((body) => {
//    if (request.request && request.request.url) {
//      if (request.request.url.includes('facebook.com')) {
//         //continue with custom code
//         var bodyObj = JSON.parse(body);//etc.
//         console.log("POST參數:", bodyObj);
//      }
//}
//});
//});


//chrome.webRequest.onBeforeRequest.addListener(
//  function(details) {
//    if (details.method === 'POST' && details.url === 'https://www.facebook.com/api/graphql/') {
//      console.log("POST參數:", details.url);
//      console.log("POST參數:", details.method);
//      console.log("details", details);
//      if (details.requestBody && details.requestBody.formData) {
//        let formData = details.requestBody.formData;
//        if (formData.fb_api_req_friendly_name && formData.fb_api_req_friendly_name.length>=1) {
//            if (formData.fb_api_req_friendly_name[0] === 'CometNewsFeedPaginationQuery'){
//                console.log("请求完成，响应数据：", details.responseBody);
//            }
//            console.log("fb_api_req_friendly_name:",formData.fb_api_req_friendly_name[0]);
//        }
//
//
//      }
//    }
//  },
//  { urls: ["<all_urls>"] },
//  ['requestBody']
//);


