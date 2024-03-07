import {useState} from 'react'

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
            <h1>Welcome FullStack Developers!</h1>

            <form onSubmit={handleOnSubmitPrompt}>
                <div style={{ marginBottom: "20px"}}>
                    <input type="text" id="question" onChange={handleOnQuestionChange}/>
                </div>

                <button type="submit">Generate</button>
            </form>
            <textarea id="answer"></textarea>
        </div>
    )
}

export default HomePage