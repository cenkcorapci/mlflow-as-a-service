"""SQLite repository for local desired-state records (NOT a SaaS tenant database)."""

import sqlite3
from contextlib import contextmanager
from pathlib import Path
from typing import Iterator


def initialize(path: str) -> None:
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    with connect(path) as connection:
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS workspaces (
                id TEXT PRIMARY KEY,
                slug TEXT NOT NULL UNIQUE,
                name TEXT NOT NULL,
                deployment_mode TEXT NOT NULL,
                status TEXT NOT NULL,
                created_at TEXT NOT NULL
            )
            """
        )


@contextmanager
def connect(path: str) -> Iterator[sqlite3.Connection]:
    connection = sqlite3.connect(path, timeout=5)
    connection.row_factory = sqlite3.Row
    try:
        yield connection
        connection.commit()
    except Exception:
        connection.rollback()
        raise
    finally:
        connection.close()


def insert_workspace(path: str, workspace: dict) -> bool:
    with connect(path) as connection:
        try:
            connection.execute(
                """INSERT INTO workspaces
                (id, slug, name, deployment_mode, status, created_at)
                VALUES (:id, :slug, :name, :deployment_mode, :status, :created_at)""",
                workspace,
            )
        except sqlite3.IntegrityError:
            return False
    return True


def find_by_slug(path: str, slug: str) -> dict | None:
    with connect(path) as connection:
        row = connection.execute("SELECT * FROM workspaces WHERE slug = ?", (slug,)).fetchone()
    return dict(row) if row else None


def find_all(path: str) -> list[dict]:
    with connect(path) as connection:
        rows = connection.execute(
            "SELECT * FROM workspaces ORDER BY created_at DESC, slug ASC"
        ).fetchall()
    return [dict(row) for row in rows]
