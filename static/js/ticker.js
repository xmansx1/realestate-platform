document.addEventListener("DOMContentLoaded", function () {
    const tickerContent = document.querySelector(".news-ticker .ticker-content");
    if (!tickerContent) return;
  
    tickerContent.style.animation = "scroll-left 20s linear infinite";
    tickerContent.style.whiteSpace = "nowrap";
    tickerContent.style.display = "inline-block";
  });
  