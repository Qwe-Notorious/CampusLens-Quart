  // Получаем все видео с классом hover-video
  var videos = document.querySelectorAll('.hover-video');

  // Добавляем обработчики событий для каждого видео
  videos.forEach(function(video) {
      video.addEventListener('mouseover', function() {
          video.play(); // Воспроизведение видео

      });

      video.addEventListener('mouseout', function() {
          video.pause(); // Приостановить воспроизведение видео
          video.currentTime = 0; // Сбросить время воспроизведения в начало
      });
  });



//                        {% if imgUser %}
//                            <img src="{{ url_for('static', filename=) }}" class="" onerror="this.style.display='none';">`
//                        {% endif %}