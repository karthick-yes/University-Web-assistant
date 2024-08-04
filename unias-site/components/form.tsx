interface FormProps {
    prompt: string;
    setPrompt : any;
    onSubmit: any;
    isLoading: boolean
    characterLimit: number;
}


const Form: React.FC<FormProps> = (props) => {
    const isPromptvalid = props.prompt.length < 100
    const updatePromptvalue = (text:string) => {
        if (text.length <= props.characterLimit){
            props.setPrompt(text);
        }
    };
    let statusColor = 'text-slate-400';
    let statusText = null;
    if (!isPromptvalid) {
        statusColor = 'text-red-300';
        statusText = `Input must be less than ${props.characterLimit} characters.`
    }
    return (
        <>
        <div className="mb-6 text-slate-400">
            <p>I am an AI assistant with knowledge from Ashoka University's website and official sources. Ask me anything about Ashoka University.</p>
        </div>
        <input className="p-2 w-full rounded-md focus:outline-teal-400 focus:outline text-slate-800" type="text" 
        placeholder="Tell me about summer semester in ashoka?" 
        value={props.prompt}
        onChange={(e) => updatePromptvalue(e.currentTarget.value)} ></input>
        <div className={statusColor +" flex justify-between my-2 mb-6 text-sm"} >
            <div>{statusText}</div>

            <div>
                {props.prompt.length}/{props.characterLimit}
            </div>
           
            </div>
        <button className="bg-gradient-to-r from-teal-400 to-blue-500 disabled:opacity-50 w-full p-2 rounded-md text-lg" 
        onClick={props.onSubmit} 
        disabled ={props.isLoading ||!isPromptvalid}> 
        Submit</button>
        </>
    );
}

export default Form;