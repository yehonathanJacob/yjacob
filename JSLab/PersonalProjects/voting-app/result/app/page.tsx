'use client';

import { useEffect, useState } from 'react';

export default function ResultPage() {
  const [results, setResults] = useState<{ a: number; b: number }>({ a: 0, b: 0 });

  const fetchResults = async () => {
    try {
      const response = await fetch('/api/results');
      if (response.ok) {
        const data = await response.json();
        setResults(data);
      }
    } catch (error) {
      console.error('Error fetching results:', error);
    }
  };

  useEffect(() => {
    fetchResults();
    const interval = setInterval(fetchResults, 2000);
    return () => clearInterval(interval);
  }, []);

  const totalVotes = results.a + results.b;
  const percentA = totalVotes === 0 ? 50 : Math.round((results.a / totalVotes) * 100);
  const percentB = totalVotes === 0 ? 50 : Math.round((results.b / totalVotes) * 100);

  return (
    <div style={{ padding: '2rem', textAlign: 'center', fontFamily: 'sans-serif' }}>
      <h1>Voting Results</h1>
      <div style={{ marginTop: '2rem', maxWidth: '600px', margin: '2rem auto' }}>
        <div style={{ display: 'flex', height: '50px', borderRadius: '25px', overflow: 'hidden', border: '1px solid #ccc' }}>
          <div
            style={{
              width: `${percentA}%`,
              backgroundColor: '#4caf50',
              color: 'white',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              transition: 'width 0.5s ease'
            }}
          >
            {percentA}%
          </div>
          <div
            style={{
              width: `${percentB}%`,
              backgroundColor: '#2196f3',
              color: 'white',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              transition: 'width 0.5s ease'
            }}
          >
            {percentB}%
          </div>
        </div>
        <div style={{ display: 'flex', justifyContent: 'space-between', marginTop: '1rem' }}>
          <span>Cats (Option A): {results.a} votes</span>
          <span>Dogs (Option B): {results.b} votes</span>
        </div>
        <p style={{ marginTop: '2rem', color: '#666' }}>Total votes: {totalVotes}</p>
      </div>
    </div>
  );
}
