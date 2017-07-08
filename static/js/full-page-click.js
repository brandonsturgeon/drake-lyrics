$("html").on('click', function() {
  const urlParams = window.location.search;
  $.ajax({
    url: './lyric' + urlParams,
    success: function(result) {
      const lyrics = result.split("\n");
      const lyricsDiv = $(".centered-lyrics");
      lyricsDiv.empty();

      for (let i = 0; i < lyrics.length; i++) {
        lyricsDiv.append(`<p>${lyrics[i]}</p>`);
      }
    }
  });
}); 
