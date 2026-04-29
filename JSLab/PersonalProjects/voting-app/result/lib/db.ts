import { Pool } from 'pg';

const pgHost = process.env.POSTGRES_HOST || 'localhost';

const pool = new Pool({
  host: pgHost,
  user: process.env.POSTGRES_USER || 'postgres',
  password: process.env.POSTGRES_PASSWORD || 'postgres',
  database: process.env.POSTGRES_DB || 'postgres',
  port: 5432,
});

pool.on('error', (err) => console.error('Postgres Client Error', err));

export default pool;
