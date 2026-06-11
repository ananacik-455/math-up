import { useEffect, useState } from 'react';
import { api } from '../api';

const WebApp = (window as any).Telegram?.WebApp;

export const AuthWrapper = ({ children, onAuthSuccess }: { children: React.ReactNode, onAuthSuccess: (user: any) => void }) => {
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const authenticate = async () => {
      try {
        const initData = WebApp?.initData;
        if (!initData) {
            throw new Error("No Telegram initData found. Please open this app inside Telegram.");
        }
        const res = await api.login(initData);
        onAuthSuccess(res.user);
        setLoading(false);
      } catch (err) {
        console.error(err);
        setError("Failed to authenticate. Ensure the backend is running.");
        setLoading(false);
      }
    };
    authenticate();
  }, []);

  if (loading) return <div style={{ textAlign: 'center', padding: '50px' }}>Loading...</div>;
  if (error) return <div style={{ color: 'var(--color-danger)', textAlign: 'center' }}>{error}</div>;

  return <>{children}</>;
};
