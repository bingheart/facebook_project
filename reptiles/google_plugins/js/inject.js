function createInterceptor() {
  let originalXHR = window.XMLHttpRequest;
  function MyXHR() {
    let xhr = new originalXHR();

    // 保存原始的 open 方法
    let originalOpen = xhr.open;
    // 保存原始的 send 方法
    let originalSend = xhr.send;

    // 重写 open 方法
    xhr.open = function(method, url) {
      this._url = url; // 保存请求链接
      this._method = method; // 保存请求类型
      return originalOpen.apply(this, arguments);
    };

    // 重写 send 方法
    xhr.send = function(data) {
      this._request = data; // 保存提交的 Form Data
      this.addEventListener("load", function() {
        if (this._url === '/api/graphql/' && this._method.toLowerCase() === 'post') {
            window.postMessage({'url': this._url, "response": this.response,"request":this._request}, '*');
//          if (this._request.includes('fb_api_req_friendly_name=CometNewsFeedPaginationQuery') || this._request.includes('fb_api_req_friendly_name=ProfileCometTimelineFeedRefetchQuery') ||
//          this._request.includes('fb_api_req_friendly_name=ProfileCometAppCollectionListRendererPaginationQuery')) {
//              window.postMessage({'url': this._url, "response": this.response,"request":this._request}, '*');
//          }
           //if (this._request.includes('fb_api_req_friendly_name=CometNewsFeedPaginationQuery') || this._request.includes('fb_api_req_friendly_name=ProfileCometTimelineFeedRefetchQuery') ||
           //this._request.includes('fb_api_req_friendly_name=ProfileCometAppCollectionListRendererPaginationQuery'))
        }
      });
       return originalSend.apply(this, arguments);
    };

    return xhr;
  }

  // 重写 window.XMLHttpRequest
  window.XMLHttpRequest = MyXHR;
}


createInterceptor();
