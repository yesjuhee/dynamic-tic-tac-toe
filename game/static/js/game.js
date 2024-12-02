document.addEventListener("DOMContentLoaded", () => {
  const cells = document.querySelectorAll(".cell");
  const statusText = document.querySelector("#statusText");
  const restartBtn = document.querySelector("#restartBtn");

  let isUserTurn = true;

  function cellClicked(event) {
    if (!isUserTurn) return;

    const cellIndex = event.target.getAttribute("cellIndex");

    fetch(`/game/play/user/${cellIndex}/`)
      .then((response) => response.json())
      .then((data) => {
        updateGame(data);

        if (data.running && data.status_text !== "Invalid move!") {
          isUserTurn = false;
          setTimeout(() => {
            fetch(`/game/play/computer`)
              .then((response) => response.json())
              .then((data) => {
                updateGame(data);
                isUserTurn = true;
              });
          }, 500);
        }
      });
  }

  cells.forEach((cell) => cell.addEventListener("click", cellClicked));

  function updateGame(data) {
    const { game_board, status_text, running } = data;
    statusText.textContent = status_text;

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
