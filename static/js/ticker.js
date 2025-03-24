document.addEventListener("DOMContentLoaded", function () {
  const tickerContent = document.querySelector(".news-ticker .ticker-content");
  if (!tickerContent) return;

  tickerContent.style.whiteSpace = "nowrap";
  tickerContent.style.display = "inline-block";
});
