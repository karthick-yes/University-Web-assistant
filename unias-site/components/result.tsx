interface Resultsprompts {
    prompt: string;
    answer: string;
    onBack: any;

}


const Results: React.FC<Resultsprompts> = (props) => {
    return (
        <>
         <div>
            <div>
                <b>Prompt</b>
            </div>
            <div>{props.prompt}</div>
        </div>
        <div>
            <div>
                <b>Answer</b>
            </div>
            <div>{props.answer}</div>
        </div>
        <button onClick = {props.onBack}> Back</button>
        </>
    );
}

export default Results;