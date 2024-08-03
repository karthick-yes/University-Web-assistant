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
        .then(onResult);;
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

    return (
        <>
        <h1>Uniai</h1> 
        {displayedElement}
        </>
    );

}

export default Uniai