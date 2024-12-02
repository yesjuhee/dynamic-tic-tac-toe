document.addEventListener("DOMContentLoaded", () => {
    const cells = document.querySelectorAll(".cell");
    const statusText = document.querySelector("#statusText");
    const analyses = document.querySelector("#analyses");
    const restartBtn = document.querySelector("#restartBtn");
    const undoBtn = document.querySelector("#undoBtn");
    const redoBtn = document.querySelector("#redoBtn");
  
  
    function cellClicked(event) {
        const cellIndex = event.target.getAttribute("cellIndex");
  
        fetch(`/game/play/practice/${cellIndex}/`)
        .then((response) => response.json())
        .then((data) => {
            updateGame(data);
        });
    }

    function undoMove() {
        fetch(`/game/play/practice/undo`)
        .then((response) => response.json())
        .then((data) => {
            updateGame(data);
        });
    }

    function redoMove() {
        fetch(`/game/play/practice/redo`)
            .then((response) => response.json())
            .then((data) => {
            updateGame(data);
       });
     }


    cells.forEach((cell) => cell.addEventListener("click", cellClicked));
    undoBtn.addEventListener("click", undoMove);
    redoBtn.addEventListener("click", redoMove);
  
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
