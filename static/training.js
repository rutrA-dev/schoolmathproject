// ================= DOM =================
const answerInput = document.querySelector("input[type='text']");
const checkBtn = document.getElementById("check-btn");
const nextBtn = document.getElementById("next-btn");
const finishBtn = document.getElementById("finish-btn");

const resultDiv = document.querySelector(".result");
const taskDiv = document.querySelector(".task");

const timeSpan = document.getElementById("time");
const solvedSpan = document.getElementById("solved");
const totalSpan = document.getElementById("total");
const accuracySpan = document.getElementById("accuracy");

// ================= STATE =================
let total = 0;
let solved = 0;
let startTime = Date.now();
let checked = false;
let trainingFinished = false;

// ================= INITIAL UI =================
nextBtn.disabled = true;

// ================= TIMER =================
function updateTimer() {
    if (trainingFinished) return;

    const elapsed = Math.floor((Date.now() - startTime) / 1000);
    const min = String(Math.floor(elapsed / 60)).padStart(2, "0");
    const sec = String(elapsed % 60).padStart(2, "0");
    timeSpan.textContent = `${min}:${sec}`;
}
setInterval(updateTimer, 1000);

// ================= WARNING =================
window.addEventListener("beforeunload", (e) => {
    if (trainingFinished) return;
    e.preventDefault();
    e.returnValue = "Вы точно хотите прервать сессию?";
});

// ================= CHECK ANSWER =================
checkBtn.addEventListener("click", checkAnswer);

function checkAnswer() {
    if (checked) return;

    const answer = answerInput.value.trim();
    if (!answer) return;

    fetch("/check_answer", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ answer })
    })
    .then(res => {
        if (!res.ok) throw new Error();
        return res.json();
    })
    .then(data => {
        checked = true;
        total++;

        if (data.correct) {
            solved++;
            resultDiv.textContent = "✔ Верно";
            resultDiv.className = "result correct";
        } else {
            resultDiv.textContent =
                "✖ Неверно. Правильные ответы: " +
                data.correct_answers.join(", ");
            resultDiv.className = "result wrong";
        }

        solvedSpan.textContent = solved;
        totalSpan.textContent = total;
        accuracySpan.textContent =
            Math.round((solved / total) * 100) + "%";

        nextBtn.disabled = false;
    })
    .catch(() => {
        resultDiv.textContent = "Ошибка проверки";
        resultDiv.className = "result wrong";
    });
}

// ================= NEXT TASK =================
nextBtn.addEventListener("click", nextTask);

function nextTask() {
    if (!checked) return;

    fetch("/next_task")
        .then(res => {
            if (!res.ok) throw new Error();
            return res.json();
        })
        .then(data => {
            taskDiv.innerHTML = data.question_latex;
            renderMathInElement(taskDiv);

            answerInput.value = "";
            resultDiv.textContent = "";
            resultDiv.className = "result";

            checked = false;
            nextBtn.disabled = true;
        });
}

// ================= FINISH TRAINING =================
finishBtn.addEventListener("click", finishTraining);

function finishTraining() {
    const ok = confirm("Вы действительно хотите завершить тренировку?");
    if (!ok) return;

    trainingFinished = true;

    // отключаем предупреждение
    window.onbeforeunload = null;

    window.location.href = "/finish_training";
}

// ================= INITIAL SYNC =================
fetch("/training_state")
    .then(res => res.json())
    .then(data => {
        if (!data.active) return;

        total = data.stats.total;
        solved = data.stats.correct;
        startTime = data.started_at * 1000;

        solvedSpan.textContent = solved;
        totalSpan.textContent = total;

        const acc = total === 0
            ? 0
            : Math.round((solved / total) * 100);
        accuracySpan.textContent = acc + "%";
    });
