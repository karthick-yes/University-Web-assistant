'use client'

import React from 'react'
import Form from './form';
import Results from './result';



const Uniai: React.FC = () => {
    const ENDPOINT: string = 'https://qtuknw51eg.execute-api.ap-south-1.amazonaws.com/prod/generate_answer';
    const CHARACTER_LIMIT: number = 100;
    const [prompt, setPrompt] = React.useState('');
    const [answer, setAnswer] = React.useState('');
    const [hasResult, setHasResult] = React.useState(false);
    const [isLoading, setIsLoading] = React.useState(false);
    const onSubmit = () => {
        console.log('Submitting:' + prompt);
        setIsLoading(true);
        fetch(
            `${ENDPOINT}?query=${prompt}`)
        .then((res) => res.json())
        .then(onResult);
    };

    const onResult = (data:any) => {
        setAnswer(data.answer);
        setHasResult(true);
        setIsLoading(false);
    };

    const onReset = () => {
        setPrompt('');
        setHasResult(false);
        setIsLoading(false);
    };

    let displayedElement = null;

    if (hasResult) {
        displayedElement = <Results answer={answer} onBack={onReset} prompt={prompt} />;
        
    } else {
        displayedElement = <Form prompt={prompt} setPrompt={setPrompt} onSubmit={onSubmit} isLoading={isLoading} characterLimit={CHARACTER_LIMIT}/>
    };
    const gradientText =
        "text-white text-transparent bg-clip-text bg-gradient-to-r from-teal-400 to-blue-500 font-light w-fit mx-auto";

    return (
        <div className='h-screen flex'>
        <div className='max-w-md m-auto p-2'>
            <div className='bg-slate-900 p-6 rounded-md text-white'>
            <div className='text-center my-6'>
             <h1 className= {gradientText +' text-3xl'}>UniAi</h1>  
            <div className={gradientText}>Your AI University Assistant</div>  
            </div>
            {displayedElement}
            </div>
        </div>
        </div>
    );

}

export default Uniai