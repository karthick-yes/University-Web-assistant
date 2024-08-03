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

    return (
        <>
        <p>Your University Assitant</p>

        <input type="text" 
        placeholder="Tell me about summer semester in ashoka?" 
        value={props.prompt}
        onChange={(e) => updatePromptvalue(e.currentTarget.value)} ></input>
        <div>{props.prompt.length}/{props.characterLimit}</div>
        <button onClick={props.onSubmit} disabled ={props.isLoading ||!isPromptvalid}> Submit</button>
        </>
    );
}

export default Form;