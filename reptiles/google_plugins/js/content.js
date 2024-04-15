var fileUrl = chrome.runtime.getURL('js/inject.js');
var s = document.createElement('script')
s.type = 'text/javascript'
s.src = fileUrl
document.documentElement.appendChild(s)
window.addEventListener("message", function(event) {
    // 确保消息来自预期的来源
    if (event.source === window) {
        // 检查消息中的内容，例如是否包含特定字段 'url' 和 'response'
        if (event.data && event.data.url && event.data.response) {
           if (event.data.request.includes('fb_api_req_friendly_name=ProfileCometTimelineFeedRefetchQuery')){
                chrome.runtime.sendMessage({ type: 'facebook', data: event.data.response });
           }
           if (event.data.request.includes('fb_api_req_friendly_name=CometSearchBootstrapKeywordsDataSourceQuery')||event.data.request.includes('fb_api_req_friendly_name=ProfileCometAppCollectionListRendererPaginationQuery')){
                chrome.runtime.sendMessage({ type: 'facebook_user', data: event.data.response });
           }



        }
    }
});
