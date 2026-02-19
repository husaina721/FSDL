
const video = document.getElementById('video');
const timeline = document.getElementById('timeline');


video.addEventListener('loadedmetadata', () => {
  timeline.max = Math.floor(video.duration);
});


video.addEventListener('timeupdate', () => {
  timeline.value = Math.floor(video.currentTime);
  updateTimelineColor();
});


timeline.addEventListener('input', () => {
  video.currentTime = timeline.value;
  updateTimelineColor();
});

function updateTimelineColor() {
  const percentage = (timeline.value / timeline.max) * 100;
  timeline.style.backgroundImage = `linear-gradient(to right, #4caf50 0%, #4caf50 ${percentage}%, #ddd ${percentage}%, #ddd 100%)`;
}
