'use client'

import React from 'react'
const Uniai: React.FC = () => {
    const ENDPOINT: string = 'https://qtuknw51eg.execute-api.ap-south-1.amazonaws.com/prod/generate_answer';
    const [prompt, setPrompt] = React.useState('');
    const onSubmit = () => {
        console.log('Submitting:' + prompt)
        fetch(
            `${ENDPOINT}?prompt=${prompt}`
        ).then(console.log);
    };
    return (
        <>
        <h1>Uniai</h1> 
        <p>Your University Assitant</p>
        <input type="text" 
        placeholder="Tell me about summer semester in ashoka?" 
        value={prompt}
        onChange={(e) => setPrompt(e.currentTarget.value)} ></input>
        <button onClick={onSubmit}>Submit</button>
        </>
    )

}

export default Uniai