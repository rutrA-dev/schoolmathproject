from flask import Flask, render_template, request, jsonify, session, redirect
from mathgenerator import eq_generator, parse_user_answers, parse_correct_answers
import time
app = Flask(__name__)
app.secret_key = "dev-secret-key" 


@app.route("/")
def main_page():
    return render_template('mainpage.html')

@app.route("/select")
def select():
    return render_template("eq_select.html")


@app.route("/start_training")
def start_training():
    eqType = request.args.get("type")
    difficulty = request.args.get("difficulty")
    if difficulty != "random": difficulty = int(request.args.get("difficulty"))
    t = session.get("training")
    # 🔥 если пользователь сознательно стартует — сбрасываем
    session.pop("training", None)

    data = eq_generator(eqType, difficulty)
    if t:
        while data["question_latex"] == t["current_task"]["question_latex"]: data = eq_generator(eqType, difficulty)

    session["training"] = {
        "meta": {
            "type_code": eqType,
            "difficulty": difficulty,
            "started_at": int(time.time())
        },
        "stats": {
            "total": 0,
            "correct": 0
        },
        "current_task": {
            "question_latex": data["question_latex"],
            "answers": data["answers"],
            "type": data["type"],
            "type_russian": data["type_russian"],
            "complexity": data["complexity"],
            "difficulty": data["difficulty"]
        },
        "history": []
    }

    return render_template(
        "training.html",
        eq_question=data["question_latex"],
        eq_type_russian=data["type_russian"],
        eq_complexity=data["complexity"],
        eq_difficulty=data["difficulty"]
    )




@app.route("/next_task")
def next_task():
    t = session.get("training")
    if not t:
        return jsonify({"error": "no active session"}), 400

    data = eq_generator(
        t["meta"]["type_code"],
        t["meta"]["difficulty"]
    )

    t["current_task"] = {
        "question_latex": data["question_latex"],
        "answers": data["answers"],
        "type": data["type"],
        "type_russian": data["type_russian"],
        "complexity": data["complexity"],
        "difficulty": data["difficulty"],
        "started_at": int(time.time())
    }

    session.modified = True

    return jsonify({
        "question_latex": data["question_latex"],
        "answers": data["answers"]
    })


@app.route("/check_answer", methods=["POST"])
def check_answer():
    t = session.get("training")
    if not t:
        return jsonify({"error": "no active training"}), 400

    user_input = request.json.get("answer", "")
    correct_answers = t["current_task"]["answers"]

    user_set = parse_user_answers(user_input)
    correct_set = parse_correct_answers(correct_answers)

    is_correct = user_set == correct_set

    t["stats"]["total"] += 1
    if is_correct:
        t["stats"]["correct"] += 1

    t["history"].append({
        "question": t["current_task"]["question_latex"],
        "user": user_input,
        "correct": is_correct
    })

    session.modified = True

    return jsonify({
        "correct": is_correct,
        "correct_answers": sorted(correct_set)
    })




@app.route("/end_training")
def end_training():
    t = session.pop("training", None)
    if not t:
        return render_template("results.html", error="Нет активной сессии")

    total_time = int(time.time()) - t["meta"]["started_at"]

    accuracy = (
        round(100 * t["stats"]["correct"] / t["stats"]["total"])
        if t["stats"]["total"] else 0
    )

    return render_template(
        "results.html",
        total=t["stats"]["total"],
        correct=t["stats"]["correct"],
        accuracy=accuracy,
        total_time=total_time,
        history=t["history"]
    )


@app.route("/training_state")
def training_state():
    t = session.get("training")
    if not t:
        return jsonify({"active": False})

    return jsonify({
        "active": True,
        "stats": t["stats"],
        "started_at": t["meta"]["started_at"]
    })


@app.route("/finish_training")
def finish_training():
    t = session.get("training")
    if not t:
        return redirect("/")

    finished_at = int(time.time())
    total_time = finished_at - t["meta"]["started_at"]
    total = t["stats"]["total"]
    correct = t["stats"]["correct"]
    accuracy = round((correct / total) * 100, 1) if total > 0 else 0
    if t["meta"]["difficulty"] == "random":
        compl = "случайный"
    else:
        compl = t["current_task"]["complexity"]
    if t["meta"]["type_code"] == "random":
        typeru = "случайный"
    else:
        typeru = t["current_task"]["type_russian"]
    result = {
        "total": total,
        "correct": correct,
        "accuracy": accuracy,
        "time": total_time,
        "history": t["history"],

        # ✅ ВОТ ЭТО ГЛАВНОЕ
        "type": t["meta"]["type_code"],
        "difficulty": t["meta"]["difficulty"],
        "type_russian": typeru,
        "complexity": compl
    }

    session["training_result"] = result
    session.pop("training", None)

    return redirect("/training_result")


@app.route("/training_result")
def training_result():
    result = session.get("training_result")
    if not result:
        return redirect("/")

    return render_template("training_result.html", result=result)


if __name__ == "__main__":
    app.run()