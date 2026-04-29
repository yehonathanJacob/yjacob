import Redis from 'ioredis';
import { Pool } from 'pg';

const redisHost = process.env.REDIS_HOST || 'localhost';
const pgHost = process.env.POSTGRES_HOST || 'localhost';

export const redis = new Redis({
  host: redisHost,
  port: 6379,
});

redis.on('error', (err) => console.error('Redis Client Error', err));
redis.on('connect', () => console.log('Connected to Redis'));

export const pool = new Pool({
  host: pgHost,
  user: process.env.POSTGRES_USER || 'postgres',
  password: process.env.POSTGRES_PASSWORD || 'postgres',
  database: process.env.POSTGRES_DB || 'postgres',
  port: 5432,
});

pool.on('error', (err) => console.error('Postgres Client Error', err));
pool.on('connect', () => console.log('Connected to Postgres'));
