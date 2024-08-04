import React from 'react';

interface FormProps {
    prompt: string;
    setPrompt: React.Dispatch<React.SetStateAction<string>>;
    onSubmit: () => void;
    isLoading: boolean;
    characterLimit: number;
}

const Form: React.FC<FormProps> = (props) => {
    const isPromptValid = props.prompt.length <= props.characterLimit;

    const updatePromptValue = (text: string) => {
        if (text.length <= props.characterLimit) {
            props.setPrompt(text);
        }
    };

    let statusColor = 'text-slate-400';
    let statusText = null;

    if (!isPromptValid) {
        statusColor = 'text-red-300';
        statusText = `Input must be less than ${props.characterLimit} characters.`;
    }

    return (
        <>
            <div className="mb-6 text-slate-400">
                <p>I&apos;m an AI assistant with knowledge from Ashoka University&apos;s website and official sources. Ask me anything about Ashoka University.</p>
            </div>
            <textarea 
                className="p-2 w-full rounded-md focus:outline-teal-400 focus:outline text-slate-800"
                placeholder="Tell me about summer semester in Ashoka?" 
                value={props.prompt}
                onChange={(e) => updatePromptValue(e.currentTarget.value)}
            ></textarea>
            <div className={`${statusColor} flex justify-between my-2 mb-6 text-sm`}>
                <div>{statusText}</div>
                <div>
                    {props.prompt.length}/{props.characterLimit}
                </div>
            </div>
            <button 
                className="bg-gradient-to-r from-teal-400 to-blue-500 disabled:opacity-50 w-full p-2 rounded-md text-lg"
                onClick={props.onSubmit}
                disabled={props.isLoading || !isPromptValid}
            > 
                Submit
            </button>
        </>
    );
}

export default Form;