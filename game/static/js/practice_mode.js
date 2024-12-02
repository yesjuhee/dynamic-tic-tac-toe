document.addEventListener("DOMContentLoaded", () => {
    const cells = document.querySelectorAll(".cell");
    const statusText = document.querySelector("#statusText");
    const analyses = document.querySelector("#analyses");
    const restartBtn = document.querySelector("#restartBtn");
  
  
    function cellClicked(event) {
      const cellIndex = event.target.getAttribute("cellIndex");
  
      fetch(`/game/play/practice/${cellIndex}/`)
        .then((response) => response.json())
        .then((data) => {
          updateGame(data);
        });
    }
  
    cells.forEach((cell) => cell.addEventListener("click", cellClicked));
  
    function updateGame(data) {
      const { game_board, status_text, running, comment } = data;
      statusText.textContent = status_text;
      analyses.textContent = comment;
  
      game_board.forEach((value, index) => {
        cells[index].textContent = value;
      });
  
      if (!running) {
        cells.forEach((cell) => cell.removeEventListener("click", cellClicked));
      }
    }
  
    restartBtn.addEventListener("click", () => {
      location.reload();
    });
  });
  