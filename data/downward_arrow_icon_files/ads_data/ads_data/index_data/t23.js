/* TUNNEL23.COM - 2020-07 - Gregor Gullberg*/
function enablerInitHandler(){new T23Dynamic}document.addEventListener("DOMContentLoaded",function(){"undefined"==typeof Enabler?enablerInitHandler():Enabler.addEventListener(studio.events.StudioEvent.INIT,enablerInitHandler)},!1),function(){function t(){if(console.log("starting banner",this.bannerLoopCount),1<this.bannerLoopCount&&(this.creative.style.display="none",n(this.cta,"in"),n(this.bg,"in"),n(this.headline,"in"),n(this.headline,"out"),n(this.headline_logo,"in"),n(this.logo_product,"in"),n(this.copyline,"in"),this.hasVideoBg&&n(this.video,"animate")),this.creative.style.display="block",this.hasVideoBg&&o(this.video,"animate"),setTimeout(function(){o(this.bg,"in")}.bind(this),500),setTimeout(function(){o(this.headline,"in"),o(this.cta,"in")}.bind(this),1200),this.hasVideoBg)var e=1e3;else e=2500;setTimeout(function(){o(this.headline,"out")}.bind(this),e+700+500),setTimeout(function(){o(this.headline_logo,"in"),o(this.logo_product,"in")}.bind(this),500+e+700+500),setTimeout(function(){o(this.copyline,"in")}.bind(this),1e3+e+700+500),this.bannerLoopCount<this.bannerLoopMax&&setTimeout(function(){this.bannerLoopCount++,t.call(this)}.bind(this),15e3)}function e(e){return e.preventDefault(),Enabler.exitOverride("clicktag",this.href),!1}function s(){this.preloadImages.length==this.imagesLoaded_done&&this.preloadVideos.length==this.videosLoaded_done&&t.call(this)}function i(e){void 0!==e&&e.preventDefault(),function(e,t){e.classList.contains(t)?n(e,t):o(e,t)}(this.settings.rechtstext,"opened")}function n(e,t){t=" "+(t=t.trim()),e.className=e.className.replace(t,"")}function o(e,t){t=" "+(t=t.trim()),e.className.includes(t)||(e.className=e.className+t)}this.T23Dynamic=function(){this.creative=document.querySelector("#T23Dynamic"),this.settings={},this.settings.rechtstext=".rechtstext",this.settings.feed="Magenta_dynamic_Creatives__MAB_AlwaysOn_2020_NAE",this.settings.feed_numbers=1,this.content_all="undefined"!=typeof dynamicContent?dynamicContent[this.settings.feed]:devDynamicContent[this.settings.feed],this.bannerLoop=!0,this.bannerLoopCount=1,this.bannerLoopMax=2,this.preloadImages=[],this.preloadVideos=[],this.imagesLoaded=0,this.videosLoaded=0,this.imagesLoaded_done=0,this.videosLoaded_done=0,function(){this.headline=this.creative.querySelector(".headline"),this.copyline=this.creative.querySelector(".copyline"),this.cta=this.creative.querySelector(".cta"),this.bg=this.creative.querySelector(".bg"),this.headline_logo=this.creative.querySelector(".logo"),this.logo_product=this.creative.querySelector(".logo-product"),0!=this.settings.rechtstext&&(this.rtxt_text=this.creative.querySelector(".rtxt"),this.settings.rechtstext=this.creative.querySelector(this.settings.rechtstext),this.settings.rechtstext.querySelector(".btn-info-open").addEventListener("click",i.bind(this),!1),this.settings.rechtstext.querySelector(".btn-info-close").addEventListener("click",i.bind(this),!1),this.settings.rechtstext.querySelector(".rtxt").addEventListener("click",i.bind(this),!1));"undefined"!=typeof Enabler&&(this.clicktag=this.creative.querySelector("#clicktag"),this.clicktag.addEventListener("click",e));"undefined"!=typeof dynamicContent||"undefined"!=typeof devDynamicContent?function(){console.log("setDynamicContent");for(var e=0;e<this.settings.feed_numbers;e++){this.content=this.content_all[e],this.clicktag.setAttribute("href",this.content.clicktag.Url),this.cta.innerText=this.content.cta;var t=this.content.hintergrund.Url;t.endsWith("empty.png")?(this.hasVideoBg=!1,this.bg.innerHTML='<img class="bg-image" src="">',this.preloadImages.push({domElement:this.bg.querySelector(".bg-image"),src:this.content.hintergrund_still.Url,complete:!1})):(this.hasVideoBg=!0,this.bg.innerHTML='<div class="spriteplayer" style="background-image: url('+t+')">',this.video=this.bg.querySelector(".spriteplayer"),this.preloadImages.push({domElement:this.bg.querySelector(".spriteplayer"),src:this.content.hintergrund.Url,complete:!1})),this.preloadImages.push({domElement:this.headline_logo,src:this.content.headline_logo.Url,complete:!1});var i=this.content.headline;i=i.replace(/\n/g,"<br>"),this.headline.innerHTML=i;var n=this.content.subline;n=n.replace(/\n/g,"<br>"),this.copyline.innerHTML=n;var s=this.content.rechtstext;s=s.replace(/\n/g,"<br>"),this.rtxt_text.innerHTML=s}}.call(this):console.error("error: no content source");0<this.preloadImages.length||0<this.preloadVideos.length?function(){console.log("images to load:",this.preloadImages.length),console.log("videos to load:",this.preloadVideos.length),0<this.preloadImages.length&&function e(){var t=this;var i=this.preloadImages[this.imagesLoaded].src;var n=new Image;n.onload=function(){t.preloadImages[t.imagesLoaded].domElement.src=i,t.imagesLoaded++,t.imagesLoaded_done++,t.preloadImages.length==t.imagesLoaded?s.call(t):e.call(t)};n.src=i}.call(this);0<this.preloadVideos.length&&function(){for(this.videosLoaded;this.videosLoaded<this.preloadVideos.length;this.videosLoaded++){var e=this.preloadVideos[this.videosLoaded].domElement;e.addEventListener("canplay",function(){this.videosLoaded_done++,s.call(this)}.bind(this)),e.src=this.preloadVideos[this.videosLoaded].src}}.call(this)}.call(this):t.call(this)}.call(this)},String.prototype.endsWith||(String.prototype.endsWith=function(e,t){return(void 0===t||t>this.length)&&(t=this.length),this.substring(t-e.length,t)===e}),String.prototype.includes||(String.prototype.includes=function(e,t){"use strict";if(e instanceof RegExp)throw TypeError("first argument must not be a RegExp");return void 0===t&&(t=0),-1!==this.indexOf(e,t)})}();