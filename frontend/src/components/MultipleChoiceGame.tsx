import { useState, useEffect } from 'react';
import { api } from '../api';

export const MultipleChoiceGame = ({ onCorrectAnswer }: { onCorrectAnswer: (xp: number) => void }) => {
  const [questions, setQuestions] = useState<any[]>([]);
  const [currentIndex, setCurrentIndex] = useState(0);
  const [selected, setSelected] = useState<string | null>(null);
  const [correctOption, setCorrectOption] = useState<string | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadQuestions();
  }, []);

  const loadQuestions = async () => {
    setLoading(true);
    try {
      const data = await api.getQuestions();
      setQuestions(data);
    } catch (e) {
      console.error(e);
    }
    setLoading(false);
  };

  const handleSelect = async (option: string) => {
    if (selected) return; // Prevent multiple clicks
    setSelected(option);
    try {
      const res = await api.submitAnswer(questions[currentIndex].id, option);
      setCorrectOption(res.correct_option);
      if (res.correct) {
        onCorrectAnswer(res.new_xp);
      }
      setTimeout(() => {
        if (currentIndex < questions.length - 1) {
          setCurrentIndex(c => c + 1);
          setSelected(null);
          setCorrectOption(null);
        } else {
          loadQuestions(); // Loop back for MVP
          setCurrentIndex(0);
          setSelected(null);
          setCorrectOption(null);
        }
      }, 1500);
    } catch (e) {
      console.error(e);
      setSelected(null);
    }
  };

  if (loading || questions.length === 0) return <div style={{textAlign: 'center', padding: '40px'}}>Loading questions...</div>;

  const q = questions[currentIndex];

  return (
    <div className="card">
      <h2 style={{ fontSize: '18px', marginBottom: '20px', textAlign: 'center' }}>{q.text}</h2>
      <div style={{ display: 'flex', flexDirection: 'column', gap: '10px' }}>
        {Object.entries(q.options).map(([key, val]) => {
          let btnClass = 'btn';
          if (correctOption) {
            if (key === correctOption) btnClass += ' correct';
            else if (key === selected && key !== correctOption) btnClass += ' wrong';
          }
          return (
            <button 
              key={key} 
              className={btnClass} 
              onClick={() => handleSelect(key)}
              disabled={!!selected}
            >
              {key}: {val as string}
            </button>
          );
        })}
      </div>
    </div>
  );
};
