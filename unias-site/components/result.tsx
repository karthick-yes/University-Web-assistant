// result.tsx
import React from 'react';
import ReactMarkdown from 'react-markdown';

interface Resultsprompts {
  prompt: string;
  answer: string;
  onBack: () => void;
}

const Results: React.FC<Resultsprompts> = (props) => {
  console.log('Answer prop:', props.answer); // Debugging line to print the answer

  const resultSelection = (label: string, body: React.ReactNode) => {
    return (
      <div className="bg-slate-700 p-4 my-2 rounded-md">
        <div className="text-slate-500 text-sm font-bold mb-1">
          {label}
        </div>
        <div>{body}</div>
      </div>
    );
  };

  return (
    <>
      <div>
        {resultSelection(
          'Prompt',
          <div className="text-md font-bold">{props.prompt}</div>
        )}
        {resultSelection(
          'Answer',
          // Render the markdown content as HTML
          <ReactMarkdown>{props.answer}</ReactMarkdown>
        )}
      </div>
      <button
        className="bg-gradient-to-r from-teal-400 to-blue-500 disabled:opacity-50 w-full p-2 rounded-md text-lg"
        onClick={props.onBack}
      >
        Back
      </button>
    </>
  );
};

export default Results;
