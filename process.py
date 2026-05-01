import json
import sys
from collections import defaultdict
from pathlib import Path


def load_data(filepath: str) -> list:
    path = Path(filepath)
    if not path.exists():
        print(f"[ERRO] Arquivo não encontrado: {filepath}", file=sys.stderr)
        sys.exit(1)
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def process(records: list) -> dict:
    valid = []
    ignored = 0

    for record in records:
        minutes = record.get("minutes", 0)
        if minutes <= 0:
            ignored += 1
        else:
            valid.append(record)

    print(f"[INFO] Total de registros: {len(records)}")
    print(f"[INFO] Registros válidos:  {len(valid)}")
    print(f"[INFO] Registros ignorados: {ignored}")

    # ─── Agrupamento por tarefa ───────────────────────────────────────────────
    task_map: dict[int, dict] = {}
    for r in valid:
        tid = r["taskId"]
        if tid not in task_map:
            task_map[tid] = {
                "taskId": tid,
                "taskName": r["taskName"],
                "totalMinutes": 0,
            }
        task_map[tid]["totalMinutes"] += r["minutes"]

    total_minutes = sum(t["totalMinutes"] for t in task_map.values())

    # Ordenação: totalMinutes desc, taskId asc em empate
    tasks_sorted = sorted(
        task_map.values(),
        key=lambda t: (-t["totalMinutes"], t["taskId"]),
    )

    # Adiciona percentual formatado
    for t in tasks_sorted:
        pct = (t["totalMinutes"] / total_minutes) * 100 if total_minutes else 0
        t["percentage"] = f"{pct:.2f}%"

    # ─── Tarefa mais trabalhada ───────────────────────────────────────────────
    most_worked_task = tasks_sorted[0] if tasks_sorted else None

    # ─── Top 3 tarefas por percentual ────────────────────────────────────────
    top3_tasks = [
        {
            "taskId": t["taskId"],
            "taskName": t["taskName"],
            "percentage": t["percentage"],
        }
        for t in tasks_sorted[:3]
    ]

    # ─── Agrupamento por funcionário ─────────────────────────────────────────
    employee_map: dict[int, dict] = {}
    for r in valid:
        uid = r["userId"]
        if uid not in employee_map:
            employee_map[uid] = {
                "userId": uid,
                "userName": r["userName"],
                "totalMinutes": 0,
                "distinctTaskIds": set(),
            }
        employee_map[uid]["totalMinutes"] += r["minutes"]
        employee_map[uid]["distinctTaskIds"].add(r["taskId"])

    # Ordenação: totalMinutes desc, userId asc em empate
    employees_sorted = sorted(
        employee_map.values(),
        key=lambda e: (-e["totalMinutes"], e["userId"]),
    )

    top3_employees = [
        {
            "userId": e["userId"],
            "userName": e["userName"],
            "totalMinutes": e["totalMinutes"],
        }
        for e in employees_sorted[:3]
    ]

    # ─── Usuário com mais tarefas distintas ──────────────────────────────────
    most_distinct = sorted(
        employee_map.values(),
        key=lambda e: (-len(e["distinctTaskIds"]), e["userId"]),
    )[0]

    most_distinct_user = {
        "userId": most_distinct["userId"],
        "userName": most_distinct["userName"],
        "distinctTasks": len(most_distinct["distinctTaskIds"]),
        "taskIds": sorted(most_distinct["distinctTaskIds"]),
    }

    return {
        "totalMinutes": total_minutes,
        "tasks": tasks_sorted,
        "mostWorkedTask": most_worked_task,
        "top3TasksPercentage": top3_tasks,
        "top3Employees": top3_employees,
        "mostDistinctUserOnTasks": most_distinct_user,
        "ignoredRecords": ignored,
    }


def main():
    input_path = Path(__file__).parent / "data.json"
    output_path = Path(__file__).parent / "result.json"

    print("[INFO] Carregando data.json...")
    records = load_data(str(input_path))

    print("[INFO] Processando registros...")
    result = process(records)

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)

    print(f"[INFO] Resultado salvo em: {output_path}")
    print(f"[INFO] Total de minutos: {result['totalMinutes']}")
    print(f"[INFO] Tarefa mais trabalhada: {result['mostWorkedTask']['taskName']}")
    print(f"[INFO] Registros ignorados: {result['ignoredRecords']}")


if __name__ == "__main__":
    main()
