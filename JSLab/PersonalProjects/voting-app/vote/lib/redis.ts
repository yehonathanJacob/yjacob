import Redis from 'ioredis';

const redisHost = process.env.REDIS_HOST || 'localhost';

const redis = new Redis({
  host: redisHost,
  port: 6379,
});

redis.on('error', (err) => console.error('Redis Client Error', err));
redis.on('connect', () => console.log('Connected to Redis'));

export default redis;
