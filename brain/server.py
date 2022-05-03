import fastapi
from fastapi.middleware.cors import CORSMiddleware
from starlette.staticfiles import StaticFiles
import load_tasks

app = fastapi.FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

TASKS = load_tasks.load()
for i,t in enumerate(TASKS):
    t.id = i
    if t.install_function != None:
        t.install_function()

@app.get("/tasks")
async def task_list():
    return [
            {
                "name":        t.name,
                "done":        t.done,
                "hinted":      t.clue_used,
                "value":       t.value,
                "description": t.description,
                "id":          t.id
            }
        for t in TASKS
        ]

@app.get("/tasks/graph")
async def task_list():

    for t in TASKS: t.verify()
    for t in TASKS: t.is_lock()

    nodes = [
            {
                "title":  t.name,
                "status": "lock" if t.lock else (( "hinted_done" if t.clue_used else "done" ) if t.done else ( "hinted_todo" if t.clue_used else "todo" )),
                "level":  t.level,
                "id":     t.id
            }
        for t in TASKS
        ]

    edges = []
    for t in TASKS:
        for tt in t.parents:
            edges.append(
                {
                    "source": tt.id,
                    "target": t.id
                }
            )
    return {"nodes":nodes, "links":edges}

@app.get("/task/{task_id}")
async def task_show(task_id: int):
    return TASKS[task_id].show()

@app.get("/task/{task_id}/done")
async def task_is_done(task_id: int):
    return TASKS[task_id].done

@app.get("/task/{task_id}/verify")
async def task_verify(task_id: int):
    ver =  TASKS[task_id].verify()
    if ver[0]:
        for t in TASKS: t.is_lock()
    return ver

@app.get("/task/{task_id}/clue")
async def task_get_clue(task_id: int):
    return TASKS[task_id].show_clue()

@app.get("/task/{task_id}/value")
async def task_value(task_id: int):
    return TASKS[task_id].value



app.mount("/", StaticFiles(directory="/srv/EFL/frontend", html=True), name="index")
