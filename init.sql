-- QuesterAI: Enable pgvector extension on database initialization.
-- All tables are managed by Alembic migrations — do NOT create tables here.
CREATE EXTENSION IF NOT EXISTS vector;
