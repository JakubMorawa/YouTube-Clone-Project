// Get the container
const container = document.getElementById("video-container");

// Fetch the JSON data
fetch("youtubeData.json")
  .then(response => response.json())
  .then(videos => {
    videos.forEach(video => {
      const videoCard = document.createElement("div");
videoCard.className = "col-sm-6 col-md-4 col-lg-3"; // responsive sizing
videoCard.innerHTML = `
    <a class="video-card" href="https://www.youtube.com/watch?v=${video.id}" target="_blank" style="text-decoration: none; color: inherit;">
        <div class="video-thumbnail">
            <img src="https://i.ytimg.com/vi/${video.id}/hqdefault.jpg" alt="Video thumbnail" class="img-fluid">
        </div>
        <div class="video-info">
            <h6 class="video-title">${video.title}</h6>
            <p class="video-channel">${video.channel}</p>
            <p class="video-stats">${video.stats}</p>
        </div>
    </a>
`;
container.appendChild(videoCard);
    });
  })
  .catch(error => console.error("Error loading JSON:", error));