import { useEffect, useState } from 'react';

export const XPCounter = ({ xp }: { xp: number }) => {
  const [animate, setAnimate] = useState(false);

  useEffect(() => {
    setAnimate(true);
    const timer = setTimeout(() => setAnimate(false), 300);
    return () => clearTimeout(timer);
  }, [xp]);

  return (
    <div style={{ 
      background: 'var(--color-background-secondary)', 
      padding: '6px 12px', 
      borderRadius: '20px',
      fontWeight: 'bold',
      color: 'var(--color-success)',
      display: 'flex',
      alignItems: 'center',
      gap: '4px',
      transform: animate ? 'scale(1.1)' : 'scale(1)',
      transition: 'transform 0.2s ease'
    }}>
      <span role="img" aria-label="star">⭐</span> {xp} XP
    </div>
  );
};
