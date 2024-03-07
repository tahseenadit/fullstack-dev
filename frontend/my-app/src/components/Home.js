import {useState} from 'react'
import './style/home.css'

function HomePage() {

    const [question, setQuestion] = useState(' ')

    const handleOnQuestionChange = (event) => {
        setQuestion(document.getElementById("question").value);
    }

    const handleOnSubmitPrompt = async (event) => {
        event.preventDefault();
        setQuestion(document.getElementById("question").value);

        var json_data = '{ \"question\": \"' + question + '\"}'

        try{
            const endpoint = "http://localhost:8000/sample/vertexai/generate/";
            const response = await fetch(endpoint, {
                method: "POST",
                body: json_data,
                headers: {
                    "Content-Type": "application/json" // Set Content-Type header here
                }
            })

            if (!response.ok) {
                throw new Error('Network response was not ok');
              }
        
            const data = await response.json();
            document.getElementById("answer").value = data;
        }catch(error) {
            console.log(error);
        }

    }

    return (
        <div>
            <h1>Welcome FullStack AI Developers!</h1>

            <form onSubmit={handleOnSubmitPrompt}>
                <h4>Ask</h4>
                <div style={{ marginBottom: "20px"}}>
                    <input type="text" id="question" onChange={handleOnQuestionChange} className="input-field"/>
                </div>

                <button type="submit">Generate</button>
            </form>
            <h4>Answer</h4>
            <textarea id="answer" className="textarea-field"></textarea>
        </div>
    )
}

export default HomePage