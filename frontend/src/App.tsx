import { useState, useEffect } from 'react';
import { AuthWrapper } from './components/AuthWrapper';
import { MultipleChoiceGame } from './components/MultipleChoiceGame';
import { XPCounter } from './components/XPCounter';
import './index.css';

const WebApp = (window as any).Telegram?.WebApp;

function App() {
  const [xp, setXp] = useState(0);

  useEffect(() => {
    if (WebApp) {
      WebApp.ready();
      WebApp.expand();
    }
  }, []);

  return (
    <div style={{ padding: '20px' }}>
      <AuthWrapper onAuthSuccess={(user) => setXp(user.xp)}>
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '20px' }}>
          <h1 style={{ margin: 0, fontSize: '24px' }}>MathUp</h1>
          <XPCounter xp={xp} />
        </div>
        <MultipleChoiceGame onCorrectAnswer={(newXp) => setXp(newXp)} />
      </AuthWrapper>
    </div>
  );
}

export default App;
