from fastapi import APIRouter, Depends, HTTPException, Query, status
from aiosqlite import Connection
from datetime import datetime, timezone

from app.models import TaskCreate, TaskRead, TaskStatus, TaskUpdate
from app.database import get_db

#Depends — FastAPI's dependency injection, how we pass the DB connection to routes
#tags=["tasks"] — groups routes together in the /docs page


router = APIRouter(prefix="/tasks",tags=["tasks"])

@router.get("/", response_model=list[TaskRead])
async def list_tasks(
    status: TaskStatus | None = Query(None),
    db: Connection = Depends(get_db) #  FastAPI calls get_db() and passes the connection here as db. This is dependency injection.
):
    if status:
        cursor = await db.execute(
            "SELECT * FROM tasks WHERE status = ? ORDER BY created_at DESC",
            (status.value,)
        )
    else:
        cursor = await db.execute(
            "SELECT * FROM tasks ORDER BY created_at DESC"
        )
    
    rows = await cursor.fetchall() #SQLite object
    return [TaskRead(**row) for row in rows] #unpacking SQLite object and spreading it to dictionary

# this:
#TaskRead(**{"id": 1, "title": "Buy milk", "status": "pending"})

# is equivalent to this:
#TaskRead(id=1, title="Buy milk", status="pending")

@router.post("/",response_model=TaskRead, status_code=status.HTTP_201_CREATED)
async def create_task(task: TaskCreate, db: Connection = Depends(get_db)):
    cursor = await db.execute(
        "INSERT INTO tasks (title, description, status) VALUES (?,?,?)",
        (task.title,task.description,task.status.value)
    )
    
    await db.commit() # await db.commit() — writes the change to disk. Without this your insert is lost

    
    row = await (await db.execute(
        "SELECT * FROM tasks WHERE id = ?", (cursor.lastrowid,)
    )).fetchone()
    
    return TaskRead(**row)

@router.get("/{task_id}",response_model=TaskRead)
async def get_task(task_id: int, db: Connection = Depends(get_db)):
    row = await (await db.execute(
        "SELECT * FROM tasks WHERE id = ?", (task_id,)
    )).fetchone()
    if row is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task {task_id} not found."
        )
    return TaskRead(**row)

@router.patch("/{task_id}", response_model=TaskRead)
async def update_task(task_id: int,
                      updates: TaskUpdate,
                      db: Connection = Depends(get_db)
                      ):
    row = await (await db.execute(
        "SELECT * FROM tasks WHERE id = ?", (task_id,)
    )).fetchone()
    if row is None:
        raise HTTPException(status_code=404,detail=f"{task_id} not found.")
    
    payload = updates.model_dump(exclude_unset=True) #exclude_unset=True means only include fields the client actually sent — not the ones that defaulted to None.
    
    if not payload:
        return TaskRead(**row)
    
    set_clause = ", ".join(f"{key} = ?" for key in payload)
    values = list(payload.values()) + [task_id]
    
    await db.execute(f"UPDATE tasks SET {set_clause} WHERE id = ?",values)
    await db.commit()
    
    updated_row = await (await db.execute(
        "SELECT * FROM tasks WHERE id = ?", (task_id,)
    )).fetchone()
    
    return TaskRead(**updated_row)

@router.delete("{task_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(task_id: int, db: Connection = Depends(get_db)):
    row = await (await db.execute(
        "SELECT id FROM tasks WHERE id = ?",(task_id,)
    )).fetchone()
    
    if row is None:
        raise HTTPException(404,detail=f"Task {task_id} not found.")
    
    await db.execute(
        "DELETE FROM tasks WHERE id=?", (task_id,))
    await db.commit()
    
@router.post("/{task_id}/complete", response_model=TaskRead)
async def complete_task(task_id: int,db: Connection = Depends(get_db)):
    row = await (await db.execute(
       "SELECT * FROM tasks where id = ?", (task_id,)
    )).fetchone()
       
    if row is None:
        raise HTTPException(404,detail=f"Task {task_id} not found.")
    if row["status"] =="done":
        raise HTTPException(status_code=400,detail="Task already completed.")
       
    now = datetime.now(timezone.utc).isoformat()
    await db.execute(
        "UPDATE tasks SET status = 'done' , completed_at= ? WHERE id = ?", (now,task_id,)
    )
    await db.commit()
       
    updated_row = await( await db.execute(
        "SELECT * FROM tasks WHERE id = ?", (task_id,)
    )).fetchone()
       
    return TaskRead(**updated_row)