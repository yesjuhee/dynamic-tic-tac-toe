document.addEventListener("DOMContentLoaded", () => {
    const cells = document.querySelectorAll(".cell");
    const statusText = document.querySelector("#statusText");
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
  
      game_board.forEach((value, index) => {
        const cell = cells[index];
        if (value !== "O" && value !== "X" && value !== "") {
          value = value * 100; // 100% 기준
          value = Math.floor(value); // 정수 변환
          cell.textContent = value + "%";

          if (value <= 20) {
            cell.style.backgroundColor = "#ff4d4d"; // Light red
            cell.style.color = "white";
          } else if (value >= 80) {
            cell.style.backgroundColor = "#4d79ff"; // Light blue
            cell.style.color = "white";
          } else {
            cell.style.backgroundColor = "#d3d3d3"; // Light gray
            cell.style.color = "black";
          }
        } else {
          cell.textContent = value;
          cell.style.backgroundColor = "#31d47d"; // Default green
          cell.style.color = "white";
        }
      });
  
      if (!running) {
        cells.forEach((cell) => cell.removeEventListener("click", cellClicked));
      }
    }
  
    restartBtn.addEventListener("click", () => {
      location.reload();
    });
  });
