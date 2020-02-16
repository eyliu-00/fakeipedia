
function updateImage(input)
{
  if (localStorage["image"])
  {
      document.getElementById('article-pic').src = localStorage["image"];
  }
}

function chooseFile() {
  document.getElementById("fileInput").click();
}
